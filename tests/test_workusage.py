import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from WorkUsage import normalize


class NormalizeTests(unittest.TestCase):
    def test_rate_limit_payload(self):
        payload = {
            "result": {
                "ordinaryUsageAllowed": True,
                "rateLimits": {
                    "planType": "plus",
                    "rateLimitReachedType": None,
                    "primary": {
                        "usedPercent": 28,
                        "windowDurationMins": 300,
                        "resetsAt": 2000000000,
                    },
                    "secondary": {
                        "usedPercent": 20,
                        "windowDurationMins": 10080,
                        "resetsAt": 2000600000,
                    },
                },
                "rateLimitResetCredits": {"availableCount": 2},
            }
        }

        usage = normalize(payload)

        self.assertEqual(usage["five_hour"]["left_percent"], 72)
        self.assertEqual(usage["weekly"]["left_percent"], 80)
        self.assertEqual(usage["reset_credits_available"], 2)
        self.assertEqual(usage["plan_type"], "plus")
        self.assertTrue(usage["ordinary_usage_allowed"])
        self.assertFalse(usage["luna_available"])
        self.assertIsNone(usage["luna_reserve_weekly"])

    def test_rate_limits_by_id_with_luna_reserve(self):
        payload = {
            "result": {
                "ordinaryUsageAllowed": False,
                "rateLimitsByLimitId": {
                    "codex": {
                        "planType": "plus",
                        "rateLimitReachedType": "primary",
                        "primary": {
                            "usedPercent": 100,
                            "windowDurationMins": 300,
                            "resetsAt": 2000000000,
                        },
                        "secondary": {
                            "usedPercent": 35,
                            "windowDurationMins": 10080,
                            "resetsAt": 2000600000,
                        },
                    },
                    "base_model_inference": {
                        "limitName": "Luna Reserve",
                        "normalModelSlug": "luna",
                        "primary": {
                            "usedPercent": 25,
                            "windowDurationMins": 10080,
                            "resetsAt": 2001200000,
                        },
                    },
                },
                "rateLimitResetCredits": {"availableCount": 1},
            }
        }

        usage = normalize(payload)

        self.assertEqual(usage["five_hour"]["left_percent"], 0)
        self.assertEqual(usage["weekly"]["left_percent"], 65)
        self.assertEqual(usage["luna_reserve_weekly"]["left_percent"], 75)
        self.assertEqual(usage["luna_reserve_weekly"]["window_minutes"], 10080)
        self.assertTrue(usage["luna_available"])
        self.assertEqual(usage["luna_limit_name"], "Luna Reserve")
        self.assertEqual(usage["luna_model"], "luna")
        self.assertEqual(usage["reset_credits_available"], 1)
        self.assertEqual(usage["rate_limit_reached_type"], "primary")


if __name__ == "__main__":
    unittest.main()
