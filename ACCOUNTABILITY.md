# 90-Day Accountability Program

**Window:** September 21–December 20, 2026  
**Objective:** Convert financial support into demonstrable AI capability while separately and transparently reporting the campaign's debt-reduction component.

## Commitments

1. Every net dollar is categorized as **Learning** or **Debt Reduction**.
2. Learning expenses require a named experiment, spending cap, success measure, and linked deliverable.
3. Robert authorizes every purchase and payment. AI agents cannot spend or transact.
4. Inspectable artifacts—not hours or certificates alone—demonstrate progress.
5. A public report is produced monthly, including when a milestone is late or unsuccessful.
6. Public evidence is sanitized to protect credentials, financial data, personal contact details, and proprietary information.

## Proposed working allocation

The proposed allocation of net proceeds is **60% Learning / 40% Debt Reduction**, subject to Robert's confirmation before the first payout or expense. Any change must be documented before it applies to new spending.

No single learning experiment should exceed 20% of total net donations without a written exception explaining the expected benefit and risk.

## 90-day scorecard

| Measure | Target | Evidence |
|---|---:|---|
| Focused learning time | 72 hours | Weekly learning log |
| Completed learning modules | 6 | Credential or completion record plus practical notes |
| Working AI/cloud prototypes | 3 | Artifact, README, and demonstration |
| Architecture and security reviews | 3 | Diagram, threat/identity notes, and decisions |
| Experiments with predefined success criteria | 100% | Approved experiment cards |
| Learning expenses linked to milestones | 100% | Aggregate ledger and evidence link |
| Funds categorized Learning vs. Debt | 100% | Reconciled aggregate ledger |
| Public progress reports | 3 of 3 | Dated reports in this repository |

## Milestone 1 — Benchmark the four-head OmniGent workflow

**Due:** October 20, 2026

Turn the existing Claude/GPT/Pi/Qwen `debby-quad` work into a repeatable, measured evaluation:

- Run a 20-prompt test spanning analysis, planning, troubleshooting, and synthesis.
- Compare a single-head baseline with four-head results.
- Measure completion rate, latency, reported cost, evidence quality, actionability, factual support, and reviewer preference.
- Apply preregistered hard gates and value gates before calling the workflow validated.
- Score security-control coverage, pairwise model divergence, repeated-run stability, and critical omissions using the published rubric.
- Publish a sanitized architecture diagram, rubric, transcript excerpts, and lessons learned.

The initial 4/4 smoke test is complete and establishes the operational baseline. The evaluation protocol is preregistered in [`evaluation/omnigent-benchmark-v1.md`](evaluation/omnigent-benchmark-v1.md); a completed run, not the smoke test alone, determines validation.

## Milestone 2 — Governed cloud prototype

**Due:** November 20, 2026

Deploy an AI workflow with observable cost, security, and human-approval controls:

- Least-privilege identity and access design.
- Logging, cost tracking, and a defined spending limit.
- Threat model covering prompt injection, data leakage, and tool misuse.
- At least one explicit human-in-the-loop control for consequential actions.
- Test results and an operating runbook.

## Milestone 3 — Capstone and reusable playbook

**Due:** December 20, 2026

Combine the learning into a reusable, documented AI-agent implementation:

- Working capstone demonstration.
- Reproducible setup instructions.
- Evaluation results compared with the September baseline.
- Architecture, security, cost, and rollback documentation.
- Final lessons-learned report and next-quarter roadmap.

## Operating cadence

### Cost baseline

Current AI learning costs come from four sources:

- Usage-based OmniGent Qwen runs through the Unity gateway.
- Usage-based Google Cloud charges for the Pi head, backed by a Gemini model.
- A paid Claude subscription.
- A paid Codex subscription.

Monthly reporting separates fixed subscriptions from metered run costs. Reports record the exact model/version used rather than relying on the changing label “latest,” and publish aggregate totals without exposing account, billing, or credential data.

### Weekly review

- Record learning time and completed modules.
- Update prototype status and evidence links.
- Reconcile donations and expenses at the aggregate level.
- Assign Green, Yellow, or Red status to the active milestone.
- Record one decision and the next concrete action.

### Monthly public reports

Reports are due **October 20, November 20, and December 20** and include:

1. Amount raised during the period and cumulative total.
2. Net funds categorized as Learning and Debt Reduction.
3. Deliverables completed, with safe evidence links.
4. KPI results versus target.
5. Spending versus authorized caps.
6. Fixed subscription costs versus metered gateway/cloud costs.
7. Failures, changes, and unresolved risks.
8. The next milestone and due date.

### Status definitions

- **Green:** On schedule; evidence and spending records are current.
- **Yellow:** At risk; recovery action and owner are documented.
- **Red:** Milestone missed, evidence absent, or spending unreconciled.

If a milestone turns Red, publish an honest update within seven days, name the recovery date, and pause new nonessential learning expenses until the plan is reset.

## Responsibilities

### Robert

- Approves spending, debt payments, public commitments, and external posts.
- Completes the hands-on learning and produces milestone artifacts.
- Retains private financial records and confirms monthly reconciliation.

### AI assistant

- Maintains templates, scorecards, and draft updates.
- Checks that claimed outcomes have evidence.
- Flags missed dates, unsupported claims, cost overruns, and allocation drift.
- Never spends funds, handles transfer credentials, or publishes without Robert's approval.
