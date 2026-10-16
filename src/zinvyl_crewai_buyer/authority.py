from __future__ import annotations

import os
import re
from dataclasses import dataclass


AUTHORIZED_OFFER = "zinvyl.api.failure-triage.v1"
AUTHORIZED_AMOUNT_MINOR = 4900


@dataclass(frozen=True)
class PurchaseAuthority:
    organization: str
    contact_email: str
    request_id: str
    task_summary: str
    allowed_offer_ids: tuple[str, ...]
    maximum_amount_minor: int
    currency: str
    terms_version: str
    delegated_authority_confirmed: bool
    terms_accepted: bool
    safe_scope_confirmed: bool


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() == "true"


def authority_from_environment() -> PurchaseAuthority:
    offers = tuple(item.strip() for item in os.getenv("ZINVYL_OFFER_ALLOWLIST", "").split(",") if item.strip())
    try:
        maximum = int(os.getenv("ZINVYL_MAXIMUM_AMOUNT_MINOR", "0"))
    except ValueError as error:
        raise ValueError("ZINVYL_MAXIMUM_AMOUNT_MINOR must be an integer in USD cents.") from error

    return PurchaseAuthority(
        organization=os.getenv("ZINVYL_BUYER_ORGANIZATION", "").strip(),
        contact_email=os.getenv("ZINVYL_BUYER_CONTACT_EMAIL", "").strip(),
        request_id=os.getenv("ZINVYL_BUYER_REQUEST_ID", "").strip(),
        task_summary=os.getenv("ZINVYL_TASK_SUMMARY", "").strip(),
        allowed_offer_ids=offers,
        maximum_amount_minor=maximum,
        currency=os.getenv("ZINVYL_CURRENCY", "").strip().lower(),
        terms_version=os.getenv("ZINVYL_TERMS_VERSION", "").strip(),
        delegated_authority_confirmed=_truthy(os.getenv("ZINVYL_DELEGATED_AUTHORITY_CONFIRMED")),
        terms_accepted=_truthy(os.getenv("ZINVYL_TERMS_ACCEPTED")),
        safe_scope_confirmed=_truthy(os.getenv("ZINVYL_SAFE_SCOPE_CONFIRMED")),
    )


def validate_purchase_authority(authority: PurchaseAuthority) -> None:
    errors: list[str] = []
    if not authority.organization:
        errors.append("buying organization is missing")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", authority.contact_email):
        errors.append("authorized business contact email is missing or invalid")
    if not re.fullmatch(r"[A-Za-z0-9._:-]{8,128}", authority.request_id):
        errors.append("buyer request ID must be 8-128 safe idempotency characters")
    if not 20 <= len(authority.task_summary) <= 4000:
        errors.append("task summary must contain 20-4000 sanitized characters")
    if AUTHORIZED_OFFER not in authority.allowed_offer_ids:
        errors.append(f"offer allowlist must include {AUTHORIZED_OFFER}")
    if authority.maximum_amount_minor < AUTHORIZED_AMOUNT_MINOR:
        errors.append("delegated ceiling must cover 4900 USD minor units")
    if authority.currency != "usd":
        errors.append("currency must be usd")
    if not authority.terms_version:
        errors.append("the exact current terms version is required")
    if not authority.delegated_authority_confirmed:
        errors.append("delegated purchase authority must be explicitly confirmed")
    if not authority.terms_accepted:
        errors.append("current terms must be explicitly accepted")
    if not authority.safe_scope_confirmed:
        errors.append("sanitized bounded scope must be explicitly confirmed")
    if errors:
        raise ValueError("Purchase is disabled: " + "; ".join(errors) + ".")

