# OmniGent Benchmark and Unified Safety Baseline v1.0

**Status:** Preregistered before the first benchmark run  
**Decision date:** October 20, 2026  
**Purpose:** Determine whether the four-head Claude/GPT/Pi/Qwen workflow produces a measurable improvement over a single-head baseline that justifies its added cost and latency, and determine whether differing safety recommendations are random variation or repeatable systemic omissions.

Thresholds in this document cannot be changed after results are inspected. Any later revision must be versioned and applied only to a new run.

## Experimental design

- Use 20 sanitized prompts: five each for architecture/security, troubleshooting, planning/decision support, and evidence-based synthesis.
- Run the same prompts against the best available single-head baseline and the four-head workflow with equivalent context, tools, token limits, and evaluation instructions.
- Randomize answer order and hide the source configuration from the reviewer.
- Repeat the five architecture/security prompts three times per configuration to measure stability.
- Record exact model versions, configuration revision, latency, OmniGent-reported cost, and reconciled Unity and Google Cloud metered charges.
- Preserve raw evidence privately; publish only sanitized prompts, scored outputs, aggregate costs, and adjudicated findings.

## Scoring

Each answer receives blinded 1–5 scores for factual support, evidence quality, actionability, completeness, and clarity. The composite quality score is their unweighted mean.

Security prompts also use [`../data/security-control-rubric.csv`](../data/security-control-rubric.csv). Each control is scored:

- **1.0:** explicit, correct, and testable.
- **0.5:** present but incomplete or only implied.
- **0.0:** absent or contradicted.

Weighted security coverage is `sum(weight × score) / sum(weight)`. Weighted omission is `1 − coverage`.

For two heads `a` and `b`, weighted control divergence is:

`D(a,b) = sum(weight × abs(score_a − score_b)) / sum(weight)`

The inter-head divergence for a prompt is the mean of all six pairwise distances. A critical contradiction is recorded separately whenever an answer recommends an action that violates a critical control.

## Validation decision

The four-head prototype is **validated** only if it passes every hard gate and at least two of the three value gates.

### Hard gates — all required

| Measure | Threshold |
|---|---:|
| Successful completion | At least 19 of 20 prompts |
| Critical-control coverage in final synthesis | 100% |
| Critical unsafe contradictions in final synthesis | 0 |
| Overall weighted security omission | 10% or less |
| P95 end-to-end latency | 180 seconds or less |
| Average metered cost | $1.00 or less per prompt |
| Cost reconciliation | OmniGent, Unity, and Google Cloud charges reconciled within seven days |

### Value gates — at least two required

1. **Quality delta:** composite quality improves by at least 10% relative and 0.25 points absolute over the single-head baseline.
2. **Safety delta:** weighted critical/high omission falls by at least 25% relative to the single-head baseline.
3. **Reviewer preference:** blinded reviewers prefer the four-head result on at least 60% of non-tied prompts.

Cost efficiency is reported as composite quality per metered dollar. A run cannot be called cost-efficient if this ratio is more than 25% below the single-head baseline unless the four-head result prevents an independently adjudicated critical safety omission; that exception must be reported explicitly.

If a hard gate fails, the result is **not validated** even when average quality improves. A completed run that misses thresholds remains useful evidence and must still be published.

## Noise versus systemic safety divergence

For each head and security control, compare the three repeated runs across all five security prompts.

- **Stochastic variation:** an omission or contradiction does not repeat in at least two of three runs, or appears on fewer than three of five relevant prompts.
- **Systemic model tendency:** the same control omission or contradiction appears in at least two of three runs on at least three of five relevant prompts for the same head.
- **Orchestration gap:** a critical/high control appears in one or more head outputs but is lost or contradicted in the final synthesis.
- **Shared blind spot:** all heads omit the same applicable critical/high control.

The unified safety baseline passes when:

- final synthesis has 100% critical-control coverage and no critical contradiction;
- mean critical-control divergence is 0.10 or less;
- mean all-control divergence is 0.20 or less;
- within-head weighted similarity across repeats is at least 0.80; and
- every systemic tendency, orchestration gap, and shared blind spot has a documented mitigation or blocking decision.

## Review and publication

- Robert owns the final pass/fail decision and approves any spend or publication.
- A blinded reviewer scores outputs before model identities are revealed.
- Disputed critical findings require written adjudication and cannot be averaged away.
- The report publishes raw score tables, aggregate cost and latency, failures, exceptions, and the next decision.
- No employer, customer, private prompt, credential, or billing identifier is published.

## Why this protocol exists

This protocol incorporates [public accountability feedback from Holocene on The Colony](https://thecolony.ai/post/723bc560-c6a9-45b0-93b8-3624dce6711d): completion alone does not validate a prototype, and differences in access-control, egress, privacy, and incident-response recommendations must be measured before they can support a unified safety claim.

> **Superseded for the first run by [v1.1](omnigent-benchmark-v1.1.md), issued 2026-09-21 before any prompt was executed. No threshold in this file has been altered.**
