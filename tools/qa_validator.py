#!/usr/bin/env python3
"""
MIRAI · QA Validator v2 — فحص شامل لكل موارد res + HTML
يخرج exit 1 إذا وُجدت مشكلة حقيقية.
"""
import os, re, sys, collections
import xml.etree.ElementTree as ET

issues, notes = [], []
LIB_STRINGS = {  # strings تأتي من مكتبة Material — ليست من مشروعنا
    'appbar_scrolling_view_behavior', 'hide_bottom_view_on_scroll_behavior',
}
FW_OK = {'color/transparent', 'color/white', 'color/black', 'drawable//ic_menu'}

# ── 0) سلامة XML ──
files = {}
for dp, _, fns in os.walk('res'):
    for fn in fns:
        if fn.endswith('.xml'):
            p = os.path.join(dp, fn)
            # نحذف التعليقات قبل الفحص حتى لا تُحسب مراجعها
            files[p] = re.sub(r'<!--.*?-->', '', open(p, encoding='utf-8').read(), flags=re.S)
for p, t in files.items():
    try:
        ET.fromstring(t)
    except Exception as e:
        issues.append(f'XML غير سليم: {p}: {e}')

# ── 1) المخزونات ──
colors, dimens, styles, strings, drawables, ids, menus, layouts_dir = set(), set(), set(), set(), set(), set(), set(), set()
for fn in os.listdir('res/values'):
    t = open('res/values/' + fn).read()
    for m in re.findall(r'<color name="([\w]+)"', t): colors.add(m)
    for m in re.findall(r'<dimen name="([\w]+)"', t): dimens.add(m)
    for m in re.findall(r'<style name="([\w.]+)"', t): styles.add(m)
    for m in re.findall(r'<string name="([\w]+)"', t): strings.add(m)
    for m in re.findall(r'<item name="([\w]+)" type="id"', t): ids.add(m)
for fn in os.listdir('res/drawable'): drawables.add(fn[:-4])
for fn in os.listdir('res/color'): colors.add(fn[:-4])
for fn in os.listdir('res/menu'): menus.add(fn[:-4])
for fn in os.listdir('res/layout'): layouts_dir.add(fn[:-4])
root_layouts = {'Jk','V9','AB','Fk','_J','L7'}
all_layout_names = layouts_dir | root_layouts

# ── 2) المراجع المتقاطعة ──
for p, t in files.items():
    for m in re.findall(r'@color/(\w+)', t):
        if m not in colors: issues.append(f'لون مفقود: {p}: @color/{m}')
    for m in re.findall(r'@dimen/(\w+)', t):
        if m not in dimens: issues.append(f'dimen مفقود: {p}: @dimen/{m}')
    for m in re.findall(r'@style/([\w.]+)', t):
        if m not in styles: issues.append(f'style مفقود: {p}: @{m}')
    for m in re.findall(r'@drawable/(\w+)', t):
        if m not in drawables and m not in all_layout_names: issues.append(f'drawable مفقود: {p}: @drawable/{m}')
    for m in re.findall(r'@string/(\w+)', t):
        if m not in strings and m not in LIB_STRINGS: issues.append(f'string مفقود: {p}: @string/{m}')
    for m in re.findall(r'@menu/(\w+)', t):
        if m not in menus: issues.append(f'menu مفقود: {p}: @menu/{m}')
    for m in re.findall(r'@id/(\w+)', t):
        if m not in ids: issues.append(f'id مفقود: {p}: @id/{m}')
    for m in re.findall(r'@layout/(\w+)', t):
        if m not in all_layout_names: issues.append(f'layout مفقود: {p}: @layout/{m}')
    for m in re.findall(r'@navigation/(\w+)', t):
        issues.append(f'مرجع navigation غير محلول (خاص بمشروعك): {p}: @navigation/{m}')
    for m in re.findall(r'@android:([\w]+)"', t):
        issues.append(f'مرجع أندرويد بدون نوع: {p}: @android:{m}')
    for m in re.findall(r'"(#[0-9A-Fa-f]{3,8})"', t):
        if not p.endswith('values/colors.xml'):
            issues.append(f'hex يدوي خارج colors.xml: {p}: {m}')
    # تدرجات مقلوبة: dark-start + angle=270 (أفقي-عمودي مقلوب)
    for g in re.findall(r'<gradient[^>]*>', t):
        if 'angle="270"' in g and re.search(r'startColor="(@color/mirai_scrim_hero_bottom|@color/mirai_scrim_media_strong)', g):
            issues.append(f'تدرج مقلوب: {p}')

# ── 3) تكرار أسماء الموارد العلوية في values ──
top = collections.defaultdict(set)
for fn in os.listdir('res/values'):
    t = open('res/values/' + fn).read()
    for tag in ('color', 'dimen', 'string', 'style'):
        for m in re.findall(rf'^\s*<{tag} name="([\w.]+)"', t, re.M):
            top[m].add(fn)
for k, v in top.items():
    if len(v) > 1: issues.append(f'اسم مكرر: {k} في {sorted(v)}')

# ── 4) فحص أنماط أندرويد شائعة ──
for p, t in files.items():
    if '/values/' in p: continue
    if re.search(r'android:layout_(margin|padding)(Left|Right)[="]', t):
        issues.append(f'قياس Left/Right (يكسر RTL): {p}')
    if 'textSize="' in t and '/values/' not in p and 'type.xml' not in p:
        issues.append(f'textSize يدوي (يجب TextAppearance): {p}')

# ── 5) ids.xml يغطي كل @id في كل الملفات (بما فيها menu) ──
for p, t in files.items():
    for m in set(re.findall(r'@id/(\w+)', t)):
        if m not in ids: issues.append(f'id غير معرّف في ids.xml: {p}: {m}')

# ── 6) HTML ──
h = open('preview/index.html', encoding='utf-8').read()
for pat in ['var(--elevated;', ';10px;', '#FFC53د']:
    if pat in h: issues.append(f'HTML typo: {pat}')
from html.parser import HTMLParser
class Chk(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack = []; s.errs = []
    def handle_starttag(s, tag, at):
        if tag not in ('br','img','meta','link','input','hr'): s.stack.append(tag)
    def handle_endtag(s, tag):
        if tag in ('br','img','meta','link','input','hr'): return
        if s.stack and s.stack[-1] == tag: s.stack.pop()
        elif tag in s.stack:
            while s.stack and s.stack[-1] != tag: s.errs.append(f'غير مغلق: {s.stack.pop()}')
            s.stack.pop()
        else: s.errs.append(f'إغلاق غريب: {tag}')
c = Chk(); c.feed(h)
for e in c.errs[:8]: issues.append(f'HTML: {e}')
if c.stack: issues.append(f'HTML: وسوم متبقية: {c.stack[:8]}')

# ── تقرير ──
print('════════ MIRAI QA VALIDATOR v2 — الفحص الشامل ════════')
print(f'ملفات: {len(files)+1} (res + preview) | ألوان {len(colors)} | dimens {len(dimens)} | styles {len(styles)} | strings {len(strings)} | drawables {len(drawables)} | ids {len(ids)}')
if not issues:
    print('\n✅ لا مشاكل — كل المراجع سليمة، XML سليم، HTML سليم')
    sys.exit(0)
print(f'\n❌ {len(issues)} مشكلة:')
seen = set()
for i in issues:
    if i not in seen: print('  •', i); seen.add(i)
sys.exit(1)
