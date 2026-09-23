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


if __name__ == "__main__":
    unittest.main()
