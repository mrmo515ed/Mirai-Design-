# Mirai Premium Redesign — دليل الاستبدال الكامل

كل شيء جاهز في مجلد `res/` **بنفس هيكل ملفاتك التي شاركتها** — تنسخ وتستبدل، بدون حذف أي ميزة أو كسر أي وظيفة.

## 📁 ما الذي تغيّر في ملفاتك الأصلية (استبدال 1:1)

| ملفك الأصلي | الجديد | ما تم |
|---|---|---|
| `res/Jk.xml` | ✅ مستبدل | تفاصيل الأنمي — نفس الشجرة والـ ids والسلوك، تصميم سينمائي موحّد |
| `res/V9.xml` | ✅ مستبدل | المضيف الرئيسي — BottomNav 68dp + FABs بألوان صحيحة |
| `res/AB.xml` | ✅ مستبدل | شاشة الحلقة — Header + RatingBar + خانة الإعلان كما هي |
| `res/Fk.xml` | ✅ مستبدل | بطاقة شخصية/طاقم — الزجاج ← سطح معتم + حد |
| `res/_J.xml` | ✅ مستبدل | صف مستخدم — شارة «متصل» دلالية بدل النيون |
| `res/L7.xml` | ✅ مستبدل | قائمة التنقل السفلي — نفس الوجهات الأربعة |
| `res/color/bottom_nav_icon_color.xml` | ✅ مستبدل | state-list موحّد |
| `res/color/bottom_nav_text_color.xml` | ✅ مستبدل | state-list موحّد |

## ➕ ملفات جديدة (تضاف ولا تحذف شيئاً)

- `res/values/` — `colors.xml` · `dimens.xml` · `type.xml` · `shapes.xml` · `styles.xml` · `themes.xml` · `attrs.xml` · `strings_ds.xml` · `ids.xml`
- `res/drawable/` — 48 ملف: أسطح + chips + scrims سينمائية + state lists + 20 أيقونة
- `res/color/` — 9 state-lists (mirai_*)
- `res/layout/` — عناصر جاهزة للأدابترز: `item_episode` · `item_anime_card` · `item_character` · `item_chip_genre` · `sheet_base` · `dialog_base` · `state_views` · `view_section_header`

## 🔧 خطوات التركيب (5 دقائق)

1. انسخ محتوى `res/` داخل `app/src/main/res/` (دمج — **استبدال** فقط الملفات المطابقة أعلاه).
2. في `values/ids.xml` الجديد: الأسماء دلالية (`animeDetailsRoot` …). إن كانت أسماؤك الحالية مختلفة، راجع **`layouts/IDS_MAP.md`** — فيه جدول hex ← الاسم الدلالي لكل id في تفاصيل الأنمي، لتعرف أي اسم يقابل أي view عندك.
3. اجعل ثيم التطبيق يرث من `Theme.Mirai` (أو انسخ عناصره إلى ثيمك الحالي — الأهم `colorPrimary=#00A3FF` و`android:colorBackground=#0B0D10`).
4. ابني المشروع — لا يوجد أي تغيير في Java/Kotlin/Adapters/Fragments.

## 🛡️ قواعد الحفاظ (تم الالتزام بها بالكامل)

- ✅ لا ميزة حُذفت: Shimmer · StateLayout · الإعلانات · YouTubePlayer · IndicatorSeekBar · كل RecyclerViews
- ✅ لا id تغيّر معناه — فقط أسماء دلالية (جدول مطابقة كامل)
- ✅ لا منطق/كولباك/أدابتر مُسّ — كل التغييرات بصرية في XML فقط
- ✅ RTL: start/end في كل القياسات، الأرقام في `layoutDirection=ltr`
- ✅ لا Glow ولا تدرجات مبالغ بها — 3 scrims مشروعة فقط (البطل، شريط الأدوات، أقدام البطاقات)

## 📄 ملفات مرجعية

- `DESIGN_AUDIT.md` — التدقيق الكامل بالأدلة (45+ لوناً يدوياً، 14 نصف قطر…)
- `layouts/IDS_MAP.md` — جدول ربط الـ ids
- `preview/index.html` — المعاينة التفاعلية لكل الشاشات (افتحها في المتصفح)
