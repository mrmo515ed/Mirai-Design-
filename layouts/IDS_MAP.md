# IDS_MAP — Anime Details (Jk.xml ⇄ redesigned layout)

كل الـ IDs في الواجهة المعاد تصميمها **نفسها** التي في الشاشة الأصلية — فقط بأسماء دلالية
بدل الأسماء المشوّشة. اربط الأسماء في `values/ids.xml` مرة واحدة (أو اعمل find/replace)
بدون أي تعديل على الأدابترز أو الفragments.

| Hex (compiled) | Semantic ID in redesign | View | ملاحظة |
|---|---|---|---|
| `0x7F0A052D` | `animeDetailsRoot` | CoordinatorLayout | خلفية → `mirai_bg` |
| `0x7F0A00B2` | `animeDetailsAppBar` | AppBarLayout | شفاف + scrim شريط الحالة |
| `0x7F0A0243` | `animeDetailsCollapsing` | CollapsingToolbarLayout | نفس scrollFlags/parallax |
| `0x7F0A0459` | `animeDetailsBackdrop` | ImageView (keyart) | centerCrop |
| — | (جديد) `View` | scrim 280dp | `mirai_scrim_hero` (3 stops) |
| `0x7F0A0093` | `animeDetailsHeroContent` | LinearLayout (hero lockup) | — |
| `0x7F0A008E` | `animeDetailsPoster` | ImageView 110×165 | radius 12, elev 12 |
| `0x7F0A008F` | `animeDetailsTitle` | TextView | Display 26sp |
| `0x7F0A0090` | `animeDetailsTitleJp` | TextView | Caption، ثانوي |
| `0x7F0A08A2` | `animeDetailsScoreChip` | TextView chip | ذهبي `mirai_bg_chip_rating` |
| `0x7F0A080F` | `animeDetailsStatusChip` | TextView chip | محايد (أو success عند البث) |
| `0x7F0A08E1` | `animeDetailsFormatChip` | TextView chip | محايد |
| `0x7F0A0844` | `animeDetailsYearChip` | TextView chip | محايد |
| `0x7F0A0138` | `animeDetailsAddToListBtn` | MaterialButton | Primary pill 52dp |
| `0x7F0A0132` | `animeDetailsShareBtn` | MaterialButton Icon | 48dp overlay |
| `0x7F0A03CA` | `animeDetailsShimmer` | ShimmerFrameLayout | ألوان skeleton موحدة |
| `0x7F0A07F4` | `animeDetailsToolbar` | Toolbar | overlay scrim |
| `0x7F0A0105` | `animeDetailsBackBtn` | MaterialButton Icon | 44dp a11y |
| `0x7F0A08DC` | `animeDetailsCollapsedTitle` | TextView | يظهر عند الالتقاط |
| `0x7F0A05AC` | `animeDetailsScroll` | NestedScrollView | — |
| `0x7F0A009D` | `animeDetailsGenresRecycler` | RecyclerView (chips rail) | أفقي |
| `0x7F0A02BA` | `animeDetailsDescription` | TextView | Body 14sp/21 |
| `0x7F0A0772` | `animeDetailsStudiosSection` | LinearLayout | gone افتراضياً |
| `0x7F0A0771` | `animeDetailsStudiosRecycler` | RecyclerView | — |
| `0x7F0A08B7` | `animeDetailsMetaSeason` | TextView | BodySmall |
| `0x7F0A08BE` | `animeDetailsMetaSource` | TextView | BodySmall |
| `0x7F0A08A1` | `animeDetailsMetaRank` | TextView | BodySmall |
| `0x7F0A08CA` | `animeDetailsMetaStatus` | TextView | BodySmall |
| `0x7F0A009E` | `animeDetailsScoreExternal` | TextView | Score 18sp |
| `0x7F0A00A3` | `animeDetailsScoreExternalLabel` | TextView | Caption |
| `0x7F0A0879` | `animeDetailsScoreCommunity` | TextView | Score باللون الأساسي |
| `0x7F0A087A` | `animeDetailsScoreCommunityLabel` | TextView | Caption |
| `0x7F0A0481` | `animeDetailsScoreCommunityIcon` | ImageView | tint أساسي |
| `0x7F0A009C` | `animeDetailsFavorites` | TextView | Score |
| `0x7F0A08E8` | `animeDetailsYourRatingLabel` | TextView | BodySmall bold |
| `0x7F0A00A1` | `animeDetailsRatingSeek` | IndicatorSeekBar | ذهبي موحّد |
| `0x7F0A00A0` | `animeDetailsDeleteRatingBtn` | MaterialButton Icon | error tint |
| `0x7F0A04C3` | `animeDetailsEpisodesTitle` | TextView | SectionHeader |
| `0x7F0A0168` | `animeDetailsEpisodesSeeAll` | TextView | Action أساسي |
| `0x7F0A030E` | `animeDetailsEpisodesRecycler` | RecyclerView | — |
| `0x7F0A04C1` | `animeDetailsCharactersTitle` | TextView | SectionHeader |
| `0x7F0A0167` | `animeDetailsCharactersSeeAll` | TextView | Action أساسي |
| `0x7F0A01FC` | `animeDetailsCharactersRecycler` | RecyclerView | أفقي |
| `0x7F0A04C7` | `animeDetailsStaffTitle` | TextView | SectionHeader |
| `0x7F0A0169` | `animeDetailsStaffSeeAll` | TextView | Action أساسي |
| `0x7F0A0757` | `animeDetailsStaffRecycler` | RecyclerView | أفقي |
| `0x7F0A04C9` | `animeDetailsStatsTitle` | TextView | SectionHeader |
| `0x7F0A037A` | `animeDetailsStatsRecycler` | RecyclerView | — |
| `0x7F0A00A6` | `animeDetailsTrailerSection` | LinearLayout | — |
| `0x7F0A098A` | `animeDetailsTrailerPlayer` | YouTubePlayerView | radius 16 |
| `0x7F0A00A4` | `animeDetailsRelatedSection` | LinearLayout | gone افتراضياً |
| `0x7F0A0696` | `animeDetailsRelatedRecycler` | RecyclerView | أفقي |
| `0x7F0A075E` | `animeDetailsState` | StateLayout | نص الحالة نفسه |

**خطوات الربط (بدون كسر أي كود):**
1. انسخ محتوى `design-system/res` إلى `app/src/main/res` (دمج، لا استبدال).
2. أضف أسماء الـ IDs إلى `values/ids.xml` بنفس القيم الحالية (`@id/...` type `id`) أو استبدلها في XML بأسمائك الحالية مباشرة.
3. استبدل ملف `Jk.xml` بالمحتوى الجديد — نفس الشجرة، نفس الـ IDs، لا تغيير على findViewById/dataBinding/viewBinding.
4. الواجهات الفرعية (`item_episode`, `item_character`, `item_anime_card`, `item_chip_genre`) تستبدل عناصر الأدابترز بنفس الطريقة.
