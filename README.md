# 🕵️‍♂️ ClaimAudit

**Automated Medical Chart Auditor for Denial Prevention.**

ClaimAudit is an AI agent that scans batches of clinical SOAP notes to identify missing information (denial risks) that would cause insurance companies to reject claims. 

## 🚀 Live Demo
*(Add Streamlit link here once deployed)*

## 💡 The Problem
Clinics lose massive revenue because doctors write incomplete notes. If a note says "patient has a cough" but doesn't say "for how long," the insurance claim is denied. Billers currently have to manually read hundreds of pages to find these errors. ClaimAudit automates this QA process.

## ✨ Features
*   **Batch Processing:** Paste dozens of notes at once (separated by `---`).
*   **Denial Risk Detection:** Scans for missing durations, missing dosages, and mismatched assessments.
*   **Actionable Fixes:** Tells the biller exactly what to ask the doctor to fix.

## 🧠 Tech Stack
*   **Python**
*   **Streamlit** (Frontend)
*   **Groq API** (Llama-3 120B model)
*   Deployed for free on Streamlit Community Cloud.

## 👨‍💻 Author
**Aizaz Ahmad** — AI Developer & Agentic SaaS Product Designer
*   [GitHub](https://github.com/aizaz-ahmad-ims)