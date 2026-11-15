import json, re, html

LATIN = re.compile(r"[A-Za-z0-9$°µΩ@][A-Za-z0-9$%°µΩ.,:\/+#&@_'’-]*(?:\s+[A-Za-z0-9$°µΩ@][A-Za-z0-9$%°µΩ.,:\/+#&@_'’-]*)*")

def r(t):
    """escape + isolate Latin runs (raw slides don't get the builder's treatment)"""
    out, last = [], 0
    for m in LATIN.finditer(t):
        out.append(html.escape(t[last:m.start()], quote=True))
        out.append(f'<span dir="ltr">{html.escape(m.group(0), quote=True)}</span>')
        last = m.end()
    out.append(html.escape(t[last:], quote=True))
    return ''.join(out)

def head(eyebrow, title, sub=None):
    s = f'<div class="hd"><div class="eyebrow"><span class="dot"></span>{r(eyebrow)}</div><h1 class="title">{title}</h1>'
    if sub: s += f'<p class="sub">{sub}</p>'
    return s + '</div>'

def take(t):
    return f'<div class="take" style="margin-top:32px;font-size:30px;">{t}</div>'

def acc(t):
    return f'<span class="spec">{r(t)}</span>'

COPY = ('<button type="button" class="chip copy-btn" style="background:var(--c1);color:#fff;border:0;cursor:pointer;font-family:inherit;" '
        'onmouseup="this.blur()" onclick="var b=this,t=b.parentNode.parentNode.querySelector(\'.prompt\').innerText;'
        'navigator.clipboard.writeText(t).then(function(){b.textContent=\'הועתק\';setTimeout(function(){b.textContent=\'העתקה\'},1600)})">העתקה</button>')
PRINT_CSS = '<style>@media print{.copy-btn{display:none!important}}</style>'

def prompt_box(label, text, fs=30):
    return (f'<div class="glass fx col" style="flex:1;padding:36px 52px;gap:30px;min-height:0;justify-content:center;">'
            f'<div class="fx ac jb"><span class="chip" style="background:var(--bg-2);color:var(--c5);">{r(label)}</span>{COPY}</div>'
            f'<p class="prompt ink-t fw5" style="white-space:pre-wrap;font-size:{fs}px;line-height:1.5;margin:0;">{r(text)}</p></div>')

def stage(inner):
    return f'<div class="f1 fx col" style="margin-top:36px;min-height:0;">{inner}</div>'

ROLES = [
    ("ניהול קהילה ותוכניות", 1, """אני מוביל/ה את תחום הקהילה והתוכניות בעמותת "חלאסרטן" (רשת תמיכה וקהילה לחולי ומחלימי סרטן צעירים בגילאי 18-44).
הצוות שלי מפיק מענים רגשיים, מפגשי קהילה, מדריכי מיצוי זכויות וליווי לחדשים.
כתוב תמיד בעברית ישירה, אנושית ובגובה העיניים — בלי קלישאות רפואיות מתנשאות ובלי "פילרים".
כשאתה מנסח תוכן לקהילה או סיכום תוכנית, פתח בצורך האמיתי של הצעירים לפני הפתרון התפעולי.
סמן תמיד הנחות שדורשות בדיקה רגישה או אישור צוות מקצועי לפני פרסום."""),
    ("גיוס משאבים וקרנות", 3, """אני מוביל/ה את תחום גיוס המשאבים, השותפויות והקרנות בעמותת "חלאסרטן".
אנחנו מגישים בקשות מענקים לקרנות בארץ ובחו"ל, בונים הצעות שותפות לחברות עסקיות ומפיקים דוחות אימפקט לתורמים.
התאם את ברירת המחדל שלך לכתיבה מבוססת-נתונים, ממוקדת תוצאות (Impact) ומשכנעת.
בכל פעם שאתה מציין נתון מספרי או מדד הצלחה, ציין מאיזה מסמך מקור הוא נלקח.
הדגש תמיד את הערך הייחודי של חלאסרטן בטיפול בצעירים חולי ומחלימי סרטן."""),
    ("מנכ\"לות, כספים ותפעול", 5, """אני בצוות הניהול והכספים של עמותת "חלאסרטן" (ע"ר).
אנחנו מנהלים תקציבי תוכניות, דוחות ביצוע מול תקציב, התקשרויות ספקים ודיווחים לוועד המנהל.
התאם את התשובות שלך לתקצירי מנהלים חדים, טבלאות השוואה ברורות ושורה תחתונה כספית בראש המסמך.
הצף תמיד סיכונים תזרימיים, חריגות תקציביות או סעיפים שחסרה בהם אסמכתא.
הימנע מהקדמות ארוכות — גש ישר למספרים ולהמלצה הניהולית."""),
]

def roles_slide():
    cols = []
    for name, c, text in ROLES:
        cols.append(f'<div class="glass fx col" style="flex:1;padding:30px 34px;gap:18px;min-width:0;border-top:6px solid var(--c{c});">'
                    f'<div class="fx ac jb" style="gap:12px;"><span class="ink-t fw8" style="font-size:30px;">{r(name)}</span>{COPY}</div>'
                    f'<p class="prompt ink-t fw5" style="white-space:pre-wrap;font-size:25px;line-height:1.5;margin:0;">{r(text)}</p></div>')
    return PRINT_CSS + head("דוגמאות · Instructions for Claude", f'כך נראית תוצאה של ראיון: {acc("דוגמה לכל תפקיד")}',
                            r("להשוואה עם מה שקיבלתם, או להעתקה כנקודת פתיחה")) + \
        stage(f'<div class="fx" style="flex:1;gap:28px;min-height:0;">{"".join(cols)}</div>')

TOKENS = ["ח", "ל", "א", "ס", "ר", "ט", "ן", "ן~", "מ", "ח", "ב", "ר", "ת", " ", "צ", "ע", "י", "ר", "ים", " ", "ח", "ו", "ל", "ים", " ", "ו", "מ", "ח", "ל", "י", "מ", "ים"]

def tokens_slide():
    chips = ''.join(f'<span class="chip" style="font-size:40px;padding:16px 26px;background:var(--c{(i % 5) + 1});color:#fff;">{t}</span>' for i, t in enumerate(TOKENS))
    words = ''.join(f'<span class="chip" style="font-size:44px;padding:16px 30px;background:#fff;color:var(--ink);border:2px solid var(--c4);">{w}</span>' for w in "חלאסרטן מחברת צעירים חולים".split())
    row = lambda lbl, inner: (f'<div class="fx col" style="gap:22px;"><span class="muted fw7" style="font-size:28px;">{lbl}</span>'
                              f'<div class="fx wrap" style="gap:16px;">{inner}</div></div>')
    body = (f'<div class="glass fx col" style="flex:1;padding:44px 64px;justify-content:space-evenly;">'
            f'{row("איך אנחנו קוראים: 4 מילים", words)}{row("איך Claude קורא: 9 טוקנים", chips)}</div>')
    return head("מושגי יסוד", f'מודל שפה לא קורא מילים. הוא קורא {acc("טוקנים")}',
                "בעברית כל מילה מתפרקת ל-2 עד 4 טוקנים, באנגלית בערך טוקן למילה.") + stage(body) + \
        take(f'כל טוקן שנכנס וכל טוקן שיוצא <span class="hi">נספר במכסה</span> שלכם.')

CW = {
    "d": ("1. התוצר", 1, ["רשימה מדורגת עם המלצות והערות", "מסמך מנהלים של 2 עמודים", "שקף מסכם לישיבת הוועד המנהל", "טבלת השוואת תוכניות ותקציב"]),
    "i": ("2. חומרי הגלם", 3, ["תיקיית משובי קהילה ופעילויות רבעון 3", "הדוח של הרבעון הקודם כתבנית ייחוס לעיצוב", "קבצי ה-PDF של בקשות התמיכה והמענקים בלבד", "תיקיית ה-Obsidian של פרויקט המנטורינג"]),
    "n": ("3. דגש והקשר", 5, ["קהל היעד הוא הנהלת חלאסרטן בריטריט התכנון השנתי שמחליטה אילו תוכניות להרחיב", "פתח ישר בשורה התחתונה ובהמלצה המעשית המובילה", "סמן בבירור כל נתון שחסר או שלא ניתן לאמת מתוך הקבצים"]),
}

def cowork_slide():
    rows = []
    for g, (lbl, c, opts) in CW.items():
        btns = ''.join(
            f'<button type="button" class="chip cw" data-g="{g}" data-c="{c}" data-v="{html.escape(o, quote=True)}" onmouseup="this.blur()" '
            f'style="font-family:inherit;cursor:pointer;font-size:22px;font-weight:700;border:2px solid var(--c{c});'
            f'background:{"var(--c%d)" % c if k == 0 else "#fff"};color:{"#fff" if k == 0 else "var(--ink)"};">{r(o)}</button>'
            for k, o in enumerate(opts))
        rows.append(f'<div class="fx ac" style="gap:24px;"><span class="fw8" style="font-size:28px;color:var(--c{c});width:210px;flex-shrink:0;">{lbl}</span>'
                    f'<div class="fx wrap" style="gap:12px;">{btns}</div></div>')
    first = {g: v[2][0] for g, v in CW.items()}
    prompt = f'תכין לי {first["d"]} על בסיס {first["i"]} — {first["n"]}.'
    out = (f'<div class="glass fx col" style="padding:28px 44px;gap:20px;">{"".join(rows)}</div>'
           f'<div class="inkcard fx col" style="margin-top:24px;padding:28px 44px;gap:14px;flex:1;justify-content:center;">'
           f'<div class="fx ac jb"><span class="chip" style="background:rgba(255,255,255,.14);color:var(--on-dark);">הפרומפט ל-Cowork</span>{COPY}</div>'
           f'<p class="prompt cw-out fw6" style="font-size:30px;line-height:1.45;margin:0;color:var(--on-dark);">{r(prompt)}</p></div>')
    script = """<script>(function(){
var sel={d:0,i:0,n:0};
function upd(){var v={};document.querySelectorAll('.cw').forEach(function(b){var on=b.dataset.on==='1';
b.style.background=on?'var(--c'+b.dataset.c+')':'#fff';b.style.color=on?'#fff':'var(--ink)';if(on)v[b.dataset.g]=b.dataset.v;});
document.querySelector('.cw-out').textContent='תכין לי '+v.d+' על בסיס '+v.i+' — '+v.n+'.';}
document.querySelectorAll('.cw').forEach(function(b,i){if(b.previousElementSibling===null)b.dataset.on='1';
b.addEventListener('click',function(){document.querySelectorAll('.cw[data-g="'+b.dataset.g+'"]').forEach(function(x){x.dataset.on='0'});b.dataset.on='1';upd();});});
upd();})();</script>"""
    return PRINT_CSS + head("Cowork · תרגול", f'נוסחת המשימה: תוצר + חומרי גלם + {acc("דגש")}',
                            "ה-Role כבר שמור ב-Global Instructions. לחצו על אפשרות בכל שורה.") + stage(out) + script

def prompt_slide(eyebrow, title, sub, label, text, takeaway, fs=30):
    return PRINT_CSS + head(eyebrow, title, sub) + stage(prompt_box(label, text, fs)) + (take(takeaway) if takeaway else '')

REVERSE = """אני חבר/ת הנהלה בעמותת 'חלאסרטן' (קהילה ותמיכה לחולי ומחלימי סרטן צעירים). אני רוצה שתעזור לי לנסח את ה-Personal Instructions שלך כדי שתכיר אותי, את תפקידי ואת סגנון העבודה שלי.
ראיין אותי עכשיו באמצעות 10 שאלות ממוקדות (שאל אותן בשני סבבים של 5 שאלות) על תחומי האחריות שלי, סוגי המסמכים שאני כותב/ת, הטון המועדף עליי והדברים שחשוב לי להימנע מהם. בסיום הראיון, כתוב לי בלוק Instructions מוכן להעתקה להגדרות הקבועות שלך."""

SKILL_PROMPT = """בוא ניצור יחד Skill חדש בשם halasartan-presentation עבור הנהלת עמותת 'חלאסרטן'.
הסקיל צריך לקבל נקודות תוכן או מסמך גולמי ולהפיק קובץ HTML יחיד של מצגת שקפים בעברית (RTL) הכוללת:
1. הטמעת הלוגו של חלאסרטן בראש/תחתית השקפים ופלטת צבעים מותאמת לעמותה.
2. שפה אנושית, ישירה ובגובה העיניים.
3. ניווט מקלדת מלא והגדרות @media print מובנות כך שניתן להדפיס את המצגת ישירות לקובץ PDF נקי."""

meta = {
    "title": "להפוך את Claude לשותף עבודה · הנהלת חלאסרטן",
    "lang": "he", "dir": "rtl", "font": "Heebo",
    "author": "עמית רוזן",
    "logo": "assets/halasartan-logo.png", "logoSize": [205, 90], "logoOffset": [104, 40],
    "timer": False,
    "tokens": {
        "c1": "#C2185B", "c2": "#DE4681", "c3": "#F06A9B", "c4": "#FFB3CF", "c5": "#8E3B63", "c6": "#5E5257",
        "ink": "#2B2326", "ink2": "#3A2F33", "muted": "#6E6267", "bg": "#FFF7FA", "bg2": "#FBE6EE", "highlight": "#FF9CC2",
        "accent": "linear-gradient(135deg, #B0124F 0%, #DE4681 55%, #F06A9B 100%)",
        "accentOnDark": "linear-gradient(135deg, #F06A9B 0%, #FF9CC2 55%, #FFD1E2 100%)"
    }
}


# ---------- visual helpers (bento cards in the style of meetings 2 and 4) ----------
def icard(icon, title, text, c, extra='', fs=31, style='', raw=False):
    return (f'<div class="glass fx col" style="flex:1;min-width:0;padding:40px 42px;gap:24px;justify-content:center;border-top:7px solid var(--c{c});{style}">'
            f'<span style="font-size:76px;line-height:1;">{icon}</span>'
            f'<span class="fw8" style="font-size:42px;color:var(--c{c});">{r(title)}</span>'
            f'<p class="ink-t fw5" style="font-size:{fs}px;line-height:1.45;margin:0;">{text if raw else r(text)}</p>{extra}</div>')

def foot(text, c):
    return (f'<div class="fw7" style="margin-top:8px;padding-top:18px;border-top:2px dashed var(--c4);font-size:27px;color:var(--c{c});">{r(text)}</div>')

def row(*cards, gap=28):
    return f'<div class="fx" style="flex:1;gap:{gap}px;min-height:0;">{"".join(cards)}</div>'

def quote(t, fs=27):
    return (f'<div style="background:var(--ink);color:var(--on-dark);border-radius:14px;padding:20px 28px;font-size:{fs}px;line-height:1.5;font-weight:500;">{t}</div>')

def tag(t, good):
    bg = 'var(--c1)' if good else 'var(--c6)'
    return f'<span class="chip" style="background:{bg};color:#fff;font-size:24px;">{t}</span>'

def icards_slide(eyebrow, title, sub, cards, takeaway=None):
    return head(eyebrow, title, sub) + stage(row(*cards)) + (take(takeaway) if takeaway else '')

def agenda_slide():
    items = [("🧠", "איך Claude חושב", "טוקנים, פרומפטים, ו-Instructions שמכירים אתכם", 1, "תרגול: הראיון ההפוך"),
             ("🛠️", "איפה עובדים", "Chat, Cowork, Code, מודלים, תיקייה ובטיחות", 3, "תרגול: Cowork"),
             ("📁", "זיכרון וצוות", "Projects, משימות מתוזמנות וארבע שכבות", 5, None),
             ("⚡", "יכולות", "סקילים, קונקטורים, פלאגינים ו-Chrome", 2, "תרגול: סקיל מצגות"),
             ("🎯", "השולחן שלכם", "מפצחים יחד משימה אמיתית מהעבודה", 1, "תרגול: Use Cases")]
    cards = []
    for i, (ic, t, x, c, ex) in enumerate(items, 1):
        cards.append(f'<div class="glass fx col" style="flex:1;min-width:0;padding:30px 30px;gap:16px;border-top:7px solid var(--c{c});">'
                     f'<div class="fx ac jb"><span style="font-size:68px;line-height:1;">{ic}</span><span class="numchip" style="background:var(--c{c});">{i}</span></div>'
                     f'<span class="fw8" style="font-size:38px;color:var(--ink);margin-top:14px;">{r(t)}</span>'
                     f'<p class="muted fw5" style="font-size:28px;line-height:1.4;margin:0;">{r(x)}</p>'
                     + (f'<span class="chip" style="margin-top:auto;background:var(--bg-2);color:var(--c5);font-size:21px;">{r(ex)}</span>' if ex else '') + '</div>')
    return head("מה הולך לקרות היום", f'שעתיים, חמישה פרקים, {acc("ארבעה תרגולים")}') + stage(row(*cards, gap=22)) + \
        take('בסוף המפגש כל אחד יוצא עם <span class="hi">תהליך אחד שכבר עובד</span>.')

def llm_slide():
    models = ''.join(f'<span class="chip" style="font-size:28px;padding:10px 22px;{st}">{m}</span>' for m, st in
                     [("ChatGPT", "background:#fff;color:var(--muted);border:2px solid var(--c4);"), ("Claude", "background:var(--c1);color:#fff;"), ("Gemini", "background:#fff;color:var(--muted);border:2px solid var(--c4);")])
    card = lambda c, f: f'<div class="glass fx col" style="flex:{f};min-width:0;padding:38px 44px;gap:24px;border-top:7px solid var(--c{c});">'
    llm = (card(5, 1) + f'<span class="fw8" style="font-size:38px;color:var(--c5);">🧠 מה זה LLM?</span>'
           f'<span class="ink-t fw7" style="font-size:28px;" dir="ltr">Large Language Model</span>'
           f'<p class="ink-t fw5" style="font-size:30px;line-height:1.45;margin:0;">מודל שפה גדול: קרא המון טקסט, ולמד מה בדרך כלל בא אחרי מה. כולם מודלי שפה, כל אחד בנוי קצת אחרת.</p>'
           f'<div class="fx wrap" style="gap:12px;" dir="ltr">{models}</div>'
           f'<p class="muted fw6" style="font-size:27px;line-height:1.4;margin:0;margin-top:auto;">לא מוח אנושי, אלא מנוע שפה ששואל כל הזמן: מה ההמשך הכי סביר?</p></div>')
    bars = [("שטיח", 61, 1), ("ספה", 24, 3), ("כיסא", 9, 5)]
    b = ''.join(f'<div class="fx ac" style="gap:18px;"><span class="ink-t fw7" style="font-size:30px;width:96px;">{w}</span>'
                f'<div style="flex:1;height:28px;border-radius:999px;background:var(--bg-2);"><div style="width:{v}%;height:100%;border-radius:999px;background:var(--c{c});"></div></div>'
                f'<span class="fw8" style="font-size:30px;color:var(--c{c});width:76px;">{v}%</span></div>' for w, v, c in bars)
    right = (card(3, 1.1) + f'<span class="fw8" style="font-size:38px;color:var(--c3);">✍️ איך Claude כותב</span>'
             f'<p class="ink-t fw5" style="font-size:30px;line-height:1.4;margin:0;">מנחש את ההמשך הכי סביר, מוסיף, וחוזר חלילה:</p>'
             f'{quote("״החתול ישב על ה___״", 34)}<div class="fx col" style="gap:18px;">{b}</div>'
             f'<span class="muted" style="font-size:22px;margin-top:auto;">המספרים להמחשה בלבד</span></div>')
    return head("מושגי יסוד", f'Claude הוא מודל שפה: הוא {acc("מנחש את ההמשך")}') + stage(row(llm, right, gap=28)) + \
        take('🤔 ומה בדיוק הוא מנחש? לא מילים שלמות, אלא <span class="hi">חתיכות קטנות של טקסט שנקראות טוקנים</span>.')

def tokens_slide2():
    def tchip(i, t):
        if t == " ":
            return '<span class="chip" style="font-size:30px;padding:8px 10px;min-width:38px;background:transparent;border:2px dashed rgba(255,255,255,.45);">&nbsp;</span>'
        faded = t.endswith("~")
        return f'<span class="chip" style="font-size:30px;padding:8px 16px;background:var(--c{(i % 5) + 1});color:#fff;{"opacity:.5;" if faded else ""}">{t.rstrip("~")}</span>'
    chips = ''.join(tchip(i, t) for i, t in enumerate(TOKENS))
    words = ''.join(f'<span class="chip" style="font-size:32px;padding:9px 22px;background:#fff;color:var(--ink);border:2px solid var(--c4);">{w}</span>' for w in "חלאסרטן מחברת צעירים חולים ומחלימים".split())
    star = '<span style="color:var(--c1);font-weight:800;">*</span>'
    main = (f'<div class="glass fx col" style="flex:1.9;min-width:0;padding:38px 44px;gap:22px;border-top:7px solid var(--c1);">'
            f'<span class="muted fw7" style="font-size:27px;">אתם כותבים 5 מילים:</span><div class="fx wrap" style="gap:12px;">{words}</div>'
            f'<span class="muted fw7" style="font-size:27px;">Claude קורא {len(TOKENS)} טוקנים{star}:</span>'
            f'<div class="fx wrap" style="gap:8px;padding:20px;border-radius:16px;background:var(--ink);">{chips}</div>'
            f'<span class="ink-t fw8" style="font-size:32px;">{r("35 תווים, " + str(len(TOKENS)) + " טוקנים:")} <span style="color:var(--c1);">כמעט טוקן לכל אות</span></span>'
            f'<p class="muted fw5" style="font-size:23px;line-height:1.4;margin:0;margin-top:auto;">{star} באנגלית כמות הטוקנים והמחיר שונים, בדרך כלל נמוכים יותר.</p></div>')
    pts = ["יחידת הטקסט הקטנה ש-Claude עובד איתה.", "יכול להיות מילה, חלק ממילה, אות או רווח.", "באנגלית בערך טוקן למילה. בעברית, כמעט טוקן לכל אות."]
    pl = ''.join(f'<div class="fx" style="gap:16px;align-items:baseline;"><span class="bullet" style="background:var(--c{c});width:16px;height:16px;flex-shrink:0;"></span>'
                 f'<span class="ink-t fw6" style="font-size:30px;line-height:1.4;">{r(t)}</span></div>' for t, c in zip(pts, [1, 3, 5]))
    side = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:38px 40px;gap:30px;justify-content:center;border-top:7px solid var(--c5);">'
            f'<span class="fw8" style="font-size:38px;color:var(--c5);">🧩 מה זה טוקן?</span>{pl}</div>')
    return head("מושגי יסוד · טוקנים", f'אתם שולחים הודעה ל-Claude. {acc("איך הוא קורא אותה?")}') + stage(row(main, side, gap=28)) + \
        take('כל טוקן שנכנס וכל טוקן שיוצא <span class="hi">נספר במכסה</span>, וכל מילה בפרומפט מכוונת את הניחוש.')

def prompt_merged_slide():
    comps = [("תפקיד", "Role", "מי אתם ומה המומחיות?", True), ("הקשר", "Context", "חלאסרטן וקהל היעד", True),
             ("הוראה", "Instruction", "מה המשימה היום?", False), ("נתוני קלט", "Input", "המסמך או הנתונים", False),
             ("פורמט וטון", "Output", "בגובה העיניים, מבנה מועדף", True)]
    rows = ''.join(
        f'<div class="fx ac" style="gap:16px;"><span class="numchip" style="background:var(--c{1 if fx else 6});width:46px;height:46px;font-size:24px;">{i}</span>'
        f'<div class="fx col" style="flex:1;gap:2px;"><span class="ink-t fw8" style="font-size:31px;">{r(n)} <span class="muted fw6" style="font-size:23px;" dir="ltr">{e}</span></span>'
        f'<span class="muted fw5" style="font-size:25px;">{r(q)}</span></div>'
        + ('<span class="chip" style="background:var(--c1);color:#fff;font-size:22px;">קבוע</span>' if fx else
           '<span class="chip" style="background:#fff;color:var(--c6);border:2px solid var(--c6);font-size:22px;">משתנה</span>') + '</div>'
        for i, (n, e, q, fx) in enumerate(comps, 1))
    comp = (f'<div class="glass fx col" style="flex:.68;min-width:0;padding:28px 34px;gap:16px;justify-content:center;border-top:7px solid var(--c5);">'
            f'<span class="fw8" style="font-size:34px;color:var(--c5);">🧱 5 המרכיבים</span>{rows}</div>')
    def dcard(icon, title, text, c):
        return (f'<div class="glass fx col" style="flex:1;min-width:0;padding:22px 30px;gap:10px;justify-content:center;border-top:7px solid var(--c{c});">'
                f'<span class="fw8" style="font-size:30px;color:var(--c{c});">{icon} {r(title)}</span>'
                f'<span class="ink-t fw5" style="font-size:26px;line-height:1.38;">{r(text)}</span></div>')
    defs = (f'<div class="fx" style="gap:22px;flex:.52;min-height:0;">'
            f'{dcard("💬", "ההוראות שנותנים ל-Claude", "הטקסט שכותבים לו: שאלה, בקשה, הוראה או הקשר. הכל פרומפט.", 1)}'
            f'{dcard("🔗", "הקשר למודל שפה", "הפרומפט מתפרק לטוקנים, ומודל השפה מנחש מהם את ההמשך. לכן כל מילה מכוונת את התשובה.", 3)}</div>')
    hi = lambda t: f'<span style="color:var(--highlight);font-weight:800;">{r(t)}</span>'
    bad = (f'<div class="glass fx col" style="flex:.8;min-width:0;padding:24px 30px;gap:14px;justify-content:center;border-top:7px solid var(--c6);">'
           f'<div>{tag("✗ פרומפט עמום", False)}</div>{quote(r("״תכתוב לי פוסט לקהילה על מפגש זכויות חדש.״"), 28)}'
           f'<span class="muted fw6" style="font-size:24px;">טקסט גנרי ומנותק</span></div>')
    good_q = ('״' + hi("אני מנהל/ת הקהילה בחלאסרטן (צעירים חולי סרטן 18-44).") + ' ' + hi("כתוב בעברית ישירה ובגובה העיניים, בלי קלישאות.") + ' '
              + r("נסח פוסט שמזמין למפגש מיצוי זכויות ביום ג׳, עם 3 סיבות למה שווה להגיע.") + '״')
    good = (f'<div class="glass fx col" style="flex:1.3;min-width:0;padding:24px 30px;gap:14px;justify-content:center;border-top:7px solid var(--c1);">'
            f'<div>{tag("✓ פרומפט מלא", True)}</div>{quote(good_q, 25)}'
            f'<span class="ink-t fw6" style="font-size:24px;">המודגש = ההקשר: מי, למי ובאיזה טון</span></div>')
    ex = f'<div class="fx" style="gap:22px;flex:1;min-height:0;">{bad}{good}</div>'
    leftcol = f'<div class="fx col" style="flex:1.3;min-width:0;gap:22px;min-height:0;">{defs}{ex}</div>'
    return head("הנדסת פרומפטים", f'מה זה {acc("פרומפט")}?') + stage(row(comp, leftcol, gap=24)) + \
        take('פרומפט טוב = תקשורת טובה: ככל שההקשר מדויק יותר, <span class="hi">התוצאה טובה יותר</span>.')

def context_slide():
    import base64
    img = base64.b64encode(open('assets/context-meter.png', 'rb').read()).decode()
    def src(icon, title, text, c):
        return (f'<div class="glass fx col" style="flex:1;min-width:0;padding:30px 40px;gap:12px;justify-content:center;border-top:7px solid var(--c{c});">'
                f'<span class="fw8" style="font-size:38px;color:var(--c{c});">{icon} {r(title)}</span>'
                f'<span class="ink-t fw5" style="font-size:30px;line-height:1.4;">{r(text)}</span></div>')
    plus = '<span class="fw8" style="font-size:72px;line-height:1;color:var(--c3);align-self:center;">+</span>'
    top = (f'<div class="fx" style="gap:22px;flex:1;min-height:0;">'
           f'{src("📤", "מה שאנחנו שולחים", "הודעות, מסמכים, קבצים ותמונות", 1)}{plus}'
           f'{src("💬", "מה ש-Claude עונה", "כל התשובות שהוא כותב לנו בחזרה", 5)}</div>')
    bottom = (f'<div class="glass fx ac" style="flex:1;min-height:0;gap:48px;padding:24px 48px;border-top:7px solid var(--c3);">'
              f'<div class="fx col" style="flex:1;gap:10px;"><span class="fw8" style="font-size:38px;color:var(--c3);">📊 כך זה נראה ב-Claude</span>'
              f'<span class="ink-t fw5" style="font-size:30px;line-height:1.4;">{r("34% מהמיליון כבר בשימוש: 335.2k מתוך 1M טוקנים.")}</span></div>'
              f'<img src="data:image/png;base64,{img}" alt="מד ההקשר ב-Claude: 34% בשימוש, 335.2k מתוך 1M" '
              f'style="height:100%;max-height:170px;width:auto;border-radius:12px;border:1px solid var(--c4);background:#fff;padding:10px 16px;box-sizing:content-box;"></div>')
    return head("חלון ההקשר", f'בכל שיחה מוקצים {acc("מיליון טוקנים")}',
                "הם מתמלאים בכל מה שנכנס לשיחה ובכל מה שיוצא ממנה.") + \
        stage(f'<div class="fx col" style="flex:1;gap:24px;min-height:0;">{top}{bottom}</div>') + \
        take('ככל שהתכנים והתשובות ארוכים יותר, <span class="hi">מגיעים מהר יותר למיליון</span>. משימה חדשה? צ׳אט חדש.')

def skills_intro_slide():
    def line(icon, lead, text, c):
        return (f'<div class="fx" style="gap:18px;align-items:flex-start;"><span style="font-size:42px;line-height:1.15;">{icon}</span>'
                f'<span class="ink-t fw5" style="font-size:28px;line-height:1.4;"><span class="fw8" style="color:var(--c{c});">{r(lead)}</span> {r(text)}</span></div>')
    know = (f'<div class="glass fx col" style="flex:1.1;min-height:0;padding:26px 36px;gap:18px;justify-content:center;border-top:7px solid var(--c1);">'
            f'<span class="fw8" style="font-size:34px;color:var(--c1);">🤔 מכירים את זה?</span>'
            + line("🔁", "משימה שחוזרת על עצמה:", "סיכום שבועי, מכתב לקופת חולים, פוסט לקהילה.", 1)
            + line("💬", "שיחה ארוכה עם Claude:", "אחרי הרבה תיקונים הגעתם לתוצאה מושלמת. ובפעם הבאה? מתחילים מאפס.", 1) + '</div>')
    ask = (f'<div class="glass fx col" style="flex:.9;min-height:0;padding:26px 36px;gap:16px;justify-content:center;border-top:7px solid var(--c3);">'
           f'<span class="fw8" style="font-size:32px;color:var(--c3);">✨ במקום להדביק את אותו פרומפט ארוך, פשוט מבקשים:</span>'
           f'{quote(r("״על בסיס השיחה הזו, צור לי Skill שאוכל להשתמש בו שוב בפעם הבאה.״"), 28)}</div>')
    right = f'<div class="fx col" style="flex:1.05;min-width:0;gap:22px;min-height:0;">{know}{ask}</div>'
    items = [("🥕", "המרכיבים", "מה הוא מקבל מכם, ובאיזה סגנון לכתוב."), ("📋", "שלבי ההכנה", "מה עושים, ובאיזה סדר."), ("⭐", "איך נראית מנה מוצלחת", "דוגמה לתוצאה שאהבתם.")]
    its = ''.join(line(ic, t + ":", x, 5) for ic, t, x in items)
    chef = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:30px 38px;gap:22px;justify-content:center;border-top:7px solid var(--c5);">'
            f'<div class="fx ac" style="gap:18px;"><span style="font-size:64px;line-height:1;">🧑‍🍳</span><div class="fx col"><span class="fw8" style="font-size:36px;color:var(--c5);">המתכון להכנת המנה המושלמת</span>'
            f'<span class="muted fw6" style="font-size:26px;">אתם כותבים, Claude מבשל</span></div></div>'
            f'{its}'
            f'<div style="background:var(--bg-2);border:2px solid var(--c4);border-radius:16px;padding:18px 24px;font-size:28px;line-height:1.4;" class="ink-t fw7">'
            f'🔥 Claude מדליק את התנור ומבצע, ובכל פעם יוצאת <span style="color:var(--c1);">אותה מנה טעימה</span>.</div></div>')
    return head("סקילים", f'Skill: {acc("המתכון שלכם")} ל-Claude') + stage(row(right, chef, gap=26)) + \
        take('Skill = <span class="hi">מתכון למשימה מסוימת</span>, ש-Claude שולף בדיוק כשצריך.')

def skills_example_slide():
    import base64
    img = base64.b64encode(open('assets/skill_morning_board.png', 'rb').read()).decode()
    left = (f'<div class="glass fx col" style="flex:1.2;min-width:0;min-height:0;padding:22px 26px;gap:12px;border-top:7px solid var(--c1);">'
            f'<div style="flex:1;min-height:0;display:flex;align-items:center;justify-content:center;">'
            f'<img src="data:image/png;base64,{img}" alt="צילום מסך: לוח משימות יומי עם עמודות לביצוע, בתהליך והושלם, שנבנה אוטומטית ממיילים, יומן ומשימות" '
            f'style="max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;border:1px solid var(--c4);"></div>'
            f'<span class="muted fw6" style="font-size:22px;text-align:center;">התוצאה: לוח יומי שאפשר לגרור בו משימות (נתונים לדוגמה)</span></div>')
    def li(icon, t):
        return f'<div class="fx ac" style="gap:16px;"><span style="font-size:34px;line-height:1;">{icon}</span><span class="ink-t fw6" style="font-size:27px;">{r(t)}</span></div>'
    write = (f'<div class="glass fx col" style="flex:none;padding:16px 34px;gap:8px;justify-content:center;border-top:7px solid var(--c3);">'
             f'<span class="fw8" style="font-size:30px;color:var(--c3);">✍️ מה אני כותב</span>{quote("☀️ ״תתחיל את היום שלי״", 28)}</div>')
    does = (f'<div class="glass fx col" style="flex:1;min-height:0;padding:18px 34px;gap:10px;justify-content:center;border-top:7px solid var(--c5);">'
            f'<span class="fw8" style="font-size:30px;color:var(--c5);">🤖 מה ה-Skill עושה לבד</span>'
            + li("📧", "קורא מיילים שעוד לא נקראו") + li("📅", "בודק מה יש ביומן היום") + li("✅", "אוסף משימות פתוחות") + li("🗂️", "ממיין לפי דחיפות ובונה לוח אחד")
            + '</div>')
    share = ('<div class="fx ac" style="gap:14px;padding:10px 28px;border-radius:16px;background:var(--bg-2);border:2px dashed var(--c3);flex:none;">'
             '<span style="font-size:34px;">🎁</span><span class="ink-t fw8" style="font-size:27px;">את הסקיל הזה אשתף אתכם</span></div>')
    right = f'<div class="fx col" style="flex:1;min-width:0;gap:18px;min-height:0;">{write}{does}{share}</div>'
    return head("סקילים · דוגמה אמיתית", f'Skill שבניתי: {acc("תדריך בוקר")}') + stage(row(right, left, gap=26)) + \
        take('משפט אחד, ותוצאה מלאה, <span class="hi">כי המתכון כבר כתוב</span>.')

def skill_structure_slide():
    chipd = 'background:rgba(255,255,255,.14);color:var(--highlight);'
    desc = (f'<div class="fx col" style="gap:8px;">'
            f'<div><span class="chip" style="{chipd}font-size:22px;" dir="ltr">description</span> <span class="fw7" style="font-size:22px;color:var(--on-dark-2);">כריכת המתכון</span></div>'
            f'<span class="fw6" style="font-size:25px;line-height:1.4;color:var(--on-dark);">{r("שם: תדריך בוקר")}</span>'
            f'<span class="fw5" style="font-size:25px;line-height:1.4;color:var(--on-dark);">{r("תיאור: בונה לוח משימות יומי מהמייל, מהיומן ומהמשימות. השתמש כשהמשתמש כותב ״תתחיל את היום שלי״.")}</span></div>')
    steps = ["בדוק מה ביקשו: תחילת יום או סוף יום", "אסוף מיילים, פגישות ומשימות פתוחות", "מיין: דחוף / בתהליך / בוצע", "בנה לוח אחד ברור", "אל תצטט תוכן אישי מהמיילים"]
    body = (f'<div class="fx col" style="gap:8px;">'
            f'<div><span class="chip" style="{chipd}font-size:22px;" dir="ltr">body</span> <span class="fw7" style="font-size:22px;color:var(--on-dark-2);">המתכון המלא</span></div>'
            + ''.join(f'<span class="fw5" style="font-size:25px;line-height:1.35;color:var(--on-dark);">{i}. {r(t)}</span>' for i, t in enumerate(steps, 1)) + '</div>')
    md = (f'<div class="inkcard fx col" style="flex:1.05;min-width:0;padding:26px 36px;gap:16px;justify-content:center;">'
          f'<div class="fx ac jb"><span class="fw8" style="font-size:30px;color:var(--on-dark);" dir="ltr">📄 SKILL.md</span><span class="fw6" style="font-size:22px;color:var(--on-dark-2);">בתרגום חופשי · קובץ טקסט אחד</span></div>'
          f'{desc}<div style="height:2px;background:rgba(255,255,255,.2);"></div>{body}</div>')
    def st(i, lead, text, c):
        return (f'<div class="fx" style="gap:16px;align-items:flex-start;"><span class="numchip" style="background:var(--c{c});width:46px;height:46px;font-size:24px;">{i}</span>'
                f'<span class="ink-t fw5" style="font-size:26px;line-height:1.4;"><span class="fw8" style="color:var(--c{c});">{r(lead)}</span> {r(text)}</span></div>')
    how = (f'<div class="glass fx col" style="flex:1;min-height:0;padding:26px 36px;gap:18px;justify-content:center;border-top:7px solid var(--c1);">'
           f'<span class="fw8" style="font-size:34px;color:var(--c1);">🤖 איך Claude קורא את זה?</span>'
           + st(1, "מעיין בתוכן העניינים:", "בתחילת השיחה הוא רואה רק את ה-description של כל הסקילים.", 1)
           + st(2, "מזהה התאמה:", "כתבתם ״תתחיל את היום שלי״? התיאור אומר לו שזה הזמן.", 3)
           + st(3, "פותח את המתכון:", "רק עכשיו הוא קורא את ה-body ומבצע שלב אחרי שלב.", 5) + '</div>')
    good = (f'<div class="glass fx col" style="flex:none;padding:16px 34px;gap:6px;border-top:7px solid var(--c3);">'
            f'<span class="ink-t fw6" style="font-size:25px;">{r("description טוב = Claude יודע מתי לשלוף את המתכון.")}</span>'
            f'<span class="ink-t fw6" style="font-size:25px;">{r("body טוב = המנה יוצאת טעימה.")}</span>'
            f'<span class="muted fw6" style="font-size:23px;">{r("ויכול לכלול גם לוגו ותבניות, דוגמאות וסקריפטים.")}</span></div>')
    right = f'<div class="fx col" style="flex:.95;min-width:0;gap:18px;min-height:0;">{how}{good}</div>'
    return head("סקילים · מבנה", f'ממה בנוי {acc("Skill")}?') + stage(row(md, right, gap=26)) + \
        take('זוכרים את הטוקנים? ככה אפשר להחזיק <span class="hi">עשרות סקילים</span> בלי להעמיס על Claude.')

def folders_safety_slide():
    tree = ("📁 Halasartan-Projects/\n  └─ 📁 2026-11-Donors-Event/\n       ├─ 📁 01-Raw-Materials/\n       ├─ 📁 02-Outputs/\n       └─ 📄 CLAUDE.md")
    legend = [("01-Raw-Materials", "מסמכי מקור ונתונים"), ("02-Outputs", "מצגות, דוחות ותוצרים"), ("CLAUDE.md", "הנחיות הפרויקט")]
    lg = ''.join(f'<div class="fx ac" style="gap:14px;font-size:25px;"><span class="dot" style="background:var(--c{c});"></span><span class="ink-t fw8" dir="ltr">{a}</span><span class="muted fw5">{r(b)}</span></div>'
                 for (a, b), c in zip(legend, [1, 3, 5]))
    folder = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:30px 36px;gap:18px;border-top:7px solid var(--c1);">'
              f'<div><span class="chip" style="background:var(--c1);color:#fff;font-size:26px;">📁 תיקייה ייעודית לכל פרויקט</span></div>'
              f'<pre dir="ltr" style="margin:0;background:var(--ink);color:var(--on-dark);border-radius:14px;padding:20px 26px;font-size:24px;line-height:1.5;font-family:ui-monospace,Menlo,Consolas,monospace;text-align:left;">{html.escape(tree)}</pre>'
              f'<div class="fx col" style="gap:8px;">{lg}</div>'
              f'<div class="fw7" style="margin-top:auto;font-size:25px;line-height:1.4;color:var(--c6);">{r("Claude קורא וכותב רק בתיקייה הזו, ולא ב-Downloads או ב-Desktop")}</div></div>')
    def mode(dot, name, text):
        return (f'<div class="fx" style="gap:16px;align-items:flex-start;"><span style="font-size:34px;line-height:1.2;">{dot}</span>'
                f'<span class="ink-t fw5" style="font-size:29px;line-height:1.4;"><span class="fw8">{r(name)}</span> {r(text)}</span></div>')
    rules = ''.join(f'<span class="chip" style="background:var(--bg-2);color:var(--c5);font-size:23px;padding:9px 18px;">{r(t)}</span>'
                    for t in ["💾 מגבים מה שאי אפשר לשחזר", "🧪 מנסים קודם על עותק", "✍️ ״טיוטה בלבד, אל תשלח״"])
    control = (f'<div class="glass fx col" style="flex:1.05;min-width:0;padding:30px 36px;gap:30px;border-top:7px solid var(--c5);">'
               f'<span class="fw8" style="font-size:38px;color:var(--c5);">🔐 אתם בשליטה</span>'
               + mode("🟢", "Ask before acting:", "ברירת המחדל. Claude עוצר לאישורכם לפני שליחה, פרסום ושיתוף.")
               + mode("🟡", "Act without asking:", "רק למשימות שאתם סומכים עליהן.")
               + mode("🔴", "מחיקה קבועה:", "תמיד שואל. אי אפשר לדלג.")
               + f'<div class="fx wrap" style="gap:10px;margin-top:auto;">{rules}</div></div>')
    return head("סדר ובטיחות", f'כל פרויקט מקבל {acc("תיקייה משלו")}') + stage(row(folder, control)) + \
        take('Claude מכין, אתם שולחים. <span class="hi">מאצילים את העבודה, לא את שיקול הדעת</span>.')

PRACTICE = """תסתכל על כל מה שיש בתיקייה הזו וכתוב לי סיכום: מה יש בה, איך המסמכים קשורים זה לזה, ומה הפתיע אותך.
טיוטה בלבד: אל תשנה ואל תמחק שום קובץ."""

def practice_slide():
    steps = [("בוחרים תיקייה עם חומר אמיתי", "או עותק שלה. לא קבצי הדגמה."), ("מחברים אפליקציה אחת", "זו שבה רוב ההקשר שלכם: מייל או דרייב."),
             ("מבקשים סיכום", "Claude מציג תוכנית ושואל שאלות. עונים ומאשרים."), ("בודקים מול מה שאתם יודעים", "מה Claude תפס שפספסתם? ומה הוא פספס?")]
    st = ''.join(f'<div class="fx" style="gap:18px;align-items:flex-start;"><span class="numchip" style="background:var(--c{c});width:50px;height:50px;font-size:26px;">{i}</span>'
                 f'<div class="fx col" style="gap:4px;"><span class="ink-t fw8" style="font-size:31px;">{r(t)}</span><span class="muted fw5" style="font-size:26px;line-height:1.4;">{r(x)}</span></div></div>'
                 for i, ((t, x), c) in enumerate(zip(steps, [1, 3, 5, 2]), 1))
    left = f'<div class="glass fx col" style="flex:.9;min-width:0;padding:32px 38px;gap:26px;justify-content:center;border-top:7px solid var(--c3);">{st}</div>'
    ideas = (f'<div class="glass fx col" style="flex:.8;min-height:0;padding:22px 34px;gap:12px;justify-content:center;border-top:7px solid var(--c5);">'
             f'<span class="fw8" style="font-size:30px;color:var(--c5);">💡 עוד רעיונות</span>'
             f'<span class="ink-t fw5" style="font-size:26px;line-height:1.4;">{r("📝 סיכום הפגישות מהשבוע האחרון, עם מסקנות ו-action items")}</span>'
             f'<span class="ink-t fw5" style="font-size:26px;line-height:1.4;">{r("🗂️ ארגון תיקייה: ״הצע תוכנית, ואל תזיז כלום עד שאאשר״")}</span></div>')
    col = f'<div class="fx col" style="flex:1.1;min-width:0;gap:20px;min-height:0;">{prompt_box("פרומפט ראשון", PRACTICE, 28).replace("flex:1;", "flex:1.2;", 1)}{ideas}</div>'
    return PRINT_CSS + head("תרגול ראשון ב-Cowork", f'מוסרים ל-Cowork {acc("משימה אמיתית")}') + stage(row(left, col)) + \
        take('תוך כדי עבודה אפשר <span class="hi">לעצור ולכוון</span>. לא מחכים לסוף.')

def projects_slide():
    steps = [("פותחים Project ומגדירים מטרה", "למשל ״גיוס שותפויות וקרנות״, עם הנחיות רק לפרויקט הזה."), ("מעלים מסמכי ליבה", "דפי עמדה, נתוני אימפקט ובקשות מענקים מוצלחות."),
             ("משתפים עם הצוות", "Share, וכולם נהנים מאותו זיכרון ומאותן הנחיות.")]
    st = ''.join(f'<div class="fx" style="gap:18px;align-items:flex-start;"><span class="numchip" style="background:var(--c{c});width:50px;height:50px;font-size:26px;">{i}</span>'
                 f'<div class="fx col" style="gap:4px;"><span class="ink-t fw8" style="font-size:32px;">{r(t)}</span><span class="muted fw5" style="font-size:26px;line-height:1.4;">{r(x)}</span></div></div>'
                 for i, ((t, x), c) in enumerate(zip(steps, [1, 3, 5]), 1))
    left = f'<div class="glass fx col" style="flex:1;min-width:0;padding:34px 40px;gap:34px;justify-content:center;border-top:7px solid var(--c1);">{st}</div>'
    items = [("📋", "הוראות", "רק לפרויקט הזה", None), ("📁", "תיקיות וקישורים", "ההקשר ש-Claude חוזר אליו", None),
             ("🕘", "משימות מתוזמנות", "רצות עם ההקשר של הפרויקט", None), ("🧠", "זיכרון", "נבנה לבד מהשיחות בפרויקט", "ההבדל הגדול")]
    it = ''.join(f'<div class="fx ac" style="gap:18px;"><span style="font-size:44px;line-height:1;">{ic}</span>'
                 f'<div class="fx col" style="flex:1;gap:2px;"><span class="ink-t fw8" style="font-size:30px;">{r(t)}</span><span class="muted fw5" style="font-size:25px;">{r(x)}</span></div>'
                 + (f'<span class="chip" style="background:var(--c1);color:#fff;font-size:21px;">{r(b)}</span>' if b else '') + '</div>' for ic, t, x, b in items)
    right = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:34px 40px;gap:22px;justify-content:center;border-top:7px solid var(--c5);">'
             f'<span class="fw8" style="font-size:34px;color:var(--c5);">🧩 מה יש בתוך פרויקט</span>{it}</div>')
    return head("עבודת צוות", f'Projects: {acc("סביבת עבודה משותפת")} לכל תחום') + stage(row(left, right)) + \
        take('מחוץ לפרויקט כל שיחה מתחילה מאפס. בפנים, <span class="hi">כל שיחה מוסיפה לידע</span>.')

def scheduled_slide():
    steps = [("עושים את המשימה פעם אחת", "ב-Cowork, ומוודאים שהתוצאה טובה."), ("כותבים /schedule", "ובוחרים תדירות: שעה, יום, ימי חול או ידני."),
             ("עוברים על הפרומפט ומאשרים", "Claude מנסח אותו, ואתם בודקים.")]
    st = ''.join(f'<div class="fx" style="gap:18px;align-items:flex-start;"><span class="numchip" style="background:var(--c{c});width:50px;height:50px;font-size:26px;">{i}</span>'
                 f'<div class="fx col" style="gap:4px;"><span class="ink-t fw8" style="font-size:31px;">{"<span dir=ltr>/schedule</span>".join(r(p) for p in t.split("/schedule"))}</span><span class="muted fw5" style="font-size:26px;line-height:1.4;">{r(x)}</span></div></div>'
                 for i, ((t, x), c) in enumerate(zip(steps, [1, 3, 5]), 1))
    how = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:30px 38px;gap:26px;justify-content:center;border-top:7px solid var(--c1);">'
           f'<span class="fw8" style="font-size:34px;color:var(--c1);">🕘 הדרך הטבעית</span>{st}</div>')
    ideas = [("📅", "סקירת יום שישי", "מה קרה בשבוע ומה מחכה בשבוע הבא"), ("📊", "סיכום חודשי", "מהגיליונות, ב-1 בחודש"), ("☀️", "בריף בוקר", "לפגישות של היום, כמו הסקיל שראינו")]
    idl = ''.join(f'<div class="fx ac" style="gap:18px;"><span style="font-size:44px;line-height:1;">{ic}</span><div class="fx col"><span class="ink-t fw8" style="font-size:30px;">{r(t)}</span>'
                  f'<span class="muted fw5" style="font-size:25px;">{r(x)}</span></div></div>' for ic, t, x in ideas)
    ide = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:30px 38px;gap:22px;justify-content:center;border-top:7px solid var(--c3);">'
           f'<span class="fw8" style="font-size:34px;color:var(--c3);">💡 מה שווה לתזמן</span>{idl}</div>')
    def note(icon, t):
        return (f'<div class="glass fx ac" style="flex:1;min-width:0;gap:16px;padding:16px 24px;"><span style="font-size:40px;line-height:1;">{icon}</span>'
                f'<span class="ink-t fw6" style="font-size:24px;line-height:1.35;">{r(t)}</span></div>')
    notes = (f'<div class="fx" style="gap:20px;flex:none;">{note("🖥️", "קבצים מקומיים: האפליקציה צריכה להיות פתוחה")}'
             f'{note("📱", "אפשר להתחיל גם מהטלפון, מול קונקטורים")}{note("✍️", "בהתחלה מתזמנים טיוטות, לא שליחה")}</div>')
    return head("Cowork · משימות מתוזמנות", f'שהעבודה תרוץ {acc("בלי שתבקשו")}') + \
        stage(f'<div class="fx col" style="flex:1;gap:20px;min-height:0;">{row(how, ide)}{notes}</div>') + \
        take('קודם <span class="hi">מוודאים שהמשימה עובדת</span> ידנית, ורק אז מתזמנים.')

def layers_slide():
    items = [("🪪", "Instructions", "מי אתם ואיך אתם עובדים", "כל משימה מתחילה כבר מכוילת לתפקיד שלכם", 1, "✓ ראינו"),
             ("📁", "Projects", "ההקשר של תחום עבודה אחד", "עובד כמו מי שכבר בצוות, עם הקבצים וההחלטות", 3, "✓ ראינו"),
             ("🍳", "Skills", "איך תהליך מסוים נעשה", "משימה מוכרת רצה לפי התבניות והצעדים שלכם", 5, "הבא"),
             ("🧩", "Plugins", "המומחיות של התפקיד שלכם", "מ-Claude כללי למומחה, עם תהליכים וחיבורים מוכנים", 2, "בהמשך")]
    cards = []
    for ic, t, learns, unlocks, c, st in items:
        done = st.startswith("✓")
        chip = (f'<span class="chip" style="background:{"var(--c1)" if done else "#fff"};color:{"#fff" if done else "var(--c5)"};{"" if done else "border:2px solid var(--c4);"}font-size:22px;">{r(st)}</span>')
        cards.append(f'<div class="glass fx col" style="flex:1;min-width:0;padding:30px 30px;gap:14px;border-top:7px solid var(--c{c});">'
                     f'<div class="fx ac jb"><span style="font-size:64px;line-height:1;">{ic}</span>{chip}</div>'
                     f'<span class="fw8" style="font-size:42px;color:var(--c{c});" dir="ltr">{t}</span>'
                     f'<span class="muted fw7" style="font-size:26px;margin-top:14px;">Claude לומד</span>'
                     f'<span class="ink-t fw6" style="font-size:32px;line-height:1.35;">{r(learns)}</span>'
                     f'<span class="muted fw7" style="font-size:26px;margin-top:14px;">וזה פותח</span>'
                     f'<span class="ink-t fw6" style="font-size:32px;line-height:1.35;">{r(unlocks)}</span></div>')
    return head("המפה", f'ארבע דרכים ללמד את Claude {acc("להכיר אתכם")}') + stage(row(*cards, gap=22)) + \
        take('כל שכבה <span class="hi">חוסכת הסברים חוזרים</span>. מתחילים מהראשונה.')

def badgood_slide():
    hi = lambda t: f'<span style="color:var(--highlight);font-weight:800;">{r(t)}</span>'
    bad = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:40px 44px;gap:30px;justify-content:center;border-top:7px solid var(--c6);">'
           f'{tag("✗ פרומפט עמום", False)}{quote(r("״תכתוב לי פוסט לקהילה על מפגש זכויות חדש.״"), 34)}'
           f'<p class="muted fw6" style="font-size:30px;margin:0;">← טקסט גנרי, רשמי, ומנותק מהשפה של חלאסרטן.</p></div>')
    good_q = ('״' + hi("אני מנהל/ת הקהילה בחלאסרטן (צעירים חולי סרטן 18-44).") + ' ' + hi("כתוב בעברית ישירה ובגובה העיניים, בלי קלישאות.") + ' '
              + r("נסח פוסט שמזמין למפגש מיצוי זכויות ביום ג׳, עם 3 סיבות למה שווה להגיע.") + '״')
    good = (f'<div class="glass fx col" style="flex:1.35;min-width:0;padding:40px 44px;gap:30px;justify-content:center;border-top:7px solid var(--c1);">'
            f'{tag("✓ פרומפט מלא", True)}{quote(good_q, 32)}'
            f'<p class="ink-t fw6" style="font-size:30px;margin:0;">← מדויק בול. אבל את <span style="color:var(--c1);font-weight:800;">החלק המודגש</span> מקלידים בכל פעם מחדש.</p></div>')
    return head("למה הניסוח משנה הכל", f'אותה בקשה, {acc("שתי תוצאות")}') + stage(row(bad, good)) + \
        take('את החלק הקבוע כותבים <span class="hi">פעם אחת</span>, ב-<span dir="ltr">Instructions for Claude</span>.')

def interview_slide():
    steps = [("מדביקים את הפרומפט", "כפתור ההעתקה כאן משמאל."), ("עונים על 10 שאלות", "תפקיד, קהל, סגנון, ומה מעצבן אתכם בתשובות AI."),
             ("שומרים את הסיכום", "בהגדרות, ב-Instructions for Claude (או Global instructions)")]
    st = ''.join(f'<div class="fx" style="gap:20px;align-items:flex-start;"><span class="numchip" style="background:var(--c{c});">{i}</span>'
                 f'<div class="fx col" style="gap:6px;"><span class="ink-t fw8" style="font-size:31px;">{r(t)}</span><span class="muted fw5" style="font-size:25px;line-height:1.4;">{r(x)}</span></div></div>'
                 for i, ((t, x), c) in enumerate(zip(steps, [1, 3, 5]), 1))
    left = f'<div class="glass fx col" style="flex:.8;min-width:0;padding:36px 38px;gap:34px;justify-content:center;border-top:7px solid var(--c3);">{st}</div>'
    return PRINT_CSS + head("תרגול: הראיון ההפוך", f'עכשיו נלמד את Claude {acc("להכיר אותנו")}', "דייקנו את הפרומפט. עכשיו נותנים ל-Claude לראיין אתכם, פעם אחת.") + \
        stage(row(left, prompt_box("פרומפט הראיון ההפוך", REVERSE, 29).replace('flex:1;', 'flex:1.25;', 1))) + \
        take('5 דקות של ראיון חוסכות <span class="hi">שעות של הסברים חוזרים</span>.')

def folders_slide():
    files = ["final_v2_new(1).docx", "מצגת חדשה (3).pptx", "סיכום-סופי-באמת.docx", "IMG_4471.jpg", "תקציב (עותק).xlsx"]
    fchips = ''.join(f'<span class="chip" style="background:#fff;border:2px dashed var(--c6);color:var(--muted);font-size:24px;font-weight:600;" dir="ltr">📄 {html.escape(f)}</span>' for f in files)
    bad = (f'<div class="glass fx col" style="flex:1;min-width:0;padding:34px 40px;gap:22px;border-top:7px solid var(--c6);">'
           f'{tag("✗ תיקיית הורדות כאוטית", False)}<div class="fx wrap" style="gap:12px;">{fchips}</div>'
           f'<p class="muted fw6" style="font-size:26px;line-height:1.45;margin:0;margin-top:auto;">Claude סורק קבצים לא קשורים, ואחרי שבועיים אף אחד לא זוכר איפה התוצר.</p></div>')
    tree = ("📁 Halasartan-Projects/\n  └─ 📁 2026-11-Donors-Event/\n       ├─ 📁 01-Raw-Materials/\n       ├─ 📁 02-Outputs/\n       └─ 📄 CLAUDE.md")
    legend = [("01-Raw-Materials", "מסמכי מקור ונתונים"), ("02-Outputs", "מצגות, דוחות ותוצרים"), ("CLAUDE.md", "הנחיות הפרויקט")]
    lg = ''.join(f'<div class="fx ac" style="gap:14px;font-size:25px;"><span class="dot" style="background:var(--c{c});"></span><span class="ink-t fw8" dir="ltr">{a}</span><span class="muted fw5">{r(b)}</span></div>'
                 for (a, b), c in zip(legend, [1, 3, 5]))
    good = (f'<div class="glass fx col" style="flex:1.2;min-width:0;padding:34px 40px;gap:22px;border-top:7px solid var(--c1);">'
            f'{tag("✓ תיקייה ברורה לכל פרויקט", True)}'
            f'<pre dir="ltr" style="margin:0;background:var(--ink);color:var(--on-dark);border-radius:14px;padding:22px 28px;font-size:26px;line-height:1.5;font-family:ui-monospace,Menlo,Consolas,monospace;text-align:left;">{html.escape(tree)}</pre>'
            f'<div class="fx col" style="gap:10px;">{lg}</div></div>')
    return head("סדר וארגון", f'כל פרויקט מקבל {acc("תיקייה משלו")}') + stage(row(bad, good)) + \
        take('לפני משימה חדשה ב-Claude, <span class="hi">פותחים לה תיקייה עם שם ברור</span>.')

def handson_slide():
    pts = ["מנקודות גולמיות או מסמך, למצגת הנהלה.", "הלוגו וצבעי העמותה, בעברית מלאה.", "Ctrl+P הופך אותה ל-PDF לתורמים."]
    p = ''.join(f'<div class="fx" style="gap:16px;align-items:baseline;"><span class="bullet" style="background:var(--c{c});width:14px;height:14px;"></span>'
                f'<span class="ink-t fw6" style="font-size:28px;line-height:1.4;">{r(t)}</span></div>' for t, c in zip(pts, [1, 3, 5]))
    left = (f'<div class="glass fx col" style="flex:.8;min-width:0;padding:36px 38px;gap:26px;border-top:7px solid var(--c3);">'
            f'<span class="fw8" style="font-size:34px;color:var(--c3);">🎨 מה הסקיל יעשה</span>{p}'
            f'<span class="chip" style="margin-top:auto;background:var(--bg-2);color:var(--c5);font-size:22px;">בונוס אם יש זמן: Claude Design</span></div>')
    return PRINT_CSS + head("תרגול משותף", f'בונים יחד: {acc("סקיל מצגות")} של חלאסרטן') + \
        stage(row(left, prompt_box("פרומפט: סקיל המצגות של חלאסרטן", SKILL_PROMPT, 27).replace('flex:1;', 'flex:1.3;', 1))) + \
        take('מקבלים <span class="hi">מצגת חיה למסך</span> וגם <span class="hi">PDF לוואטסאפ</span>.')

def usecases_slide():
    ex = [("💰", "גיוס", "Project + סקיל מצגות לתורמים", 1), ("📋", "זכויות", "Haiku סורק עדכונים ומנגיש אותם", 3), ("🗓️", "ישיבות", "Cowork + דשבורד משימות", 5)]
    exs = ''.join(f'<div class="glass fx ac" style="flex:1;gap:22px;padding:22px 30px;border-inline-start:7px solid var(--c{c});">'
                  f'<span style="font-size:46px;">{i}</span><div class="fx col" style="gap:4px;"><span class="fw8" style="font-size:30px;color:var(--c{c});">{r(t)}</span>'
                  f'<span class="ink-t fw5" style="font-size:28px;">{r(x)}</span></div></div>' for i, t, x, c in ex)
    qs = ["מה גוזל לכם הכי הרבה זמן השבוע?", "איזה הקשר Claude צריך? תיקייה או Project", "איזה כלי ומודל? Haiku, Sonnet, Cowork", "כדאי לארוז את זה לסקיל?"]
    q = ''.join(f'<div class="fx ac" style="gap:20px;"><span class="numchip" style="background:var(--c{c});">{i}</span><span class="fw6" style="font-size:29px;color:var(--on-dark);line-height:1.35;">{r(t)}</span></div>'
                for i, (t, c) in enumerate(zip(qs, [1, 2, 3, 4]), 1))
    right = (f'<div class="inkcard fx col" style="flex:1.2;min-width:0;padding:36px 42px;gap:26px;justify-content:center;">'
             f'<span class="fw8" style="font-size:34px;color:var(--highlight);">🧭 תבנית פיצוח</span>{q}</div>')
    left = f'<div class="fx col" style="flex:1;min-width:0;gap:20px;">{exs}</div>'
    return head("שולחן עגול", f'מפצחים יחד {acc("משימה אמיתית")} שלכם') + stage(row(left, right)) + \
        take('כל אחד יוצא עם <span class="hi">תהליך אחד שכבר עובד</span> השבוע.')

# ---------- slides ----------
S = []
S.append({"type": "cover", "mode": "dark", "eyebrow": "סדנת המשך · הנהלת חלאסרטן",
          "title": "להפוך את Claude\n*לשותף עבודה* שמכיר אתכם",
          "subtitle": "מצ'אט שמתחיל כל פעם מאפס, לסביבת עבודה עם זיכרון, פרויקטים משותפים וסקילים.",
          "notes": "ברוכים הבאים לסדנת ההמשך של הנהלת חלאסרטן! במפגש הקודם טעמנו מהעולם של AI, והיום אנחנו עולים קומה.\n\nנתחיל מלהבין איך המודל קורא טוקנים ופרומפטים, ונראה איך מתוך ההבנה הזו בונים לקלוד זיכרון קבוע, פרויקטים משותפים וסקילים שחוסכים שעות של עבודה."})
S.append({"type": "raw", "html": agenda_slide(),
          "notes": "סדר היום בקצרה. חלוקת זמנים מוצעת לשעתיים:\n\nאיך Claude חושב + ראיון הפוך (שקפים 3-7): 25 דקות.\nאיפה עובדים, תיקייה ובטיחות + תרגול ראשון ב-Cowork (8-12): 35 דקות.\nזיכרון וצוות: Projects, משימות מתוזמנות וארבע שכבות (13-15): 15 דקות.\nיכולות: סקילים, תרגול סקיל מצגות, קונקטורים, פלאגינים ו-Chrome (16-22): 30 דקות.\nשולחן עגול וסיכום (23-24): 15 דקות.\n\nלהדגיש: ארבעה תרגולים, לא הרצאה.\n\nלפני המפגש כדאי לבקש מהמשתתפים להתקין את אפליקציית הדסקטופ של Claude ולוודא שיש להם תוכנית בתשלום: Cowork עובד על קבצים מקומיים רק משם."})
S.append({"type": "raw", "html": llm_slide(),
          "notes": "LLM = Large Language Model: מודל שפה גדול שקרא המון טקסט ולמד לזהות מה בדרך כלל בא אחרי מה. ChatGPT, Claude ו-Gemini הם כולם מודלי שפה: אותו רעיון בסיסי, כל אחד בנוי קצת אחרת.\n\nזה לא מוח אנושי, זה מנוע שפה. בכל רגע הוא שואל: מה ההמשך הכי סביר לטקסט הזה? לכן ככל שנדבר איתו ברור יותר, נקבל תוצאה טובה יותר.\n\nדוגמה: \"החתול ישב על ה___\". המודל נותן הסתברות לכל המשך אפשרי ובוחר. המספרים להמחשה בלבד.\n\nומה בדיוק הוא מנחש? לא מילים שלמות, אלא חתיכות קטנות של טקסט שנקראות טוקנים. זה המעבר לשקף הבא."})
S.append({"type": "raw", "html": tokens_slide2(),
          "notes": "כמו שלמדנו במפגש 2: מודל שפה מנבא את הטוקן הבא על סמך הטוקנים שכבר נמצאים בחלון ההקשר שלו.\n\nטוקן הוא אבן הבניין הקטנה ביותר שהמודל מעבד. בעברית זה בולט במיוחד: המשפט \"חלאסרטן מחברת צעירים חולים ומחלימים\" (35 תווים) יוצא 32 טוקנים, כמעט טוקן לכל אות. האות ן הצריכה אפילו שני טוקנים (הטוקן הדהוי), והרווחים נספרים גם הם. הפירוק לקוח מכלי הערכה (Lunary, לפי המודל claude-opus-5-5), אז זו הערכה ולא מספר מדויק של Claude.\n\n* באנגלית אותו רעיון יוצא בדרך כלל בפחות טוקנים (בערך טוקן למילה), ולכן גם המחיר שונה: הכל נספר לפי טוקנים, ועברית יקרה יותר מאנגלית.\n\nגם הפרומפט שלכם וגם התשובה הם רצף של טוקנים, וכולם נספרים במכסה."})
S.append({"type": "raw", "html": context_slide(),
          "notes": "במילים פשוטות: בכל שיחה מוקצים ל-Claude מיליון טוקנים. הם מורכבים מכל מה שאנחנו שולחים לו (הודעות, מסמכים, תמונות) וגם מכל התשובות שהוא נותן לנו. ככל שהתכנים שאנחנו שולחים והתשובות שלו ארוכים יותר, מגיעים מהר יותר למיליון.\n\nבצילום המסך: מד ה-Context. כאן 34% בשימוש, 335.2k מתוך 1M. (המספר המדויק משתנה לפי המודל והתוכנית.)\n\nמי ששמע את המונח הטכני: זה נקרא חלון הקשר (Context Window). כמו שולחן עבודה: ככל שהוא עמוס בנושאים שונים, Claude פחות ממוקד.\n\nכלל ברזל: משימה חדשה? פותחים צ'אט חדש.\n\nמעבר לשקף הבא: איך מדייקים את מה שאנחנו כותבים, כלומר הפרומפט."})
S.append({"type": "raw", "html": prompt_merged_slide(),
          "notes": "פרומפט = ההוראות שאנחנו נותנים ל-AI: הטקסט שאנחנו כותבים לו. שאלה, בקשה, הוראה, הקשר, הכל פרומפט.\n\nאיך זה קשור למה שראינו: הפרומפט מתפרק לטוקנים, ומודל השפה מנבא מהם את ההמשך. לכן כל מילה בפרומפט מכוונת את התשובה.\n\nפרומפט טוב = תקשורת טובה. זה לא קסם טכני, זה בדיוק כמו לתת הנחיה לעובד חדש: ככל שנהיה ברורים ומכוונים יותר, נקבל תוצאה טובה יותר.\n\nלהשוות את שתי הדוגמאות: העמום נותן טקסט גנרי; המלא נותן ל-Claude הקשר מדויק (מי כותב, למי, באיזה טון ומה המשימה), ולכן התוצאה מדויקת.\n\n5 המרכיבים: תפקיד, הקשר, הוראה, נתוני קלט, פורמט וטון. שלושה מהם (תפקיד, הקשר, סגנון) כמעט לא משתנים אצלכם. בשקף הבא נראה איך גורמים ל-Claude להכיר אותנו, כדי שלא נצטרך לכתוב אותם כל פעם."})
S.append({"type": "raw", "html": interview_slide(),
          "notes": "המעבר: אחרי שהבנו איך לדייק את הפרומפטים שאנחנו כותבים, נבין איך גורמים ל-Claude להכיר אותנו, כדי שההקשר הבסיסי יהיה שם בכל שיחה.\n\nבמקום לשבור את הראש מול דף לבן, מבקשים מ-Claude לשאול 10 שאלות ולהרכיב בעצמו את ה-Instructions. כל אחד לוחץ העתקה, מדביק ועונה.\n\nבשקף הבא: דוגמאות למה שאמור לצאת."})
S[-1]["notes"] += "\n\nמה כותבים ב-Instructions: מי אתם ומה אתם עושים; ראשי תיבות וקיצורים שאתם משתמשים בהם (כדי ש-Claude לא ישאל מה זה 'דוח הרבעון'); ואיך אתם אוהבים לקבל תוצרים (פורמט, אורך, טון). לא צריך לגמור ביום הראשון: כל תיקון שאתם חוזרים עליו, כמו 'פתח בשורה התחתונה', הוא מועמד להוראה קבועה.\n\nדוגמאות לשלושה תפקידים בהנהלה (להעתקה מהמסך שלי):\n\n" + "\n\n".join(f"{n}:\n{t}" for n, c, t in ROLES)
S.append({"type": "raw", "html": icards_slide("שלוש סביבות עבודה", f'יועץ, עובד או בונה: {acc("Chat, Cowork, Code")}', None, [
    icard("💬", "Chat · היועץ", "סיעור מוחות, חידוד מסרים, ניסוח מכתבים לתורמים והתייעצות מהירה.", 6, foot("מתי: התשובה היא השיחה", 6)),
    icard("🤝", "Cowork · העובד", "עובד על התיקיות שלכם, מתכנן ומבצע משימה שלמה מתחילה ועד סוף.", 1, foot("מתי: יש קבצים ותוצר שנשמר", 1),
          style="flex:1.3;box-shadow:0 0 0 4px var(--c1),0 18px 48px rgba(194,24,91,.22);").replace(
          '<span style="font-size:76px;line-height:1;">🤝</span>',
          '<div class="fx ac jb"><span style="font-size:76px;line-height:1;">🤝</span><span class="chip" style="background:var(--c1);color:#fff;font-size:24px;">⭐ כאן עובדים היום</span></div>', 1),
    icard("⚡", "Code · הבונה", "בונה כלים, דשבורדים, מצגות וסקילים, גם מבקשה בשפה פשוטה.", 5, foot("מתי: רוצים כלי חדש", 5))],
    'בסדנה נעבוד ב-<span class="hi">Cowork</span>: נותנים משימה ותיקייה, ומקבלים <span class="hi">קובץ מוכן</span>.'),
          "notes": "חשוב: את כל התרגולים היום נעשה ב-Cowork. Chat ו-Code מוצגים כדי להבין את ההבדל.\n\nכלל הכרעה: יש קבצים אמיתיים ותוצר שנשמר? Cowork. התשובה היא השיחה עצמה? Chat. גם כשיש חיבור לקונקטור, זה לא הופך משימה ל-Cowork: השאלה היא מה אתם רוצים לקבל.\n\nCowork הוא הכלי להאצלה: מתארים תוצאה, ו-Claude מתכנן, מבצע ומחזיר תוצר שלם. בשביל גישה לקבצים צריך את אפליקציית הדסקטופ ותוכנית בתשלום. מהאינטרנט או מהטלפון Cowork מגיע רק לקונקטורים.\n\nלהדגיש את ההבדל בין Chat (שיחה) לבין Cowork (\"Claude Code בלי קוד\" לאנשי ניהול ותפעול) שבו מצביעים על תיקייה במחשב ונותנים לקלוד לעבוד.\n\nדוגמה ל-Cowork: \"עבור על כל הקבלות בתיקייה והפק טבלת סיכום\"."})
S.append({"type": "table", "eyebrow": "בחירת המודל", "title": "Haiku, Sonnet או Opus: *מודל לפי משימה*",
          "columns": ["מודל", "האופי", "מתי להשתמש", "מהירות ומכסה"],
          "rows": [["⚡ Haiku", "הסורק המהיר", "קריאת מסמכים, סיכום פרוטוקולים", "מיידי · הכי חסכוני"],
                   ["*🎯 Sonnet*", "*סוס העבודה*", "*ניוזלטרים, דוחות, מצגות*", "*ברירת מחדל ל-80%*"],
                   ["🧠 Opus", "האסטרטג", "תוכנית שנתית, דילמות רגישות", "איטי · מכסה גבוהה"]],
          "takeaway": "רוצים ש-Claude יקרא מסמכים? *עדיף Haiku*.",
          "notes": "הכל מתחבר לטוקנים: מסמכים ארוכים שורפים המון טוקנים. עם Opus המכסה תיגמר מהר. Haiku קורא מסמכים מהר ובמינימום עלות.\n\nBest practice: Haiku לקריאה וסריקה, Sonnet לכתיבה ויצירה, Opus לחשיבה אסטרטגית."})
S.append({"type": "raw", "html": cowork_slide(),
          "notes": "התפקיד והרקע כבר שמורים ב-Instructions, אז ב-Cowork מגדירים רק 3 מרכיבים: התוצר, חומרי הגלם והדגש.\n\nללחוץ על אפשרויות שונות ולהראות איך הפרומפט משתנה. כפתור ההעתקה מעתיק את הפרומפט המורכב."})
S.append({"type": "raw", "html": folders_safety_slide(),
          "notes": "כשעובדים עם סוכני AI, סדר בתיקיות הוא לא עניין טכני: התיקייה היא הגבול של מה ש-Claude יכול לקרוא, לכתוב ולמחוק (באישורכם). ב-Cowork, לתיקייה שבוחרים יש הרשאת קריאה וגם כתיבה.\n\nתיקייה ייעודית, ולא Downloads, Desktop או Documents. זה כמו לתת לעמית חדש לחטט בכל הקבצים שלכם. כלל אצבע: לפני משימה חדשה פותחים לה תיקייה עם שם ברור.\n\nשני מצבי הרשאה. Ask before acting (ברירת המחדל): Claude עוצר לאישורכם לפני כל פעולה שמשפיעה החוצה, כמו שליחת מייל, פרסום או שיתוף. Act without asking: רק למשימות שאתם סומכים עליהן. מחיקה קבועה תמיד דורשת אישור, ואי אפשר לדלג עליו.\n\nשלושה הרגלים: מגבים מה שאי אפשר לשחזר (עותק במקום ש-Cowork לא מגיע אליו). מנסים משימה חדשה קודם על עותק. מנסחים במפורש: 'טיוטה בלבד, אל תשלח', 'אל תמחק', 'רק 3 הקבצים האחרונים'.\n\nמתי Cowork לא הכלי הנכון: תהליכים שדורשים תיעוד לביקורת, מידע אישי רגיש מעבר למה שהארגון אישר, ופעולות שלא הייתם משאירים לעמית חכם בלי פיקוח (שליחת מסמך משפטי, הודעה פומבית). Claude יכין, אתם שולחים."})
S.append({"type": "raw", "html": practice_slide(),
          "notes": "זה התרגול הראשון ב-Cowork. כל אחד בוחר תיקייה עם חומר אמיתי (או עותק שלה) ומחבר אפליקציה אחת, בדרך כלל מייל או דרייב.\n\nהלולאה של Cowork: Claude מציג תוכנית לפני שהוא מתחיל, ושואל שאלות הבהרה (בדרך כלל בוחרים אפשרות, ואפשר לענות במילים שלכם). תוך כדי עבודה רואים את ההתקדמות, ואפשר לעצור ולכוון. לא מחכים לסוף כדי להתחיל מחדש.\n\nבסוף בודקים את התוצר כמו טיוטה ממישהו שאתם סומכים עליו אבל עוד לא מכירים: האם הוא עונה על המטרה? האם העובדות נכונות (לבקש ממנו לציין מאילו מסמכים לקח)? האם משהו נשמע מומצא, כמו תאריך, שם או ציטוט שאי אפשר לאתר? אם התוצאה כמעט נכונה, מבקשים תיקון ולא מתחילים מחדש.\n\nרעיונות: סיכום הפגישות מהשבוע האחרון, עם מסקנות ופעולות, ואיפה הייתי יכול להיות יעיל יותר. בוחרים תיקייה של סיכומי שיחות, Claude שואל איך להציג את התשובה, בונה תוכנית, ותוך זמן קצר יש סיכום של כל השבוע. או ארגון תיקייה: 'ארגן את תיקיית Downloads. הצע תוכנית, ואל תשנה כלום עד שאאשר'.\n\nאם יש זמן: לנסח משימה לפי הנוסחה מהשקף הקודם: תוצר, חומרי גלם ודגש. אתם מאצילים את העבודה, לא את שיקול הדעת."})
S.append({"type": "raw", "html": projects_slide(),
          "notes": "להראות בלייב: Projects ← New, הוספת תיקיות וקבצים, ואם יש אצלכם, Share לשיתוף עם ההנהלה.\n\nב-Cowork פרויקט הוא מרחב עבודה לתחום אחד: הוראות (כמו Instructions, רק לפרויקט), תיקיות וקישורים שהשיחות מסתמכות עליהם, משימות מתוזמנות, וזיכרון ש-Claude בונה לבד מהשיחות. זה ההבדל הגדול: מחוץ לפרויקט כל שיחה מתחילה מאפס (חוץ מה-Instructions). בתוכו כל שיחה מוסיפה לידע, וכך המשימה הבאה כבר פותחת עם המצב של הלקוח, ההחלטות מהשבוע שעבר ומה שעדיין פתוח.\n\nשלוש דרכים להתחיל: מאפס, מתיקייה קיימת במחשב, או מפרויקט קיים.\n\nאם עולה שאלה על זיכרון ארוך טווח: Obsidian היא תיקייה של קבצי טקסט שאפשר לחבר ל-Cowork כמוח שני של הארגון."})
S.append({"type": "raw", "html": scheduled_slide(),
          "notes": "יש שתי דרכים להגדיר משימה מתוזמנת. הדרך הטבעית: עושים את המשימה פעם אחת ב-Cowork, בודקים שהתוצאה טובה, וכותבים /schedule כדי להפוך בדיוק את התהליך הזה לחוזר. אפשר גם להתחיל מאפס: כותבים /schedule, מתארים את המשימה ואת התדירות, ו-Claude מנסח פרומפט לאישורכם.\n\nתדירות: כל שעה, כל יום, ימי חול או ידני.\n\nאיפה זה רץ: משימה שמשתמשת רק בקונקטורים יכולה לרוץ מרחוק, גם כשהמחשב כבוי. משימה שצריכה קבצים או אפליקציות מהמחשב רצה על המחשב, ולכן אפליקציית הדסקטופ צריכה להיות פתוחה. אם המחשב סגור או ישן, Claude ימשיך כשתחזרו ויודיע שהיה עיכוב.\n\nרעיונות: סקירה ביום שישי (מה קרה בשבוע, החלטות, מה מחכה בשבוע הבא), סיכום חודשי מגיליונות ב-1 בחודש, ובריף בוקר לפגישות של היום, בדיוק כמו סקיל תדריך בוקר.\n\nגם מהטלפון: אפשר להתחיל משימה מאפליקציית המובייל, והיא רצה מרחוק ומחכה לכם. היא מגיעה לקונקטורים, לא לתיקיות במחשב.\n\nבהתחלה מתזמנים טיוטות לבדיקה, ולא שליחה אוטומטית."})
S.append({"type": "raw", "html": layers_slide(),
          "notes": "זו מפה של מה שראינו ומה שמגיע. יש ארבע דרכים ללמד את Claude להכיר אתכם, וכל אחת חוסכת הסברים חוזרים.\n\nInstructions: Claude לומד מי אתם ואיך אתם עובדים, ולכן כל משימה מתחילה כבר מכוילת לתפקיד שלכם.\nProjects: הוא לומד את ההקשר של תחום עבודה אחד, ועובד כמו מי שכבר בצוות: יש לו את הקבצים, ההיסטוריה וההחלטות.\nSkills: הוא לומד איך תהליך מסוים נעשה, ומשימה מוכרת רצה לפי התבניות, הסטנדרטים והצעדים שלכם.\nPlugins: הוא לומד את המומחיות של התפקיד שלכם, ומ-Claude כללי הופך למומחה עם תהליכים וחיבורים מוכנים.\n\nשתי הראשונות כבר ראינו. הבא: סקילים."})
S.append({"type": "raw", "html": skills_intro_slide(),
          "notes": "מכירים את זה? משימה שחוזרת על עצמה, או שיחה ארוכה שבסוף הגעתם בה לתוצאה מושלמת, ובפעם הבאה מתחילים מאפס.\n\nבמקום להדביק בכל שיחה את אותו פרומפט ארוך, מבקשים מ-Claude בסוף שיחה מוצלחת: \"על בסיס השיחה הזו, צור לי Skill שאוכל להשתמש בו שוב בפעם הבאה\".\n\nמתכון שף: קובץ שאורז את המרכיבים (מה Claude מקבל מכם ובאיזה סגנון לכתוב), שלבי ההכנה (מה עושים ובאיזה סדר) ואיך נראית מנה מוצלחת. Claude שולף את המתכון לבד כשהמשימה מתאימה ומבצע ברמה של שף.\n\nכל פעולה שחוזרת יותר מפעמיים בחודש ראויה לסקיל. את הסיפור המלא (איך בניתי סקיל ומה למדתי) נותנים בנפרד: skills-example.html."})
S.append({"type": "raw", "html": skills_example_slide(),
          "notes": "הדוגמה הכי ויזואלית: סקיל שבניתי לניהול משימות. כותבים משפט אחד, \"תתחיל את היום שלי\", ו-Claude קורא מיילים, בודק את היומן, אוסף משימות פתוחות, ממיין לפי דחיפות ובונה לוח אחד. בערב: \"סיים את היום\" ומקבלים סיכום של מה הספקתי ומה עובר למחר. הנתונים בצילום הם דוגמה.\n\nמבפנים: הסקיל הוא קובץ טקסט אחד (SKILL.md) עם תיאור שאומר ל-Claude מתי להשתמש בו, ומתכון מלא. Claude רואה בתחילת השיחה רק את התיאורים של כל הסקילים, ופותח את המתכון המלא רק כשצריך. זוכרים את הטוקנים? בגלל זה אפשר להחזיק הרבה סקילים בלי להעמיס על חלון ההקשר.\n\nאת הסקיל הזה אשתף אתכם."})
S.append({"type": "raw", "html": skill_structure_slide(),
          "notes": "סקיל הוא קובץ טקסט אחד (SKILL.md) עם שני חלקים, וכל חלק נקרא בזמן אחר. זה אותו סקיל תדריך בוקר מהשקף הקודם, בתרגום חופשי.\n\ndescription: כריכת המתכון. שם ותיאור קצר שאומר ל-Claude מתי להשתמש בסקיל.\nbody: המתכון המלא, שלב אחרי שלב.\n\nאיך Claude קורא את זה: בתחילת השיחה הוא רואה רק את התיאורים של כל הסקילים (כמו תוכן עניינים). כשכתבתם \"תתחיל את היום שלי\" הוא מזהה התאמה, ורק אז פותח את המתכון המלא.\n\nזוכרים את הטוקנים? בגלל זה אפשר להחזיק עשרות סקילים בלי להעמיס על חלון ההקשר: רק התיאורים נטענים, והמתכון נפתח רק כשצריך.\n\ndescription טוב = Claude יודע מתי לשלוף. body טוב = התוצאה יוצאת טעימה.\n\nסקיל יכול להכיל ארבעה סוגי קבצים: הוראות (SKILL.md), נכסים (לוגו, תבניות, פונטים), דוגמאות (איך נראה תוצר טוב) וסקריפטים (קוד קטן לחלקים שחייבים להיעשות אותו דבר בכל פעם). סקיל המצגות שלנו כולל את כולם. לפני ששולחים סקיל לאחרים, בודקים אותו על בקשה אמיתית ומשווים למה ש-Claude היה עושה בלעדיו."})
S.append({"type": "raw", "html": icards_slide("לא להמציא את הגלגל", f'מתקינים סקיל, או {acc("מוצאים מוכן")}', None, [
    icard("💬", "איך מתקינים?", "פשוט מבקשים מ-Claude להתקין, והוא כבר מתקין בשבילכם.", 1, foot("בלי קבצים ובלי הגדרות", 1)),
    icard("🔎", "Find Skills", "הסקיל של Vercel מחפש בשבילכם בין אלפי סקילים שמישהו כבר בנה ובדק.", 3,
          '<a href="https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md" target="_blank" rel="noopener noreferrer" dir="ltr" '
          'class="chip" style="align-self:flex-start;background:var(--c3);color:#fff;font-size:24px;text-decoration:none;">github.com/vercel-labs/skills ↗</a>'),
    icard("✨", "מתי לבנות לבד", "כשאין סקיל מתאים, והמשימה חוזרת על עצמה שוב ושוב.", 5)],
    'לפני שבונים סקיל, <span class="hi">בודקים אם מישהו כבר בנה</span>.'),
          "notes": "מתקינים סקיל? פשוט מבקשים מ-Claude להתקין, והוא כבר מתקין. אפשר גם להדביק לו את הקישור לסקיל.\n\nלהדגים את find-skills של Vercel (הקישור על השקף): סקיל שמחפש בין אלפי סקילים שמישהו כבר בנה ובדק. לפני שבונים לבד, בודקים אם כבר יש.\n\nלמי שרוצה את הפקודה (לא לשקף): npx skills add vercel-labs/skills --skill find-skills"})
S.append({"type": "raw", "html": handson_slide(),
          "notes": "כל אחד מעתיק את הפרומפט, מדביק בקלוד ובונים יחד את הסקיל עם הלוגו של חלאסרטן. אחרי שנבנה: לבקש מצגת קצרה, ו-Ctrl+P ל-PDF.\n\nבונוס אם נשאר זמן: 3 דקות של Claude Design ואיך בונים שם סיסטם דיזיין.\n\nדוגמה מוכנה לתוצר: המצגת הזו, ו-skills-example.html."})
_srcs = ''.join(f'<span class="chip" style="background:#fff;color:var(--c5);border:2px solid var(--c4);font-size:23px;padding:7px 16px;" dir="ltr">{n}</span>' for n in ["Google Drive", "Gmail", "Calendar", "Slack", "Notion"])
S.append({"type": "raw", "html": icards_slide("קונקטורים, אבטחה ופלאגינים", f'לחבר את Claude {acc("למקורות המידע שלכם")}', None, [
    icard("🔌", "Connectors", "Claude מתחבר ישירות למקורות שלכם ושולף את המסמך העדכני בעצמו.", 1,
          f'<div class="fx wrap" style="gap:10px;">{_srcs}</div>' + foot("מדליקים רק מה שצריך למשימה", 1), fs=28),
    icard("🛡️", "אבטחת מידע", "בלי פרטים מזהים של חברי קהילה: מידע רפואי עולה רק אחרי התממה, ורק במסגרת מה שהארגון אישר. פעולות רגישות מאשרים ידנית.", 3, fs=28),
    icard("🦸", "פלאגינים · רשות", 'חבילת סקילים לתפקיד, בהתקנה אחת. כותבים <span dir="ltr">/setup-claude</span> ו-<span dir="ltr">Claude</span> מראיין אתכם ומציע פלאגין. למשל: <span dir="ltr">Superpowers</span>.', 5, fs=28, raw=True)],
    'אנחנו תמיד <span class="hi">הטייס שמאשר</span> לפני שליחה או שינוי של מידע ארגוני.'),
          "notes": "הקונקטורים הם הגשר בין Claude למקורות המידע שלכם: Drive, Gmail, יומן, Slack, Notion. במקום להוריד ולהעלות קבצים ידנית, Claude שולף את המסמך העדכני בעצמו. להראות איפה בתפריט מחברים (הגדרות → Connectors).\n\nלהדגיש את נהלי אבטחת המידע בעמותה שמטפלת בצעירים חולי סרטן: מידע רפואי או אישי לא עולה בלי התממה; הרשאות מינימליות, כלומר מחברים רק מה שצריך; פעולות רגישות מאשרים ידנית.\n\nאופציונלי, אם יש זמן ויש סקרנות: פלאגין הוא חבילה של סקילים (וגם הקונקטורים שהם צריכים) סביב תפקיד. Anthropic מפרסמת פלאגינים לתפקידים נפוצים, כמו כספים, משפטים, שיווק ותמיכה, ואפשר להתקין אחד, להתאים אותו או לבנות משלכם. הדרך הקלה למצוא: לכתוב /setup-claude בשיחה חדשה. Claude מראיין על סוג העבודה שלכם ומציע פלאגין. עוד דוגמה: Superpowers גורם ל-Claude לתכנן לפני ביצוע: סיעור מוחות, תוכנית, ביצוע ובדיקה עצמית. 2 דקות להדגים.\n\nכל קונקטור שמדליקים הוא כלי ש-Cowork יכול להגיע אליו, ולכן מדליקים רק את מה שצריך לכל משימה. חלק מהקונקטורים רק קוראים ומחפשים (כמו Drive), וחלקם גם יוצרים ועורכים: קוראים את התיאור לפני שמדליקים."})
S.append({"type": "raw", "html": icards_slide("סוכן בתוך הדפדפן", f'Claude in Chrome: {acc("Claude בא אל האתר")}', None, [
    icard("📥", "התקנה ב-30 שניות", "תוסף רשמי מחנות Chrome, נצמד לסרגל ונפתח בחלונית צד.", 1, foot("עובד על כל אתר פתוח", 1)),
    icard("🪄", "מה זה נותן", "הגשר לכלים בלי קונקטור: פורטלים ודשבורדים. הוא אוסף בדפדפן, ו-Cowork בונה את התוצר.", 3),
    icard("🛡️", "עבודה בטוחה", "אתם מתחברים לאתר בעצמכם. רואים כל צעד ומאשרים פעולות חשובות.", 5, foot("Claude לא מתחבר בשבילכם", 5))],
    'במקום להעתיק מאתרים ל-Claude, <span class="hi">מביאים את Claude לאתר</span>.'),
          "notes": "להדגים פתיחה של התוסף על עמוד אמיתי ולהראות איך קלוד קורא את המסך ומבצע פעולה שחוסכת עבודה ידנית.\n\nלהזכיר את מצב ההרשאות."})
S.append({"type": "raw", "html": usecases_slide(),
          "notes": "החלק האינטראקטיבי המרכזי: עוברים משתתף-משתתף, שומעים את ה-Use Case, וממפים אותו יחד על המסך: תיקייה, מודל, הקשר וסקיל."})
S.append({"type": "closing", "eyebrow": "צ'קליסט למחר בבוקר", "title": "5 צעדים קטנים, *לפי הסדר*",
          "points": [{"title": "הראיון ההפוך", "text": "מריצים את 10 השאלות ומעדכנים Instructions."},
                     {"title": "סדר בתיקיות", "text": "תיקייה ברורה לפרויקט של השבוע, ו-Ask before acting נשאר דלוק."},
                     {"title": "Haiku למסמכים", "text": "Haiku לסריקה, Sonnet לכתיבה."},
                     {"title": "Project משותף", "text": "Project אחד עם הצוות, עם מסמכי הליבה."},
                     {"title": "סקיל ראשון", "text": "סקיל המצגות, ונסיון עם תוסף Chrome."}],
          "note": "Claude · Cowork · Find Skills · Superpowers · Claude in Chrome · בהצלחה!",
          "notes": "אל תנסו ליישם הכל ביום אחד, מתחילים מחמשת הצעדים לפי הסדר.\n\nלהזכיר שאפשר להדפיס את המצגת ל-PDF (Ctrl+P) כדי שהפרומפטים יישארו זמינים."})

json.dump({"meta": meta, "slides": S}, open('meeting-5.json', 'w'), ensure_ascii=False, indent=1)
print(len(S), 'slides')
