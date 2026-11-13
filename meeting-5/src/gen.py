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

TOKENS = ["חלא", "סרט", "ן", "מחבר", "ת", "צעיר", "ים", "חול", "ים"]

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

S = []
S.append({"type": "cover", "mode": "dark", "eyebrow": "סדנת המשך · הנהלת חלאסרטן",
          "title": "להפוך את Claude\n*לשותף עבודה* שמכיר אתכם",
          "subtitle": "מצ'אט שמתחיל כל פעם מאפס, לסביבת עבודה עם זיכרון, פרויקטים משותפים וסקילים.",
          "notes": "ברוכים הבאים לסדנת ההמשך של הנהלת חלאסרטן! במפגש הקודם טעמנו מהעולם של AI, והיום אנחנו עולים קומה.\n\nנתחיל מלהבין איך המודל קורא טוקנים ופרומפטים, ונראה איך מתוך ההבנה הזו בונים לקלוד זיכרון קבוע, פרויקטים משותפים וסקילים שחוסכים שעות של עבודה.\n\n12 כלים מעשיים ליישום מיידי."})

# ---- foundations
S.append({"type": "raw", "html": tokens_slide(),
          "notes": "כמו שלמדנו במפגש 2: מודל שפה מנבא את הטוקן הבא על סמך הטוקנים שכבר נמצאים בחלון ההקשר שלו.\n\nטוקן הוא אבן הבניין הקטנה ביותר שהמודל מעבד: מילה שלמה, הברה או חלק ממילה. באנגלית מילה היא לרוב טוקן אחד; בעברית כל מילה מתפרקת ל-2 עד 4 טוקנים.\n\nכל טוקן שנכנס (בקשה ומסמכים) וכל טוקן שיוצא (תשובת המודל) נספרים במכסת השיחה."})
S.append({"type": "compare", "eyebrow": "חלון ההקשר", "title": "חלון ההקשר הוא *שולחן העבודה* של Claude",
          "subtitle": "כמות הטוקנים ש-Claude רואה וזוכר בשיחה אחת, בבת אחת.",
          "left": {"label": "שולחן עמוס", "title": "אובדן פוקוס", "items": ["5 נושאים באותה שיחה ארוכה", "הטוקנים מתבזבזים", "איכות התשובה צונחת"]},
          "right": {"label": "שולחן נקי", "title": "תשובה חדה", "items": ["רק ההקשר של המשימה", "Claude ממוקד במה שחשוב", "*צ'אט חדש לכל משימה*"]},
          "takeaway": "כלל ברזל: משימה חדשה? *פותחים צ'אט חדש ונקי*.",
          "notes": "חלון ההקשר הוא כמות הטוקנים המקסימלית שקלוד מסוגל לראות ולזכור בשיחה אחת, כמו שולחן עבודה.\n\nשולחן נקי = תשובה חדה. שולחן עמוס = אובדן פוקוס.\n\nמעבר לשקף הבא: אז איך מכוונים את חיזוי הטוקנים בדיוק למה שאנחנו צריכים? כאן נכנס מבנה הפרומפט."})
S.append({"type": "table", "eyebrow": "הנדסת פרומפטים", "title": "5 מרכיבים של פרומפט טוב. *3 מהם קבועים*",
          "columns": ["מרכיב", "השאלה", "בכל שיחה"],
          "rows": [["1. תפקיד (Role)", "מי אתם ומה המומחיות?", "*קבוע*"],
                   ["2. הקשר (Context)", "חלאסרטן וקהל היעד", "*קבוע*"],
                   ["3. הוראה (Instruction)", "מה המשימה היום?", "משתנה"],
                   ["4. נתוני קלט (Input)", "המסמך או הנתונים", "משתנה"],
                   ["5. פורמט וטון (Output)", "בגובה העיניים, מבנה מועדף", "*קבוע*"]],
          "highlight": 2,
          "takeaway": "את הקבועים כותבים *פעם אחת*, ב-Global Instructions.",
          "notes": "פרומפט הוא ההוראה שמכוונת את המודל. כשבונים אותו מ-5 מרכיבים ברורים מקבלים תוצאה מעולה.\n\nאבל שימו לב: סעיפים 1 (התפקיד), 2 (ההקשר של חלאסרטן) ו-5 (סגנון הכתיבה) קבועים אצלכם."})
S.append({"type": "compare", "eyebrow": "למה הניסוח משנה הכל", "title": "אותה בקשה, *שתי תוצאות*",
          "left": {"label": "פרומפט עמום", "title": "\"תכתוב לי פוסט לקהילה על מפגש זכויות חדש.\"", "items": ["טקסט גנרי ורשמי", "מנותק מהשפה של חלאסרטן"]},
          "right": {"label": "פרומפט מלא", "title": "תפקיד + הקשר + טון + המשימה", "items": ["\"אני מנהל/ת הקהילה בחלאסרטן…\"", "\"כתוב בגובה העיניים, בלי קלישאות\"", "*מדויק בול*, אבל מתיש להקליד כל פעם"]},
          "takeaway": "למה להקליד את ההקדמה בכל פעם מחדש? *שומרים אותה פעם אחת*.",
          "notes": "הפרומפט המלא: \"אני מנהל/ת הקהילה בחלאסרטן (צעירים חולי סרטן 18-44). כתוב בעברית ישירה ובגובה העיניים בלי קלישאות. נסח פוסט שמזמין למפגש מיצוי זכויות ביטוח לאומי ביום ג', עם 3 סיבות למה שווה להגיע.\"\n\nזה הגשר בין הנדסת פרומפטים (ממפגש 2) לבין עבודה חכמה בקלוד: 3 מתוך 5 הרכיבים קבועים לתפקיד שלהם. בשקף הבא נראה איך מקבעים אותם ב-Global Instructions."})

# ---- global instructions
S.append({"type": "raw", "html": roles_slide(),
          "notes": "לעבור על שלוש העמודות (ניהול קהילה, גיוס משאבים, מנכ\"לות וכספים) כדי שהמשתתפים יראו איך 3 המרכיבים הקבועים (Role + Context + Output) מתורגמים ל-Global Instructions.\n\nמה זה נותן: שומר על השפה הישירה והלא-מתנשאת בלי לבקש בכל פרומפט; גיוס: מצמיד מקור לכל נתון מספרי; כספים: פותח כל ניתוח בשורה התחתונה ומציג טבלאות.\n\nכפתור ההעתקה מעתיק את הבלוק של כל תפקיד. רוצים כזה שמותאם בול אליכם? השקף הבא."})
S.append({"type": "steps", "eyebrow": "תרגול: הראיון ההפוך", "title": "נותנים ל-Claude *לראיין אתכם*",
          "steps": [{"title": "מדביקים את פרומפט הראיון", "text": "בשקף הבא, עם כפתור העתקה."},
                    {"title": "עונים על 10 שאלות", "text": "תפקיד, קהל יעד, סגנון כתיבה, ומה אתם שונאים בתשובות AI."},
                    {"title": "שומרים את הסיכום", "text": "מדביקים ב-Settings → Profile → Instructions."}],
          "takeaway": "5 דקות של ראיון חוסכות *שעות של הסברים חוזרים*.",
          "notes": "במקום לשבור את הראש מול דף לבן, מבקשים מקלוד לשאול אתכם 10 שאלות ולהרכיב עבורכם את ההנחיות הקבועות.\n\nמעכשיו בכל צ'אט חדש קלוד כבר ידבר בדיוק בשפה שלכם."})
S.append({"type": "raw", "html": prompt_slide("תרגול: הראיון ההפוך", f'הפרומפט: {acc("העתיקו והדביקו")}', None,
                                              "פרומפט הראיון ההפוך", REVERSE, f'בסוף הראיון: מדביקים את הסיכום ב-<span class="hi" dir="ltr">Settings → Profile</span>', 40),
          "notes": "אחרי שהם ראו בשקף הקודם איך נראה תוצר מוגמר של Global Instructions, עכשיו כל אחד לוחץ על כפתור ההעתקה, מדביק בקלוד ועונה על 10 השאלות כדי לקבל בלוק מותאם אישית לתפקיד שלו."})

# ---- environments
S.append({"type": "cards", "eyebrow": "שלוש סביבות עבודה", "title": "יועץ, עובד או בונה: *Chat, Cowork, Code*", "subtitle": "מתי צריך שיחה, מתי צריך שיבצעו בשבילכם, ומתי צריך כלי חדש.",
          "cards": [{"title": "Chat · היועץ", "text": "סיעור מוחות, חידוד מסרים, ניסוח מכתבים לתורמים והתייעצות מהירה."},
                    {"title": "Cowork · העובד", "text": "עובד על התיקיות שלכם, מתכנן ומבצע משימה שלמה מתחילה ועד סוף."},
                    {"title": "Code · הבונה", "text": "בונה כלים, דשבורדים, מצגות וסקילים שלמים, גם מבקשה בשפה פשוטה."}],
          "takeaway": "ב-Chat הוא עונה. ב-Cowork וב-Code הוא *מחזיר קובץ מוכן*.",
          "notes": "להדגיש את ההבדל בין Chat (שיחה) לבין Cowork (\"Claude Code בלי קוד\" לאנשי ניהול ותפעול) שבו פשוט מצביעים על תיקייה במחשב ונותנים לקלוד לעבוד.\n\nדוגמה ל-Cowork: \"עבור על כל הקבלות בתיקייה והפק טבלת סיכום\".\n\nבשקף הבא נראה איך בונים פרומפט מנצח ל-Cowork אחרי שכבר הגדרנו Global Instructions."})
S.append({"type": "raw", "html": cowork_slide(),
          "notes": "שימו לב לחיבור: מכיוון שהתפקיד והרקע של חלאסרטן כבר שמורים ב-Global Instructions, ב-Cowork צריך להגדיר רק 3 מרכיבים משתנים: התוצר (Deliverable), חומרי הגלם (Inputs) והדגש הספציפי למשימה (Nuance).\n\nללחוץ על אפשרויות שונות ולהראות איך הפרומפט משתנה בלייב. כפתור ההעתקה מעתיק את הפרומפט המורכב."})
S.append({"type": "table", "eyebrow": "בחירת המודל", "title": "Haiku, Sonnet או Opus: *מודל לפי משימה*",
          "columns": ["מודל", "האופי", "מתי להשתמש", "מהירות ומכסה"],
          "rows": [["Haiku", "הסורק המהיר", "סיכום פרוטוקולים, חילוץ נתונים", "מיידי · הכי חסכוני"],
                   ["*Sonnet*", "*סוס העבודה*", "*ניוזלטרים, דוחות, מצגות*", "*ברירת מחדל ל-80%*"],
                   ["Opus", "האסטרטג", "תוכנית שנתית, דילמות רגישות", "איטי · מכסה גבוהה"]],
          "takeaway": "מסמך ארוך? *Haiku קורא אותו* בלי לשרוף את המכסה.",
          "notes": "כאן הכל מתחבר למה שלמדנו על טוקנים: מסמכים ארוכים שורפים המון טוקנים. אם נסרוק אותם עם Opus המכסה תיגמר מהר מאוד. Haiku קורא מסמכים במהירות שיא ובמינימום עלות.\n\nהתאמת המודל לסוג המשימה חוסכת זמן, מונעת הגבלות מכסה ומדייקת את התוצאה."})

# ---- context & memory
S.append({"type": "compare", "eyebrow": "סדר וארגון", "title": "כל פרויקט מקבל *תיקייה משלו*",
          "left": {"label": "איך רוב האנשים עובדים", "title": "תיקיית הורדות כאוטית", "items": ["final_v2_new(1).docx על שולחן העבודה", "Claude סורק קבצים לא קשורים", "אף אחד לא זוכר איפה התוצר"]},
          "right": {"label": "הרגל מנצח", "title": "2026-11-Annual-Donors-Event", "items": ["01-Raw-Materials: מסמכי מקור", "02-Outputs: מצגות ודוחות", "CLAUDE.md: הנחיות הפרויקט"]},
          "takeaway": "לפני משימה חדשה ב-Claude, *פותחים לה תיקייה עם שם ברור*.",
          "notes": "כשעובדים עם סוכני AI, סדר בתיקיות הוא לא עניין טכני. הוא המפתח לכך שנדע איפה כל דבר נשמר.\n\nהמבנה: Halasartan-Projects / 2026-11-Annual-Donors-Event / 01-Raw-Materials, 02-Outputs, CLAUDE.md.\n\nלהראות איך המבנה הפשוט הזה מונע את הבלגן של \"איפה הקובץ שקלוד יצר לי בשבוע שעבר?\" ומאפשר ל-Cowork לעבוד רק בתוך התיקייה של אותו פרויקט."})
S.append({"type": "cards", "eyebrow": "הזיכרון הארגוני", "title": "Obsidian: *זיכרון אמיתי* על הידע שלנו", "subtitle": "הדבר הכי חשוב בעבודה עם AI הוא ההקשר.",
          "cards": [{"title": "מה זה?", "text": "מחברת שמחזיקה סיכומים, פרויקטים ונהלים כקבצי טקסט פשוטים במחשב."},
                    {"title": "איך מחברים?", "text": "זו פשוט תיקייה, אז Claude ניגש אליה דרך Cowork או Connector."},
                    {"title": "שואלים בשפה טבעית", "text": "\"מה החלטנו ברבעון האחרון על תוכנית המנטורינג?\""}],
          "takeaway": "המודל הוא המנוע. *ההקשר ב-Obsidian הוא הדלק*.",
          "notes": "הדבר הכי חשוב בכל עבודה עם AI הוא ה-Context: היכולת לתשאל את הידע שלנו בלי להזין אותו כל פעם מחדש.\n\nקבצי Obsidian מקושרים זה לזה כמו מוח שני. ברגע שהמידע יושב שם בצורה מסודרת, קלוד מכיר את הדאטה שלנו ואפשר לייצר ממנה תובנות בשניות."})
S.append({"type": "steps", "eyebrow": "עבודת צוות", "title": "Projects: *סביבת עבודה משותפת* לכל תחום",
          "steps": [{"title": "פותחים Project ומגדירים מטרה", "text": "למשל \"גיוס שותפויות וקרנות\", עם הנחיות רק לפרויקט הזה."},
                    {"title": "מעלים מסמכי ליבה", "text": "דפי עמדה, נתוני אימפקט ובקשות מענקים מוצלחות מהעבר."},
                    {"title": "משתפים עם הצוות", "text": "כל מי שנכנס נהנה מאותו זיכרון ומאותן הנחיות."}],
          "takeaway": "שפה ארגונית אחידה, *וחפיפה קצרה בהרבה*.",
          "notes": "להראות בלייב בממשק של קלוד איך לוחצים על Projects, מוסיפים קובץ ל-Project Knowledge ולוחצים על Share כדי שכל ההנהלה תעבוד על אותה תשתית ידע."})

# ---- skills (folded in from the skills mini-deck)
S.append({"type": "section", "eyebrow": "אוטומציה של מומחיות", "title": "איך בונים\n*סקיל טוב*", "subtitle": "הסיפור מאחורי כלי אחד שבניתי, ומה אפשר ללמוד ממנו.",
          "notes": "פתיחת החלק על סקילים. לא נדבר על קוד.\n\nהמטרה: שכל אחד ייצא עם הבנה מה זה סקיל, ואיך מתחילים לכתוב אחד בעצמו."})
S.append({"type": "image", "eyebrow": "מה זה בכלל?", "title": "סקיל = נוהל עבודה ל-Claude",
          "subtitle": "כמו מסמך קליטה לעובד חדש, או מתכון קבוע של שף.",
          "src": "assets/onboarding-binder.jpg", "alt": "איור: אדם מגיש לעוזר דיגיטלי קלסר נהלים מסודר עם רשימת בדיקה",
          "points": ["*מסביר איך עובדים*: מה לשאול, אילו צעדים, ומה נחשב תוצאה טובה.", "*נטען רק כשצריך*, כמו קלסר שנשלף מהמדף.", "*ניתן לשיתוף*: כותבים פעם אחת, וכל הצוות מקבל אותה איכות."],
          "takeaway": "סקיל הוא *ידע שנכתב פעם אחת* ונעשה בו שימוש שוב ושוב.",
          "notes": "דימוי מרכזי: עובד חדש ומוכשר שעוד לא מכיר את הארגון. סקיל הוא המסמך שאתם נותנים לו ביום הראשון. או: מתכון שף. קובץ SKILL.md אורז את כל שלבי העבודה, העיצוב ובדיקות האיכות, וקלוד שולף אותו לבד כשהמשימה מתאימה.\n\nלשאול את הקהל: איזה נוהל הייתם רוצים שעובד חדש יכיר מהיום הראשון?"})
S.append({"type": "image", "eyebrow": "מאיפה זה התחיל", "title": "בעיה אמיתית, לא רעיון טכנולוגי",
          "src": "assets/one-hour-left.jpg", "alt": "איור: אדם מול מחשב נייד עם מצגת לא גמורה, ושעון קיר שמראה שנשארה שעה",
          "points": ["הייתי צריך מצגות מעוצבות, מהר, ובעברית.", "כלי העיצוב דרשו קרדיטים, והעברית בעורכי המצגות התהפכה.", "*הסברתי ל-Claude את אותם דברים* בכל פעם מחדש."],
          "takeaway": "הסימן הכי טוב לסקיל: *משימה שחוזרת על עצמה*.",
          "notes": "הנקודה החשובה היא השלישית: כשאתם מוצאים את עצמכם מסבירים שוב ושוב את אותו הדבר, זה סקיל שמחכה להיכתב.\n\nלהזמין דוגמאות מהקהל: דוחות חודשיים, מכתבי תודה לתורמים, סיכומי ישיבות."})
S.append({"type": "steps", "eyebrow": "האנטומיה", "title": "ארבעה דברים שכל סקיל טוב כולל",
          "steps": [{"title": "מתי להפעיל", "text": "משפט שמתאר באילו בקשות הסקיל רלוונטי."},
                    {"title": "מה לשאול לפני שמתחילים", "text": "אצלי: מי הקהל, כמה שקופיות, ושם המציג."},
                    {"title": "איך לעבוד", "text": "הצעדים, הסגנון, והדוגמאות למה שנחשב טוב."},
                    {"title": "איך לבדוק את עצמו", "text": "רשימת בדיקה שהתוצאה עוברת לפני שהיא מגיעה אליכם."}],
          "notes": "אפשר לעבור על כל שלב עם הדוגמה של המצגות.\n\nלהדגיש את שלב 2: Claude שואל במקום לנחש. זה ההבדל הכי מורגש למשתמש."})
S.append({"type": "compare", "eyebrow": "מה למדתי בדרך", "title": "מ\"עובד\" ל\"טוב\"",
          "left": {"label": "הגרסה הראשונה", "title": "עבד, אבל רק אצלי", "items": ["מותאם לארגון אחד ולעיצוב אחד", "מנחש מה רוצים", "עושה הכל בבת אחת", "מקווה שיצא טוב"]},
          "right": {"label": "הגרסה שפרסמתי", "title": "עובד לכל אחד", "items": ["צבעים, לוגו ושפה ניתנים לשינוי", "שואל לפני שמתחיל", "מחלק את העבודה לשלבים", "*בודק את עצמו* ומתקן"]},
          "takeaway": "כל ניסוי על תוכן אמיתי חשף בעיה, ו*כל בעיה הפכה לשיפור*.",
          "notes": "לספר על הניסויים: לוגו עם רקע שחור, צילום מסך של טלפון שנמתח, עברית שהתהפכה ליד מילה באנגלית. כל אחד מהם הפך לכלל בנוהל.\n\nהמסר: לא צריך לכתוב סקיל מושלם בפעם הראשונה. המצגת הזו עצמה נבנתה עם הסקיל."})
S.append({"type": "cards", "eyebrow": "לא להמציא את הגלגל", "title": "לפני שבונים, *מחפשים*", "subtitle": "מישהו אולי כבר בנה את הסקיל שאתם צריכים.",
          "cards": [{"title": "דוגמה מהשטח", "text": "סקיל שאוסף משימות מאקסלים, פתקים ומיילים ובונה דשבורד ניהולי."},
                    {"title": "Find Skills", "text": "סקיל של Vercel שמחפש בין אלפי סקילים שמישהו כבר בנה ובדק."},
                    {"title": "מתי לבנות לבד", "text": "כשאין סקיל מתאים, והמשימה חוזרת יותר מפעמיים בחודש."}],
          "takeaway": "כל פעולה שחוזרת *יותר מפעמיים בחודש* ראויה לסקיל.",
          "notes": "להציג את הסקיל לבניית דשבורד ניהול משימות מכל סוגי הדאטאות, להראות איך מתקינים סקיל בתיקייה או בממשק, ולהדגים את find-skills.\n\nפקודת ההתקנה (להעתקה מהמסך שלי, לא לשקף):\nnpx skills add vercel-labs/skills --skill find-skills"})
S.append({"type": "bullets", "eyebrow": "תרגול משותף", "title": "בונים יחד: *סקיל מצגות* של חלאסרטן",
          "items": ["מנקודות גולמיות או מסמך, למצגת הנהלה מוכנה.", "הלוגו וצבעי העמותה, בעברית מלאה.", "Ctrl+P הופך אותה ל-PDF לשליחה לתורמים ולשותפים."],
          "takeaway": "מקבלים *מצגת חיה למסך* וגם *PDF לוואטסאפ*.",
          "notes": "להדגים איך בונים את הסקיל עם הלוגו של חלאסרטן על בסיס html-presentation, ואז להראות איך הדפסה בדפדפן הופכת את ה-HTML ל-PDF.\n\nבונוס אם נשאר זמן: 3 דקות של Claude Design / Artifacts לתכנון ויזואלי."})
S.append({"type": "raw", "html": prompt_slide("תרגול משותף", f'הפרומפט ליצירת {acc("הסקיל")}', None,
                                              "פרומפט: סקיל המצגות של חלאסרטן", SKILL_PROMPT, f'אחרי שנבנה: מבקשים ממנו מצגת, ו-<span dir="ltr">Ctrl+P</span> הופך אותה ל-<span class="hi">PDF נקי</span>.', 36),
          "notes": "כל אחד מעתיק את הפרומפט, מדביק בקלוד ובונים יחד את הסקיל. אחרי שנבנה: לבקש ממנו מצגת קצרה על נושא מהעבודה, ולראות את התוצאה."})

# ---- connect & act
S.append({"type": "cards", "eyebrow": "חיבורים, אבטחה ופלאגינים", "title": "לחבר את Claude *בצורה אחראית*", "subtitle": "גישה למערכות העבודה, עם בקרה שלנו.",
          "cards": [{"title": "Connectors", "text": "Drive, Gmail, יומן, Slack או Notion. Claude שולף את המסמך העדכני בעצמו."},
                    {"title": "אבטחת מידע", "text": "בלי פרטים מזהים של חברי קהילה. מחברים רק תיקיות רלוונטיות."},
                    {"title": "Superpowers (רשות)", "text": "פלאגין שגורם ל-Claude לחשוב ולתכנן לפני שהוא מבצע."}],
          "takeaway": "אנחנו תמיד *הטייס שמאשר* לפני שליחה או שינוי של מידע ארגוני.",
          "notes": "להראות איפה בתפריט מחברים Connectors (כמו Google Drive).\n\nלהדגיש את נהלי אבטחת המידע בעמותה שמטפלת בצעירים חולי סרטן: מידע רפואי/אישי רגיש לא עולה בלי אנונימיזציה; הרשאות מינימליות; פעולות רגישות מאשרים ידנית.\n\nאם הקהל סקרן: 2 דקות על Superpowers (סיעור מוחות → תוכנית → ביצוע ובדיקה עצמית)."})
S.append({"type": "cards", "eyebrow": "סוכן בתוך הדפדפן", "title": "Claude in Chrome: *Claude בא אל האתר*", "subtitle": "תוסף שרואה את הכרטיסייה הפתוחה ופועל בה.",
          "cards": [{"title": "התקנה ב-30 שניות", "text": "תוסף רשמי מחנות Chrome, נצמד לסרגל ונפתח בחלונית צד."},
                    {"title": "מה זה נותן", "text": "סיכום עמודים ארוכים, איסוף נתונים מפורטלים, מילוי טפסים חוזרים."},
                    {"title": "עבודה בטוחה", "text": "רואים כל צעד שהוא מתכנן, ומאשרים לפני פעולות חשובות."}],
          "takeaway": "במקום להעתיק מאתרים ל-Claude, *מביאים את Claude לאתר*.",
          "notes": "להדגים פתיחה של תוסף הכרום על עמוד אינטרנט אמיתי ולהראות איך קלוד קורא את המסך ומבצע פעולה שחוסכת עבודה ידנית.\n\nלהזכיר את מצב ההרשאות (Permissions Mode)."})
S.append({"type": "compare", "eyebrow": "שולחן עגול", "title": "מפצחים יחד *משימה אמיתית* שלכם",
          "left": {"label": "דוגמאות מהעמותה", "title": "שילובים של מה שלמדנו", "items": ["גיוס: Project + Obsidian + סקיל מצגות", "זכויות: Haiku סורק עדכונים ומנגיש אותם", "ישיבות: Cowork + דשבורד משימות"]},
          "right": {"label": "תבנית פיצוח", "title": "ארבע שאלות", "items": ["מה גוזל לכם הכי הרבה זמן השבוע?", "איזה הקשר Claude צריך?", "איזה מודל וכלי?", "כדאי לארוז את זה לסקיל?"]},
          "takeaway": "כל אחד יוצא עם *תהליך אחד שכבר עובד* השבוע.",
          "notes": "החלק האינטראקטיבי המרכזי של סוף המפגש: עוברים משתתף-משתתף, שומעים את ה-Use Case, וממפים אותו יחד על המסך: תיקייה, מודל, קונטקסט וסקיל.\n\nתזכורת לכלים: Haiku לקריאה, Sonnet ליצירה, Cowork לביצוע; הקשר מתיקייה, Obsidian או Project."})
S.append({"type": "closing", "eyebrow": "צ'קליסט למחר בבוקר", "title": "5 צעדים קטנים, *לפי הסדר*",
          "points": [{"title": "הראיון ההפוך", "text": "מריצים את 10 השאלות ומעדכנים Instructions."},
                     {"title": "סדר בתיקיות", "text": "תיקייה ברורה לפרויקט המרכזי של השבוע."},
                     {"title": "Haiku למסמכים", "text": "Haiku לסריקה, Sonnet לכתיבה."},
                     {"title": "Project + Obsidian", "text": "מאגר הקשר ארגוני, ו-Project משותף אחד."},
                     {"title": "סקיל ראשון", "text": "סקיל המצגות, ונסיון עם תוסף Chrome."}],
          "note": "Claude · Cowork · Obsidian · Find Skills · Superpowers · Claude in Chrome · בהצלחה!",
          "notes": "סיכום אנרגטי! אל תנסו ליישם הכל ביום אחד, מתחילים מחמשת הצעדים לפי הסדר.\n\nלהזכיר שאפשר להדפיס את המצגת ל-PDF (Ctrl+P) כדי שהפרומפטים יישארו זמינים."})

DROP = {"איך בונים\n*סקיל טוב*", "בעיה אמיתית, לא רעיון טכנולוגי", "ארבעה דברים שכל סקיל טוב כולל", "מ\"עובד\" ל\"טוב\""}
S = [x for x in S if x.get("title") not in DROP]
for x in S:
    if x.get("title") == "סקיל = נוהל עבודה ל-Claude":
        x["notes"] += "\n\nאת הסיפור המלא (איך בניתי סקיל, מה כל סקיל טוב כולל, ומה למדתי בדרך) נותנים בנפרד: skills-example.html."
    if x.get("type") == "bullets" and "סקיל מצגות" in x.get("title", ""):
        x["notes"] += "\n\nדוגמה מוכנה לתוצר של סקיל כזה: המצגת הנפרדת skills-example.html, שנבנתה כולה עם סקיל המצגות."
json.dump({"meta": meta, "slides": S}, open('meeting-5.json', 'w'), ensure_ascii=False, indent=1)
print(len(S), 'slides')
