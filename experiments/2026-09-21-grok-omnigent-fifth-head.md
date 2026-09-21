# Experiment EX-001 — Grok as an OmniGent Fifth Head

**Approval date:** September 21, 2026

**Decision date:** October 20, 2026

**Status:** Approved; setup pending

| Field | Entry |
|---|---|
| Experiment name | Grok Build as an incremental fifth OmniGent head |
| Evidence ID | E-003 |
| Milestone | 1 — Benchmark the OmniGent workflow |
| Question | Does adding Grok Build to the established Claude/GPT/Pi/Qwen workflow produce a measurable, repeatable improvement that justifies a $30 monthly subscription? |
| Baseline | The verified four-head `debby-quad` smoke test and the preregistered 20-prompt four-head benchmark |
| Comparator | The same sanitized prompts, context, scoring rubric, and reviewer process run first with four heads and then with Grok added as a fifth head |
| Deliverable | Sanitized setup record, smoke-test result, comparative score table, cost and latency summary, observed Grok contributions, failure modes, and keep/revise/cancel decision |
| Spending cap | $30 for the initial SuperGrok month; no separate metered xAI API spend is authorized |
| Time box | Complete the decision by October 20, 2026, before authorizing another month |
| Exact model/version | Record the account-selected Grok model reported by the CLI at execution time; do not assume a changing default |
| Data classification | Public benchmark inputs only; private credentials and billing evidence remain private |
| Robert's approval | Approved by Robert Woods on September 21, 2026 through the reported $30 purchase and direction to document it |

## Sequence and controls

1. Preserve and execute the existing four-head benchmark without modifying its preregistered protocol.
2. Install the official Grok CLI inside the same WSL environment used by OmniGent.
3. Authenticate with xAI's device-login flow; never commit session tokens, API keys, receipts, or account identifiers.
4. Run a standalone Grok smoke test, followed by an OmniGent `grok` harness smoke test.
5. Record the exact model, configuration revision, completion status, latency, and any separately metered cost.
6. Repeat the same 20 sanitized prompts with Grok added as a fifth head.
7. Blind-score results before revealing which configuration produced them.

## Hard gates — all required

| Measure | Threshold |
|---|---:|
| Successful completion | At least 19 of 20 five-head prompts |
| Critical-control coverage in final synthesis | 100% |
| Critical unsafe contradictions in final synthesis | 0 |
| Credential or private-data exposure | 0 incidents |
| Unapproved xAI API spend | $0 |
| Purchase reconciliation | $30 subscription reconciled privately within seven days of the first public monthly report |

## Value gates — at least one required

1. **Quality:** blinded composite quality improves by at least 5% relative and 0.15 points absolute over the four-head result.
2. **Unique contribution:** Grok supplies an independently verified, material correction or missing control on at least 4 of 20 prompts that survives final synthesis.
3. **Safety:** weighted critical/high control omission falls by at least 15% relative to the four-head result without introducing a critical contradiction.

Latency, total cost per prompt, and reviewer preference are reported even when they do not determine the gate result. The subscription is not described as cost-effective until the comparative run is complete.

## Decision rule

- **Keep:** all hard gates and at least one value gate pass, and the incremental benefit is worth $30/month to Robert.
- **Revise:** setup works but the comparison is inconclusive; document one bounded follow-up without increasing the approved spend.
- **Cancel:** any safety or spending hard gate fails, the integration is unreliable, or the measured benefit does not justify renewal.

## Closeout

| Field | Result |
|---|---|
| Actual cost | Pending; initial purchase reported as $30 |
| Actual duration | Pending |
| Result against hard and value gates | Pending |
| Evidence links | Pending |
| Failure modes | Pending |
| Lesson learned | Pending |
| Decision | Pending — Keep / Revise / Cancel |
