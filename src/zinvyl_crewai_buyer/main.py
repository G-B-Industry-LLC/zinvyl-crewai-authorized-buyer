from __future__ import annotations

import json
import os
from dataclasses import asdict

from .authority import authority_from_environment, validate_purchase_authority
from .crew import ZinvylAuthorizedBuyerCrew, ZinvylPreviewCrew


CAMPAIGN_URL = "https://zinvyl.com/marketplace/campaigns/authorized-buyer-agent.json?source=partner_operator"
def preview() -> None:
    """Safely match one sanitized need without enabling any purchase tool."""
    summary = os.getenv(
        "ZINVYL_TASK_SUMMARY",
        "Assess one sanitized repeatable workflow timeout and return the smallest evidence-backed next action.",
    ).strip()
    ZinvylPreviewCrew().crew().kickoff(inputs={"task_summary": summary, "campaign_url": CAMPAIGN_URL})


def buy() -> None:
    """Invoke the bounded buyer crew only after all authority assertions pass locally."""
    authority = authority_from_environment()
    validate_purchase_authority(authority)
    inputs = asdict(authority)
    inputs["allowed_offer_ids"] = json.dumps(authority.allowed_offer_ids)
    inputs["campaign_url"] = CAMPAIGN_URL
    ZinvylAuthorizedBuyerCrew().crew().kickoff(inputs=inputs)


def run() -> None:
    """Default to read-only preview; purchasing requires an explicit command and complete authority."""
    preview()


if __name__ == "__main__":
    run()

