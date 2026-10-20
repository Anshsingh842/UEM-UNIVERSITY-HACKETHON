"""Jan Sahayak - Flask backend.

Privacy: koi bhi user detail file, database, session ya cookie mein save nahi hoti.
Sab kuch sirf request ke dauran memory mein rehta hai aur jawab ke baad khatam.
"""
import json
import logging
from datetime import date
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from rules import check_eligibility

app = Flask(__name__)

# Werkzeug ke log mein sirf "POST /check" jaisi line aati hai, body nahi.
# Phir bhi extra suraksha ke liye request logs band kar diye.
logging.getLogger("werkzeug").setLevel(logging.ERROR)

SCHEMES_DIR = Path(__file__).parent / "data" / "schemes"
UNSURE_PREFIX = "Pakka nahi keh sakte"


def load_schemes():
    """Sirf padhta hai (read-only). Startup par ek baar."""
    schemes = []
    for path in sorted(SCHEMES_DIR.glob("*.json")):
        schemes.append(json.loads(path.read_text(encoding="utf-8")))
    return schemes


SCHEMES = load_schemes()


@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store"
    return response


def error(message, status=400):
    return jsonify({"error": message}), status


def clean_text(value):
    return value.strip() if isinstance(value, str) else ""


# ---------------------------------------------------------------- /check
def parse_check_input(data):
    """(user_dict, error_message) wapas deta hai."""
    age, income = data.get("age"), data.get("income")
    if isinstance(age, bool) or not isinstance(age, int) or not 0 <= age <= 120:
        return None, "'age' 0 se 120 ke beech ka poora number hona chahiye"
    if isinstance(income, bool) or not isinstance(income, (int, float)) or income < 0:
        return None, "'income' saalana aay (₹) ka number hona chahiye"
    occupation = clean_text(data.get("occupation"))
    gender = clean_text(data.get("gender")).lower()
    state = clean_text(data.get("state"))
    if not occupation:
        return None, "'occupation' likhna zaroori hai"
    if gender not in ("male", "female", "other"):
        return None, "'gender' sirf 'male', 'female' ya 'other' ho sakta hai"
    if not state:
        return None, "'state' likhna zaroori hai"
    return {"age": age, "income": income, "occupation": occupation,
            "gender": gender, "state": state}, None


@app.post("/check")
def check():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error("JSON body bhejo")
    user, problem = parse_check_input(data)
    if problem:
        return error(problem)

    matching, unsure = [], []
    for scheme in SCHEMES:
        ok, reason = check_eligibility(user, scheme)
        item = {
            "name": scheme["name"],
            "benefit_amount": scheme["benefit_amount"],
            "documents": scheme["documents"],
            "official_url": scheme["official_url"],
            "last_verified": scheme["last_verified"],
        }
        if ok:
            item["reason"] = reason
            matching.append(item)
        elif reason.startswith(UNSURE_PREFIX):
            item["reason"] = reason
            unsure.append(item)

    return jsonify({
        "matching": matching,
        "pakka_nahi_verify_karo": unsure,
        "note": "Yojanaon ki shartein state ke hisaab se alag ho sakti hain; "
                "'state' abhi matching mein use nahi hoti. Apply karne se pehle official site dekho.",
    })


# ---------------------------------------------------------------- /draft
RTI_EN = """To,
The Public Information Officer (PIO),
{office}
{state}

Date: {date}

Subject: Application under Section 6(1) of the Right to Information Act, 2005 - {subject}

Sir/Madam,

I, {name}, resident of {address}, request the following information under the Right to Information Act, 2005:

{details}

I am enclosing the application fee as per the rules (fee may differ by state - please verify). If the information concerns another department, kindly transfer this application to the correct authority under Section 6(3) of the Act.

I would like to receive the information by post at the above address.

Yours faithfully,
{name}
{address}
"""

COMPLAINT_EN = """To,
The Officer In-Charge,
{office}
{state}

Date: {date}

Subject: Complaint regarding {subject}

Sir/Madam,

I, {name}, resident of {address}, wish to bring the following matter to your notice:

{details}

I request you to kindly look into this matter, take necessary action at the earliest, and inform me in writing about the action taken.

Thanking you,
Yours faithfully,
{name}
{address}
"""

RTI_HI = """सेवा में,
जन सूचना अधिकारी (PIO),
{office}
{state}

दिनांक: {date}

विषय: सूचना का अधिकार अधिनियम, 2005 की धारा 6(1) के अंतर्गत आवेदन - {subject}

महोदय/महोदया,

मैं, {name}, निवासी {address}, सूचना का अधिकार अधिनियम, 2005 के अंतर्गत निम्नलिखित जानकारी चाहता/चाहती हूँ:

{details}

मैं नियमानुसार आवेदन शुल्क संलग्न कर रहा/रही हूँ (शुल्क राज्य के अनुसार अलग हो सकता है - कृपया जाँच लें)। यदि यह जानकारी किसी अन्य विभाग से संबंधित है, तो कृपया धारा 6(3) के अंतर्गत आवेदन संबंधित विभाग को भेज दें।

कृपया जानकारी उपरोक्त पते पर डाक द्वारा भेजें।

भवदीय,
{name}
{address}
"""

COMPLAINT_HI = """सेवा में,
प्रभारी अधिकारी,
{office}
{state}

दिनांक: {date}

विषय: {subject} के संबंध में शिकायत

महोदय/महोदया,

मैं, {name}, निवासी {address}, निम्नलिखित विषय आपके संज्ञान में लाना चाहता/चाहती हूँ:

{details}

कृपया इस मामले की जाँच कर शीघ्र उचित कार्रवाई करें और की गई कार्रवाई की सूचना मुझे लिखित में दें।

धन्यवाद,
भवदीय,
{name}
{address}
"""

TEMPLATES = {
    ("rti", "en"): RTI_EN, ("complaint", "en"): COMPLAINT_EN,
    ("rti", "hi"): RTI_HI, ("complaint", "hi"): COMPLAINT_HI,
}


@app.post("/draft")
def draft():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error("JSON body bhejo")

    kind = clean_text(data.get("type")).lower()
    lang = clean_text(data.get("language")).lower() or "en"
    if (kind, lang) not in TEMPLATES:
        return error("'type' 'rti' ya 'complaint' ho; 'language' 'en' ya 'hi' ho")

    fields = {k: clean_text(data.get(k)) for k in
              ("name", "address", "state", "office", "subject", "details")}
    missing = [k for k, v in fields.items() if not v]
    if missing:
        return error("Ye fields zaroori hain: " + ", ".join(missing))

    fields["date"] = clean_text(data.get("date")) or date.today().strftime("%d-%m-%Y")
    return jsonify({"type": kind, "language": lang,
                    "letter": TEMPLATES[(kind, lang)].format(**fields)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
