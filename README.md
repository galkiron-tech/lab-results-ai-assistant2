# 🏥 MedExplain AI — הסבר תוצאות בדיקות דם בעברית פשוטה

## Medical AI Course — Proof of Concept

**MedExplain AI** is an academic proof-of-concept demonstrating how an AI explanation layer, integrated directly into an HMO app, can help patients understand their blood test results in plain Hebrew — reducing anxiety, improving health literacy, and generating better physician questions.

> ⚠️ This system is **not a diagnostic tool**. It is an educational explanation layer. All data is synthetic. No real patient data is used.

---

## What This PoC Demonstrates

- Structured lab result interpretation with 3-tier classification (תקין / גבולי / חריג)
- Safe, non-alarming Hebrew explanations for 10 realistic patient scenarios
- Physician-question generation per abnormal/borderline finding
- Comparison with public AI chatbots (privacy, safety, clinical context)
- Evaluation framework for real-world deployment
- Full RTL Hebrew interface built in Streamlit

---

## Supported Lab Tests

| Test | Description |
|------|-------------|
| WBC | White Blood Cell Count |
| Hemoglobin | Red blood cell oxygen carrier |
| Ferritin | Iron storage protein |
| HbA1c | 3-month blood sugar average |
| LDL | "Bad" cholesterol |
| HDL | "Good" cholesterol |
| Triglycerides | Blood fat level |
| CRP | C-Reactive Protein (inflammation) |

---

## Installation & Running

```bash
# Clone or download the project
cd medical_ai_poc

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Deploy to Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the entry point
4. Deploy — no configuration needed

---

## Project Structure

```
medical_ai_poc/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## Academic Context

This PoC was created as part of a **Medical AI course** to demonstrate responsible AI integration in healthcare settings. It illustrates key principles:

- **AI as augmentation, not replacement** of physician judgment
- **Privacy-preserving design** using structured, already-available HMO data
- **Safe language boundaries** preventing diagnostic or treatment language
- **Evaluation framework** for responsible deployment

---

## Ethical Statement

All patient data in this application is entirely synthetic. No real medical records, names, or health information are used. The explanations generated are pre-authored educational content, not outputs from a live language model. This is a demonstration of what such a system could look like, not a production system.

---

*Built with Streamlit · Python · No external APIs · No database · Fully local*
