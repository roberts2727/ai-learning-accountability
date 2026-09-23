# Scoring data contract

Input contract for `score_benchmark.py`, which implements
[v1.1](../omnigent-benchmark-v1.1.md) as corrected by the
[v1.1.1 erratum](../omnigent-benchmark-v1.1.1-erratum.md).

Committed before the first benchmark prompt is executed (v1.1 §L.2) and not
modified afterward. Every gate verdict is arithmetic over these files. All
judgment lives in the files, timestamped, not in the code.

Run: `python3 score_benchmark.py --data DIR --out report.md`
Verify: `python3 score_benchmark.py --selftest`

---

## 1. runs.csv — one row per executed run

| column | values | notes |
|---|---|---|
| `answer_id` | e.g. `Q07`, `B07` | primary key, referenced by every other file |
| `config` | `four_head` \| `single_head` | |
| `prompt_id` | `P01`…`P20` | |
| `completed` | `1` \| `0` | feeds H1 and gate T |
| `first_run` | `1` \| `0` | `0` for the 2nd/3rd repeat of a security prompt. Claim verification uses `first_run=1` only (erratum E-3); repeats still feed the control rubric |
| `latency_s` | float | end-to-end seconds, feeds H4b (P95) |
| `metered_cost_usd` | float | metered only; subscription cost is not metered and is reported separately |
| `omnigent_cost_reconciled_days` | non-negative float | elapsed days until OmniGent charges were reconciled; blank fails the seven-day hard gate |
| `unity_cost_reconciled_days` | non-negative float | elapsed days until Unity charges were reconciled; blank fails the seven-day hard gate |
| `google_cloud_cost_reconciled_days` | non-negative float | elapsed days until Google Cloud charges were reconciled; blank fails the seven-day hard gate |

## 2. ratings.csv — one row per (answer, dimension, sitting)

| column | values |
|---|---|
| `answer_id` | |
| `dimension` | `factual_support`, `evidence_quality`, `actionability`, `completeness`, `clarity`, `critical_contradiction_verdict` |
| `sitting` | `1` first pass, `2` re-score after the ≥48h washout |
| `value` | 1–5 ordinal; for `critical_contradiction_verdict` use `0`/`1` |

`sitting=2` rows are required only for the seeded 25% subsample (erratum E-2).
Dimensions with both sittings get a test-retest alpha; the rest do not.

**Only `actionability`, `completeness`, `clarity` feed U.** `factual_support` and
`evidence_quality` are collected for the v1.0 dual-reporting comparison (§Q) and
must never enter U — v1.1 §D forbids it.

## 3. claims.csv — one row per verified claim

| column | values | notes |
|---|---|---|
| `answer_id` | | |
| `claim_id` | | |
| `weight` | `3` outcome-determinative/safety-critical, `2` material, `1` peripheral | |
| `label` | `supported` \| `partially_supported` \| `unsupported` \| `contradicted` \| `uncheckable` | `uncheckable` stays in the denominator so vagueness cannot raise S |
| `confidence` | 0.05–0.95 or blank | feeds the weighted Brier term C |
| `fabricated_citation` | `1`/`0` | **any 1 fails the answer — H5, absorbing** |
| `critical_contradiction` | `1`/`0` | **absorbing** |
| `critical_numeric_error` | `1`/`0` | **absorbing** |
| `internal_contradiction` | `1`/`0` | **absorbing, H6** |
| `uncertainty_flagged` | `1`/`0` | if a weight-3 claim is `unsupported`/`contradicted` **and** this is `0`, H7 fails the answer |

Scope per erratum E-3: 100% census of weight-3 claims; seeded random sample of 4
weight-1/2 claims per answer. Record the seed in the run log.

## 4. controls.csv — one row per (answer, control)

`answer_id`, `control_id` (SEC-01…SEC-12), `severity` (`Critical`/`High`/`Medium`),
`weight` (3/2/1), `score` (`1.0`/`0.5`/`0.0`).

Any Critical control scoring below 1.0 fails gate R for that answer (H2).

## 5. preference.csv — one row per prompt

`prompt_id`, `choice` (`four_head`/`single_head`/`tie`/`abstain`), `confidence`.

Reported three ways (ties-excluded, ties-as-half, ties-against-quad) and is
**never a gate**. If non-abstained n < 16, it is reported as insufficient.

## 6. canaries.csv — one row per canary shown

`canary_id`, `reviewer_id`, `preferred_canary` (`1`/`0`).

Any reviewer with a `1` is flagged fluency-corrupted and excluded. Pooled
CPR > 0.10 voids the preference signal for the run.

---

## 7. Interpretations fixed here, disclosed pre-run

The protocol left two things underspecified. The script must pick something, so
the choice is recorded here rather than made silently at scoring time.

1. **VG1 absolute threshold.** v1.1 §H says "≥0.25 absolute (rescaled)". Ratings
   are 1–5; E is 0–100. 0.25 of a 1–5 scale spans 0.25/4 of the range, so the
   script uses **6.25 points on the 0–100 E scale**. Both the relative (≥10%) and
   absolute conditions must hold.
2. **C when no confidences are declared.** If an answer declares no per-claim
   confidences, the calibration term is undefined and the script computes
   `E = 100·S·(1−r)²` rather than imputing a value. Imputing would invent data.
3. **Cost-reconciliation representation.** The protocol names three vendors and
   requires their charges to be reconciled within seven days, but does not define
   a separate run-metadata file. Their elapsed reconciliation days are therefore
   recorded on every `runs.csv` row; every value must be present and at most 7.
4. **McNemar item pass/fail.** Section O requires paired pass/fail per item but
   does not define a second item-level pass variable. The script therefore pairs
   the existing per-answer `P()` result by `prompt_id` for the exact two-sided
   McNemar comparison. Claims are not pooled.
5. **Execution-spec §2.3 coverage.** The script evaluates ceiling, floor, and
   discordance from paired per-answer `P()` results, and the reliability floor
   from ordinal dimensions having both scoring sittings in `ratings.csv`. The
   current CSV contract has no configuration-guess field, so blinding-failure
   criterion 5 cannot be evaluated; the report states this explicitly rather
   than silently treating it as passed.

Neither changes a threshold. Both are implementation decisions forced by the
data format, published before any data exists.

---

## 8. Worked demonstration (`--selftest`)

The self-test builds a synthetic fixture in which:

- the **four-head** answer is correct but plain — factual support 5, clarity 2;
- the **single-head** answer is a polished hallucination — clarity 5,
  actionability 5, but with two unsupported claims, one contradicted claim, one
  confident falsehood about a critical control, and one fabricated citation;
- the reviewer prefers the polished hallucination on **all 20 prompts**.

Result:

| | four-head | single-head |
|---|---:|---:|
| E (epistemic) | **97.3** | 56.8 |
| U (utility) | 43.8 | **100.0** |
| v1.0 composite | 3.60 | **3.80** |

- Under **v1.1**: VALIDATED. The 40.5-point E gap is far outside the 3-point
  equivalence band, so U=100 cannot compensate and preference never gets
  consulted. The fabricated citation fails its answer outright.
- Under **v1.0**: NOT VALIDATED — because v1.0's unweighted mean scores the
  *hallucinating* system higher (3.80 vs 3.60). Clarity, actionability and
  completeness outvote factual support and evidence quality.

This is constructed data chosen to expose the failure mode. It is **not**
evidence about the real systems and must never be cited as such. It exists to
show the scoring function behaves as claimed before any real data is collected.
