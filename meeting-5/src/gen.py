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
    return PRINT_CSS + head("Global Instructions", f'הנחיות קבועות לכל תפקיד: {acc("פעם אחת")} ודי',
                            r("Settings → Profile → Personal Preferences · מעתיקים את הבלוק של התפקיד שלכם")) + \
        stage(f'<div class="fx" style="flex:1;gap:28px;min-height:0;">{"".join(cols)}</div>')

TOKENS = ["חלא", "סרט", "ן", "מחבר", "ת", "צעיר", "ים", "חול", "ים", "ו", "מחלימ", "ים"]

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
def icard(icon, title, text, c, extra='', fs=31, style=''):
    return (f'<div class="glass fx col" style="flex:1;min-width:0;padding:40px 42px;gap:24px;justify-content:center;border-top:7px solid var(--c{c});{style}">'
            f'<span style="font-size:76px;line-height:1;">{icon}</span>'
            f'<span class="fw8" style="font-size:42px;color:var(--c{c});">{r(title)}</span>'
            f'<p class="ink-t fw5" style="font-size:{fs}px;line-height:1.45;margin:0;">{r(text)}</p>{extra}</div>')

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
             ("🛠️", "איפה עובדים", "Chat, Cowork, Code, ואיזה מודל לבחור", 3, "תרגול: Cowork"),
             ("📁", "סדר וצוות", "תיקייה לכל פרויקט, ו-Projects משותפים", 5, None),
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

def tokens_slide2():
    words = ''.join(f'<span class="chip" style="font-size:28px;padding:10px 18px;background:#fff;color:var(--ink);border:2px solid var(--c4);">{w}</span>' for w in "חלאסרטן מחברת צעירים חולים ומחלימים".split())
    chips = ''.join(f'<span class="chip" style="font-size:26px;padding:8px 14px;background:var(--c{(i % 5) + 1});color:#fff;">{t}</span>' for i, t in enumerate(TOKENS))
    models = ''.join(f'<span class="chip" style="font-size:26px;padding:10px 20px;{st}">{m}</span>' for m, st in
                     [("ChatGPT", "background:#fff;color:var(--muted);border:2px solid var(--c4);"), ("Claude", "background:var(--c1);color:#fff;"), ("Gemini", "background:#fff;color:var(--muted);border:2px solid var(--c4);")])
    card = lambda c, f: f'<div class="glass fx col" style="flex:{f};min-width:0;padding:30px 32px;gap:18px;border-top:7px solid var(--c{c});">'
    llm = (card(5, 1) + f'<span class="fw8" style="font-size:32px;color:var(--c5);">🧠 מה זה LLM?</span>'
           f'<span class="ink-t fw7" style="font-size:24px;" dir="ltr">Large Language Model</span>'
           f'<p class="ink-t fw5" style="font-size:25px;line-height:1.45;margin:0;">מודל שפה גדול: קרא המון טקסט, ספרים, מאמרים, אתרים ושיחות, ולמד מה בדרך כלל בא אחרי מה.</p>'
           f'<div class="fx wrap" style="gap:10px;" dir="ltr">{models}</div>'
           f'<p class="ink-t fw6" style="font-size:24px;line-height:1.4;margin:0;">כולם מודלי שפה: אותו רעיון, כל אחד בנוי קצת אחרת.</p>'
           f'<p class="muted fw6" style="font-size:24px;line-height:1.4;margin:0;margin-top:auto;">לא מוח אנושי, אלא מנוע שפה ששואל כל הזמן: מה ההמשך הכי סביר?</p></div>')
    left = (card(1, 1.1) + f'<span class="fw8" style="font-size:32px;color:var(--c1);">🧩 איך Claude קורא</span>'
            f'<span class="muted fw7" style="font-size:23px;">אנחנו רואים 5 מילים:</span><div class="fx wrap" style="gap:10px;">{words}</div>'
            f'<span class="muted fw7" style="font-size:23px;">Claude רואה {len(TOKENS)} טוקנים:</span>'
            f'<div class="fx wrap" style="gap:8px;padding:16px;border-radius:16px;background:var(--ink);">{chips}</div></div>')
    bars = [("שטיח", 61, 1), ("ספה", 24, 3), ("כיסא", 9, 5)]
    b = ''.join(f'<div class="fx ac" style="gap:14px;"><span class="ink-t fw7" style="font-size:25px;width:70px;">{w}</span>'
                f'<div style="flex:1;height:22px;border-radius:999px;background:var(--bg-2);"><div style="width:{v}%;height:100%;border-radius:999px;background:var(--c{c});"></div></div>'
                f'<span class="fw8" style="font-size:25px;color:var(--c{c});width:58px;">{v}%</span></div>' for w, v, c in bars)
    right = (card(3, 1) + f'<span class="fw8" style="font-size:32px;color:var(--c3);">✍️ איך Claude כותב</span>'
             f'<p class="ink-t fw5" style="font-size:25px;line-height:1.4;margin:0;">מנחש את הטוקן הבא הכי סביר, מוסיף, וחוזר חלילה:</p>'
             f'{quote("״החתול ישב על ה___״", 27)}<div class="fx col" style="gap:12px;">{b}</div>'
             f'<span class="muted" style="font-size:20px;">המספרים להמחשה בלבד</span></div>')
    return head("מושגי יסוד", f'Claude הוא מודל שפה. הוא קורא וכותב {acc("טוקנים")}') + stage(row(llm, left, right, gap=22)) + \
        take('כל טוקן שנכנס וכל טוקן שיוצא <span class="hi">נספר במכסה</span>, וכל מילה בפרומפט מכוונת את הניחוש.')

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
             ("שומרים את הסיכום", "Settings → Profile → Instructions for Claude")]
    st = ''.join(f'<div class="fx" style="gap:20px;align-items:flex-start;"><span class="numchip" style="background:var(--c{c});">{i}</span>'
                 f'<div class="fx col" style="gap:6px;"><span class="ink-t fw8" style="font-size:31px;">{r(t)}</span><span class="muted fw5" style="font-size:25px;line-height:1.4;">{r(x)}</span></div></div>'
                 for i, ((t, x), c) in enumerate(zip(steps, [1, 3, 5]), 1))
    left = f'<div class="glass fx col" style="flex:.8;min-width:0;padding:36px 38px;gap:34px;justify-content:center;border-top:7px solid var(--c3);">{st}</div>'
    return PRINT_CSS + head("תרגול: הראיון ההפוך", f'נותנים ל-Claude {acc("לראיין אתכם")}') + \
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
          "notes": "סדר היום בקצרה. חלוקת זמנים מוצעת לשעתיים:\n\nאיך Claude חושב + ראיון הפוך: 30 דקות.\nאיפה עובדים + משימה ל-Cowork: 20 דקות.\nסדר וצוות: 10 דקות.\nיכולות + סקיל מצגות: 35 דקות.\nשולחן עגול: 20 דקות.\n\nלהדגיש: ארבעה תרגולים, לא הרצאה."})
S.append({"type": "raw", "html": tokens_slide2(),
          "notes": "LLM = Large Language Model: מודל שפה גדול שקרא המון טקסט ולמד לזהות מה בדרך כלל בא אחרי מה. ChatGPT, Claude ו-Gemini הם כולם מודלי שפה: אותו רעיון בסיסי, כל אחד בנוי קצת אחרת. זה לא מוח אנושי, זה מנוע שפה. לכן ככל שנדבר איתו ברור יותר, נקבל תוצאה טובה יותר.\n\nכמו שלמדנו במפגש 2: מודל שפה מנבא את הטוקן הבא על סמך הטוקנים שכבר נמצאים בחלון ההקשר שלו.\n\nטוקן הוא אבן הבניין הקטנה ביותר: מילה, הברה או חלק ממילה. בעברית כל מילה מתפרקת ל-2 עד 4 טוקנים.\n\nהצד השמאלי: Claude לא 'יודע' את התשובה, הוא מנחש את ההמשך הכי סביר. לכן כל מילה בפרומפט משנה לאן הניחוש הולך."})
S.append({"type": "compare", "eyebrow": "חלון ההקשר", "title": "חלון ההקשר הוא *שולחן העבודה* של Claude",
          "subtitle": "כמות הטוקנים ש-Claude רואה וזוכר בשיחה אחת, בבת אחת.",
          "left": {"label": "שולחן עמוס", "title": "אובדן פוקוס", "items": ["5 נושאים באותה שיחה ארוכה", "הטוקנים מתבזבזים", "איכות התשובה צונחת"]},
          "right": {"label": "שולחן נקי", "title": "תשובה חדה", "items": ["רק ההקשר של המשימה", "Claude ממוקד במה שחשוב", "*צ'אט חדש לכל משימה*"]},
          "takeaway": "כלל ברזל: משימה חדשה? *פותחים צ'אט חדש ונקי*.",
          "notes": "חלון ההקשר הוא כמות הטוקנים המקסימלית שקלוד מסוגל לראות ולזכור בשיחה אחת, כמו שולחן עבודה.\n\nמעבר לשקף הבא: אז איך מכוונים את הניחוש בדיוק למה שאנחנו צריכים? מבנה הפרומפט."})
S.append({"type": "table", "eyebrow": "הנדסת פרומפטים", "title": "5 מרכיבים של פרומפט טוב. *3 מהם קבועים*",
          "columns": ["מרכיב", "השאלה", "בכל שיחה"],
          "rows": [["1. תפקיד (Role)", "מי אתם ומה המומחיות?", "*קבוע*"], ["2. הקשר (Context)", "חלאסרטן וקהל היעד", "*קבוע*"],
                   ["3. הוראה (Instruction)", "מה המשימה היום?", "משתנה"], ["4. נתוני קלט (Input)", "המסמך או הנתונים", "משתנה"],
                   ["5. פורמט וטון (Output)", "בגובה העיניים, מבנה מועדף", "*קבוע*"]],
          "highlight": 2, "takeaway": "את הקבועים כותבים *פעם אחת*, ב-Instructions for Claude.",
          "notes": "פרומפט הוא ההוראה שמכוונת את המודל. כשבונים אותו מ-5 מרכיבים ברורים מקבלים תוצאה מעולה.\n\nשימו לב: סעיפים 1 (התפקיד), 2 (ההקשר של חלאסרטן) ו-5 (סגנון הכתיבה) קבועים אצלכם."})
S.append({"type": "raw", "html": badgood_slide(),
          "notes": "זה הגשר בין הנדסת פרומפטים לבין עבודה חכמה בקלוד: 3 מתוך 5 הרכיבים קבועים לתפקיד שלהם (החלק המודגש). במקום להקליד אותם כל פעם, מקבעים אותם ב-Instructions for Claude."})
S.append({"type": "raw", "html": roles_slide(),
          "notes": "לעבור על שלוש העמודות (ניהול קהילה, גיוס משאבים, מנכ\"לות וכספים) ולהראות איך 3 המרכיבים הקבועים (Role + Context + Output) הופכים להנחיות קבועות.\n\nמה זה נותן: שומר על השפה הישירה והלא-מתנשאת; בגיוס: מצמיד מקור לכל נתון; בכספים: פותח בשורה התחתונה ומציג טבלאות.\n\nרוצים כזה שמותאם בול אליכם? השקף הבא."})
S.append({"type": "raw", "html": interview_slide(),
          "notes": "במקום לשבור את הראש מול דף לבן, מבקשים מקלוד לשאול אתכם 10 שאלות ולהרכיב עבורכם את ההנחיות הקבועות.\n\nכל אחד לוחץ על כפתור ההעתקה, מדביק בקלוד ועונה. מעכשיו בכל צ'אט חדש קלוד כבר ידבר בשפה שלכם."})
S.append({"type": "raw", "html": icards_slide("שלוש סביבות עבודה", f'יועץ, עובד או בונה: {acc("Chat, Cowork, Code")}', None, [
    icard("💬", "Chat · היועץ", "סיעור מוחות, חידוד מסרים, ניסוח מכתבים לתורמים והתייעצות מהירה.", 1, foot("מתי: צריכים תשובה או עריכה", 1)),
    icard("🤝", "Cowork · העובד", "עובד על התיקיות שלכם, מתכנן ומבצע משימה שלמה מתחילה ועד סוף.", 3, foot("מתי: משימה רב-שלבית על קבצים", 3)),
    icard("⚡", "Code · הבונה", "בונה כלים, דשבורדים, מצגות וסקילים, גם מבקשה בשפה פשוטה.", 5, foot("מתי: רוצים כלי חדש", 5))],
    'ב-Chat הוא עונה. ב-Cowork וב-Code הוא <span class="hi">מחזיר קובץ מוכן</span>.'),
          "notes": "להדגיש את ההבדל בין Chat (שיחה) לבין Cowork (\"Claude Code בלי קוד\" לאנשי ניהול ותפעול) שבו מצביעים על תיקייה במחשב ונותנים לקלוד לעבוד.\n\nדוגמה ל-Cowork: \"עבור על כל הקבלות בתיקייה והפק טבלת סיכום\"."})
S.append({"type": "raw", "html": cowork_slide(),
          "notes": "התפקיד והרקע כבר שמורים ב-Instructions, אז ב-Cowork מגדירים רק 3 מרכיבים: התוצר, חומרי הגלם והדגש.\n\nללחוץ על אפשרויות שונות ולהראות איך הפרומפט משתנה. כפתור ההעתקה מעתיק את הפרומפט המורכב."})
S.append({"type": "table", "eyebrow": "בחירת המודל", "title": "Haiku, Sonnet או Opus: *מודל לפי משימה*",
          "columns": ["מודל", "האופי", "מתי להשתמש", "מהירות ומכסה"],
          "rows": [["⚡ Haiku", "הסורק המהיר", "קריאת מסמכים, סיכום פרוטוקולים", "מיידי · הכי חסכוני"],
                   ["*🎯 Sonnet*", "*סוס העבודה*", "*ניוזלטרים, דוחות, מצגות*", "*ברירת מחדל ל-80%*"],
                   ["🧠 Opus", "האסטרטג", "תוכנית שנתית, דילמות רגישות", "איטי · מכסה גבוהה"]],
          "takeaway": "רוצים ש-Claude יקרא מסמכים? *עדיף Haiku*.",
          "notes": "הכל מתחבר לטוקנים: מסמכים ארוכים שורפים המון טוקנים. עם Opus המכסה תיגמר מהר. Haiku קורא מסמכים מהר ובמינימום עלות.\n\nBest practice: Haiku לקריאה וסריקה, Sonnet לכתיבה ויצירה, Opus לחשיבה אסטרטגית."})
S.append({"type": "raw", "html": folders_slide(),
          "notes": "כשעובדים עם סוכני AI, סדר בתיקיות הוא לא עניין טכני. הוא המפתח לכך שנדע איפה כל דבר נשמר ואיך חוזרים אליו.\n\nהמבנה הזה מונע את \"איפה הקובץ שקלוד יצר לי בשבוע שעבר?\" ומאפשר ל-Cowork לעבוד רק בתוך התיקייה של הפרויקט."})
S.append({"type": "steps", "eyebrow": "עבודת צוות", "title": "Projects: *סביבת עבודה משותפת* לכל תחום",
          "steps": [{"title": "פותחים Project ומגדירים מטרה", "text": "למשל \"גיוס שותפויות וקרנות\", עם הנחיות רק לפרויקט הזה."},
                    {"title": "מעלים מסמכי ליבה", "text": "דפי עמדה, נתוני אימפקט ובקשות מענקים מוצלחות מהעבר."},
                    {"title": "משתפים עם הצוות", "text": "Share, וכל מי שנכנס נהנה מאותו זיכרון ומאותן הנחיות."}],
          "takeaway": "שפה ארגונית אחידה, *וחפיפה קצרה בהרבה*.",
          "notes": "להראות בלייב: Projects → New, Project Knowledge, ואז Share כדי שכל ההנהלה תעבוד על אותה תשתית ידע.\n\nאם עולה שאלה על זיכרון ארוך טווח: Obsidian היא תיקייה של קבצי טקסט שאפשר לחבר ל-Cowork כמוח שני של הארגון."})
S.append({"type": "image", "eyebrow": "סקילים", "title": "סקיל = *מתכון של שף* ל-Claude",
          "subtitle": "בלי סקיל מסבירים כל פעם מחדש. עם סקיל, Claude מקבל יכולת קבועה.",
          "src": "assets/onboarding-binder.jpg", "alt": "איור: אדם מגיש לעוזר דיגיטלי קלסר נהלים מסודר עם רשימת בדיקה",
          "points": ["*המרכיבים*: מה Claude מקבל, ובאיזה סגנון לכתוב.", "*שלבי ההכנה*: מה עושים, ובאיזה סדר.", "*איך נראית מנה מוצלחת*: בדיקה לפני שמגישים."],
          "takeaway": "כל פעולה שחוזרת *יותר מפעמיים בחודש* ראויה לסקיל.",
          "notes": "מתכון שף: קובץ SKILL.md אורז את כל שלבי העבודה, הסגנון ובדיקות האיכות. כשמבקשים משימה מוכרת, Claude שולף את המתכון לבד ומבצע ברמה של שף.\n\nאת הסיפור המלא (איך בניתי סקיל ומה למדתי) נותנים בנפרד: skills-example.html."})
S.append({"type": "image", "eyebrow": "סקיל שבניתי", "title": "מכל המקורות, *לוח משימות אחד*",
          "src": "assets/skill_morning_board.png", "alt": "צילום מסך: לוח משימות יומי עם עמודות לביצוע, בתהליך והושלם, שנבנה ממיילים, יומן וכלי משימות",
          "points": ["מבקשים במשפט אחד: *״תתחיל את היום שלי״*.", "קורא מיילים, יומן, אקסלים ופתקים.", "ממיין לפי דחיפות ובונה דשבורד אחד."],
          "takeaway": "משפט אחד, ותוצאה מלאה, *כי המתכון כבר כתוב*.",
          "notes": "לספר מאיפה זה בא: צורך לנהל משימות טוב יותר מכל סוגי הדאטות. להראות את הסקיל רץ בלייב.\n\nהנתונים בצילום הם דוגמה."})
S.append({"type": "raw", "html": icards_slide("לא להמציא את הגלגל", f'מתקינים סקיל, או {acc("מוצאים מוכן")}', None, [
    icard("📦", "איך מתקינים", "מעלים את קובץ הסקיל בהגדרות של Claude, או שמים אותו בתיקיית הסקילים של הפרויקט.", 1),
    icard("🔎", "Find Skills", "הסקיל של Vercel מחפש בשבילכם בין אלפי סקילים שמישהו כבר בנה ובדק.", 3, foot("לפני שבונים, מחפשים", 3)),
    icard("✨", "מתי לבנות לבד", "כשאין סקיל מתאים, והמשימה חוזרת על עצמה שוב ושוב.", 5)],
    'לפני שבונים סקיל, <span class="hi">בודקים אם מישהו כבר בנה</span>.'),
          "notes": "להראות איך מתקינים סקיל בממשק (הגדרות → Skills) ובתיקייה.\n\nלהדגים את find-skills. פקודת ההתקנה (מהמסך שלי, לא לשקף):\nnpx skills add vercel-labs/skills --skill find-skills"})
S.append({"type": "raw", "html": handson_slide(),
          "notes": "כל אחד מעתיק את הפרומפט, מדביק בקלוד ובונים יחד את הסקיל עם הלוגו של חלאסרטן. אחרי שנבנה: לבקש מצגת קצרה, ו-Ctrl+P ל-PDF.\n\nבונוס אם נשאר זמן: 3 דקות של Claude Design ואיך בונים שם סיסטם דיזיין.\n\nדוגמה מוכנה לתוצר: המצגת הזו, ו-skills-example.html."})
S.append({"type": "raw", "html": icards_slide("קונקטורים ואבטחת מידע", f'לחבר את Claude {acc("בצורה אחראית")}', None, [
    icard("🔌", "Connectors", "Drive, Gmail, יומן, Slack או Notion. Claude שולף את המסמך העדכני בעצמו.", 1, foot("מחברים בהגדרות → Connectors", 1)),
    icard("🛡️", "מידע רגיש", "בלי פרטים מזהים של חברי קהילה. מידע רפואי עולה רק אחרי התממה.", 3),
    icard("🔑", "הרשאות מינימליות", "מחברים רק תיקיות רלוונטיות, ופעולות רגישות מאשרים ידנית.", 5)],
    'אנחנו תמיד <span class="hi">הטייס שמאשר</span> לפני שליחה או שינוי של מידע ארגוני.'),
          "notes": "להראות איפה בתפריט מחברים Connectors (כמו Google Drive) ומה זה חוסך: לא מורידים ומעלים קבצים ידנית.\n\nלהדגיש את נהלי אבטחת המידע בעמותה שמטפלת בצעירים חולי סרטן."})
S.append({"type": "steps", "eyebrow": "פלאגינים · רשות", "title": "Superpowers: Claude *חושב לפני שהוא עושה*",
          "steps": [{"title": "סיעור מוחות", "text": "שואל ומברר מה בדיוק צריך, במקום לקפוץ לביצוע."},
                    {"title": "תוכנית", "text": "כותב תוכנית עבודה ומציג אותה לאישור."},
                    {"title": "ביצוע ובדיקה", "text": "מבצע לפי התוכנית ובודק את עצמו בסוף."}],
          "takeaway": "פלאגין = *חבילה של סקילים וכלים* שמתקינים בבת אחת.",
          "notes": "אופציונלי, רק אם הקהל סקרן ויש זמן: 2 דקות להראות איך Superpowers גורם לקלוד לתכנן לפני ביצוע."})
S.append({"type": "raw", "html": icards_slide("סוכן בתוך הדפדפן", f'Claude in Chrome: {acc("Claude בא אל האתר")}', None, [
    icard("📥", "התקנה ב-30 שניות", "תוסף רשמי מחנות Chrome, נצמד לסרגל ונפתח בחלונית צד.", 1, foot("עובד על כל אתר פתוח", 1)),
    icard("🪄", "מה זה נותן", "סיכום עמודים ארוכים, איסוף נתונים מפורטלים, מילוי טפסים חוזרים.", 3),
    icard("🛡️", "עבודה בטוחה", "רואים כל צעד שהוא מתכנן, ומאשרים לפני פעולות חשובות.", 5, foot("אתם מאשרים, הוא מבצע", 5))],
    'במקום להעתיק מאתרים ל-Claude, <span class="hi">מביאים את Claude לאתר</span>.'),
          "notes": "להדגים פתיחה של התוסף על עמוד אמיתי ולהראות איך קלוד קורא את המסך ומבצע פעולה שחוסכת עבודה ידנית.\n\nלהזכיר את מצב ההרשאות."})
S.append({"type": "raw", "html": usecases_slide(),
          "notes": "החלק האינטראקטיבי המרכזי: עוברים משתתף-משתתף, שומעים את ה-Use Case, וממפים אותו יחד על המסך: תיקייה, מודל, הקשר וסקיל."})
S.append({"type": "closing", "eyebrow": "צ'קליסט למחר בבוקר", "title": "5 צעדים קטנים, *לפי הסדר*",
          "points": [{"title": "הראיון ההפוך", "text": "מריצים את 10 השאלות ומעדכנים Instructions."},
                     {"title": "סדר בתיקיות", "text": "תיקייה ברורה לפרויקט המרכזי של השבוע."},
                     {"title": "Haiku למסמכים", "text": "Haiku לסריקה, Sonnet לכתיבה."},
                     {"title": "Project משותף", "text": "Project אחד עם הצוות, עם מסמכי הליבה."},
                     {"title": "סקיל ראשון", "text": "סקיל המצגות, ונסיון עם תוסף Chrome."}],
          "note": "Claude · Cowork · Find Skills · Superpowers · Claude in Chrome · בהצלחה!",
          "notes": "אל תנסו ליישם הכל ביום אחד, מתחילים מחמשת הצעדים לפי הסדר.\n\nלהזכיר שאפשר להדפיס את המצגת ל-PDF (Ctrl+P) כדי שהפרומפטים יישארו זמינים."})

json.dump({"meta": meta, "slides": S}, open('meeting-5.json', 'w'), ensure_ascii=False, indent=1)
print(len(S), 'slides')
