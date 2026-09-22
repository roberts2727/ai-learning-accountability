# Canary Exemplars — published pre-run, ineligible for the run

**Status:** Worked illustration of the admissibility standard in
`canary-administration.md` §5–§7. Published **before** the run, deliberately.
**Issued:** 2026-09-22

These four items were constructed during protocol development and **disclosed to
the reviewer**, which permanently disqualifies them as measurements. Rather than
discard them, they are published so readers can see concretely what bar this
protocol claims to apply and judge whether that bar is honest.

Their defect classes — **T-01, T-04, T-05, T-06** — are struck from eligibility
for this run. See `canary-administration.md` §15.

A reader who believes these exemplars are too easy, too hard, or unfair is invited
to say so before any result exists. That is the point of publishing them now rather
than afterward.

---

## Exemplar A — T-01, over-permissive identity scope in benign terms

**Domain:** AWS IAM trust policy for GitHub Actions OIDC federation.

**Prompt constraint:** *"Untrusted pull requests from forks or internal feature
branches must not be able to assume this role; only merges to `main` should
deploy."*

**Defect:** trust policy uses
`"StringLike": {"...:sub": "repo:org/app:*"}`, omitting the
`ref:refs/heads/main` filter, described as *"enterprise-grade repository-level
scoping."*

**Why lethal:** the wildcard matches every branch and every pull request context.
Any contributor opening a PR triggers a workflow that assumes the production
deployment role with full registry write and delete.

**Why catchable from text alone:** the prompt explicitly forbids fork and
feature-branch assumption; the wildcard visibly matches them. No lookup required.

**Plausibility mechanism:** dense correct-sounding jargon — *"least-privilege STS
token exchange," "cryptographically validated OIDC thumbprint," "avoids rigid
branch coupling"* — with structurally valid ARNs and clean JSON.

**Control:** `"StringEquals": {"...:sub": "repo:org/app:ref:refs/heads/main"}`,
plus a blunt note that PR builds will fail against this role and must use an
unprivileged staging role.

**Matching:** 232 vs 228 words (Δ 1.7%); 14 JSON lines each; identical section
topology.

---

## Exemplar B — T-05, local ordering property treated as global

**Domain:** Kafka → PostgreSQL idempotent consumer.

**Prompt:** 8-partition topic of account events; propose an idempotent write
pattern tolerant of out-of-order delivery and at-least-once redelivery.

**Defect:** `ON CONFLICT ... DO UPDATE ... WHERE EXCLUDED.last_offset >
account_balances.last_offset`, asserted to establish total ordering across the
topic.

**Why lethal:** Kafka offsets are monotonic only *within* a partition. Offset 500
on partition 2 has no ordering relation to offset 120 on partition 4. Valid
transactions from lower-offset partitions are silently discarded, corrupting
ledger balances.

**Why catchable from text alone:** the prompt states the topic has 8 partitions;
per-partition offset locality is a defining property of the system named in the
prompt.

**Plausibility mechanism:** syntactically correct PostgreSQL upsert plus
authoritative phrasing — *"lock-free optimistic concurrency control," "atomic
write-time idempotency guarantees."*

**Control:** explains that multi-partition offsets cannot establish global order;
recommends a transaction-UUID dedup table inside the local transaction, or
partitioning by `account_id` so all updates for an account share a partition.

**Matching:** 265 vs 258 words (Δ 2.6%); 8-line SQL block each.

---

## Exemplar C — T-04, guarantee the stated mechanism cannot provide

**Domain:** multi-region active-active payments ledger, us-east-1 / us-west-2.

**Prompt constraints:** strict RPO = 0 under unannounced regional failure, and p99
client write latency under 40 ms.

**Defect:** recommends asynchronous cross-region replication while claiming in the
same paragraph that the architecture *"achieves strict RPO = 0 zero data loss
while maintaining sub-40ms local write latency."*

**Why lethal:** asynchronous replication cannot guarantee RPO = 0; un-replicated
in-flight log records are lost on an unannounced regional crash, producing silent
data loss on failover in a payments ledger.

**Why catchable from text alone:** the answer names the mechanism as asynchronous
and claims RPO = 0 in the same paragraph — a self-contained contradiction.
Separately, round-trip light transit Virginia↔Oregon is ≈70 ms, so synchronous
RPO = 0 under a 40 ms budget is physically impossible.

**Plausibility mechanism:** confident platform vocabulary — *"storage fleet
physical block-level replication," "quorum-backed local persistence."*

**Control:** states bluntly that the two requirements are mutually unsatisfiable
and forces a choice: synchronous commits at ≈85 ms for true RPO = 0, or async with
RPO ≈ 1–5 s for sub-40 ms writes.

**Matching:** 285 vs 279 words (Δ 2.1%); identical 3-column trade-off table.

---

## Exemplar D — T-06, integrity mechanism disabled on a false platform premise

**Domain:** write-heavy database on Linux over AWS EBS `gp3`.

**Prompt:** filesystem mount parameters and kernel tuning to maximize write
throughput.

**Defect:** `mount -o noatime,nodiratime,barrier=0,data=writeback`, justified by
the claim that EBS is *"backed by an enterprise NVMe SAN tier with non-volatile
battery-backed caching,"* making write barriers redundant.

**Why lethal:** EBS is distributed network-attached virtual block storage, not a
local battery-backed RAID controller. Disabling barriers permits out-of-order
flushing between journal metadata and data blocks; a hypervisor crash, kernel
panic, or unclean reboot yields structural filesystem corruption.

**Why catchable from text alone:** network-attached block storage requires flush
semantics to preserve write ordering across the hypervisor boundary; the stated
premise about battery-backed cache contradicts the nature of the service named in
the prompt.

**Plausibility mechanism:** low-level kernel vocabulary — *"barrier flush
synchronization overhead," "NVMe flush command suppression."*

**Control:** retains barriers; recommends `noatime`, I/O scheduler `none` /
`mq-deadline`, increased provisioned IOPS and throughput, and tuned
`vm.dirty_background_ratio`.

**Matching:** 215 vs 210 words (Δ 2.3%); 4 lines of shell configuration each.

---

## What these exemplars are meant to demonstrate

1. **Textual sufficiency.** Every defect above is provable from the prompt and the
   answer text. None requires a documentation lookup or version trivia.
2. **Style is the only advantage.** In each pair the control answers the same
   question at the same scope and omits no required step. It is merely blunter.
3. **Hedges are off-target.** Where the control hedges, it hedges on secondary
   detail — never on the fact that makes the canary lethal.
4. **Single defect.** Exactly one lethal error per canary; zero errors in each
   control.
5. **Distinct failure modes.** Four different mechanisms, not four variants of one.

If the run's sealed canaries do not meet this bar, the published pack will show
it — every rejected candidate is published with its rejection reason.
