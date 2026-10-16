# Zinvyl Authorized Buyer Agent for CrewAI

A marketplace-ready CrewAI template that gives an operator a safe path from one sanitized workflow problem to one fixed-price Zinvyl purchase.

The template solves a narrow procurement problem: a CrewAI operator can inspect the current Zinvyl offer and purchase requirements, then invoke `buy_matching_service` only when the principal already supplied an exact offer allowlist, a sufficient USD ceiling, current terms acceptance, a safe bounded scope, and an authorized business contact.

## Why this is useful

- Connects to the public Zinvyl Streamable HTTP MCP server.
- Defaults to a read-only preview with no purchase-capable tool.
- Exposes a separate purchase command only after a deterministic local authority preflight.
- Restricts the initial campaign to the **$49 Workflow Health Check** (`zinvyl.api.failure-triage.v1`).
- Never treats a tool call, intent, checkout, or payment route as funded work.
- Requires Stripe-verified ledger funding before fulfillment can begin.

## Public endpoints

- MCP server: `https://zinvyl.com/marketplace/agent-mcp`
- CrewAI install packet: `https://zinvyl.com/marketplace/operator-activation-packet.json?target=crewai`
- Authorized-buyer campaign: `https://zinvyl.com/marketplace/campaigns/authorized-buyer-agent.json?source=partner_operator`
- Terms: `https://zinvyl.com/marketplace/terms`
- Privacy: `https://zinvyl.com/marketplace/privacy`
- Security: `https://zinvyl.com/marketplace/security`

## Install

Python 3.10-3.13 and an operator-selected CrewAI-supported LLM are required. Zinvyl does not require the operator to use OpenAI.

```bash
git clone https://github.com/G-B-Industry-LLC/zinvyl-crewai-authorized-buyer.git
cd zinvyl-crewai-authorized-buyer
python -m venv .venv
pip install -e .
```

Configure the LLM required by your CrewAI runtime according to the official CrewAI documentation. Do not place any LLM key, buyer credential, payment data, or customer file in this repository.

## Safe preview

The default command cannot access `buy_matching_service` or `buy_service`:

```bash
set ZINVYL_TASK_SUMMARY=Assess one sanitized repeatable webhook timeout and return the smallest next action.
zinvyl_preview
```

The preview returns the closest offer, exact price, current terms version, acceptance boundary, and missing authority fields.

## Authorized purchase

The buyer principal—not this template—must supply every value below. Retrieve the current terms version through the read-only preview or `get_purchase_requirements`; never pre-accept a future version.

```bash
set ZINVYL_BUYER_ORGANIZATION=Example Buyer LLC
set ZINVYL_BUYER_CONTACT_EMAIL=buyer@example.com
set ZINVYL_BUYER_REQUEST_ID=example-request-001
set ZINVYL_TASK_SUMMARY=Assess one sanitized repeatable webhook timeout and return the smallest next action.
set ZINVYL_OFFER_ALLOWLIST=zinvyl.api.failure-triage.v1
set ZINVYL_MAXIMUM_AMOUNT_MINOR=4900
set ZINVYL_CURRENCY=usd
set ZINVYL_TERMS_VERSION=REPLACE_WITH_CURRENT_EXACT_VERSION
set ZINVYL_DELEGATED_AUTHORITY_CONFIRMED=true
set ZINVYL_TERMS_ACCEPTED=true
set ZINVYL_SAFE_SCOPE_CONFIRMED=true
zinvyl_buy
```

The purchase command:

1. Fails locally if any authority field is absent or insufficient.
2. Re-reads the live price and terms before purchase.
3. Stops on any mismatch.
4. Calls `buy_matching_service` once only when the exact delegation remains valid.
5. Returns a Stripe machine-payment or hosted-checkout route as **unfunded**.
6. Waits for Zinvyl’s authoritative ledger before work can begin.

## What not to send

Never send credentials, tokens, private keys, payment-card data, personal data, confidential files, production secrets, or unredacted regulated data. The initial offer accepts one sanitized trace for one endpoint or workflow step.

## Test

The preflight tests require no LLM, payment, or network call:

```bash
python -m unittest discover -s tests -v
```

The live MCP connection has separately been verified to expose ten Zinvyl tools in CrewAI. A connection is not a buyer, a purchase, or revenue.

## Seller and support

Seller of record: **G.B. Industry LLC d/b/a Zinvyl**  
Support: `gabriel@zinvyl.com`  
Canonical marketplace: `https://zinvyl.com/marketplace/`

