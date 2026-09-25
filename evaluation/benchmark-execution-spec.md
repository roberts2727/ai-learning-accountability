# Benchmark Execution Specification

**Status:** Specification of procedures that omnigent-benchmark-v1.1.md left
undefined, plus a correction to how the study's own findings may be described.
**No threshold, count, gate, or decision rule in v1.1 is altered.** This is not an
amendment and not an erratum.
**Issued:** 2026-09-22 — before any benchmark prompt has been executed.

---

## 1. The study is a pilot. It cannot validate.

### 1.1 The arithmetic that forces this

The preregistered primary analysis is an exact McNemar test on discordant pairs.
McNemar discards concordant pairs; conditional on D discordances the null is
Binomial(D, ½). The most favourable possible result — every discordance favouring
the four-head configuration — yields

    p_exact = 2 · (1/2)^D = 2^(1−D)

    D = 5  →  p = 0.0625     (not significant)
    D = 6  →  p = 0.03125    (significant)

**At least six discordant pairs, all in the same direction, are required for any
significant result at two-sided α = 0.05.** With n = 20 distinct prompts, the
smallest observable significant effect is therefore

    Δ_min = 6/20 = 0.30      (30 percentage points)

One contrary discordance breaks it: 7:1 among eight discordances gives p = 0.0703.
Significance requires 8:1 among nine.

Ceiling compounds this. Under independence, q = p₀ + p₁ − 2p₀p₁; at
p₀ = p₁ = 0.98 the expected discordant count across 20 items is **0.784**. Positive
pairing covariance — which shared prompt difficulty produces — makes discordance
rarer still. And improvement is capped at Δ ≤ 1 − p₀, so a 98%-accurate baseline
admits at most a two-point gain.

### 1.2 Prompts required for a real test

Best case, assuming **zero** baseline-favourable discordances:

| True one-way effect | n for ≈80% power |
|---:|---:|
| 0.05 | 157 |
| 0.10 | 78 |
| 0.15 | 52 |
| 0.20 | 39 |

With discordance in both directions (q = 0.20, Δ = 0.10), the matched-pair normal
approximation gives **n ≈ 154**.

### 1.3 Required language — abstract, not footnote

The prompt count is frozen at 20 by v1.0 and is not changed. What changes is what
the study claims. The following appears in the abstract of any published report and
in any public post citing a result:

> **This is a preregistered pilot, not a validation study.** With 20 paired
> prompts, the preregistered primary analysis (exact McNemar on discordant pairs)
> cannot return a significant result unless the observed improvement is at least
> 30 percentage points, because significance requires at least six discordant
> pairs all favouring one configuration. Detecting a realistic 10-point effect at
> 80% power would require approximately 78 prompts in the most favourable case and
> approximately 154 with discordance in both directions. This study is therefore
> **incapable of demonstrating that the four-head workflow is better, and equally
> incapable of demonstrating that it is not.** A null result here is not evidence
> of equivalence.
>
> What this study can contribute is the parameters a properly powered study would
> need and which are not currently published: item difficulty distribution,
> discordance rate q, directional asymmetry θ, within-prompt variance, intra-answer
> claim correlation ρ_c, and intra-rater reliability. Those are reported as the
> primary output.

**Forbidden:** any headline of the form "the four-head workflow was validated," "no
difference was found," or "the ensemble outperformed the baseline," with or without
qualification elsewhere in the document.

---

## 2. Self-invalidation criteria

Preregistered conditions under which the benchmark declares **itself**
uninformative. Checked and reported before any comparison is interpreted.

The study is reported as **INSTRUMENT UNINFORMATIVE** if any of:

1. **Ceiling.** ≥ 60% of items are concordant-correct for both configurations.
2. **Floor.** ≥ 30% of items are concordant-incorrect for both configurations.
3. **Insufficient discordance.** Fewer than 6 discordant pairs total — in which
   case significance was arithmetically unreachable regardless of performance.
4. **Reliability floor.** Test-retest Gwet's AC1 (§7) below 0.667 for the
   gate-carrying set `{critical_contradiction_verdict}`.
5. **Blinding failure.** Configuration-guess accuracy (§7.3) significantly above
   chance, in which case the study is reported as *blind compromised* rather than
   described as blinded.

Under any of these the conclusion is **"underpowered or compromised instrument,"**
never "no difference" and never "ensemble wins on the margin." The ceiling and
floor diagnostics are computed and published before the primary comparison is
looked at.

---

## 3. Mechanical claim decomposition

**Rationale.** Claim decomposition is prior to claim labeling and sets the
denominator of every score computed. It is highly discretionary, resistant to
blinding (answer shape often reveals configuration), and untouched by any control
on prompt selection. It is the single largest uncontrolled degree of freedom in the
protocol.

**Procedure.**

1. All 60 answers are decomposed into atomic claims by a model instance in
   **neither configuration** and not used elsewhere in this protocol.
2. The decomposition is run with configuration labels stripped and answer order
   randomised.
3. **The full decomposition is published before any label or weight is assigned.**
   Its SHA-256 is committed at that point.
4. The reviewer may not add, merge, split, or delete claims. Disagreement with a
   decomposition is recorded as a logged note against the claim and does not alter
   it.
5. Weight assignment (3/2/1) and labeling (Supported / Partially / Unsupported /
   Contradicted / Uncheckable) occur only after the decomposition hash is
   published.

The denominator stops being the reviewer's choice.

---

## 4. Pre-run reference keys — closing the coverage circularity

**Defect addressed.** v1.1 §F gates on *"100% critical-control coverage in the
final synthesis."* If the critical controls for an item are identified by reading
the answer, an answer that omits a control has defined that control out of
existence and the gate is unfalsifiable. The gate is frozen; the procedure for
determining its referent was never specified. It is specified here.

**Every item must ship, before the run, with a reference key containing:**

1. **Critical controls** — which of SEC-01…SEC-12 are critical *for this item*,
   fixed in advance. Gate evaluation uses this list and nothing else.
2. **Must-hit claim set** — the claims a correct answer is required to contain.
   Minimum **6 must-hit claims, of which at least 3 are weight-3.** An item that
   cannot support this floor is too shallow to enter the pool.
3. **Ground-truth dossier** — the specific public sources against which each
   anticipated claim class will be adjudicated: vendor documentation, CIS
   benchmarks, CVE/CVSS records, RFCs, regulatory text. **If the dossier cannot be
   written before the run, the item does not enter the pool.**

**Anchoring control.** The reference key governs *admissibility and gate
evaluation*, not the scope of scoring. Unanticipated claims are still decomposed and
labeled. An unanticipated claim that cannot be checked against a public source is
labeled **Uncheckable and counted in the denominator**. No label assigned during
scoring removes an item from gate determination.

Dossiers and keys are published at reveal.

---

## 5. Verification scope — frozen erratum E-3

Claim verification applies to first-run answers only: 20 prompts × 2
configurations = 40 answers. Repeat runs of the five architecture/security prompts
are scored on the security-control rubric only.

Within each first-run answer, verification comprises:

- a 100% census of all weight-3 claims, with no cap; and
- a random sample of 4 claims drawn from the combined weight-1 and weight-2 pool,
  using a published seed before verification begins.

S is computed over those verified claims. The weight-1/weight-2 component is
reported with a sampling confidence interval; the weight-3 census is reported
without one. H5, H6, and H7 remain full-answer checks: their scope is not limited
by the claim sample.

---

## 6. Analysis — unit, aggregation, and the repeat structure

### 6.1 The inferential unit is the prompt

Claims are observations nested within prompt × answer × configuration cells;
repeated generations add a further nested level. With intra-answer claim
correlation ρ_c and m claims per answer, the cluster design effect is
1 + (m−1)ρ_c. For J = 20, m = 30:

| ρ_c | effective n |
|---:|---:|
| 0 | 600 |
| 0.10 | 154 |
| 0.30 | 62 |
| 0.50 | 39 |
| 1.00 | 20 |

Real ρ_c is high — a single misunderstood premise produces many related omissions.
**Claim-level scoring improves resolution within a prompt; it cannot manufacture
independent prompt replication.** Claim counts are never reported as if they were
independent trials.

### 6.2 Repeats are descriptive only

5 items × 3 runs = 15 of 30 runs. Security prompts are 25% of items but **50% of
runs**, so any run-pooled statistic silently double-weights that stratum.

- **Primary analysis is item-weighted.** Repeats collapse to one item-level
  endpoint before comparison; the paired sample size remains **n = 20, not 30**.
- Run-weighted figures are secondary and explicitly labeled as such. The run-level
  design effect is n_eff = 30/(1+ρ), between 15 and 30.
- **Aggregation rule, preregistered:** mean per-run omission is primary; "any
  omission across the three repeats" is reported as a secondary robustness
  endpoint. **Majority-of-three is not used** — one lethal failure must not vanish
  because two runs were safe.
- **Stability statistic, preregistered:** max−min spread of weighted omission
  across the three runs; whether the *same* critical control is missed each time.
  The weight-3 label-flip term is deferred to v2.0 per D-9 because erratum E-3
  scores repeat runs on the security-control rubric only.
- **n = 3 estimates variance badly. The stability comparison is descriptive only.
  No inferential claim is made about which configuration is more stable.**

### 6.3 Test selection

Exact McNemar applies to the paired binary item endpoint. It does **not** apply to
the weighted continuous claim score; where a continuous score is compared, a paired
permutation test with a preregistered statistic is used, and this is stated rather
than substituting one test for the other silently.

---

## 7. Scoring-integrity controls

### 7.1 Blind re-score
A random **25%** subsample of answers, drawn with a published seed before any
scoring begins, is re-scored after a minimum **48-hour** washout, blind to the
first-pass scores and blind to configuration identity. Intra-rater agreement
(Krippendorff's α for ordinal dimensions; raw percent agreement, prevalence, and
Gwet's AC1 for binary safety verdicts) is computed and published. This is labeled
as test-retest reliability wherever reported, never as inter-rater reliability.

**Pre-declared consequence:** every reported delta is presented against this
number. If the applicable statistic is below 0.667 on a dimension, that dimension
is reported as **UNRELIABLE** and cannot support a gate (§2.4). A 5-point delta
measured by a rater who agrees with himself at α = 0.6 is not a finding.

### 7.2 Decomposition immutability
Per §3.4, the reviewer cannot alter the published decomposition.

### 7.3 Blinding manipulation check
For every answer scored, the reviewer records a guess of which configuration
produced it, before scoring. **Guess accuracy is published.** A four-head synthesis
is expected to leak through blinding via length, structure, and hedging; measuring
the leak is honest where asserting its absence would not be.

---

## 8. Prompt-set composition

### 8.1 Archetype balance — the honesty requirement

A set drawn only from archetypes where ensembling is expected to help cannot
distinguish "the ensemble works" from "only favourable questions were asked."
Ensembling has a threshold — under strict three-of-four majority with ties counted
as failure, p_E = 4p³ − 3p⁴ exceeds p only when p > (1+√13)/6 ≈ 0.768 — and four
distinct harm mechanisms. Both must be exercised.

| Band | Count | Content |
|---|---:|---|
| **Favourable archetypes** | 14 | conjunctive multi-constraint omission; trojan default; unsatisfiable specification / safe refusal; cross-silo boundary collision; stateful sequence inversion |
| **Null-or-negative archetypes** | **6** | single-fact retrieval; latency-critical decision; post-training-cutoff knowledge; opinion-merging with no correct answer; nested within-answer contradiction; adversarial defect-catching where synthesis may blunt obviousness |

**Per-archetype results are reported in the main body, adjacent to the headline
figure. They are never placed in an appendix.** If the four-head configuration
loses on the null-or-negative band, the reported conclusion is restricted
accordingly — e.g. "improves on synthesis-heavy multi-constraint tasks, degrades on
latency-bound and single-fact tasks" — and the restriction appears in the abstract.

### 8.2 Domain quotas

Expertise is for constructing items and locating ground truth, **never for being
the ground truth.**

- **Tier A** (reviewer's professional domain: Azure, Databricks, enterprise
  identity): **≤ 10 of 20.** Claims adjudicated against citable public documents,
  not reviewer judgement.
- **Tier B** (outside the reviewer's expertise, documentary ground truth —
  regulatory text, published standards, RFCs): **≥ 6 of 20.**
- **Tier C** (not adjudicable by anyone from public sources): excluded.
- **≤ 8** items may share a single vendor ecosystem.
- **≤ 2** of the 5 security items may be Tier A.

**Preregistered moderator analysis.** Tier A and Tier B deltas are reported
separately. **Committed in advance:** an ensemble advantage appearing only in
Tier A is interpreted as diagnostic of selection or scoring bias, not of ensemble
benefit.

### 8.3 Priming control
Every finalised prompt is passed through a rephrasing step that preserves semantics
while removing multi-perspective priming language ("consider several viewpoints,"
"weigh competing perspectives"). Phrasing that invites a multi-perspective answer
hands the four-head configuration a structural advantage before generation. Original
and rephrased text are both published.

---

## 9. Pool, draw, and commitment ordering

- **Candidate pool: 60 items** under the §8 quota cells, each with a §4 reference
  key and dossier.
- **Difficulty screen:** an item enters the pool only if a screening model **in
  neither configuration** produces ≥ 1 weight-3 error against its reference key.
  Screener ID, date, and raw outputs published. *Caveat, pre-stated: selecting
  items where a model errs partly selects for noise; "both configurations beat the
  screener" is not a finding.*
- **Selection: 20 drawn by public verifiable randomness** — a named future beacon
  value at a named future timestamp, seed-derivation function published in advance.
  The draw is recomputable by any reader from pool + beacon + algorithm.
- **Security stratum drawn the same way**, and **all drawn security items are
  repeated**, which dissolves the "which five get repeated" decision rather than
  adjudicating it.
- **Commitment order — the order is the argument:**

      1. system freeze (both configurations: model IDs, versions, system prompts,
         synthesiser prompt, retrieval config, temperature, head composition) → hash
      2. this specification + v1.1 + v1.1.1 → hash
      3. candidate pool + reference keys + dossiers → hash
      4. beacon draw
      5. runs, interleaved across configurations, never blocked

  All commitments go to **one named public append-only log**. Any hash posted there
  and never revealed invalidates the study. The full pool including undrawn items is
  published, so a reader can check whether undrawn items look systematically harder.

- **Replacement escape hatch:** closed list of admissible reasons (irreparable
  ambiguity on close reading; requires non-public data; publication legally or
  safety problematic). **Hard cap: ≤ 3 of 20; exceeding it invalidates the run.**
  Replacements drawn from the same quota cell by the same beacon. Every invocation
  logged with reason and timestamp.

- **Baseline parity attestation.** The baseline configuration receives documented
  equivalent prompt-engineering effort. Asymmetric effort on the baseline is the
  most common way a solo benchmark flatters itself and requires no bad faith. The
  attestation states what was done to each side and is published.

---

## 10. Adversarial item donation

The methodological challenger from the public exchange is invited to contribute up
to **5 candidate items** to the pool, sight-unseen by either configuration, under
the same quota rules, reference-key requirement, and dossier requirement as all
other items. Donated items are marked as such in the published pool and are subject
to the same beacon draw.

**The invitation and its outcome are published either way.** A declination is
recorded without characterisation. Acceptance does not imply the donor endorses the
project, the protocol, or any result, and no statement to that effect will be made.

---

## 11. Known limitations

1. **The study cannot validate or refute the hypothesis.** §1.
2. **Hash commitment is only as strong as its venue.** A solo researcher could in
   principle generate several pools and reveal the favourable one. Partial closure:
   single named append-only log, unrevealed hashes invalidate, full pool published.
   This does not close the hole completely.
3. **Difficulty screening partly selects for noise**, not only for difficulty.
4. **Scoring drift remains the largest residual risk.** §3 and §7 reduce it; no
   procedure available to a single unaudited rater eliminates it.
5. **Repeats measure stability badly at n = 3** and support no inferential claim.
6. **Blinding is expected to leak** and is measured rather than asserted.
7. **Self-preregistration with no external party is a trust-reducing device, not a
   trust-eliminating one.**
