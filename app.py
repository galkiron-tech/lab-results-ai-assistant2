import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MedExplain AI | הסבר תוצאות בדיקות דם",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — RTL, palette, cards
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&display=swap');

/* ── Base RTL ── */
html, body, [class*="css"] {
    direction: rtl;
    text-align: right;
    font-family: 'Heebo', sans-serif;
}

/* ── Palette variables ── */
:root {
    --blue-900: #0a2540;
    --blue-700: #1a4a7a;
    --blue-500: #2271b3;
    --blue-300: #5ba4d4;
    --blue-100: #e8f4fd;
    --teal-500: #0d9488;
    --teal-100: #ccfbf1;
    --amber-500: #d97706;
    --amber-100: #fef3c7;
    --red-500: #dc2626;
    --red-100: #fee2e2;
    --green-500: #16a34a;
    --green-100: #dcfce7;
    --gray-50:  #f8fafc;
    --gray-100: #f1f5f9;
    --gray-200: #e2e8f0;
    --gray-600: #475569;
    --gray-900: #0f172a;
    --white: #ffffff;
    --shadow-sm: 0 1px 3px rgba(0,0,0,.08);
    --shadow-md: 0 4px 16px rgba(0,0,0,.10);
    --shadow-lg: 0 8px 32px rgba(0,0,0,.13);
    --radius: 12px;
}

/* ── App background ── */
.stApp {
    background: linear-gradient(160deg, #f0f7ff 0%, #f8fafc 60%, #f0fdfa 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--blue-900) 0%, var(--blue-700) 100%);
    color: white !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #a8d4f0 !important; font-weight: 500; }
[data-testid="stSidebar"] .stRadio label { color: #cce4f7 !important; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Card base ── */
.card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.6rem 2rem;
    box-shadow: var(--shadow-md);
    margin-bottom: 1.2rem;
    border: 1px solid var(--gray-200);
}
.card-blue {
    background: linear-gradient(135deg, var(--blue-700), var(--blue-500));
    color: white;
}
.card-teal {
    background: linear-gradient(135deg, var(--teal-500), #0f766e);
    color: white;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, var(--blue-900) 0%, var(--blue-700) 50%, var(--teal-500) 100%);
    border-radius: 16px;
    padding: 3rem 2.5rem;
    color: white;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; left: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255,255,255,.05);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -30px;
    width: 280px; height: 280px;
    border-radius: 50%;
    background: rgba(255,255,255,.04);
}
.hero h1 { font-size: 2.4rem; font-weight: 800; margin: 0 0 .4rem 0; line-height: 1.2; }
.hero .subtitle { font-size: 1.1rem; opacity: .85; font-weight: 300; margin: 0; }
.hero .tag {
    display: inline-block;
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.3);
    border-radius: 20px;
    padding: .25rem .9rem;
    font-size: .8rem;
    font-weight: 600;
    letter-spacing: .04em;
    margin-bottom: 1rem;
}

/* ── Section heading ── */
.section-heading {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--blue-900);
    border-right: 4px solid var(--blue-500);
    padding-right: .75rem;
    margin-bottom: 1rem;
}

/* ── Stat pill ── */
.stat-row { display: flex; gap: .8rem; flex-wrap: wrap; margin-bottom: 1.2rem; }
.stat-pill {
    background: var(--blue-100);
    border: 1px solid #bfdbfe;
    border-radius: 999px;
    padding: .35rem 1.1rem;
    font-size: .85rem;
    font-weight: 600;
    color: var(--blue-700);
}

/* ── Status badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: .3rem;
    border-radius: 999px;
    padding: .28rem .9rem;
    font-size: .82rem;
    font-weight: 700;
    letter-spacing: .02em;
}
.badge-normal  { background: var(--green-100); color: var(--green-500); border: 1px solid #86efac; }
.badge-border  { background: var(--amber-100); color: var(--amber-500); border: 1px solid #fcd34d; }
.badge-abnormal{ background: var(--red-100);   color: var(--red-500);   border: 1px solid #fca5a5; }

/* ── Pipeline ── */
.pipeline {
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    gap: 0;
    overflow-x: auto;
    padding: 1rem 0;
}
.pipe-step {
    background: white;
    border: 1.5px solid var(--blue-300);
    border-radius: 10px;
    padding: .8rem 1.1rem;
    min-width: 130px;
    text-align: center;
    font-size: .82rem;
    font-weight: 600;
    color: var(--blue-900);
    line-height: 1.35;
    flex-shrink: 0;
}
.pipe-arrow {
    font-size: 1.4rem;
    color: var(--blue-400, #60a5fa);
    padding: 0 .3rem;
    flex-shrink: 0;
}

/* ── Lab table ── */
.lab-table { width: 100%; border-collapse: collapse; font-size: .92rem; }
.lab-table th {
    background: var(--blue-900);
    color: white;
    padding: .65rem 1rem;
    text-align: right;
    font-weight: 600;
    font-size: .83rem;
}
.lab-table td { padding: .6rem 1rem; border-bottom: 1px solid var(--gray-200); }
.lab-table tr:last-child td { border-bottom: none; }
.lab-table tr:hover td { background: var(--blue-100); }

/* ── Explanation panel ── */
.exp-block {
    background: var(--gray-50);
    border-right: 4px solid var(--blue-500);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
}
.exp-block.border-finding { border-right-color: var(--amber-500); }
.exp-block.abnormal-finding { border-right-color: var(--red-500); }
.exp-block h4 { font-size: 1rem; font-weight: 700; color: var(--blue-900); margin: 0 0 .5rem 0; }
.exp-block .exp-label { font-size: .78rem; font-weight: 700; color: var(--blue-500); text-transform: uppercase; letter-spacing: .05em; margin-bottom: .2rem; }
.exp-block p { font-size: .9rem; color: var(--gray-600); margin: 0 0 .6rem 0; line-height: 1.55; }

/* ── Question pills ── */
.q-list { list-style: none; padding: 0; margin: 0; }
.q-list li {
    background: var(--blue-100);
    border-radius: 8px;
    padding: .5rem .9rem;
    margin-bottom: .45rem;
    font-size: .88rem;
    color: var(--blue-900);
    border-right: 3px solid var(--blue-500);
}
.q-list li::before { content: "❓ "; }

/* ── Comparison table ── */
.cmp-table { width: 100%; border-collapse: collapse; font-size: .88rem; }
.cmp-table th {
    padding: .7rem 1rem;
    text-align: right;
    font-weight: 700;
    font-size: .85rem;
}
.cmp-table td { padding: .6rem 1rem; border-bottom: 1px solid var(--gray-200); vertical-align: top; }
.cmp-table .col-public { background: #fff7ed; color: #92400e; }
.cmp-table .col-hmo    { background: #f0fdf4; color: #14532d; }
.cmp-table .th-public  { background: #f97316; color: white; }
.cmp-table .th-hmo     { background: var(--teal-500); color: white; }

/* ── Ethics / safety boxes ── */
.ethics-box {
    background: var(--amber-100);
    border: 1.5px solid #fcd34d;
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    font-size: .88rem;
    color: #78350f;
    margin-bottom: .8rem;
}
.ethics-box strong { color: #92400e; }

/* ── Metric card ── */
.metric-card {
    background: white;
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    border: 1px solid var(--gray-200);
    box-shadow: var(--shadow-sm);
    margin-bottom: .7rem;
}
.metric-card .m-title { font-size: .82rem; font-weight: 700; color: var(--blue-700); margin-bottom: .3rem; }
.metric-card .m-body  { font-size: .88rem; color: var(--gray-600); }

/* ── Patient info chip row ── */
.patient-chips { display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: 1rem; }
.patient-chip {
    background: var(--blue-100);
    border-radius: 999px;
    padding: .25rem .8rem;
    font-size: .82rem;
    color: var(--blue-700);
    font-weight: 600;
}

/* ── Tabs (override Streamlit) ── */
.stTabs [data-baseweb="tab-list"] { gap: .5rem; border-bottom: 2px solid var(--gray-200); }
.stTabs [data-baseweb="tab"] {
    font-family: 'Heebo', sans-serif !important;
    font-weight: 600;
    font-size: .93rem;
    color: var(--gray-600);
    border-radius: 8px 8px 0 0;
    padding: .5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: var(--blue-500) !important;
    color: white !important;
}

/* ── Info/warning callout ── */
.callout {
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    font-size: .88rem;
    margin-bottom: 1rem;
    line-height: 1.6;
}
.callout-info    { background: var(--blue-100); border-right: 4px solid var(--blue-500); color: var(--blue-900); }
.callout-warning { background: var(--amber-100); border-right: 4px solid var(--amber-500); color: #78350f; }
.callout-success { background: var(--green-100); border-right: 4px solid var(--green-500); color: #14532d; }

/* footer note */
.footnote { font-size: .75rem; color: #94a3b8; text-align: center; padding: 1.5rem 0 .5rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA — SYNTHETIC PATIENTS + INTERPRETATIONS
# ─────────────────────────────────────────────

REFERENCE = {
    "WBC":          {"unit": "10³/μL",  "low": 4.0,  "high": 10.0,  "border_low": None, "border_high": 12.0},
    "Hemoglobin":   {"unit": "g/dL",    "low": 12.0, "high": 17.5,  "border_low": 11.0, "border_high": None},
    "Ferritin":     {"unit": "ng/mL",   "low": 12.0, "high": 200.0, "border_low": 20.0, "border_high": None},
    "HbA1c":        {"unit": "%",       "low": None,  "high": 5.6,   "border_low": None, "border_high": 6.4},
    "LDL":          {"unit": "mg/dL",   "low": None,  "high": 100.0, "border_low": None, "border_high": 129.0},
    "HDL":          {"unit": "mg/dL",   "low": 40.0,  "high": None,  "border_low": 50.0, "border_high": None},
    "Triglycerides":{"unit": "mg/dL",   "low": None,  "high": 150.0, "border_low": None, "border_high": 199.0},
    "CRP":          {"unit": "mg/L",    "low": None,  "high": 5.0,   "border_low": None, "border_high": 10.0},
}

def classify(test, value):
    """Returns ('תקין'|'גבולי'|'חריג', css_class)"""
    r = REFERENCE[test]
    # Hard abnormal
    if r["low"]  is not None and value < r["low"]:
        # check borderline low
        if r["border_low"] is not None and value >= r["border_low"]:
            return "גבולי", "badge-border"
        return "חריג", "badge-abnormal"
    if r["high"] is not None and value > r["high"]:
        # check borderline high
        if r["border_high"] is not None and value <= r["border_high"]:
            return "גבולי", "badge-border"
        return "חריג", "badge-abnormal"
    return "תקין", "badge-normal"


EXPLANATIONS = {
    "WBC_גבולי": {
        "summary": "ספירת תאי הדם הלבנים שלך גבוהה מעט מהנורמה — רמה זו נחשבת קלה ואינה מצריכה טיפול מיידי.",
        "what": "WBC (תאי דם לבנים) הם חיילי מערכת החיסון שלך. הם עוזרים לגוף להילחם בזיהומים.",
        "why": "ספירה מעט גבוהה יכולה להופיע לאחר זיהום קל, מאמץ גופני, מתח נפשי, עישון, או נטילת תרופות מסוימות.",
        "ask_doc": ["האם ספירת WBC זו משמעותית בהשוואה לבדיקות קודמות שלי?", "האם כדאי לחזור על הבדיקה?", "האם יש סיבה ספציפית שאתה מזהה לעלייה זו?", "האם יש צורך בבדיקות נוספות?"],
        "attention": "במידה ומופיעים חום מתמשך, עייפות קיצונית או נפיחות לא מוסברת — פנה לרופאך.",
    },
    "WBC_חריג": {
        "summary": "ספירת תאי הדם הלבנים שלך גבוהה באופן ניכר מהנורמה — ממצא זה ראוי לבדיקה רפואית.",
        "what": "WBC גבוה יכול להצביע על כך שמערכת החיסון שלך פעילה מאוד כרגע.",
        "why": "סיבות נפוצות כוללות זיהום פעיל, דלקת, תגובה לתרופות, או גורמים אחרים שרופאך יוכל להעריך.",
        "ask_doc": ["מה עשוי לגרום לספירה כה גבוהה?", "אילו בדיקות נוספות ממולצות?", "האם נדרש מעקב דחוף?", "האם יש קשר לתסמינים שאני חש/ת?", "מתי כדאי לחזור לבדיקת דם?"],
        "attention": "אם מופיעים חום גבוה, כאבים עזים, קשיי נשימה או חולשה קיצונית — פנה לעזרה רפואית.",
    },
    "Hemoglobin_גבולי": {
        "summary": "רמת ההמוגלובין שלך מעט נמוכה מהנורמה — רמה זו נחשבת קלה.",
        "what": "המוגלובין הוא חלבון בתאי הדם האדומים שנושא חמצן בכל הגוף.",
        "why": "ירידה קלה יכולה לנבוע מתזונה דלת ברזל, וסת מרובה, הריון, או שינויים עונתיים.",
        "ask_doc": ["האם הירידה משמעותית?", "האם כדאי לבדוק רמות ברזל ופריטין?", "האם נדרש שינוי תזונתי?", "מתי לחזור על הבדיקה?"],
        "attention": "אם אתה/את חש/ה עייפות חריגה, קוצר נשימה, או סחרחורות — ציין/י זאת לרופא.",
    },
    "Hemoglobin_חריג": {
        "summary": "רמת ההמוגלובין שלך נמוכה משמעותית — ממצא זה ראוי לבחינה רפואית.",
        "what": "ירידה ניכרת בהמוגלובין עלולה להשפיע על אספקת החמצן לגוף ועל תחושת העייפות שלך.",
        "why": "סיבות אפשריות כוללות חוסר ברזל, חוסר ויטמין B12 או חומצה פולית, ועוד — רופאך יוכל לאבחן.",
        "ask_doc": ["מה הסיבה הסבירה לירידה?", "אילו בדיקות נוספות נחוצות?", "האם נדרש טיפול תזונתי?", "כיצד ניתן לעקוב אחר השיפור?"],
        "attention": "אם אתה/את חש/ה קוצר נשימה במנוחה, דפיקות לב מואצות, או עלפון — פנה לרופא בהקדם.",
    },
    "Ferritin_גבולי": {
        "summary": "רמת הפריטין שלך נמצאת בטווח נמוך-תקין — ייתכן שמאגרי הברזל שלך מתחילים לרדת.",
        "what": "פריטין הוא חלבון שמאחסן ברזל בגוף. רמתו משקפת את מאגרי הברזל שלך.",
        "why": "פריטין נמוך יכול להופיע לפני שמוריד את ההמוגלובין, ולעיתים מלווה בעייפות, ירידת ריכוז, או נשירת שיער.",
        "ask_doc": ["האם כדאי לשפר תזונת ברזל?", "האם נדרש תוסף ברזל?", "האם יש קשר לתסמינים שאני חש/ת?", "מתי לבדוק שוב?"],
        "attention": "אין צורך בפנייה דחופה, אך ממולץ לדון עם רופאך בבדיקה הבאה.",
    },
    "Ferritin_חריג": {
        "summary": "רמת הפריטין שלך נמוכה — מאגרי הברזל בגוף ירודים.",
        "what": "פריטין נמוך מצביע על מאגרי ברזל מדולדלים, גם אם ספירת הדם עדיין תקינה.",
        "why": "גורמים נפוצים: תזונה דלת ברזל, ספיגה לקויה, איבוד דם חוזר (למשל וסת מרובה).",
        "ask_doc": ["מה הגורם המשוער לפריטין הנמוך?", "האם נדרש טיפול בתוסף ברזל?", "כיצד יש להתאים את התזונה?", "מתי לבדוק מחדש?"],
        "attention": "במידה ועייפות חמורה, נשירת שיער קיצונית, או קוצר נשימה — ציין/י לרופאך.",
    },
    "HbA1c_גבולי": {
        "summary": "רמת ה-HbA1c שלך נמצאת בטווח המעיד על עלייה מסוימת ברמות הסוכר — ממצא הדורש שימת לב ומעקב.",
        "what": "HbA1c מודד את רמת הסוכר הממוצעת בדם במשך 3 החודשים האחרונים.",
        "why": "ערכים גבוליים קשורים לעיתים לתזונה, פעילות גופנית, עלייה במשקל, גנטיקה, או גורמים אחרים.",
        "ask_doc": ["האם ערך זה השתנה לעומת בדיקות קודמות?", "האם כדאי לעקוב אחר רמות הסוכר?", "אילו שינויי תזונה ממולצים?", "האם נדרשת בדיקה מעמיקה יותר?"],
        "attention": "אין צורך בפנייה דחופה. ממולץ לדון עם רופאך על מעקב ושינוי אורח חיים.",
    },
    "HbA1c_חריג": {
        "summary": "רמת ה-HbA1c שלך גבוהה מהנורמה — ממצא שדורש בחינה רפואית ומעקב.",
        "what": "רמה גבוהה מצביעה על כך שרמות הסוכר בדם היו גבוהות יחסית בחודשים האחרונים.",
        "why": "קיימים גורמים שונים שעשויים להשפיע על ערך זה — רופאך יוכל להעריך את ההקשר האישי שלך.",
        "ask_doc": ["מה עשויה להיות משמעות הממצא עבורי?", "האם נדרשת בדיקת סוכר נוספת?", "אילו שינויים בתזונה ופעילות ממולצים?", "מתי לבצע בדיקת מעקב?", "האם יש התאמה נדרשת בטיפול?"],
        "attention": "ממולץ לקבוע תור לרופא בקרוב לדיון בממצא זה.",
    },
    "LDL_גבולי": {
        "summary": "רמת ה-LDL שלך מעט גבוהה מהיעד המומלץ — ממצא שכדאי לדון בו עם הרופא.",
        "what": "LDL הוא סוג של כולסטרול. רמות גבוהות לאורך זמן עשויות להשפיע על בריאות כלי הדם.",
        "why": "תזונה עשירה בשומן רווי, פעילות גופנית מופחתת, גנטיקה, ועוד — עשויים להשפיע על רמת ה-LDL.",
        "ask_doc": ["האם הרמה השתנתה לאורך זמן?", "אילו שינויים תזונתיים ממולצים?", "האם נדרשת בדיקת מעקב?", "מהו היעד המומלץ עבורי?"],
        "attention": "אין צורך בפנייה דחופה. מומלץ להתייעץ עם רופאך על אורח חיים בריא.",
    },
    "LDL_חריג": {
        "summary": "רמת ה-LDL שלך גבוהה — ממצא שכדאי לטפל בו בתשומת לב.",
        "what": "LDL גבוה לאורך זמן עשוי להשפיע על בריאות כלי הדם ועל הלב.",
        "why": "גורמים כוללים תזונה, אורח חיים, גנטיקה, ועוד — רופאך יוכל להעריך את ההקשר.",
        "ask_doc": ["מהי הסיבה הסבירה לרמת ה-LDL הגבוהה?", "מהו יעד ה-LDL המומלץ עבורי?", "אילו שינויים בתזונה ממולצים?", "האם נדרש טיפול תרופתי?", "מתי לבדוק מחדש?"],
        "attention": "מומלץ לקבוע תור לרופא לדיון בממצא.",
    },
    "HDL_גבולי": {
        "summary": "רמת ה-HDL שלך מעט נמוכה מהאידיאלי — כולסטרול HDL גבוה נחשב מגן.",
        "what": "HDL הוא 'כולסטרול טוב' — הוא עוזר לפנות עודפי כולסטרול מכלי הדם.",
        "why": "פעילות גופנית, הפסקת עישון, ותזונה בריאה עשויים לסייע בהעלאת רמת HDL.",
        "ask_doc": ["האם רמת ה-HDL שלי מדאיגה?", "כיצד ניתן לשפר אותה?", "האם יש קשר לממצאים אחרים בבדיקה?"],
        "attention": "אין צורך בפנייה דחופה. מומלץ לדון עם הרופא.",
    },
    "Triglycerides_גבולי": {
        "summary": "רמת הטריגליצרידים שלך גבוהה מעט מהנורמה.",
        "what": "טריגליצרידים הם שומנים בדם. רמה גבוהה לאורך זמן עשויה להשפיע על בריאות כלי הדם.",
        "why": "גורמים נפוצים: תזונה עשירה בסוכרים ושומנים, שתיית אלכוהול, חוסר פעילות גופנית.",
        "ask_doc": ["האם הרמה עלתה לעומת בדיקות קודמות?", "מהם השינויים התזונתיים המומלצים?", "מתי לבדוק מחדש?"],
        "attention": "אין צורך בפנייה דחופה. מומלץ לדון בבדיקה הבאה.",
    },
    "Triglycerides_חריג": {
        "summary": "רמת הטריגליצרידים שלך גבוהה — ממצא שדורש תשומת לב רפואית.",
        "what": "רמה גבוהה של טריגליצרידים עשויה להיות קשורה לגורמים שונים שרופאך יוכל להעריך.",
        "why": "תזונה, אלכוהול, פעילות גופנית, ומצבים רפואיים מסוימים — עשויים להשפיע על רמת הטריגליצרידים.",
        "ask_doc": ["מה הגורם המשוער?", "אילו שינויים ממולצים?", "האם נדרשת בדיקה נוספת?", "מתי לחזור על הבדיקה?"],
        "attention": "מומלץ לקבוע תור לרופא לדיון בממצא.",
    },
    "CRP_גבולי": {
        "summary": "רמת ה-CRP שלך מעט גבוהה — סמן דלקת קל.",
        "what": "CRP הוא חלבון שעולה בתגובה לדלקת בגוף.",
        "why": "דלקת קלה, זיהום עובר, מאמץ גופני, עישון, ועוד — עשויים להסביר עלייה קלה.",
        "ask_doc": ["מה עשוי לגרום לעלייה?", "האם נדרשת בדיקה חוזרת?", "האם יש קשר לתסמינים שאני חש/ת?"],
        "attention": "אין צורך בפנייה דחופה. מומלץ לדון עם הרופא.",
    },
    "CRP_חריג": {
        "summary": "רמת ה-CRP שלך גבוהה — ממצא המצביע על דלקת פעילה.",
        "what": "CRP גבוה מצביע על כך שמערכת החיסון מגיבה לגורם כלשהו בגוף.",
        "why": "זיהום, מחלה דלקתית, או גורמים אחרים — עשויים להסביר את הממצא.",
        "ask_doc": ["מה הגורם המשוער לרמה גבוהה זו?", "אילו בדיקות נוספות נחוצות?", "מה צעדי המעקב?"],
        "attention": "אם מלווה בחום, כאב עז, או תסמינים אחרים — פנה לרופא בהקדם.",
    },
}

def get_exp(test, status):
    key = f"{test}_{status}"
    return EXPLANATIONS.get(key, None)


PATIENTS = [
    {
        "id": 1,
        "name": "ד״ר דוד כהן (בדיקת ביקורת)",
        "age": 45,
        "sex": "זכר",
        "scenario": "כל הערכים תקינים",
        "labs": {
            "WBC": 6.8, "Hemoglobin": 15.2, "Ferritin": 95.0,
            "HbA1c": 5.1, "LDL": 88.0, "HDL": 52.0,
            "Triglycerides": 115.0,
        },
    },
    {
        "id": 2,
        "name": "מיכל לוי",
        "age": 52,
        "sex": "נקבה",
        "scenario": "LDL גבולי",
        "labs": {
            "WBC": 7.2, "Hemoglobin": 13.5, "Ferritin": 45.0,
            "HbA1c": 5.3, "LDL": 118.0, "HDL": 48.0,
        },
    },
    {
        "id": 3,
        "name": "אבי שמואלי",
        "age": 61,
        "sex": "זכר",
        "scenario": "HbA1c גבולי",
        "labs": {
            "WBC": 6.5, "Hemoglobin": 14.8, "Ferritin": 78.0,
            "HbA1c": 6.1, "LDL": 92.0, "Triglycerides": 130.0,
        },
    },
    {
        "id": 4,
        "name": "שרה ברקוביץ'",
        "age": 38,
        "sex": "נקבה",
        "scenario": "WBC מעט מוגבה",
        "labs": {
            "WBC": 11.4, "Hemoglobin": 12.8, "Ferritin": 28.0,
            "HbA1c": 5.0, "LDL": 82.0,
        },
    },
    {
        "id": 5,
        "name": "יוסי גולן",
        "age": 34,
        "sex": "זכר",
        "scenario": "WBC מוגבה בבירור",
        "labs": {
            "WBC": 14.5, "Hemoglobin": 14.1, "Ferritin": 55.0,
            "HbA1c": 5.2, "LDL": 95.0, "CRP": 12.0,
        },
    },
    {
        "id": 6,
        "name": "נורית אברהם",
        "age": 29,
        "sex": "נקבה",
        "scenario": "פריטין נמוך ללא אנמיה",
        "labs": {
            "WBC": 6.1, "Hemoglobin": 12.4, "Ferritin": 16.0,
            "HbA1c": 4.9, "LDL": 79.0,
        },
    },
    {
        "id": 7,
        "name": "חנה מזרחי",
        "age": 41,
        "sex": "נקבה",
        "scenario": "המוגלובין נמוך עם פריטין נמוך",
        "labs": {
            "WBC": 7.0, "Hemoglobin": 10.8, "Ferritin": 8.0,
            "HbA1c": 5.1, "LDL": 88.0,
        },
    },
    {
        "id": 8,
        "name": "רון שפירא",
        "age": 58,
        "sex": "זכר",
        "scenario": "LDL גבוה, HbA1c תקין",
        "labs": {
            "WBC": 7.8, "Hemoglobin": 15.0, "Ferritin": 110.0,
            "HbA1c": 5.4, "LDL": 145.0, "HDL": 38.0,
            "Triglycerides": 160.0,
        },
    },
    {
        "id": 9,
        "name": "לאה כץ",
        "age": 67,
        "sex": "נקבה",
        "scenario": "HbA1c גבוה ו-LDL גבוה",
        "labs": {
            "WBC": 8.2, "Hemoglobin": 13.1, "Ferritin": 32.0,
            "HbA1c": 7.2, "LDL": 138.0, "HDL": 42.0,
            "Triglycerides": 195.0,
        },
    },
    {
        "id": 10,
        "name": "משה אלון",
        "age": 49,
        "sex": "זכר",
        "scenario": "ממצאים גבוליים מעורבים",
        "labs": {
            "WBC": 10.8, "Hemoglobin": 13.9, "Ferritin": 18.0,
            "HbA1c": 5.9, "LDL": 112.0, "HDL": 45.0,
            "CRP": 7.5,
        },
    },
]

TEST_NAMES_HEB = {
    "WBC": "תאי דם לבנים (WBC)",
    "Hemoglobin": "המוגלובין",
    "Ferritin": "פריטין",
    "HbA1c": "המוגלובין מסוכרר (HbA1c)",
    "LDL": "כולסטרול LDL",
    "HDL": "כולסטרול HDL (טוב)",
    "Triglycerides": "טריגליצרידים",
    "CRP": "CRP (חלבון C-תגובתי)",
}

NORMAL_RANGE_STR = {
    "WBC": "4.0–10.0",
    "Hemoglobin": "12.0–17.5",
    "Ferritin": "12–200",
    "HbA1c": "< 5.7",
    "LDL": "< 100",
    "HDL": "≥ 40",
    "Triglycerides": "< 150",
    "CRP": "< 5.0",
}


# ─────────────────────────────────────────────
# SIDEBAR — NAVIGATION
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='padding:.5rem 0 1.2rem; border-bottom:1px solid rgba(255,255,255,.2); margin-bottom:1.2rem;'>
      <div style='font-size:1.5rem;'>🏥</div>
      <div style='font-size:1.1rem; font-weight:800; margin-top:.2rem;'>MedExplain AI</div>
      <div style='font-size:.75rem; opacity:.7; margin-top:.2rem;'>הסבר תוצאות בדיקות דם</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "ניווט",
        ["🏠 עמוד הבית", "📊 לוח מטופל", "⚙️ כיצד זה עובד", "🆚 מדוע לא ChatGPT?",
         "🛡️ בטיחות ואתיקה", "📈 מדדי הערכה"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,.2); margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:.75rem; opacity:.6; line-height:1.6;'>
      ⚠️ כלי זה מיועד לצרכי לימוד בלבד.<br>
      כל הנתונים סינתטיים.<br>
      אינו מאבחן ואינו ממליץ על טיפול.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────

if page == "🏠 עמוד הבית":
    st.markdown("""
    <div class='hero'>
      <div class='tag'>📚 Medical AI Course — Proof of Concept</div>
      <h1>🏥 MedExplain AI</h1>
      <p class='subtitle'>שכבת הסבר מבוססת בינה מלאכותית לתוצאות בדיקות דם — בשפה עברית פשוטה</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='card'>
          <div class='section-heading'>הבעיה</div>
          <p style='color:#475569; line-height:1.7; font-size:.93rem;'>
            מטופלים רבים מקבלים תוצאות בדיקות דם דרך אפליקציית הקופה — אך אינם יודעים כיצד לפרש אותן.
            ערכים "גבוליים" גורמים לדאגה מיותרת, בעוד ממצאים שכדאי לבדוק עוברים מבלי משים.
            הפנייה לרופא לעיתים מאוחרת, קצרה מדי, ולא מוכנה מספיק.
          </p>
          <div class='stat-row'>
            <span class='stat-pill'>📊 60% מהמטופלים דואגים מבדיקות לא תקינות</span>
            <span class='stat-pill'>💬 40% לא פונים לרופא</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='card'>
          <div class='section-heading'>מה המערכת עושה</div>
          <ul style='color:#475569; font-size:.92rem; line-height:1.9; padding-right:1.2rem;'>
            <li>מציגה תוצאות בדיקות דם בשפה עברית פשוטה ומובנת</li>
            <li>מסווגת ערכים: תקין / גבולי / חריג — ללא אזעקה מיותרת</li>
            <li>מסבירה <em>מה</em> הבדיקה מודדת ו<em>מדוע</em> ייתכן ערך לא תקין</li>
            <li>מציעה שאלות מוכנות לפגישה עם הרופא</li>
            <li>מפחיתה חרדה סביב ממצאים גבוליים נפוצים</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
          <div class='section-heading'>מדוע זה חשוב בקהילה</div>
          <p style='color:#475569; line-height:1.7; font-size:.92rem;'>
            רפואת קהילה מתמודדת עם פגישות קצרות, מטופלים רבים, וצורך בשיחות יעילות.
            כלי שמכין את המטופל — מגדיל את ערך הפגישה, מפחית פניות מיותרות, ומשפר תוצאות בריאותיות לאורך זמן.
          </p>
          <div class='callout callout-success'>
            ✅ המערכת משתמשת בנתונים מובנים <strong>הקיימים ממילא</strong> בתיק הרפואי האלקטרוני של הקופה — ללא העברת מידע נוסף.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='card'>
          <div class='section-heading'>מה המערכת <u>אינה</u> עושה</div>
          <ul style='color:#475569; font-size:.92rem; line-height:1.9; padding-right:1.2rem;'>
            <li>❌ אינה מאבחנת מחלות</li>
            <li>❌ אינה ממליצה על טיפול תרופתי</li>
            <li>❌ אינה מחליפה את הרופא</li>
            <li>❌ אינה מתאימה לממצאים מורכבים</li>
            <li>❌ אינה פועלת על נתונים אמיתיים (בגרסת ה-PoC)</li>
          </ul>
          <div class='callout callout-warning' style='margin-top:.7rem;'>
            ⚕️ <strong>הרופא נשאר הסמכות הרפואית הסופית בכל מקרה.</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card card-blue' style='margin-top:.5rem;'>
      <div style='display:flex; align-items:center; gap:1.2rem; flex-wrap:wrap;'>
        <div style='font-size:2.5rem;'>🩺</div>
        <div>
          <div style='font-size:1rem; font-weight:700; opacity:.9;'>בדיקות נתמכות ב-PoC זה</div>
          <div style='font-size:.88rem; opacity:.8; margin-top:.3rem;'>
            WBC · המוגלובין · פריטין · HbA1c · LDL · HDL · טריגליצרידים · CRP
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: HOW IT WORKS
# ─────────────────────────────────────────────

elif page == "⚙️ כיצד זה עובד":
    st.markdown("""
    <div class='hero'>
      <div class='tag'>⚙️ ארכיטקטורה</div>
      <h1>כיצד המערכת עובדת</h1>
      <p class='subtitle'>צינור עיבוד מובנה — מתוצאת הבדיקה ועד להכנה לפגישת הרופא</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
      <div class='section-heading'>צינור העיבוד</div>
    """, unsafe_allow_html=True)

    steps = [
        ("🔬", "תוצאות הבדיקה", "מופיעות באפליקציית הקופה"),
        ("📋", "נתונים מובנים", "ערכים מספריים מתיק ה-EHR"),
        ("🤖", "שכבת הסבר AI", "סיווג + הסבר בעברית פשוטה"),
        ("❓", "שאלות לרופא", "המטופל מגיע מוכן לפגישה"),
        ("👨‍⚕️", "הרופא — הסמכות הסופית", "מחליט, מאבחן, מטפל"),
    ]

    cols = st.columns(len(steps))
    for i, (icon, title, sub) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div style='text-align:center; padding:.8rem .5rem;'>
              <div style='font-size:2.2rem; margin-bottom:.4rem;'>{icon}</div>
              <div style='font-size:.88rem; font-weight:700; color:#0a2540; line-height:1.3;'>{title}</div>
              <div style='font-size:.78rem; color:#475569; margin-top:.3rem; line-height:1.4;'>{sub}</div>
              {'<div style="font-size:1.5rem; color:#60a5fa; margin-top:.5rem;">←</div>' if i < len(steps)-1 else ''}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='card'>
          <div class='section-heading'>לוגיקת הסיווג</div>
          <p style='font-size:.9rem; color:#475569; margin-bottom:1rem;'>המערכת משתמשת ב-3 קטגוריות — לא בינארי תקין/לא תקין:</p>
          <div style='display:flex; flex-direction:column; gap:.6rem;'>
            <div style='display:flex; align-items:center; gap:.8rem;'>
              <span class='badge badge-normal'>✅ תקין</span>
              <span style='font-size:.88rem; color:#475569;'>הערך בטווח הרגיל לפי מגדר וגיל</span>
            </div>
            <div style='display:flex; align-items:center; gap:.8rem;'>
              <span class='badge badge-border'>⚠️ גבולי</span>
              <span style='font-size:.88rem; color:#475569;'>מעט מחוץ לטווח — כדאי לעקוב ולדון עם רופא</span>
            </div>
            <div style='display:flex; align-items:center; gap:.8rem;'>
              <span class='badge badge-abnormal'>🔴 חריג</span>
              <span style='font-size:.88rem; color:#475569;'>מחוץ לטווח — נדרשת שיחה עם רופא</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card'>
          <div class='section-heading'>עקרונות שפה בטוחה</div>
          <ul style='font-size:.9rem; color:#475569; line-height:1.9; padding-right:1.2rem;'>
            <li>לא משתמשים במילה "מחלה" או "אבחנה"</li>
            <li>לא אומרים "יש לך סוכרת" או "יש לך אנמיה"</li>
            <li>לא ממליצים על תרופות ספציפיות</li>
            <li>לא משתמשים בשפה מבהילה</li>
            <li>לא מחליפים פגישה עם הרופא</li>
            <li>מעודדים שיחה פתוחה עם הצוות הרפואי</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
      <div class='section-heading'>דוגמת פלט — HbA1c גבולי (5.9%)</div>
      <div class='exp-block border-finding'>
        <div class='exp-label'>סיכום</div>
        <p>רמת ה-HbA1c שלך נמצאת בטווח המעיד על עלייה מסוימת ברמות הסוכר — ממצא הדורש שימת לב ומעקב.</p>
        <div class='exp-label'>מה הבדיקה מודדת</div>
        <p>HbA1c מודד את רמת הסוכר הממוצעת בדם במשך 3 החודשים האחרונים.</p>
        <div class='exp-label'>שאלות מוצעות לרופא</div>
        <ul class='q-list'>
          <li>האם ערך זה השתנה לעומת בדיקות קודמות שלי?</li>
          <li>אילו שינויי תזונה ממולצים?</li>
          <li>האם נדרשת בדיקה מעמיקה יותר?</li>
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: PATIENT DASHBOARD
# ─────────────────────────────────────────────

elif page == "📊 לוח מטופל":
    st.markdown("""
    <div class='hero'>
      <div class='tag'>📊 לוח מטופל</div>
      <h1>תוצאות בדיקות ופרשנות</h1>
      <p class='subtitle'>בחר מטופל מהרשימה — הצג ממצאים, הסברים, ושאלות לרופא</p>
    </div>
    """, unsafe_allow_html=True)

    patient_options = {f"{p['id']}. {p['name']} — {p['scenario']}": p for p in PATIENTS}
    selected_label = st.sidebar.selectbox("בחר מטופל", list(patient_options.keys()))
    patient = patient_options[selected_label]

    # ── Patient header ──
    sex_icon = "♂️" if patient["sex"] == "זכר" else "♀️"
    st.markdown(f"""
    <div class='card'>
      <div style='display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;'>
        <div>
          <div style='font-size:1.5rem; font-weight:800; color:#0a2540;'>{patient['name']}</div>
          <div class='patient-chips' style='margin-top:.6rem;'>
            <span class='patient-chip'>{sex_icon} {patient['sex']}</span>
            <span class='patient-chip'>🎂 גיל {patient['age']}</span>
            <span class='patient-chip'>🏷️ {patient['scenario']}</span>
          </div>
        </div>
        <div style='text-align:left;'>
          <div style='font-size:.78rem; color:#94a3b8; font-weight:600;'>מספר מטופל</div>
          <div style='font-size:1.4rem; font-weight:800; color:#2271b3;'>#{patient['id']:03d}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Lab results table ──
    tab1, tab2 = st.tabs(["📋 תוצאות הבדיקות", "💡 הסברים ושאלות לרופא"])

    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>תוצאות הבדיקה</div>", unsafe_allow_html=True)

        rows = []
        for test, value in patient["labs"].items():
            status, css = classify(test, value)
            badge = f"<span class='badge {css}'>{status}</span>"
            rows.append({
                "בדיקה": TEST_NAMES_HEB.get(test, test),
                "ערך": value,
                "יחידות": REFERENCE[test]["unit"],
                "טווח תקין": NORMAL_RANGE_STR.get(test, "—"),
                "סטטוס": badge,
            })

        table_html = """<table class='lab-table'><thead><tr>
            <th>בדיקה</th><th>ערך</th><th>יחידות</th><th>טווח תקין</th><th>סטטוס</th>
        </tr></thead><tbody>"""
        for r in rows:
            table_html += f"""<tr>
                <td><strong>{r['בדיקה']}</strong></td>
                <td style='font-weight:700; font-size:1rem;'>{r['ערך']}</td>
                <td style='color:#64748b; font-size:.85rem;'>{r['יחידות']}</td>
                <td style='color:#64748b; font-size:.85rem;'>{r['טווח תקין']}</td>
                <td>{r['סטטוס']}</td>
            </tr>"""
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)

        # Summary chips
        statuses = [classify(t, v)[0] for t, v in patient["labs"].items()]
        n_normal = statuses.count("תקין")
        n_border = statuses.count("גבולי")
        n_abnormal = statuses.count("חריג")

        st.markdown(f"""
        <div style='display:flex; gap:.8rem; flex-wrap:wrap; margin-top:1.2rem; padding-top:1rem; border-top:1px solid #e2e8f0;'>
          <span style='font-size:.85rem; color:#475569; font-weight:600;'>סיכום:</span>
          <span class='badge badge-normal'>✅ תקין: {n_normal}</span>
          <span class='badge badge-border'>⚠️ גבולי: {n_border}</span>
          <span class='badge badge-abnormal'>🔴 חריג: {n_abnormal}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        findings = [(t, v, classify(t, v)) for t, v in patient["labs"].items()
                    if classify(t, v)[0] != "תקין"]

        if not findings:
            st.markdown("""
            <div class='card'>
              <div class='callout callout-success'>
                ✅ כל ערכי הבדיקה תקינים. אין ממצאים הדורשים הסבר מיוחד.<br>
                מומלץ להמשיך עם בדיקות מעקב סדירות ולדון עם הרופא בפגישה הבאה.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for test, value, (status, css) in findings:
                exp = get_exp(test, status)
                border_class = "border-finding" if status == "גבולי" else "abnormal-finding"
                test_heb = TEST_NAMES_HEB.get(test, test)

                st.markdown(f"""
                <div class='card'>
                  <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:.8rem;'>
                    <div style='font-size:1.05rem; font-weight:700; color:#0a2540;'>{test_heb}</div>
                    <div style='display:flex; gap:.6rem; align-items:center;'>
                      <span style='font-size:1.1rem; font-weight:800; color:#2271b3;'>{value} {REFERENCE[test]['unit']}</span>
                      <span class='badge {css}'>{status}</span>
                    </div>
                  </div>
                """, unsafe_allow_html=True)

                if exp:
                    st.markdown(f"""
                    <div class='exp-block {border_class}'>
                      <div style='font-size:.95rem; font-weight:600; color:#0a2540; margin-bottom:.6rem;'>
                        📌 {exp['summary']}
                      </div>

                      <div class='exp-label'>מה הבדיקה מודדת</div>
                      <p>{exp['what']}</p>

                      <div class='exp-label'>מדוע ייתכן ערך זה</div>
                      <p>{exp['why']}</p>

                      <div class='exp-label'>מה לשאול את הרופא</div>
                      <ul class='q-list'>
                        {''.join(f"<li>{q}</li>" for q in exp['ask_doc'])}
                      </ul>

                      <div class='exp-label' style='margin-top:.7rem;'>מתי לפנות לעזרה רפואית</div>
                      <p style='color:#92400e; background:#fef3c7; border-radius:6px; padding:.5rem .7rem; font-size:.85rem;'>
                        ⚠️ {exp['attention']}
                      </p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

        # All-normal bonus message
        st.markdown("""
        <div class='callout callout-info'>
          💡 <strong>תזכורת חשובה:</strong> ההסברים שלעיל מיועדים לסייע להבין את הממצאים ולהכין שאלות לרופא.
          הרופא הוא הסמכות הרפואית הסופית ויוכל לפרש את הממצאים בהקשר האישי שלך.
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: WHY NOT CHATGPT
# ─────────────────────────────────────────────

elif page == "🆚 מדוע לא ChatGPT?":
    st.markdown("""
    <div class='hero'>
      <div class='tag'>🆚 השוואה</div>
      <h1>מדוע לא ChatGPT?</h1>
      <p class='subtitle'>השוואה בין מודל שפה ציבורי לבין שכבת הסבר משולבת במערכת HMO</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
      <div class='section-heading'>השוואה: ChatGPT ציבורי vs. MedExplain AI</div>
      <table class='cmp-table'>
        <thead>
          <tr>
            <th style='background:#f8fafc; color:#0a2540;'>היבט</th>
            <th class='th-public'>🤖 צ'אטבוט ציבורי (ChatGPT)</th>
            <th class='th-hmo'>🏥 MedExplain AI — משולב בקופה</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>גישה לנתונים</strong></td>
            <td class='col-public'>המטופל מעתיק נתונים ידנית לממשק ציבורי</td>
            <td class='col-hmo'>נתוני הבדיקה קיימים ממילא בתיק הרפואי האלקטרוני</td>
          </tr>
          <tr>
            <td><strong>פרטיות</strong></td>
            <td class='col-public'>מידע רפואי עלול להישלח לשרתים חיצוניים</td>
            <td class='col-hmo'>הנתונים נשארים בתוך תשתית הקופה</td>
          </tr>
          <tr>
            <td><strong>הקשר קליני</strong></td>
            <td class='col-public'>מודל כללי ללא הקשר היסטוריה רפואית</td>
            <td class='col-hmo'>ניתן לשלב עם היסטוריה רפואית והקשר אישי</td>
          </tr>
          <tr>
            <td><strong>שליטה על הפלט</strong></td>
            <td class='col-public'>הפלט לא מוגבל — עלול לאבחן, להמליץ על תרופות</td>
            <td class='col-hmo'>שפה מוגדרת מראש — ללא אבחנה, ללא המלצת טיפול</td>
          </tr>
          <tr>
            <td><strong>סיכון לחרדה מוגברת</strong></td>
            <td class='col-public'>גבוה — תשובות כלליות עלולות להבהיל</td>
            <td class='col-hmo'>נמוך — שפה מכוונת ומידתית לפי חומרת הממצא</td>
          </tr>
          <tr>
            <td><strong>שילוב רופא</strong></td>
            <td class='col-public'>אין אינטגרציה — המטופל פועל לבד</td>
            <td class='col-hmo'>שאלות לרופא מוכנות — מעודד תקשורת</td>
          </tr>
          <tr>
            <td><strong>רגולציה ואחריות</strong></td>
            <td class='col-public'>אחריות לא ברורה</td>
            <td class='col-hmo'>פועל תחת מסגרת רגולטורית של הקופה</td>
          </tr>
          <tr>
            <td><strong>נגישות שפה</strong></td>
            <td class='col-public'>תלוי ביכולת המטופל לנסח שאלה</td>
            <td class='col-hmo'>הסבר ניתן אוטומטית בעברית ברורה</td>
          </tr>
        </tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='card'>
          <div class='section-heading'>סיכון מרכזי בשימוש ב-ChatGPT ציבורי</div>
          <div class='callout callout-warning'>
            ⚠️ מטופל שמעתיק תוצאות HbA1c גבוהות ל-ChatGPT עלול לקבל תשובה שמרמזת על "סוכרת" — גם כאשר הממצא דורש בדיקה נוספת בלבד. שפה כזו מבהילה ועלולה לגרום לנטישת טיפול.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card'>
          <div class='section-heading'>יתרון מרכזי של שילוב ב-HMO</div>
          <div class='callout callout-success'>
            ✅ המערכת יודעת מראש את ההיסטוריה, תרופות, ובדיקות קודמות של המטופל. ההסבר יכול להיות מדויק יותר ומותאם אישית — תוך שמירה מלאה על פרטיות.
          </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: SAFETY & ETHICS
# ─────────────────────────────────────────────

elif page == "🛡️ בטיחות ואתיקה":
    st.markdown("""
    <div class='hero'>
      <div class='tag'>🛡️ בטיחות ואתיקה</div>
      <h1>עקרונות בטיחות ואתיקה</h1>
      <p class='subtitle'>מסגרת אחראית לשימוש ב-AI בסביבה רפואית</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-heading'>הצהרות יסוד</div>", unsafe_allow_html=True)

        for item in [
            ("📚", "כלי חינוכי בלבד", "המערכת מסבירה ממצאים בשפה פשוטה. אינה מאבחנת, אינה ממליצה על טיפול, ואינה מחליפה שיחה עם רופא."),
            ("🔬", "נתונים סינתטיים", "כל פרטי המטופלים בגרסת ה-PoC הם בדיוניים לחלוטין. לא נעשה שימוש בנתוני מטופלים אמיתיים."),
            ("⚕️", "הרופא — הסמכות הסופית", "כל פרשנות, אבחון, והחלטת טיפול נשארים בידי הצוות הרפואי בלבד."),
            ("🔒", "פרטיות ואבטחה", "מערכת מוטמעת בתשתית HMO — הנתונים לא יוצאים ממערכות הקופה. גישה מוגבלת למורשים בלבד."),
        ]:
            st.markdown(f"""
            <div class='metric-card'>
              <div class='m-title'>{item[0]} {item[1]}</div>
              <div class='m-body'>{item[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-heading'>סיכונים ידועים</div>", unsafe_allow_html=True)

        for item in [
            ("🎭", "הזיות AI (Hallucinations)", "מודלי שפה עלולים לייצר מידע שגוי. ב-PoC זה ההסברים קבועים מראש — אך בגרסה עם LLM חי, נדרש פיקוח וסינון."),
            ("😌", "הרגעת יתר", "הסבר מרגיע מדי על ממצא חריג עלול לגרום למטופל לא לפנות לרופא בזמן."),
            ("⚖️", "הטיות (Bias)", "מערכות AI מאומנות על נתונים שעלולים להכיל הטיות לפי מגדר, גיל, או מוצא."),
            ("♿", "נגישות", "יש לוודא שהממשק נגיש למשתמשים עם מוגבלויות ולאוכלוסיות מגוונות."),
        ]:
            st.markdown(f"""
            <div class='ethics-box'>
              <strong>{item[0]} {item[1]}</strong><br>
              <span style='font-size:.85rem;'>{item[2]}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card' style='margin-top:.5rem;'>
      <div class='section-heading'>מה המערכת לעולם לא תאמר</div>
      <div style='display:flex; flex-wrap:wrap; gap:.6rem; margin-top:.5rem;'>
        <span style='background:#fee2e2; color:#dc2626; border-radius:999px; padding:.3rem .9rem; font-size:.83rem; font-weight:600;'>❌ "יש לך סוכרת"</span>
        <span style='background:#fee2e2; color:#dc2626; border-radius:999px; padding:.3rem .9rem; font-size:.83rem; font-weight:600;'>❌ "אתה זקוק לתרופה"</span>
        <span style='background:#fee2e2; color:#dc2626; border-radius:999px; padding:.3rem .9rem; font-size:.83rem; font-weight:600;'>❌ "הממצא מסוכן"</span>
        <span style='background:#fee2e2; color:#dc2626; border-radius:999px; padding:.3rem .9rem; font-size:.83rem; font-weight:600;'>❌ "אין צורך לראות רופא"</span>
        <span style='background:#fee2e2; color:#dc2626; border-radius:999px; padding:.3rem .9rem; font-size:.83rem; font-weight:600;'>❌ "יש לך אנמיה"</span>
        <span style='background:#fee2e2; color:#dc2626; border-radius:999px; padding:.3rem .9rem; font-size:.83rem; font-weight:600;'>❌ "זה ממאיר"</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: EVALUATION
# ─────────────────────────────────────────────

elif page == "📈 מדדי הערכה":
    st.markdown("""
    <div class='hero'>
      <div class='tag'>📈 הערכה</div>
      <h1>כיצד ניתן להעריך את ה-PoC?</h1>
      <p class='subtitle'>מסגרת הערכה אקדמית למערכת AI רפואית</p>
    </div>
    """, unsafe_allow_html=True)

    metrics = [
        {
            "icon": "🎯",
            "title": "דיוק סיווג ערכי הבדיקה",
            "desc": "האם המערכת מסווגת נכון ערכים תקינים / גבוליים / חריגים?",
            "method": "השוואה ידנית של 10 תרחישים סינתטיים ל-Ground Truth שהוגדר מראש",
            "target": "100% בגרסת הPoC (הסיווג קבוע מראש)",
        },
        {
            "icon": "📖",
            "title": "בהירות ההסברים",
            "desc": "האם ההסברים מובנים למטופל ממוצע?",
            "method": "2–3 משתמשים לא מקצועיים מקראים את ההסברים ומדרגים: בהירות, חרדה שנגרמה, מועילות",
            "target": "ממוצע ≥4/5 בבהירות, חרדה ≤2/5",
        },
        {
            "icon": "🚫",
            "title": "היעדר שפה אבחנתית / טיפולית",
            "desc": "האם שום פלט אינו מכיל אבחנה, המלצת תרופה, או שפה מבהילה?",
            "method": "סריקה ידנית של כל הפלטים, + בדיקת מילות מפתח אסורות",
            "target": "0 הפרות",
        },
        {
            "icon": "⏱️",
            "title": "זמן השלמת זרימת עבודה",
            "desc": "האם מטופל יכול להבין ממצאיו ולהכין שאלות לרופא בפחות מ-3 דקות?",
            "method": "מדידת זמן עם 3 משתמשי ניסיון",
            "target": "≤3 דקות מכניסת הנתונים ועד סיום הקריאה",
        },
        {
            "icon": "🌍",
            "title": "נגישות שפה ו-RTL",
            "desc": "האם הממשק נקרא ונראה נכון בעברית RTL?",
            "method": "בדיקה ב-Chrome, Safari, Firefox, ובמובייל",
            "target": "RTL תקין בכל הדפדפנים, ללא שגיאות עימוד",
        },
    ]

    for m in metrics:
        st.markdown(f"""
        <div class='card'>
          <div style='display:flex; gap:1rem; align-items:flex-start;'>
            <div style='font-size:2rem; flex-shrink:0;'>{m['icon']}</div>
            <div style='flex:1;'>
              <div style='font-size:1rem; font-weight:700; color:#0a2540; margin-bottom:.3rem;'>{m['title']}</div>
              <div style='font-size:.88rem; color:#475569; margin-bottom:.7rem;'>{m['desc']}</div>
              <div style='display:flex; gap:1rem; flex-wrap:wrap;'>
                <div style='flex:1; min-width:200px; background:#f0f9ff; border-radius:8px; padding:.6rem .9rem;'>
                  <div style='font-size:.75rem; font-weight:700; color:#0369a1; margin-bottom:.2rem;'>🔬 שיטת הערכה</div>
                  <div style='font-size:.85rem; color:#0c4a6e;'>{m['method']}</div>
                </div>
                <div style='flex:1; min-width:200px; background:#f0fdf4; border-radius:8px; padding:.6rem .9rem;'>
                  <div style='font-size:.75rem; font-weight:700; color:#15803d; margin-bottom:.2rem;'>🎯 יעד</div>
                  <div style='font-size:.85rem; color:#14532d;'>{m['target']}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='callout callout-info'>
      💡 <strong>הערה אקדמית:</strong> גרסת ה-PoC הזו משתמשת בהסברים קבועים (rule-based) ולא ב-LLM חי.
      הערכה של גרסת LLM תדרוש גם: בדיקת עקביות בין הפעלות, bוניית test-set גדול יותר, ופאנל מומחים רפואיים.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class='footnote'>
  MedExplain AI · Proof of Concept · Medical AI Course · כל הנתונים סינתטיים · אינו כלי אבחוני
</div>
""", unsafe_allow_html=True)
