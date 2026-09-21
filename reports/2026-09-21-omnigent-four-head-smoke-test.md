# OmniGent Four-Head Smoke Test

**Date:** September 21, 2026  
**Outcome:** **PASS — Claude, GPT, Pi, and Qwen all completed and were included in the final synthesis.**

## Conditions

| Field | Value |
|---|---|
| OmniGent version | 0.14.0 (`fc89a3ba`) |
| End-to-end elapsed time | 1 minute 42 seconds |
| Session-record active interval | 79 seconds |
| Completion | 4 of 4 heads |
| Recorded session errors | None |
| Exported internal evidence | 40 conversation items plus session metadata |

## Prompt

> A mid-sized enterprise is piloting an AI assistant that can read internal documentation but cannot take external actions. Identify the three most important controls for a 30-day pilot. For each control, provide one measurable success criterion. Keep the answer under 180 words.

The prompt contained no personal, employer, customer, or proprietary information.

## Results

### Claude

- Permission-mirrored retrieval and ACL trimming.
- Complete prompt, response, and retrieval logging.
- Grounded answers with verifiable citations.

### GPT

- Least-privilege document access.
- Source traceability and uncertainty handling.
- Logging, monitoring, incident response, and an assigned human owner.

### Pi

- RBAC and user-specific data boundaries.
- Citation verification.
- Audit logging plus vendor data-retention safeguards.

### Qwen

- Restricted data sources and blocked external egress.
- Explicit prevention of write actions without human approval.
- Citation and output-audit requirements.

## Synthesis quality

The orchestrator found meaningful agreement and disagreement:

- All four converged on citation-grounded output.
- Claude, GPT, and Pi prioritized identity-scoped retrieval and ACL enforcement.
- Qwen prioritized validating egress and write-action boundaries.
- GPT uniquely required a named human owner for alerts and incident response.
- Pi uniquely called out vendor-side data-retention terms.
- The synthesis identified a gap across all four: none initially proposed a usefulness or adoption gate for determining whether the pilot should continue.

This is evidence of independent perspectives rather than four cosmetic variations of one answer.

## Orchestration behavior

- Claude returned through the expected notification path.
- GPT and Qwen completed but required bounded history reconciliation because their completion notifications were silent.
- Pi completed last.
- The orchestrator waited for all four before synthesizing.
- A duplicate wake notification arrived after synthesis and was correctly treated as non-new information.

## Usage and cost

OmniGent reported **$0.53123885** in session cost:

| Reported model | Reported cost |
|---|---:|
| Claude Opus 5 | $0.49457750 |
| GPT-5.6 Sol | $0.02585760 |
| Gemini 3.7 Flash | $0.01080375 |
| **Reported total** | **$0.53123885** |

The Qwen call routed through the Unity gateway and was not separately itemized in the OmniGent session total. Unity billing must be reconciled before the reported total is treated as the complete all-in cost.

## Success criteria

| Criterion | Result |
|---|---|
| Four heads dispatched | Pass |
| Four substantive responses returned | Pass |
| Every response attributed | Pass |
| Synthesis included agreement and disagreement | Pass |
| Completion below three minutes | Pass — 1:42 |
| No recorded session error | Pass |
| Reproducible evidence retained privately | Pass |

## Limitations

- One smoke-test prompt is not the planned 20-prompt benchmark.
- Quality was reviewed qualitatively, not scored blindly.
- Individual head latency was not captured precisely.
- Qwen cost was not separately itemized.
- The synthetic scenario did not validate proprietary-data handling.
