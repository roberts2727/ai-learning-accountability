# OmniGent Benchmark v1.1.1 — Erratum

**Status:** Erratum to [v1.1](omnigent-benchmark-v1.1.md). Issued before the first benchmark run.
**Issued:** 2026-09-21
**Corrects:** v1.1 §C, §N. Specifies v1.1 §E.
**Leaves unchanged:** every threshold, gate, weight, dimension, and decision rule in v1.1.

## 0. Data-state attestation

As of the commit timestamp of this file: zero benchmark prompts have been executed against either configuration; no scored output exists; no reviewer has seen any answer. v1.1 was committed 2026-09-21 21:13:22 UTC and no run has occurred since.

## 1. Why an erratum exists at all

v1.1 §C froze the protocol at its commit timestamp and provided **no mechanism for correcting a clause that cannot be executed as written**. Two such clauses were found after commit and before the run.

This document establishes that mechanism and immediately binds itself to it. An erratum:

- may correct only a clause that is unexecutable as written, or that contradicts another clause in the same document;
- **may not change any threshold, gate, weight, dimension, or decision rule**;
- must be issued before the first benchmark answer is generated;
- must be published as a separate versioned document, leaving the corrected document unmodified except for a pointer line;
- must be disclosed publicly at the time of issue, not at publication of results.

Anything that does not meet all five conditions is an amendment, not an erratum, and is deferred to v2.0 applied to a future run.

The defects corrected here were found by the project owner before the run and disclosed unprompted. That sequence is itself part of the record.

---

## E-1. §C — two mutually exclusive freeze triggers

**Defect.** v1.1 §C reads: "This protocol is frozen at its commit timestamp. From the moment the first benchmark answer is generated, no threshold, gate, dimension, weight, or analysis rule may change." These name two different trigger times. The document cannot be frozen at both. A protocol whose gate H6 fails an answer for internal contradiction contained one.

**Correction.** The **stricter** reading governs. §C is replaced in full by:

> This protocol is frozen at the commit timestamp of v1.1 (2026-09-21 21:13:22 UTC). No threshold, gate, dimension, weight, decision rule, or analysis rule may change from that moment. The sole permitted exception is an erratum meeting all five conditions in v1.1.1 §1, issued before the first benchmark answer is generated. Any analysis not specified in v1.1 as corrected by v1.1.1 appears only in a section titled "Exploratory — not preregistered," is never used to determine validation, and never appears in a headline claim.

This resolves the contradiction in the direction that removes discretion rather than adding it.

---

## E-2. §N — reliability statistics that cannot be computed

**Defect.** v1.1 §N requires Krippendorff's alpha across raters, Cohen's kappa, and Gwet's AC1. All three are **inter-rater** statistics requiring two or more independent raters. v1.1 §L states that there is one reviewer. All three are therefore uncomputable for this run, and the pre-declared consequence attached to them could never trigger. The clause was decorative — the precise failure mode v1.1 was written to prevent.

**Correction.** §N is replaced in full by:

> **Inter-rater reliability cannot be computed for this run.** There is one reviewer (v1.1 §L). Krippendorff's alpha across raters, Cohen's kappa, and Gwet's AC1 all require two or more independent raters and are not reported. Their absence is stated in the report abstract alongside the §L.1 disclosure.
>
> **Intra-rater test-retest reliability is reported in their place.** A random 25% subsample of answers, drawn with a published seed before any scoring begins, is re-scored after a minimum 48-hour washout, blind to the first-pass scores and blind to configuration identity.
>
> - For the 1–5 dimensions: **Krippendorff's alpha (ordinal)**, computed treating the two sittings as two coders of the same material.
> - For binary safety verdicts: **raw percent agreement, prevalence, and Gwet's AC1**, computed across the two sittings. Raw agreement and prevalence are always reported together, because a skewed marginal distribution collapses chance-corrected coefficients toward zero even at high raw agreement.
>
> **Thresholds are unchanged from v1.1 §N:** 0.800 or above for firm conclusions; 0.667 as the minimum for tentative conclusions.
>
> **The pre-declared consequence is unchanged:** if the statistic falls below 0.667 on any dimension, that dimension is reported as unreliable and **cannot support a validation gate**.
>
> **Stated limitation.** Test-retest measures whether one judge is self-consistent. It does not measure independence and cannot detect a bias held consistently across both sittings — including a systematic preference for the four-head output. It is a strictly weaker control than inter-rater agreement and is labeled as such wherever it is reported. It must not be described as inter-rater reliability.
>
> **Calibration set:** unchanged from v1.1 §N. Five prompt-pairs disjoint from the 20 benchmark prompts, scored first, with agreement published before the benchmark set is scored.

No threshold and no consequence changed. Only the statistic that feeds them changed, from one that cannot exist to one that can.

---

## E-3. §E — verification scope, specified

**Status: specification, not correction.** v1.1 §E defines how claims are weighted and labeled but never states how many claims must be extracted or verified. Scope must be fixed before scoring or the result is not reproducible. Deciding it during scoring, after seeing answers, would be a researcher degree of freedom. It is therefore fixed here, in public, before the run.

**Specification.**

1. **Claim verification applies to first-run answers only** — 20 prompts × 2 configurations = 40 answers. The repeat runs of the five architecture/security prompts exist to measure stability and divergence and are scored on the security-control rubric only, which is the measure those repeats were designed to feed.

2. **Within each answer:**
   - **100% census of all weight-3 claims** (outcome-determinative or safety-critical). No sampling of the safety-critical layer.
   - **A random sample of 4 weight-1 and weight-2 claims**, drawn with a published seed before verification begins.

3. **Computation.** S is computed over verified claims per v1.1 §E. The weight-1/weight-2 component is reported with a sampling confidence interval; the weight-3 component is a census and is reported without one.

4. **Gates are unaffected in scope.** H5 (fabricated citations), H6 (internal contradictions), and H7 (unsupported critical-control claims) remain full-answer checks. A fabricated citation anywhere in an answer fails the run whether or not the claim carrying it was drawn in the sample.

**Stated limitation.** Sampling the peripheral layer reduces sensitivity to peripheral factual error, and the reported support rate for weight-1/2 claims carries sampling uncertainty that a census would not. This is accepted deliberately to keep the protocol executable by a single operator within the milestone window. The safety-critical layer is unaffected.

---

## 2. What this erratum does not change

- No hard gate (H1–H7) is added, removed, or altered.
- No value gate (VG1–VG3) is added, removed, or altered. VG2 remains mandatory.
- No threshold: not 0.667, not 0.800, not 10%, not 25%, not 30%, not $1.00, not 180 seconds, not 19/20.
- §I (reviewer preference removed as a gate, ties counted against the four-head system) is untouched.
- §J (canaries), §K (four passes), §L (no independent reviewer, sealed verdicts, adjudication by publication), §M, §O, §P, §Q, §R are untouched.
- §L.4 remains as written. Publishing the strongest counter-argument to each gate-determining judgment is expensive and is retained, because it is the primary substitute for the independent adjudicator this run does not have.

## 3. Freeze

With this erratum committed, v1.1 as corrected is final. No further erratum will be issued for this run. Any subsequent methodological change is v2.0 and applies only to a future run, per v1.1 §B and §C as corrected.
