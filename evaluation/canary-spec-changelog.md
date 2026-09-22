# Canary Specification Changelog

**Purpose.** `canary-administration.md` specifies procedures that v1.1 §J left
undefined. It was drafted, tested against a real candidate pool, and revised
**before being committed, hashed, or published**, and before any benchmark prompt
was executed. This file records every revision, what was known at the time, and
what caused it.

**Why this file exists.** A specification that arrives clean invites the question
of what was discarded on the way. Publishing the sequence is cheaper than being
asked for it. Nothing here alters v1.1 §J, whose count, thresholds, and decision
rule are frozen and untouched throughout.

**State at every entry below:** zero benchmark prompts executed, zero real answers
generated, no configuration compared to any other. No revision below could have
advantaged either configuration, because no configuration output existed.

---

## C-01 — Pool regenerated for length

**Observed:** first candidate pool satisfied pair-internal token matching (±7.5%,
all 12 passing) but produced answers of 92–113 tokens (~70–85 words).

**Problem:** real benchmark answers are multi-hundred-word technical responses. A
75-word item is identifiable as synthetic on length alone, defeating the blinding
the pack exists to support. The generation instruction enforced pair matching but
omitted distribution matching.

**Action:** regenerated all 12 candidates at 450–700 tokens. Resulting mean 520.7
(canary) / 518.8 (control), pair delta 0.20–1.53%.

**Superseded pool retained** at `sealed/superseded/canary-candidate-pool-v1.json`,
SHA-256 `e6fad6af...`, for publication.

---

## C-02 — §6 distribution check resequenced

**Observed:** pair-internal deltas came out at mean 0.70% — far tighter than §6
requires and tighter than is useful. Real A/B pairs from two different systems will
not be matched to four tokens. Perfect symmetry is itself a tell.

**Problem:** §6 requires canaries to match the real arms' output distribution, but
the real answers do not exist yet. The check was specified at a point in the
sequence where it cannot be executed.

**Action:** §6 amended to run the distribution check **after the 40 real answers
are generated and before the queue is sealed**, tuning canary pair deltas to sit
inside the observed real distribution while remaining under the ±7.5% ceiling.
Generating answers is not adjudicating them, so this occurs before any frozen
constraint binds.

---

## C-03 — Two defect classes eliminated by independent audit

**Observed:** the generating model passed all 12 of its own candidates on all 7
self-checks, three times, including after an explicit instruction to be
adversarial. An independent auditor instance rejected 4 of 12.

**Finding — self-assessment by the generating model carries no information.** This
is the empirical justification for the delegated audit in §4.3, which had been
adopted on principle.

| Class | Result | Criterion |
|---|---|---|
| T-03 fabricated API / config key | both rejected | P7b |
| T-08 credential exposure | both rejected | C4 |

**T-03 is a structural limit, not a generation defect.** A fabricated construct
cannot be recognized as fabricated from an isolated line without knowing the real
surface — which is a lookup, which P7b forbids. **The canary mechanism therefore
cannot test fabrication**, the failure mode that motivated the amendment and the
subject of hard gate H5. Fabrication is covered instead by claim verification
(§E), where lookup is permitted. Recorded in §14; no further regeneration
attempted for this class.

**T-08 is a generation artifact.** Expanding answers from ~100 to ~520 tokens is
the mechanism by which a canary acquires a second defect or a control acquires a
first. Recoverable by regeneration; not regenerated in this run.

---

## C-04 — Detectability band withdrawn

This is the most consequential revision and the one most exposed to the charge of
tuning. The full sequence:

**Original §5.2 (as drafted):** five detector instances, neutral probe *"is
anything in this answer wrong or dangerous?"*, admissible only if detection rate
∈ [0.4, 0.9], precommitted and not to be tuned after seeing results.

**Measurement 1.** Five instances (Pi ×2, Qwen ×2, Claude ×1; the generating model
excluded). Detection **40/40 = 1.00**. On a literal reading, all eight surviving
candidates inadmissible.

**Diagnosis offered at the time:** the probe wording primed defect-hunting and did
not model the review task, which asks for a preference rather than a fault.
A contradiction was also identified between two drafted criteria — **P7b demands
the defect be obvious within ten seconds from an isolated line, while §5.2 forbids
it being detected more than 90% of the time.** Any item passing one is likely to
fail the other.

**Commitment made before the second measurement**, recorded here because it was
made in advance and is now moot: a rate below 0.4 would be read against
measurement 1, such that low-under-preference but high-under-defect-hunting would
indicate a genuine fluency effect rather than an invisible defect.

**Measurement 2.** Same eight items rebuilt as a blinded paired-preference task —
both answers unlabeled, **forced 4A/4B side balance**, seed `20260921`, neutral
question *"which would you act on?"*, no indication that a defect existed. Five
instances across three model families.

    pooled detection            36/36 = 1.000
    side-choice distribution    19 A / 17 B   (no position bias)
    per-item rate               1.00 on all 8 items

**The diagnosis was wrong.** Reframing the probe changed nothing. The
leading-question hypothesis is falsified.

**Conclusion.** §5.2 was aimed at the wrong question. Its purpose was to calibrate
difficulty **for a human reviewer**; it was measured with **model detectors**,
which is the circularity identified as the design's weakest link. Models read every
token with uniform attention; a reviewer in a fourth session does not. Without
human pilot subjects — unavailable under §L — canary difficulty for the population
that matters cannot be calibrated at all.

**Action.** The band is **withdrawn, not satisfied**. It is replaced by a
**pair-unambiguity** criterion: ≥4 of 5 detectors across ≥3 model families must
choose the control. All eight candidates pass at 5/5.

**What the replacement does and does not claim.** Unanimity across three families
with balanced sides is strong evidence that each canary is genuinely defective and
each control genuinely non-inferior — independent corroboration of C4, C5 and C6,
and the closest thing to third-party adjudication this protocol contains. It says
**nothing** about whether the items are hard enough to discriminate a human
reviewer. That is now §14.7, an untested assumption.

**Effect on the protocol's claims: none.** §2 already holds, on independent
binomial grounds, that a canary pass licenses no positive inference. This
revision removes a comfort that was never load-bearing. The kill switch is
unchanged: a failure remains conclusive.

---

## C-05 — Detector deviation

One of five instances in measurement 2 returned verdicts for 4 of 8 items and
stopped. Affected items are scored on completed verdicts only (n=4 rather than
n=5); unanimity is unaffected. The partial result is published as-is rather than
re-run. Recorded in §14.8.

---

## C-06 — Contamination disclosures

**C-06a — exemplars burned deliberately.** Four worked canary designs (classes
T-01, T-04, T-05, T-06) were produced during development and shown to the
reviewer. They are permanently ineligible and are published pre-run in
`canary-exemplars.md` as the worked illustration of the admissibility bar. Their
classes are struck from eligibility.

**C-06b — assistant-side leakage, three occurrences.** While supervising
generation, the assistant viewed candidate content on three occasions by reading
sub-agent session transcripts rather than querying metadata. The reviewer was not
exposed and no candidate content was reproduced to the reviewer. A working rule
was adopted after the third occurrence: **verification of blinded artifacts goes
through metadata-only queries, never session history.**

This is disclosed because the reviewer's blinding is the mechanism §J depends on,
and a partial breach on the supervising side is the kind of detail that is cheap
to disclose now and expensive to have discovered later.

---

## Selection

Performed after the audit and the pair-unambiguity probe, by seeded draw with no
human choice.

    selection seed      20260921
    rule                one candidate per surviving defect class
    surviving classes   T-02, T-07, T-09, T-10
    admissible pool     8 candidates (2 per surviving class)
    selected            cand_01, cand_05, cand_09, cand_11

**Disclosure on the selection rule.** Stratification by class was specified
*after* the audit revealed which classes survived. It is recorded here rather than
presented as a prior decision. It cannot advantage either configuration — no
configuration output exists — and its effect is to maximise failure-mode coverage
across the four canaries, which is strictly harder than an unstratified draw that
might have selected two items of the same type.

---

## Artifact hashes at specification close

    canary-candidate-pool.json     72280cc070795bd1...
    audit-transcript.json          ab05afa806875575...
    probe-blinded-items.json       419a1112b9fa3910...
    probe-results.json             b5b5fb92fe00e345...
    canary-selection.json          df87989c99e579bd...
    superseded pool v1             e6fad6afb3012213...

Full-length hashes are recorded in `sealed/pool-manifest.json`. Every file listed
is published after the run, including the superseded pool, the four rejected
candidates with reasons, both probe measurements, and this changelog.
