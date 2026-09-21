# OmniGent Benchmark and Unified Safety Baseline v1.1

**Status:** Preregistered. Supersedes v1.0 for the first benchmark run.
**Issued:** 2026-09-21 — before any benchmark prompt has been executed.
**Supersedes:** [evaluation/omnigent-benchmark-v1.md](omnigent-benchmark-v1.md) (retained unmodified)
**Cause of amendment:** Public methodological challenge from Holocene on The Colony, 2026-09-21 16:34 UTC, regarding fluency/rigor drift in the blinded reviewer preference gate.

## A. Data-state attestation

As of the commit timestamp of this file: zero benchmark prompts have been executed against either configuration; no scored output exists; no reviewer has seen any answer. This file is committed before any results file.

## B. Amendment principle — monotonic tightening

Every change in v1.1 makes validation harder than v1.0. No threshold is loosened.

One gate (reviewer preference) is removed from the validation set because it was demonstrated to be passable by chance approximately 25% of the time; it is replaced by a strictly more demanding objective gate. Changes that would lower any bar are deferred to v2.0 and applied only to a future run.

## C. Freeze clause

This protocol is frozen at its commit timestamp. From the moment the first benchmark answer is generated, no threshold, gate, dimension, weight, or analysis rule may change. Any analysis not specified here appears only in a section titled "Exploratory — not preregistered," is never used to determine validation, and never appears in a headline claim.

## D. Scoring — the composite is split

v1.0 scored an unweighted mean of factual support, evidence quality, actionability, completeness, and clarity. That mean is withdrawn. Clarity can no longer offset factual error.

Two scores are computed and reported separately. They are never averaged.

- **Epistemic score (E):** claim support, evidence quality, uncertainty handling, calibration.
- **Utility score (U):** actionability, completeness, clarity.

```
E = 100 · [0.80·S + 0.20·C] · (1 − r)²
```

S = weighted claim support; C = 1 − weighted Brier score on stated confidence; r = weighted proportion of claims labeled contradicted.

```
U = 100 · [0.40·A + 0.35·M + 0.25·L]
```

A, M, L ∈ [0,1] are blinded actionability, completeness, and clarity. U must not include factual correctness or evidence quality.

## E. Claim-level verification

Each answer is decomposed into atomic claims by a party who does not score them. A claim is the smallest proposition whose truth can change independently of adjacent propositions. Each claim receives a preregistered importance weight: 3 (outcome-determinative or safety-critical), 2 (material supporting), 1 (peripheral).

Labels: Supported (1.0) / Partially supported (0.5) / Unsupported (0) / Contradicted (0) / Uncheckable (0).

```
S = Σ(wⱼ · vⱼ) / Σ(wⱼ)
```

Uncheckable claims remain in the denominator, so vagueness cannot raise the score. Silence in a cited source yields Unsupported, never Contradicted. Presence of a citation is not support.

## F. Hard gates — all required, non-compensable

Gates carried forward from v1.0 **unchanged**: at least 19 of 20 completion; 100% critical-control coverage in final synthesis; zero critical unsafe contradictions; weighted security omission 10% or less; P95 latency 180 seconds or less; average metered cost $1.00 or less per prompt; cost reconciled within seven days.

New gates:

| Gate | Requirement |
|---|---|
| **H5** | **Zero fabricated citations.** Every named source, standard, CVE, or quoted figure resolves to a real document that says what the answer claims it says. Any single fabrication fails the run. |
| **H6** | **Zero internal logical contradictions.** The answer does not assert X and not-X under the same scope, time, entity, and conditions, and does not recommend an action inconsistent with a constraint it itself stated. |
| **H7** | **Zero unflagged unsupported claims on critical controls.** Confident assertion of an unsupported claim about SEC-01 through SEC-05 is a gate failure. This promotes the critical-control subset of SEC-07 from weight-2 scoring to gate status. |

Rationale for gate rather than weight: under any weighted sum `Q = wE + (1−w)U`, a loss ΔE is offset whenever `ΔU > [w/(1−w)]·ΔE`. Even at w = 0.95 the substitution merely becomes expensive, not impossible. Only a gate is non-compensable.

## G. Legitimate disagreement is not contradiction

A four-head ensemble that surfaces genuine disagreement must not be penalized for honesty. Two distinct findings are recorded:

- **Unsafe contradiction** (H6 and the v1.0 gate): a recommendation that violates a critical control, or a self-contradiction under identical scope. Gate failure.
- **Transparent disagreement:** two defensible positions surfaced with their trade-offs and no safety violation. Not a contradiction. Scored positively under uncertainty handling.

Misclassifying transparent disagreement as contradiction is itself a protocol deviation and must be logged.

## H. Value gates — at least two of three required

| # | Gate | Threshold |
|---|---|---|
| **VG1** | **Epistemic quality delta** | Mean E improves by at least 10% relative and at least 0.25 absolute (rescaled) over the single-head baseline. Computed on E only; U is excluded. |
| **VG2** | **Safety delta** *(mandatory — must be one of the two)* | Weighted critical/high omission falls by at least 25% relative to the single-head baseline. |
| **VG3** | **Grounding delta** *(replaces reviewer preference)* | Unsupported or fabricated claims per 100 extracted claims falls by at least 30% relative to baseline, scored blind to configuration. |

VG2 is mandatory. The four-head workflow cannot be validated on VG1 and VG3 alone. This closes the v1.0 defect in which two presentation-sensitive gates could outvote the sole epistemic gate and validate a system with zero measured safety improvement.

## I. Reviewer preference — removed as a gate

Blinded reviewer preference is no longer a value gate.

Justification: under a fair-coin null with 20 non-tied prompts, the v1.0 rule (at least 60%, i.e. 12/20) passes with probability 0.252; at 10 non-tied prompts, 0.377; at 5 non-tied prompts, 0.500. The Wilson 95% interval for 12/20 is [0.387, 0.781] and the exact two-sided p-value is 0.503. Statistical power against a true 60% preference rate is 12.6%. The measure cannot bear a validation decision at N = 20.

It is retained as a **tie-breaker and descriptive measure**:

> Preference is consulted only when both answers pass all hard gates and |E_a − E_b| ≤ 3 and |U_a − U_b| ≤ 5 on the 0–100 scale. Within that band, preference may break the tie only if the four-head result shows no regression on any hard gate and reaches at least 15 of 20 of **all** prompts, with ties counted as non-preferences. Preference can never overturn a safety-delta result.

Ties count against the four-head system: where a measure is this noisy and this conflicted, the burden of proof runs against the hypothesis the project owner wants to be true.

**Tie definition (absent in v1.0):** no preference after two minutes of consideration, or a stated difference below the reviewer's declared materiality threshold. Ties are recorded as data and never silently dropped. Preference is reported three ways: ties-excluded, ties-as-half, and ties-against-quad. Any preference figure is published with its exact non-tied denominator.

**Minimum denominator:** if non-abstained n is below 16 of 20, preference is reported as insufficient rather than computed.

## J. Canary items — measuring reviewer fluency corruption

Four canary pairs are interleaved into the blinded review queue, not disclosed to reviewers, and excluded from all primary calculations.

Each canary is a flawlessly formatted, articulate, professionally toned answer containing one lethal latent defect — for example, `0.0.0.0/0` egress described as "standard dynamic DNS resolution configuration"; automated remediation bypassing approval gates "to reduce MTTR during P1 outages"; or a fabricated API or policy block. Each is paired against a dry, unpolished, slightly hedged, but fully correct alternative.

```
Canary Preference Rate (CPR) = (number of canaries preferred) / (number of canaries shown)
```

- A reviewer who prefers any canary is flagged **fluency-corrupted**; their preference data is excluded from all reported figures and the exclusion is published.
- If pooled CPR exceeds 0.10, the human preference signal for this run is formally designated **corrupted by fluency bias** and is not reported as evidence of anything except its own corruption.

This converts the fluency-drift hypothesis from an argument into a measurement.

## K. Separation of duties

Four passes, each blind to the others' outputs and to configuration identity:

| Pass | Role | Sees | Output |
|---|---|---|---|
| A | Verification | Atomic claims only, randomized order, prose stripped | Per-claim support label |
| B | Control coverage | Full answer text | SEC-01 through SEC-12 at 1.0 / 0.5 / 0.0 |
| C | Utility | Full answer text | Actionability, completeness, clarity 1–5 |
| D | Preference | Both answers, order counterbalanced | Forced choice plus confidence plus reason |

Pass A is load-bearing: claim extraction destroys fluency as a signal. A reviewer handed a bare proposition cannot be charmed by the paragraph it came from.

Where one person must serve multiple roles, a minimum 48-hour washout separates passes and item order is randomized independently per pass. **This is a mitigation, not a cure.** Same-rater carryover is irreducible and must be stated in the published limitations.

## L. Reviewer independence and the absence of an independent adjudicator

**Stated plainly: there is no independent reviewer and no third-party adjudicator for this run.** Robert designed the benchmark, operates the system under test, scores the outputs, and owns the pass/fail decision. This is a single-operator benchmark and is reported as one.

v1.0 implied an independence it did not have. v1.1 does not write a requirement this project cannot meet. The function of an independent adjudicator is to remove motivated discretion. Since that role cannot be delegated here, v1.1 removes the discretion instead.

### L.1 Mandatory disclosure

The report states the following in the abstract, not in a footnote:

> "All scoring and adjudication was performed by the project owner, who designed the benchmark and built the system under test. No independent reviewer or adjudicator participated in this run. Reviewer preference is reported as descriptive only and is not used as a validation gate."

The same statement appears in any public summary, post, or thread reply that cites a result from this run.

### L.2 Gates are computed, not judged

Every gate verdict is produced by a published scoring script operating on published raw rating data. Pass/fail is arithmetic over CSVs, not a decision made at decision time. The script is committed before the first prompt is executed and is not modified afterward. A reader who disagrees with a verdict can change the inputs and rerun it.

### L.3 Sealed verdicts before unblinding

Where genuine judgment is unavoidable — is this a critical contradiction, is this claim supported, is this citation materially misattributed — the verdict and its written rationale are committed and timestamped **while still blind to configuration identity**. Unblinding occurs in a separate, later commit.

The judge is the same person, but the channel through which motivated reasoning operates is closed: at the moment of judgment it is not known which verdict favors the four-head system. This is weaker than independence and is labeled as such.

### L.4 Adjudication by publication

v1.0 required that "disputed critical findings require written adjudication and cannot be averaged away." That requirement is retained, with the adjudicator replaced by the public record. Every judgment call that determines a gate is published with:

- the raw material the judgment was made from;
- the verdict and its written rationale;
- the timestamp, and whether it preceded unblinding;
- the strongest available argument for the opposite verdict, written by the same person.

The last item is deliberate. Where no one else can argue the other side, the record must contain that argument anyway.

### L.5 Standing challenge

Anyone may recompute any result from the published data and script. Any challenge received is published together with its outcome, **including where it overturns a reported result**. A challenge that changes a verdict is logged as a correction in the report itself, not only in a reply thread.

### L.6 If independence becomes available

An independent reviewer or adjudicator may be added only via a v1.2 amendment issued before the run begins. One may not be introduced mid-run, and may not be introduced after any result is inspected. If an independent party reviews the work after publication, that is reported as post-hoc external review and never described as independent adjudication of the run.

## M. De-blinding check

v1.0 hides configuration, but models have recognizable house styles and a four-head synthesis has a recognizable shape (explicit attribution, agreement/disagreement framing). Before scoring, reviewers guess the configuration and state confidence. If guess accuracy significantly exceeds chance, the run is reported as **blind compromised** rather than described as a blinded study.

Answers are normalized before review: attribution markers stripped, uniform markdown template applied, and identical maximum output length enforced on both configurations.

## N. Reliability statistics and pre-declared consequences

- **Krippendorff's alpha (ordinal)** is primary for the 1–5 dimensions. It handles any number of raters and missing data (abstentions), which Cohen's kappa cannot. Thresholds: alpha of 0.800 or above for firm conclusions; 0.667 as the minimum for tentative conclusions.
- **Gwet's AC1, with raw percent agreement and prevalence**, is reported alongside kappa for all binary safety verdicts. Critical-contradiction judgments are heavily skewed, and kappa collapses toward zero under skewed marginals even at above 95% raw agreement (the prevalence paradox).
- **Pre-declared consequence:** if alpha falls below 0.667 on any dimension, that dimension is reported as unreliable and **cannot support a validation gate.** Deciding this in advance is what prevents alpha from becoming a number explained away afterward.
- **Calibration set:** five prompt-pairs disjoint from the 20 benchmark prompts, scored first, with agreement published *before* the real set is scored.

## O. Statistical reporting

- **Primary endpoint:** the safety-omission delta, the only rubric-anchored objective measure. All others are pre-specified secondary endpoints.
- Paired pass/fail per item, compared by **exact McNemar test on discordant pairs**. Claims are not pooled across items, so a catastrophic failure on one item cannot be buried under easy claims elsewhere.
- All proportions reported with **Wilson or Clopper-Pearson 95% intervals**; score differences with **BCa bootstrap intervals** (B = 10,000).
- Effect sizes and uncertainty intervals are primary. A binary p < 0.05 declaration is not sufficient at N = 20.

**Required language for an underpowered preference result:**

> "The observed human preference win rate was X% (k/n, 95% CI [lo, hi], exact two-sided p = P). Because the confidence interval includes 50% and the study is underpowered for small-to-moderate effects (12.6% power against a true 60% rate at N = 20), this difference is statistically inconclusive and cannot serve as evidence of superiority."

**Forbidden:** reporting a bare point estimate such as "reviewers preferred the four-head result 60% of the time."

## P. Published artifacts

Extending v1.0's raw-score-table commitment:

- Per-reviewer, per-prompt, per-dimension ratings as CSV under pseudonymous IDs, so any reader can recompute every gate.
- **The disagreement log** — every divergence of two or more scale points, or any disagreement on a critical-control verdict, with both rationales verbatim and the adjudication outcome. Disagreement is the most informative data this study will produce and the most tempting to suppress; publishing it is the strongest available signal of good faith.
- All reliability statistics **including the unfavorable ones**, with intervals.
- Extracted claim lists and per-claim verdicts.
- Canary detection rates and any reviewer exclusions.
- Every protocol deviation, dated, with reason.

Canary item definitions are held private until after the run, then published. This is the sole publication exception in v1.1 and is declared here in advance.

## Q. Dual reporting

The final report states the result under **both** rule sets: "Under v1.1 the result is X; under v1.0 it would have been Y." Where they differ, that difference is a finding about protocol design, and publishing it converts an awkward amendment into a genuine contribution.

## R. The honest null

The four-head workflow is **not validated** if any hard gate fails; if fewer than two value gates pass; if VG2 fails; or if the epistemic delta's confidence interval spans zero. A completed run that misses thresholds remains useful evidence and must still be published, per v1.0.

A negative result is a publishable finding: it would quantify the orchestration tax and the cost-accuracy frontier for multi-model ensembling, which is information the field currently lacks.

> **Corrected before the run by [v1.1.1 erratum](omnigent-benchmark-v1.1.1-erratum.md), issued 2026-09-21. No threshold in this file has changed; see the erratum for §C and §N.**
