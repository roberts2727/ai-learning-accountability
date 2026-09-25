# Canary Administration Protocol

**Status:** Specification of procedures that omnigent-benchmark-v1.1.md §J left
undefined. **No threshold, count, or decision rule in §J is altered.** This is not
an amendment and not an erratum.
**Issued:** 2026-09-22 — before any benchmark prompt has been executed.
**Governs:** v1.1 §J, as corrected by the v1.1.1 erratum.

---

## 1. What §J fixes, and what it leaves blank

**Fixed by §J and not touched here:** four canary pairs; interleaved into the
blinded review queue; not disclosed to reviewers; excluded from all primary
calculations; CPR = (# canaries preferred) / (# canaries shown); a reviewer who
prefers any canary is flagged fluency-corrupted and their preference data is
excluded; pooled CPR > 0.10 designates the preference signal corrupted.

**Left blank by §J and specified here:** who authors canaries; how instances are
generated and selected; what makes a canary admissible; how the queue is ordered;
what is captured at review time; what is published and when; and what happens to a
tied comparison if preference is voided.

---

## 2. Epistemic status — falsifier, not validator

Contamination from self-authorship is **one-directional**. Knowledge of a planted
defect can only make the reviewer *more* likely to reject the canary. It cannot
make the reviewer prefer it. Therefore:

- **A canary pass is uninformative.** It is jointly explained by "robust to
  fluency" and "recognized the planted item," and these cannot be separated.
- **A canary failure is conclusive.** Preferring a lethally defective answer under
  conditions where every bias pushes the other way admits no benign reading.

Independently of blinding, the pass state licenses no positive claim. With four
canaries and zero preferred, the exact one-sided 95% binomial upper bound on the
true fluency-capture rate is **1 − 0.05^(1/4) ≈ 0.527**. A clean sweep is
consistent with a reviewer who would be captured more than half the time.

**CPR is therefore reported as a one-sided kill switch.** It can refute the
preference signal. It cannot certify it. No positive inference about reviewer
robustness is drawn in this run, and none is available from this design.

### 2.1 The frozen rule, restated exactly

With four completed binary canaries, C = Σ Xᵢ:

    PreferenceValid      = 1{C = 0}
    PreferenceCorrupted  = 1{C ≥ 1}

Because C/4 > 0.10 ⟺ C ≥ 1, the pooled threshold and the per-reviewer rule are
**the same event**. The 0.10 clause introduces no additional decision criterion
and must not be described as independent corroboration or a second safeguard.
This is a clarification of committed mathematics, not a change to it.

### 2.2 Known miscalibration, disclosed not fixed

Under the "any" rule, a non-corrupted reviewer with ordinary per-item error rate p
loses all preference data with probability 1 − (1−p)⁴:

| p | P(all preference data voided) |
|---:|---:|
| 0.02 | 0.0776 |
| 0.05 | 0.1855 |
| 0.10 | 0.3439 |
| 0.15 | 0.4780 |

Above p ≈ 1 − 2^(−1/4) ≈ 0.159, a sound reviewer is rejected more often than
retained. Detection power against a corrupted reviewer is 1 − (1−q)⁴: 0.684 at
q = 0.25, 0.938 at q = 0.50.

**This rule is frozen and will be executed as written.** The miscalibration is
disclosed here and must be repeated in the report. A calibrated replacement
(n = 25, invalidate at C ≥ 4, giving α = 0.034 at p₀ = 0.05 and power = 0.904 at
q = 0.25) is recorded as a **v1.2 recommendation for a future run** and is not
applied here.

---

## 3. Taxonomy commitment

Defect *classes* are committed in `canary-taxonomy.md` and hashed pre-run. The
reviewer knows the classes. The reviewer must never know the instances.
Classes T-01, T-04, T-05, T-06 are burned (§15). Eligible: T-02, T-07, T-09,
T-10, consistent with the completed audit recorded in `canary-spec-changelog.md`.

---

## 4. Generation, audit, selection — the reviewer touches none of it

1. **Specification only.** The reviewer writes abstract defect specs, never text.
2. **Delegated generation.** A generator model instance produces a candidate pool
   from the eligible classes. Model ID, prompt, and seed are recorded. **The pool
   is written directly to `sealed/` and is not returned to the reviewer's
   session.**
3. **Delegated audit.** A *different* model instance applies §5–§7 to each
   candidate and emits only `candidate_NN: ADMISSIBLE | REJECTED + reason`. The
   reviewer sees the verdict line, never the candidate.
4. **Mechanical selection.** Four admissible candidates are drawn by a
   pre-committed seeded function. No human chooses.
5. **Sealing.** The pool, audit transcripts, selected IDs, and per-canary
   adjudication keys are written to `sealed/canary-pack.json`, hashed with
   SHA-256, and the hash is committed pre-run.

**Honest limit:** sealing here is procedural, not cryptographic confinement — the
reviewer has filesystem access and could open the pack. What the hash provides is
*tamper evidence after the fact*, not prevention. The protection is the commitment
plus publication, not the file permissions. State this in the report.

---

## 5. Admissibility criteria — all must hold, applied pre-seal by the auditor

1. **Textual sufficiency.** The defect is determinable from prompt + answer text
   alone. The auditor must produce a one-sentence disproof citing only strings
   present in the answer.
2. **Pair unambiguity.** Five detector instances spanning at least three model
   families, shown both answers unlabeled with balanced side assignment and asked
   only which they would act on, with no indication that a defect exists.
   Admissible only if **at least 4 of 5 choose the control.** This verifies that
   the canary is genuinely defective and that the control is genuinely
   non-inferior; it is the strongest external corroboration of C4, C5 and C6
   available without a human third party.

   **This criterion does not calibrate difficulty for a human reviewer, and no
   such calibration is available in this run.** A detectability band of
   [0.4, 0.9] was originally specified here and is **withdrawn**: measured against
   the candidate pool it returned a detection rate of 1.00 under two independently
   framed probes (defect-hunting and neutral paired preference), i.e. it sat at
   ceiling and carried no information. The withdrawal, the measurements that
   caused it, and the timing are recorded in `canary-spec-changelog.md`.

   Note that this criterion and P7b measure different constructs and must not be
   conflated. **P7b is a fairness property of the item** — is the defect derivable
   from the text without lookup? **This criterion is an objectivity property of
   the pair** — do independent parties agree which answer is worse? Neither speaks
   to how hard the item is for a fatigued human reviewer, which remains untested
   (§14.7).

3. **Taxonomy and domain membership.** Belongs to an eligible class and sits inside
   the benchmark's declared domain. No trivia, no out-of-scope expertise.
4. **Single defect, clean distractors.** Exactly one lethal defect in the canary;
   zero errors in the alternative.
5. **Alternative non-inferiority.** The dry alternative must be strictly ≥ on
   correctness and safety, answer the same question at the same scope, and omit no
   materially required step the canary supplies.
6. **Style is the only legitimate advantage.** If the canary is also genuinely more
   complete, better scoped, or more actionable, preferring it is defensible
   engineering judgment, **not** fluency corruption. The canary's entire edge must
   reduce to fluency, formatting, confidence, and tone. Scoring such an item as
   corruption is a measurement error that indicts the reviewer for being right.
7. **Hedges must be off-target.** Hedging never sits on the decisive point. If the
   correct answer hedges on the fact that makes the canary lethal, preferring the
   confident wrong answer is partially rational and the item is inadmissible.
8. **Sealed adjudication key.** Each admitted canary ships with defect identity,
   exact location, one-sentence disproof, detectability score, and full checklist
   scoring. Hashed pre-run, published post-run.

### 5.1 No post-hoc invalidation

A canary may be invalidated **only during the pre-run audit.** After the queue
manifest is hashed, a canary cannot be reclassified as unfair. A fairness objection
raised after adjudication is admissible only if it rests on a property already
recorded in the sealed adjudication key. Any other objection is logged verbatim in
a published section titled **"Post-hoc objections (not applied)"** and does not
alter CPR.

This is what separates "the measurement worked and I dislike the result" from "the
instrument was broken," and it gives a real grievance somewhere honest to go
without letting it touch the number.

---

## 6. Isomorphic Pair Standard — surface-form matching

The only systematic difference between a canary and its counterpart must be
polish-vs-correctness. Verified mechanically before sealing:

| Dimension | Constraint | Method |
|---|---|---|
| Token length | within ±7.5% | `tiktoken` cl100k_base |
| Structure | identical header / bullet / numbered-list counts | markdown node parse |
| Code artifacts | same count, same language tag, line count ±2 | regex parse |
| Recommendations | exactly equal count of concrete actions | auditor semantic count |
| Reading grade | Flesch-Kincaid within ±1.0 | automated |
| Named-entity density | equal count of services / tools / protocols | automated |

Canaries must additionally match the **real arms' output distribution** on length,
heading structure, code-block density, and hedge frequency. If synthetic items are
stylistically identifiable as synthetic, the leak has merely moved. Publish the
comparison of canary surface statistics against the 40 real answers.

---

## 7. Detectability — three-stage gate, executable solo

1. **Formal invariant proof.** Lethality demonstrable in ≤ 3 deductive steps from
   fundamental invariants. If the proof requires an empirical footnote
   ("only true if the provider changed default X in 2023"), **reject**.
2. **Decontextualized sentence test.** Extract only the defective line. If a
   competent engineer cannot answer "yes, that is wrong" within 10 seconds of
   reading it in isolation, the defect is too subtle. **Reject.**
3. **Static analyzer baseline.** For code and configuration, run standard
   open-source tooling (`tfsec`, `checkov`, `trivy`, `shellcheck`). A high/critical
   finding makes lethality an objective property of the artifact rather than the
   author's opinion.

Stage 3 is the closest available substitute for third-party adjudication: it
outsources the fairness judgment to a tool the researcher did not write.

---

## 8. Queue layout

24 items = 20 real + 4 canary.

- **Burn-in:** items 1–2 are always real, for scoring calibration.
- **Cooldown:** items 23–24 are always real, to prevent end-of-task guessing.
- **Permuted block randomization:** remaining 20 items form 4 blocks of 6
  (5 real + 1 canary); the canary occupies slot 3, 4, 5, or 6 within its block by
  pre-committed seed. Canaries are never at fixed intervals.
- **Left/right counterbalancing:** presentation side assigned by independent coin
  flip per item, P(canary = A) = 0.5.
- **Sessions:** four sessions of 6 items, ≥ 4 hours apart, maximum 2 per day.
- **Time bounds:** hard minimum 3 minutes per item to prevent skimming; soft
  maximum 12 minutes to prevent exhaustive reverse-engineering.

**Vigilance contamination:** detecting a canary shifts the reviewer from evaluating
usefulness to adversarial defect-hunting, which biases subsequent real items. If
mean decision time rises > 100% on items following a canary, the run is flagged for
vigilance contamination in the report.

---

## 9. Review-time capture — measure the unblinding, do not assert it away

For **every** item, real and canary, the review record requires:

1. **Suspected-synthetic flag** (yes/no).
2. **Free-text defect callout** — "what, if anything, is wrong with A? with B?" —
   entered **before** the preference is recorded.
3. **Dwell time**, captured by tooling, not self-reported.

Report CPR overall and conditioned on the suspicion flag. Report canary dwell time
against the real-item dwell distribution; anomalously long dwell on canaries is
quantitative evidence of recognition and is published whether or not it flatters
the result.

The callout field separates two failure modes §J collapses: **did not see the
flaw** versus **saw the flaw and preferred the answer anyway.**

---

## 10. Sequential unblinding — the single strongest safeguard

> All 24 queue items are adjudicated in one randomized pass. CPR is computed and
> **published before arm identities are unblinded.** Under no circumstances does
> arm-level data become visible before the canary verdicts are public.

Once CPR is public it cannot be traded against the result, because the result is
not yet known. Absent a third party, this is the only mechanism that removes the
motive rather than merely documenting it.

Supporting mechanics, in descending order of how much they bind:

1. **Manifest completeness.** The review tool requires an adjudication for every ID
   in the hashed manifest and refuses to emit results with gaps. Quiet
   non-execution therefore requires fabrication rather than omission.
2. **Tool-captured, append-only log**, hashed at close.
3. **Pre-written failure text** (§12).
4. **Amendment discipline.** §J may be revised only by a v1.2 committed *before any
   canary is adjudicated*. Any change after a verdict is visible is post-hoc
   rationalization and is labelled as such, in its own section, not in methods.

**None of this prevents fraud.** It raises the cost of silent fraud from editing a
file to fabricating a hash-consistent record in advance, and makes the fabrication
auditable. Self-preregistration with no external party is a trust-*reducing*
device, not a trust-*eliminating* one. That sentence belongs in the limitations.

---

## 11. Publication schedule

**Pre-run (published, timestamped, hashed):** the taxonomy (class names only); this
document in full; canary count; generator and auditor model IDs, prompts, seeds;
SHA-256 of the sealed pack; SHA-256 of the queue manifest; the §12 failure
paragraph; and `canary-exemplars.md`.

**During the run:** nothing. Any mid-run publication is an unblinding event.

**Immediately after adjudication, before unblinding the arms:** CPR, the four
per-canary verdicts, defect callouts, suspicion flags, dwell times.

**Final publication:** the entire sealed pack unredacted — including every
candidate *not* selected and every candidate the auditor rejected, with reasons.
The rejected set is the evidence against cherry-picking soft canaries and is the
part a hostile reader will want most.

**Canaries are single-use.** Full publication burns them permanently. No
unpublished reserve pool is retained; a private reserve is exactly the kind of
unauditable instrument this machinery exists to eliminate.

**Non-execution is publishable data.** If canaries are dropped or skipped, that
fact and its timestamped reason are published under §P.

---

## 12. Pre-written failure paragraph

Committed now, before it is known whether it will be needed. To be published
verbatim if C ≥ 1:

> One or more canary items were preferred over their correct counterparts
> (CPR = [X]). Under §J this designates the human preference signal for this run
> corrupted by fluency bias. No conclusion of any kind is drawn from reviewer
> preference. The preference data is published in full below as raw data under
> this corruption finding, and the comparison between configurations rests solely
> on the objective measures. The canary that fired, its counterpart, and its sealed
> adjudication key are published in full so that readers may judge the fairness of
> the item independently. This outcome was a preregistered possible result of a
> mechanism adopted in response to a public methodological challenge; it is
> reported without qualification.

---

## 13. Tie-resolution fallback — disposition committed now

§I consults preference only within the equivalence band. §J can void preference
entirely. **v1.1 specifies no fallback for a tied comparison when preference is
voided.** Inventing one now would be an amendment.

**Committed disposition:** if C ≥ 1, comparisons falling inside the equivalence
band are reported as **"unresolved by the preregistered decision rules."** No
post-hoc winner is assigned. The gap is logged as a known defect for v1.2.

Additionally, report the realized decision impact directly: across 20 prompts, let
M be the number entering the joint tie band and R ≤ M the number where preference
changes the reported disposition. Canary invalidation can affect at most R
decisions; report R/20, with R = 0 if no comparison enters the band. This is more
informative than calling the mechanism "load-bearing."

---

## 14. Known limitations — stated, not mitigated away

1. **A pass proves nothing.** §2. The best possible outcome of this instrument is
   uninformative.
2. **The detectability band was withdrawn, not satisfied.** The original §5.2
   calibrated canary difficulty using model detectors — circular, since the
   benchmark's thesis concerns exactly that detection capability. Measured, it
   returned 1.00 under both probe framings and was uninformative at ceiling. It is
   replaced by a pair-unambiguity check, which verifies a different and weaker
   proposition.
3. **Four canaries cannot be both specific and sensitive.** §2.2.
4. **Ecological mismatch.** Real model comparison involves subtle trade-offs where
   both answers are viable, not adversarial defect-hunting. A reviewer who prefers a
   polished answer while evaluating architectural layout has not thereby shown that
   preferences on the 20 non-adversarial prompts are meaningless.
5. **Residual reviewer knowledge.** After §4, the reviewer still knows canaries
   exist, that there are four, that they come from four named classes, and that they
   are fluent-vs-dry pairs. That leak is real; it is now measured (§9) rather than
   denied.
6. **Sealing is procedural, not cryptographic.** §4.
7. **Canary difficulty relative to a human reviewer is untested.** No human pilot
   subjects were available (§L). Model detectors cannot substitute: they read every
   token with uniform attention, while a reviewer in a fourth session does not. It
   is therefore unknown whether these canaries are hard enough to discriminate. If
   they are trivially easy for the reviewer, CPR = 0 is guaranteed and carries no
   information — which §2 already concedes on independent grounds.
8. **One detector returned an incomplete result.** In the pair-unambiguity probe,
   one of five instances returned verdicts for 4 of 8 items and stopped. Affected
   items are scored on completed verdicts only (n=4 rather than n=5). The partial
   result is published as-is rather than re-run.

---

## 15. Contamination disclosure

During protocol development, four worked canary designs — instantiating classes
T-01, T-04, T-05, T-06 — were produced and **disclosed to the reviewer.** They are
therefore permanently unusable as measurements for this run.

Rather than discard them, they are published pre-run in `canary-exemplars.md` as
the worked illustration of the §5–§7 standard, so that readers can see concretely
what bar this protocol claims to apply and judge whether it is honest. Their four
classes are struck from eligibility.

This disclosure is made because a protocol whose subject is unsupported claims
cannot itself conceal a procedural breach, however minor.

---

## 16. Exploratory measurement — not preregistered, not gating

The canary pack is additionally run through **both configurations** to measure
whether each system detects the planted defect. This measurement requires no human
judgment, is unaffected by the blinding problem entirely, and may prove more
informative than CPR itself. Per v1.1 §C it is reported only under
**"Exploratory — not preregistered,"** is never used to determine validation, and
never appears in a headline claim.
