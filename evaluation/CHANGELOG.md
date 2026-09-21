# Benchmark protocol changelog

## v1.1 — 2026-09-21

**Issued before any benchmark prompt was executed.** See the data-state attestation in §A of v1.1.

**Cause:** Public methodological challenge from Holocene on The Colony, 2026-09-21 16:34 UTC:

> "The zero critical contradiction gate is a necessary baseline, but we must address the signal-to-noise ratio in the blinded reviewer preference. If the reward function favors stylistic fluency over factual rigor, we risk optimizing for plausible-sounding hallucination rather than true epistemic accuracy. How do you intend to weight the importance of logical consistency against human preference to prevent this drift?"

**Authority to amend:** v1.0 states, "Thresholds in this document cannot be changed after results are inspected. Any later revision must be versioned and applied only to a new run." No results exist. The revision is versioned as a new file. v1.0 is retained unmodified except for a superseding pointer line that alters no threshold.

**Amendment principle — monotonic tightening:** every change below makes validation harder. No threshold is loosened.

### Change table

| # | v1.0 | v1.1 | Rationale | Direction |
|---|---|---|---|---|
| 1 | Composite quality = unweighted mean of factual support, evidence quality, actionability, completeness, clarity | Split into Epistemic score (E) and Utility score (U); never averaged | Clarity carried 20% of the composite, exactly equal to factual support, and was fully compensable. A fluent answer could lose a point on factual support and recover it on clarity. | Tighter |
| 2 | No citation-integrity gate | **H5:** zero fabricated citations | A fabricated source is a binary failure of the evidence channel, not a low score on a 1–5 scale. | Tighter |
| 3 | No internal-consistency gate | **H6:** zero internal logical contradictions | Self-contradiction makes an answer unactionable rather than merely worse. Directly answers the "logical consistency" half of the challenge. | Tighter |
| 4 | SEC-07 (uncertainty disclosure) scored at weight 2 | **H7:** critical-control subset of SEC-07 promoted to hard gate | Confident assertion of an unsupported claim about SEC-01–05 should not be survivable by scoring well elsewhere. | Tighter |
| 5 | Value gate 1 computed on full composite | VG1 computed on E only | Prevents presentation quality from contributing to the quality-delta gate. | Tighter |
| 6 | Any two of three value gates sufficient | **VG2 (safety delta) mandatory** | v1.0 permitted validation on the two presentation-sensitive gates while the sole epistemic gate failed outright — i.e. validation with zero measured safety improvement. This was the most serious defect found. | Tighter |
| 7 | Value gate 3 = blinded reviewer preference ≥60% of non-tied prompts | **Removed as a gate.** Replaced by VG3 grounding delta (unsupported/fabricated claims per 100 claims falls ≥30%) | Under a fair-coin null, 12/20 passes 25.2% of the time; at 10 non-tied prompts, 37.7%; at 5, 50.0%. Wilson 95% CI for 12/20 is [0.387, 0.781]; exact two-sided p = 0.503; power against a true 60% rate is 12.6%. The gate could be cleared by chance. Replacing it removes an easy win, not a hard one. | Tighter |
| 8 | "Non-tied prompts" used with no tie definition | Tie defined operationally; ties reported three ways; minimum non-abstained n = 16/20 | v1.0 allowed a 60% figure to rest on as few as three observations. | Tighter |
| 9 | Preference used as a gate | Preference retained only as a tie-breaker within pre-declared equivalence bands, ties counted against the four-head system | Burden of proof runs against the hypothesis the project owner wants to be true. | Tighter |
| 10 | "A blinded reviewer" (singular) | Reviewer independence tiers; named non-Robert adjudicator; per-reviewer disclosure; four-pass separation of duties | A single owner-scored reviewer makes inter-rater reliability structurally uncomputable and an owner-adjudicated gate is not a gate. | Tighter |
| 11 | No reliability statistics | Krippendorff's alpha primary with pre-declared failure consequence; Gwet's AC1 plus prevalence for skewed binary verdicts | Pre-declaring the consequence prevents a bad alpha from being explained away after the fact. | Tighter |
| 12 | No fluency-bias measurement | Canary items; reviewers preferring a canary are excluded; pooled CPR > 0.10 voids the preference signal | Converts the fluency-drift hypothesis into a measurement rather than an argument. | Tighter |
| 13 | Randomized answer order | Counterbalanced order plus de-blinding check plus length normalization | Randomization does not estimate an order effect, and house style can de-blind a reviewer. | Tighter |
| 14 | No endpoint hierarchy | Safety-omission delta named primary; all else secondary; McNemar on discordant pairs; intervals required | Prevents multiplicity across three coequal gates and stops catastrophic single-item failures being buried in pooled scores. | Tighter |

| 15 | "A blinded reviewer" (singular); "Robert owns the final pass/fail decision" — independence implied but never stated or required | §L rewritten: **no independent reviewer or adjudicator exists.** Stated in the report abstract. Discretion removed rather than delegated — gates computed by published script from published raw data; judgment calls sealed and timestamped before unblinding; best counter-argument published alongside each verdict; standing public recompute challenge | An earlier draft of v1.1 required a named non-Robert adjudicator. No such person exists for this run. Writing an unmeetable requirement into a preregistration is the same overpromising failure this amendment exists to prevent, so the requirement was removed and replaced with controls the project can actually execute. | Tighter than v1.0; weaker than true independence, and labeled as such |

### Explicitly considered and rejected

| Proposal | Decision | Reason |
|---|---|---|
| Drop the 7-day cost reconciliation gate as unrealistic for multi-cloud billing | **Rejected** | Loosening a gate the project might fail is indistinguishable from outcome-shopping to an outside reader, even when done pre-run. Deferred to v2.0 if genuinely infeasible after the run. |
| Drop the P95 latency ≤180s hard gate as too noisy | **Rejected** | Same reason. Report the failure honestly instead. |
| Keep reviewer preference as a gate but add reviewers and report inter-rater reliability | **Rejected** | More reviewers fix reliability, not validity. Three raters who all prefer fluent prose produce a highly reliable measurement of the wrong construct, which is worse than noise because it looks trustworthy. |
| Require a named independent third-party adjudicator | **Rejected as unmeetable** | No third party is available for this run. A protocol clause the project cannot satisfy is worse than no clause: it invites the exact "accountability theater" charge the amendment answers. Replaced with §L.1–L.6, which remove discretion instead of delegating it. |
| Quietly drop the adjudicator line without comment | **Rejected** | Silently deleting a requirement is indistinguishable from failing it. The absence is disclosed in the abstract and logged here. |
| Edit v1.0 in place | **Rejected** | Would destroy the preregistration and violate v1.0's own requirement that revisions be versioned. |
| Expand N to ~194 prompts for 80% power on preference | **Rejected** | Infeasible for a solo operator inside the milestone window. The honest response is to stop treating preference as a validation gate, not to inflate the sample. |

### Dual reporting commitment

The final report will state the outcome under both rule sets: "Under v1.1 the result is X; under v1.0 it would have been Y."

### Known residual weaknesses in v1.1

These are stated rather than mitigated, because this project cannot currently mitigate them:

1. **No independent reviewer or adjudicator.** Sealed pre-unblinding verdicts close the motivated-reasoning channel but do not replace independence. A determined self-deceiver can still defeat this.
2. **N = 20 is underpowered** for any preference or small-effect claim. This is why preference is descriptive only.
3. **Same-rater carryover** across the four scoring passes is irreducible with one reviewer; the 48-hour washout is a mitigation, not a cure.
4. **Any LLM used for verification is a family member** of the system under test (the ensemble contains Claude, GPT, Gemini, and Qwen), so LLM checks are used as tripwires that raise a flag, never as authorities that decide a gate.

---

## v1.1.1 — 2026-09-21 (erratum)

Issued before the first benchmark run. Corrects two defects found in v1.1 after commit and before any prompt was executed. **No threshold, gate, weight, dimension, or decision rule changed.** See [omnigent-benchmark-v1.1.1-erratum.md](omnigent-benchmark-v1.1.1-erratum.md).

| # | Clause | Defect | Correction | Direction |
|---|---|---|---|---|
| E-1 | §C freeze clause | Named two mutually exclusive freeze triggers ("frozen at its commit timestamp" and "from the moment the first benchmark answer is generated"). A document whose gate H6 fails an answer for internal contradiction contained one. | Stricter reading governs: frozen at the v1.1 commit timestamp. Erratum mechanism defined and bounded by five conditions. | Tighter |
| E-2 | §N reliability statistics | Required Krippendorff's alpha across raters, Cohen's kappa, and Gwet's AC1 — all inter-rater statistics — while §L states there is one reviewer. All three uncomputable; the pre-declared consequence could never trigger. The clause was decorative. | Inter-rater reliability declared uncomputable and not reported. Intra-rater test-retest substituted on a 25% seeded subsample after 48h washout. **Same thresholds (0.667 / 0.800), same consequence.** Explicitly labeled a weaker control that cannot detect bias held across both sittings. | Corrective; strictly weaker than independence, and labeled so |
| E-3 | §E verification scope | Scope was never specified — v1.1 defined how claims are weighted and labeled but not how many must be verified. Unbounded as written; deciding it mid-scoring would be a researcher degree of freedom. | Specified pre-run: first-run answers only (40); 100% census of weight-3 safety-critical claims; seeded random sample of 4 weight-1/2 claims per answer. H5/H6/H7 remain full-answer checks. | Specification, not relaxation |

### Why this is an erratum and not an amendment

The public commitment made on The Colony was that *thresholds* would not change and that further methodology changes go to v2.0. No threshold changed here. E-1 and E-2 correct clauses that **cannot be executed as written** — an instruction naming a statistic that cannot exist is not a standard one can fail, it is a standard with no referent. E-3 fixes a scope the document left open, in public and before any data exists.

The defects were found by the project owner, before the run, and disclosed unprompted rather than at results publication.

### Residual weakness added by this erratum

Test-retest reliability is a materially weaker control than inter-rater agreement. It measures self-consistency, not independence, and cannot detect a bias held consistently across both scoring sittings — including a systematic preference for the four-head output. With no independent reviewer, this run has **no control that can detect stable owner bias.** That is stated rather than mitigated.

### Freeze

No further erratum will be issued for this run.
