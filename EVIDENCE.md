# Evidence Register

Evidence is labeled using these strengths:

- **Verified:** Inspected directly or supported by a fresh, reproducible artifact.
- **Documented:** Supported by dated notes or logs but not freshly reproduced during this program.
- **Reported:** Stated by Robert but awaiting credential metadata or another inspectable artifact.

## E-001 — OmniGent four-head orchestrator

**Claim:** Robert configured and tested a four-head OmniGent brainstorming system using Claude, GPT, Pi, and Qwen.

**Status:** **Verified.**

Evidence includes:

- A four-head configuration with distinct Claude, GPT, Pi, and Qwen workers.
- Parallel dispatch, explicit attribution, synthesis, bounded history reconciliation, and blast-radius controls.
- Dated technical records of native-harness, runtime, gateway-schema, PATH, and streaming/SSE troubleshooting.
- A fresh OmniGent 0.14.0 smoke test completed September 21, 2026.
- All four heads completed in 1 minute 42 seconds with no recorded session error.
- A sanitized report: [`reports/2026-09-21-omnigent-four-head-smoke-test.md`](reports/2026-09-21-omnigent-four-head-smoke-test.md).

Remaining work:

1. Execute the preregistered 20-prompt benchmark in [`evaluation/omnigent-benchmark-v1.md`](evaluation/omnigent-benchmark-v1.md).
2. Complete blind quality scoring and the single-head comparison against the published pass/fail gates.
3. Capture precise per-head latency.
4. Reconcile Qwen's external gateway cost.
5. Publish a sanitized architecture diagram.
6. Report weighted security coverage, inter-head divergence, repeated-run stability, and systemic versus stochastic omissions.

## E-002 — First Claude certification

**Claim:** Robert completed his first Claude certification and listed it on LinkedIn.

**Status:** **Reported by Robert; credential metadata pending.**

Required metadata:

1. Exact certification title.
2. Issuing organization.
3. Completion or issue date.
4. Public credential or LinkedIn verification URL.
5. Optional redacted certificate image.

Once captured, the credential counts as a completed learning module. It should be paired with an applied artifact to demonstrate both structured learning and practical implementation.

## E-003 — SuperGrok purchase and OmniGent fifth-head experiment

**Claim:** Robert purchased a $30 SuperGrok subscription to evaluate Grok Build as a potential fifth head in the OmniGent workflow.

**Status:** **Purchase reported by Robert; experiment design documented; technical integration pending.**

Evidence includes:

- Robert's September 21, 2026 purchase report.
- The fixed monthly cost recorded in [`data/monthly-cost-baseline.csv`](data/monthly-cost-baseline.csv).
- The purchase event recorded in [`data/learning-expenses.csv`](data/learning-expenses.csv), with receipt or statement reconciliation kept pending rather than overstated.
- A controlled experiment card: [`experiments/2026-09-21-grok-omnigent-fifth-head.md`](experiments/2026-09-21-grok-omnigent-fifth-head.md).
- Official documentation for OmniGent's built-in [`grok` harness](https://omnigent.ai/docs/build/harnesses/configuration) and [xAI Grok Build](https://docs.x.ai/build/overview).

Remaining work:

1. Install and authenticate the Grok CLI in the WSL environment where OmniGent runs.
2. Record the exact Grok Build model selected by the account at test time.
3. Complete standalone and OmniGent smoke tests.
4. Run the incremental four-head-versus-five-head comparison after the preregistered four-head baseline.
5. Reconcile the purchase evidence privately and publish only the aggregate amount.
6. Make and document a keep, revise, or cancel decision before the next billing period.

## Evidence policy

- Do not publish claims stronger than the available evidence.
- Label self-reported credentials until metadata is captured.
- Prefer reproducible demonstrations over screenshots alone.
- Preserve failures and corrective actions because they demonstrate troubleshooting depth.
- Redact credentials, personal contact details, enterprise identifiers, private prompts, and financial information.
- Link each public progress claim to an evidence-record ID.
