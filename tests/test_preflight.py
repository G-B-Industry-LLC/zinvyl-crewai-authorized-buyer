import unittest

from zinvyl_crewai_buyer.authority import PurchaseAuthority, validate_purchase_authority


def valid_authority(**overrides):
    values = {
        "organization": "Example Buyer LLC",
        "contact_email": "buyer@example.com",
        "request_id": "example-request-001",
        "task_summary": "Assess one sanitized repeatable webhook timeout and report the smallest next action.",
        "allowed_offer_ids": ("zinvyl.api.failure-triage.v1",),
        "maximum_amount_minor": 4900,
        "currency": "usd",
        "terms_version": "current-exact-version",
        "delegated_authority_confirmed": True,
        "terms_accepted": True,
        "safe_scope_confirmed": True,
    }
    values.update(overrides)
    return PurchaseAuthority(**values)


class PurchasePreflightTests(unittest.TestCase):
    def test_complete_exact_delegation_passes(self):
        validate_purchase_authority(valid_authority())

    def test_missing_authority_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "delegated purchase authority"):
            validate_purchase_authority(valid_authority(delegated_authority_confirmed=False))

    def test_insufficient_ceiling_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "delegated ceiling"):
            validate_purchase_authority(valid_authority(maximum_amount_minor=4899))

    def test_offer_outside_allowlist_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "offer allowlist"):
            validate_purchase_authority(valid_authority(allowed_offer_ids=("zinvyl.api.workflow-failure-rescue.v1",)))

    def test_missing_current_terms_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "exact current terms version"):
            validate_purchase_authority(valid_authority(terms_version=""))


if __name__ == "__main__":
    unittest.main()

