# Jan Sahayak

**An AI-assisted citizen rights and welfare navigator (educational prototype).**

Many citizens miss out on government benefits simply because they don't know which schemes they qualify for, what documents to carry, or how to file an RTI or complaint. Jan Sahayak solves this in one simple, bilingual (Hindi + English) web app.

## Features
- **Scheme eligibility checker:** enter basic details (age, occupation, income, gender) and get the list of central government schemes you are eligible for.
- **Document checklist:** for every matched scheme, see exactly which documents are required.
- **RTI and complaint drafts:** generate a ready-to-use RTI application or complaint letter in English or Hindi.
- **Privacy first:** user details are not stored anywhere.

## Schemes Covered
PM-KISAN, Ayushman Bharat, PMFBY, Ujjwala, Mudra, PMAY, Sukanya Samriddhi, e-Shram, PM Matru Vandana, NSP Scholarship.

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Data:** JSON data packs (`data/schemes/`)
- **Eligibility logic:** rule-based engine (`rules.py`) with tests (`test_rules.py`)

## How to Run Locally
Prerequisite: Python 3 installed.

1. Extract the zip (do not run from inside the zip).
2. Windows: double-click `START.bat` | Mac/Linux: run `./start.sh`
3. Open http://127.0.0.1:5000 in your browser.

## Deploy (Render)
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

## Disclaimer
Educational prototype. Scheme details may change, so verify on official government portals before applying.

## Author
**Ansh Singh** | BTech CE&A, VGU x IST
