#!/usr/bin/env python3
"""Minimal but robust AXML (Android binary XML) decoder -> readable XML."""
import struct, sys, os, re

RES_STRING_POOL_TYPE = 0x0001
RES_XML_START_NAMESPACE = 0x0100
RES_XML_END_NAMESPACE = 0x0101
RES_XML_START_ELEMENT = 0x0102
RES_XML_END_ELEMENT = 0x0103
RES_XML_CDATA = 0x0104
RES_XML_RESOURCE_MAP = 0x0180

TYPE_NULL=0x00; TYPE_REFERENCE=0x01; TYPE_ATTRIBUTE=0x02; TYPE_STRING=0x03
TYPE_FLOAT=0x04; TYPE_DIMENSION=0x05; TYPE_FRACTION=0x06; TYPE_INT_DEC=0x10
TYPE_INT_HEX=0x11; TYPE_INT_BOOLEAN=0x12; TYPE_INT_COLOR_ARGB8=0x1c
TYPE_INT_COLOR_RGB8=0x1d; TYPE_INT_COLOR_ARGB4=0x1e; TYPE_INT_COLOR_RGB4=0x1f

UNITS = {0:'', 1:'dp', 2:'sp', 3:'pt', 4:'in', 5:'mm'}
FRAC = {0:'%', 1:'p'}
DIM_MULT = {0: 1.0/256, 1: 1.0/2, 2: 1.0*128, 3: 1.0*32768}

class StrPool:
    def __init__(self, data, chunk_start):
        hdr = data[chunk_start:chunk_start+28]
        (ctype, hsize, csize, scount, stylecount, flags, sstart, sststart) = struct.unpack('<HHIIIIII', hdr)
        self.utf8 = bool(flags & (1 << 8))
        self.strings = []
        off = chunk_start + sstart
        is_sorted = flags & 1
        for i in range(scount):
            if self.utf8:
                # u16 len, u8 byte len, bytes, null
                l16 = data[off]
                if l16 & 0x80: off += 2
                else: off += 1
                bl = data[off]
                if bl & 0x80:
                    bl = ((bl & 0x7f) << 8) | data[off+1]; off += 2
                else:
                    off += 1
                s = data[off:off+bl].decode('utf-8', 'replace')
                off += bl + 1
            else:
                l = struct.unpack('<H', data[off:off+2])[0]
                off += 2
                if l & 0x8000:
                    l2 = struct.unpack('<H', data[off:off+2])[0]
                    l = ((l & 0x7fff) << 16) | l2
                    off += 2
                s = data[off:off+l*2].decode('utf-16-le', 'replace')
                off += l*2 + 2
            self.strings.append(s)
    def get(self, i):
        if 0 <= i < len(self.strings):
            return self.strings[i]
        return '@string%d' % i

def fmt_value(dtype, data, pool):
    if dtype == TYPE_STRING:
        return pool.get(data)
    if dtype == TYPE_REFERENCE:
        if (data >> 24) == 0x01:  # android framework resource
            return '@android:%08X' % data
        return '@ref/0x%08X' % data
    if dtype == TYPE_ATTRIBUTE:
        return '?attr/0x%08X' % data
    if dtype == TYPE_FLOAT:
        try: return '%g' % struct.unpack('<f', struct.pack('<I', data))[0]
        except: return str(data)
    if dtype in (TYPE_DIMENSION, TYPE_FRACTION):
        m = (data & 0xFFFFFF00) * DIM_MULT[(data >> 4) & 3]
        if dtype == TYPE_DIMENSION:
            v = int(m) if abs(m - round(m)) < 1e-6 else round(m, 3)
            return '%d%s' % (v, UNITS[data & 0xF])
        v = int(m) if abs(m - round(m)) < 1e-6 else round(m, 3)
        return '%d%s' % (v, FRAC[data & 0xF])
    if dtype == TYPE_INT_DEC: return str(data if data < 2**31 else data - 2**32)
    if dtype == TYPE_INT_HEX: return '0x%X' % data
    if dtype == TYPE_INT_BOOLEAN: return 'true' if data != 0 else 'false'
    if dtype in (TYPE_INT_COLOR_ARGB8, TYPE_INT_COLOR_RGB8, TYPE_INT_COLOR_ARGB4, TYPE_INT_COLOR_RGB4):
        if dtype in (TYPE_INT_COLOR_ARGB4, TYPE_INT_COLOR_RGB4):
            s = '%04X' % data
            if dtype == TYPE_INT_COLOR_ARGB4: return '#%s' % s
            return '#%s' % s[1:] if s[0] == 'F' else '#%s' % s
        s = '%08X' % data
        if dtype == TYPE_INT_COLOR_RGB8:
            return '#%s' % s[2:]
        return '#%s' % s
    return str(data)

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

AXML_MAGIC = 0x00080003

def parse_axml(path):
    data = open(path, 'rb').read()
    if len(data) < 8 or struct.unpack('<I', data[:4])[0] != AXML_MAGIC:
        # maybe plain xml
        try:
            t = data.decode('utf-8')
            if t.lstrip().startswith('<'): return t, 'plain'
        except: pass
        return None, 'unknown'
    # top-level header: type(2) headersize(2) size(4)
    total = struct.unpack('<I', data[4:8])[0]
    pos = 8
    pool = None
    nsmap = {}   # prefix -> uri
    out = []
    stack = []
    resmap = []
    while pos < min(len(data), total):
        if pos + 8 > len(data): break
        ctype, hsize, csize = struct.unpack('<HHI', data[pos:pos+8])
        if csize == 0: break
        if ctype == RES_STRING_POOL_TYPE:
            pool = StrPool(data, pos)
        elif ctype == RES_XML_RESOURCE_MAP:
            n = (csize - 8) // 4
            resmap = struct.unpack('<%dI' % n, data[pos+8:pos+8+4*n])
        elif ctype in (RES_XML_START_NAMESPACE,):
            pref, uri = struct.unpack('<II', data[pos+16:pos+24])
            nsmap[pool.get(uri)] = pool.get(pref)
        elif ctype == RES_XML_END_NAMESPACE:
            pass
        elif ctype == RES_XML_CDATA:
            pass
        elif ctype == RES_XML_START_ELEMENT:
            (ln, com, ns, name, astart, asize, acount, idix, clsix, stix) = struct.unpack('<IIIIHHHHHH', data[pos+8:pos+36])
            tag = pool.get(name)
            attrs = []
            base = pos + 16 + astart  # astart relative to ResXMLTree_attrExt start (pos+16)
            for i in range(acount):
                a = base + i * asize
                ans, aname, araw, vsize, vres0, vdtype, vdata = struct.unpack('<IIIHBBI', data[a:a+20])
                key = pool.get(aname)
                uri = pool.get(ans) if ans != 0xFFFFFFFF else None
                if uri and uri in nsmap:
                    prefix = nsmap[uri]
                    key = '%s:%s' % (prefix, key)
                raw = pool.get(araw) if araw != 0xFFFFFFFF else None
                val = fmt_value(vdtype, vdata, pool)
                if raw is not None and raw != val and vdtype == TYPE_STRING:
                    val = raw
                attrs.append((key, val))
            astr = ''.join(' %s="%s"' % (k, esc(v)) for k, v in attrs)
            out.append('%s<%s%s>' % ('\t' * len(stack), tag, astr))
            stack.append(tag)
        elif ctype == RES_XML_END_ELEMENT:
            ns, name = struct.unpack('<II', data[pos+16:pos+24])
            tag = pool.get(name)
            if stack and stack[-1] == tag:
                stack.pop()
                if out and out[-1].startswith('%s<%s ' % ('\t'*len(stack), tag)):
                    out[-1] = out[-1][:-1] + '/>'
                else:
                    out.append('%s</%s>' % ('\t'*len(stack), tag))
        pos += csize
    while stack:
        tag = stack.pop()
        out.append('</%s>' % tag)
    return '\n'.join(out), 'axml'

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    xml, kind = parse_axml(src)
    if xml is None:
        sys.exit(1)
    open(dst, 'w', encoding='utf-8').write(xml)
