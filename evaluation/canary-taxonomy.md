# Canary Defect Taxonomy — committed pre-run

**Status:** Specification of a procedure §J left undefined. Alters no threshold,
count, or decision rule in omnigent-benchmark-v1.1.md.
**Issued:** 2026-09-22 — before any benchmark prompt has been executed.

This file names the *classes* of defect from which canary instances may be drawn.
It does not contain, and must never contain, any canary instance. The reviewer may
read this file. The reviewer must never read the generated instance pool.

## Defect classes

| ID | Class | Lethality mechanism |
|---|---|---|
| **T-01** | Over-permissive network or identity scope described in benign operational terms | Grants access far beyond the stated requirement while sounding like scoping |
| **T-02** | Control bypass justified by an operational metric | Removes an approval, review, or safety gate "to reduce MTTR / cost / latency" |
| **T-03** | Fabricated API surface, configuration key, or policy block | Named construct does not exist; config silently no-ops or fails closed at the worst time |
| **T-04** | Durability or consistency guarantee the stated mechanism cannot provide | Asserts RPO/RTO/isolation the named technology structurally cannot deliver |
| **T-05** | Cross-boundary ordering or identity assumption that holds only locally | Treats a partition-, node-, or region-local property as global |
| **T-06** | Safety or integrity mechanism disabled on an incorrect platform premise | Turns off a barrier/flush/verification based on a false property of the substrate |
| **T-07** | Self-contradiction within the same answer | Recommendation violates a constraint the answer itself stated earlier |
| **T-08** | Secret or credential exposure presented as a convenience pattern | Places material in a location readable beyond its trust boundary |
| **T-09** | Silent data-loss path presented as cleanup or optimization | Destructive operation without a guard, framed as hygiene |
| **T-10** | Misapplied isolation or consistency level presented as a performance win | Correctness-relevant setting weakened for throughput without disclosing the exchange |

## Classes burned as published exemplars — NOT eligible for the run

**T-01, T-04, T-05, T-06** were instantiated as worked examples during protocol
development and disclosed to the reviewer. They are published in
`canary-exemplars.md` as part of the fairness standard and are permanently
ineligible for this run. See `canary-administration.md` §15.

**Eligible classes for this run: T-02, T-07, T-09, T-10.**

## Commitment

The SHA-256 of this file is recorded in the pre-run commit. Canary instances are
generated from the eligible classes only, by the pipeline in
`canary-administration.md` §4, and are not read by the reviewer before review.
