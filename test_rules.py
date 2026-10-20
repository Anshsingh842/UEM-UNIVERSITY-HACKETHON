import json
import unittest
from pathlib import Path

from rules import check_eligibility

SCHEMES = Path(__file__).parent / "data" / "schemes"


def load(name):
    return json.loads((SCHEMES / f"{name}.json").read_text(encoding="utf-8"))


class TestRules(unittest.TestCase):
    def test_farmer_gets_pm_kisan(self):
        user = {"age": 40, "occupation": "Farmer", "income": 100000, "gender": "male"}
        ok, why = check_eligibility(user, load("pm_kisan"))
        self.assertTrue(ok, why)

    def test_male_not_eligible_for_ujjwala(self):
        user = {"age": 30, "occupation": "farmer", "income": 50000, "gender": "male"}
        ok, why = check_eligibility(user, load("ujjwala"))
        self.assertFalse(ok)
        self.assertIn("female", why)

    def test_too_old_for_e_shram(self):
        user = {"age": 62, "occupation": "unorganised worker", "income": 80000, "gender": "male"}
        ok, why = check_eligibility(user, load("e_shram"))
        self.assertFalse(ok)
        self.assertIn("umar", why)

    def test_income_limit(self):
        scheme = {"name": "Test", "official_url": "x",
                  "eligibility": {"min_age": None, "max_age": None, "occupation": None,
                                  "max_income": 300000, "gender": None}}
        user = {"age": 30, "occupation": "driver", "income": 500000, "gender": "male"}
        ok, why = check_eligibility(user, scheme)
        self.assertFalse(ok)
        self.assertIn("aay", why)

    def test_unsure_rule_is_not_true(self):
        user = {"age": 30, "occupation": "farmer", "income": 100000, "gender": "male"}
        ok, why = check_eligibility(user, load("pmay"))
        self.assertFalse(ok)
        self.assertIn("verify karo", why)


if __name__ == "__main__":
    unittest.main()
