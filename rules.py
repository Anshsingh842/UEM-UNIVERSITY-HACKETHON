"""Jan Sahayak - eligibility rules.

user = {"age": int, "occupation": str, "income": int (saalana, ₹), "gender": "male"/"female"/"other"}
scheme = ek JSON file ka dict (data/schemes/ se).

Scheme mein:
  None         -> is cheez ki koi shart nahi
  "verify karo" -> shart pakka nahi pata, isliye True nahi diya jayega
"""

UNSURE = "verify karo"


def check_eligibility(user, scheme):
    """(True/False, wajah) wapas deta hai."""
    rules = scheme["eligibility"]
    fails = []    # pakka nahi milegi
    unsure = []   # pakka nahi pata

    def get(field):
        value = user.get(field)
        if value is None:
            unsure.append(f"user ka '{field}' nahi diya")
        return value

    # Age
    age_needed = rules["min_age"] is not None or rules["max_age"] is not None
    if age_needed:
        age = get("age")
        for key, label in (("min_age", "kam se kam"), ("max_age", "zyada se zyada")):
            limit = rules[key]
            if limit is None or age is None:
                continue
            if limit == UNSURE:
                unsure.append(f"{key} {UNSURE}")
            elif key == "min_age" and age < limit:
                fails.append(f"umar {age} hai, {label} {limit} chahiye")
            elif key == "max_age" and age > limit:
                fails.append(f"umar {age} hai, {label} {limit} chahiye")

    # Occupation
    occ_rule = rules["occupation"]
    if occ_rule == UNSURE:
        unsure.append(f"occupation {UNSURE}")
    elif occ_rule is not None:
        occ = get("occupation")
        if occ is not None and occ.strip().lower() not in [o.lower() for o in occ_rule]:
            fails.append(f"kaam '{occ}' hai, chahiye: {', '.join(occ_rule)}")

    # Income
    inc_rule = rules["max_income"]
    if inc_rule == UNSURE:
        unsure.append(f"max_income {UNSURE}")
    elif inc_rule is not None:
        income = get("income")
        if income is not None and income > inc_rule:
            fails.append(f"aay ₹{income} hai, zyada se zyada ₹{inc_rule} chahiye")

    # Gender
    gen_rule = rules["gender"]
    if gen_rule == UNSURE:
        unsure.append(f"gender {UNSURE}")
    elif gen_rule is not None:
        gender = get("gender")
        if gender is not None and gender.strip().lower() != gen_rule.lower():
            fails.append(f"ye yojana sirf '{gen_rule}' ke liye hai")

    if fails:
        return False, "Nahi milegi: " + "; ".join(fails)
    if unsure:
        return False, "Pakka nahi keh sakte: " + "; ".join(unsure) + f". Official site dekho: {scheme['official_url']}"
    return True, "Sab shartein poori hain (documents aur latest rules official site par verify karo)."
