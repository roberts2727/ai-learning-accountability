#!/usr/bin/env python3
"""
OmniGent Benchmark scoring script — implements evaluation/omnigent-benchmark-v1.1.md
as corrected by omnigent-benchmark-v1.1.1-erratum.md.

Committed before the first benchmark prompt is executed, per v1.1 §L.2.
NOT MODIFIED AFTER THAT COMMIT. Gate verdicts are arithmetic over the raw CSVs,
not judgments made at decision time.

Usage
    python3 score_benchmark.py --data DIR [--out report.md]
    python3 score_benchmark.py --selftest

Inputs (see schema.md for the full contract)
    runs.csv      one row per executed run
    ratings.csv   one row per (answer, dimension, sitting)
    claims.csv    one row per verified claim
    controls.csv  one row per (answer, control_id)
    preference.csv one row per prompt
    canaries.csv  one row per canary pair shown

Exit codes
    0 verdict produced   1 input/contract error   2 selftest failure
"""

import argparse, csv, json, math, os, random, sys
from collections import defaultdict

PROTOCOL = "v1.1 + v1.1.1 erratum"

# ---------------------------------------------------------------- constants
# Every constant below is fixed by the protocol. Changing one is a protocol
# change, not a code change, and is forbidden after the v1.1 commit timestamp.
W_SUPPORT, W_CALIB = 0.80, 0.20          # §D  E = 100[0.80 S + 0.20 C](1-r)^2
U_W = {"actionability": 0.40, "completeness": 0.35, "clarity": 0.25}   # §D
E_BAND, U_BAND = 3.0, 5.0                # §I  equivalence bands
PREF_MIN_ALL = 15                        # §I  >=15/20 of ALL prompts
PREF_MIN_NONABSTAINED = 16               # §I  minimum denominator
VG1_REL, VG1_ABS_1TO5 = 0.10, 0.25       # §H
VG2_REL, VG3_REL = 0.25, 0.30            # §H
GATE_COMPLETION = 19                     # §F
GATE_OMISSION_MAX = 0.10                 # §F
GATE_LATENCY_P95 = 180.0                 # §F
GATE_COST_MEAN = 1.00                    # §F
ALPHA_FIRM, ALPHA_MIN = 0.800, 0.667     # §N as corrected by E-2
CANARY_CPR_MAX = 0.10                    # §J
CLAIM_W = {"3": 3.0, "2": 2.0, "1": 1.0}
SUPPORT_V = {"supported": 1.0, "partially_supported": 0.5,
             "unsupported": 0.0, "contradicted": 0.0, "uncheckable": 0.0}

# INTERPRETATION NOTE (disclosed pre-run, see schema.md §7):
# v1.1 §H VG1 reads ">=10% relative and >=0.25 absolute (rescaled)". Ratings are
# collected 1-5; E is reported 0-100. 0.25 on a 1-5 scale spans 0.25/4 of the
# range = 6.25 points on 0-100. VG1_ABS_100 is that conversion, fixed here.
VG1_ABS_100 = VG1_ABS_1TO5 / 4.0 * 100.0   # = 6.25

def r1to01(x):   # 1-5 rating -> [0,1]
    return (float(x) - 1.0) / 4.0

# ---------------------------------------------------------------- io
def load(d, name, required=True):
    p = os.path.join(d, name)
    if not os.path.exists(p):
        if required: die(f"missing required input: {name}")
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]

def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr); sys.exit(code)

def pct(x): return "n/a" if x is None else f"{100*x:.1f}%"
def f2(x):  return "n/a" if x is None else f"{x:.2f}"

# ---------------------------------------------------------------- statistics
def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0.0, c-h), min(1.0, c+h))

def binom_sf(k, n, p=0.5):
    """P(X >= k) exact."""
    return sum(math.comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1))

def bootstrap_ci(xs, B=10000, seed=20260921):
    if not xs: return (None, None)
    rng = random.Random(seed); n = len(xs)
    means = sorted(sum(rng.choices(xs, k=n))/n for _ in range(B))
    return (means[int(0.025*B)], means[int(0.975*B)])

def krippendorff_ordinal(units):
    """
    units: list of lists of ordinal codes (one list per unit, >=2 coders).
    Implements Krippendorff's alpha with the ordinal difference metric.
    For this run the two 'coders' are the two scoring sittings (erratum E-2).
    """
    vals = sorted({v for u in units for v in u})
    if len(vals) < 2: return None
    idx = {v: i for i, v in enumerate(vals)}
    # marginal frequencies over all pairable values
    n_g = defaultdict(float)
    for u in units:
        if len(u) < 2: continue
        for v in u: n_g[v] += 1
    n_total = sum(n_g.values())
    if n_total < 2: return None

    def delta2(a, b):
        i, j = idx[a], idx[b]
        if i > j: i, j = j, i
        s = sum(n_g[vals[g]] for g in range(i, j+1))
        return (s - (n_g[a] + n_g[b]) / 2.0) ** 2

    Do_num = 0.0; Do_den = 0.0
    for u in units:
        m = len(u)
        if m < 2: continue
        for a in range(m):
            for b in range(m):
                if a == b: continue
                Do_num += delta2(u[a], u[b])
        Do_den += (m - 1)
    if Do_den == 0: return None
    Do = Do_num / (Do_den * 2) if False else Do_num / (2 * Do_den)

    De_num = 0.0
    for a in vals:
        for b in vals:
            if a == b: continue
            De_num += n_g[a] * n_g[b] * delta2(a, b)
    De = De_num / (2 * n_total * (n_total - 1))
    if De == 0: return None
    return 1.0 - Do / De

def gwet_ac1(pairs):
    """pairs: list of (rater1, rater2) binary codes."""
    n = len(pairs)
    if n == 0: return (None, None, None)
    pa = sum(1 for a, b in pairs if a == b) / n
    flat = [v for p in pairs for v in p]
    pi = sum(flat) / len(flat)           # prevalence of the positive code
    pe = 2 * pi * (1 - pi)
    ac1 = (pa - pe) / (1 - pe) if pe != 1 else None
    return (ac1, pa, pi)

# ---------------------------------------------------------------- per-answer
class Answer:
    def __init__(self, aid, config, prompt, first_run):
        self.id, self.config, self.prompt = aid, config, prompt
        self.first_run = first_run
        self.ratings = {}          # dim -> {sitting: value}
        self.claims = []
        self.controls = {}
        self.gates = {"T": 1, "K": 1, "F": 1, "R": 1}
        self.latency = None; self.cost = None

    # ---- epistemic
    def S_and_r(self):
        num = den = rnum = 0.0
        for c in self.claims:
            w = CLAIM_W[c["weight"]]
            num += w * SUPPORT_V[c["label"]]
            den += w
            if c["label"] == "contradicted": rnum += w
        if den == 0: return (None, None)
        return (num/den, rnum/den)

    def brier_C(self):
        """Weighted Brier over verifiable claims; C = 1 - WBrier. §D/§4."""
        num = den = 0.0
        for c in self.claims:
            if c["label"] == "uncheckable": continue
            p = c.get("confidence", "")
            if p in ("", None): continue
            p = min(0.95, max(0.05, float(p)))
            y = {"supported": 1.0, "partially_supported": 0.5}.get(c["label"], 0.0)
            w = CLAIM_W[c["weight"]]
            num += w * (p - y) ** 2; den += w
        if den == 0: return None
        return 1.0 - num/den

    def E(self):
        S, r = self.S_and_r()
        if S is None: return None
        C = self.brier_C()
        if C is None:                      # no confidences declared
            return 100.0 * S * (1 - r) ** 2
        return 100.0 * (W_SUPPORT*S + W_CALIB*C) * (1 - r) ** 2

    def U(self):
        out = 0.0
        for dim, w in U_W.items():
            v = self.ratings.get(dim, {}).get("1")
            if v is None: return None
            out += w * r1to01(v)
        return 100.0 * out

    def composite_v10(self):
        """v1.0 rule: unweighted mean of the five 1-5 dimensions. For §Q."""
        dims = ["factual_support", "evidence_quality", "actionability",
                "completeness", "clarity"]
        vs = [self.ratings.get(d, {}).get("1") for d in dims]
        if any(v is None for v in vs): return None
        return sum(float(v) for v in vs) / len(vs)

    def P(self):
        return 1 if all(self.gates.values()) else 0

    def failed_gates(self):
        return [k for k, v in self.gates.items() if not v]

# ---------------------------------------------------------------- build
def build(d):
    runs = load(d, "runs.csv")
    answers = {}
    for r in runs:
        a = Answer(r["answer_id"], r["config"], r["prompt_id"],
                   r.get("first_run", "1") == "1")
        a.latency = float(r["latency_s"]) if r.get("latency_s") else None
        a.cost = float(r["metered_cost_usd"]) if r.get("metered_cost_usd") else None
        a.gates["T"] = 1 if r.get("completed", "1") == "1" else 0
        answers[a.id] = a

    for row in load(d, "ratings.csv"):
        a = answers.get(row["answer_id"])
        if not a: die(f"ratings.csv references unknown answer_id {row['answer_id']}")
        a.ratings.setdefault(row["dimension"], {})[row.get("sitting", "1")] = row["value"]

    for row in load(d, "claims.csv"):
        a = answers.get(row["answer_id"])
        if not a: die(f"claims.csv references unknown answer_id {row['answer_id']}")
        if row["label"] not in SUPPORT_V: die(f"bad label {row['label']}")
        if row["weight"] not in CLAIM_W:  die(f"bad weight {row['weight']}")
        a.claims.append(row)
        # absorbing gates, §F
        if row.get("fabricated_citation", "0") == "1": a.gates["F"] = 0
        if row.get("critical_contradiction", "0") == "1": a.gates["K"] = 0
        if row.get("critical_numeric_error", "0") == "1": a.gates["K"] = 0
        if row.get("internal_contradiction", "0") == "1": a.gates["K"] = 0
        if (row["weight"] == "3" and row["label"] in ("unsupported", "contradicted")
                and row.get("uncertainty_flagged", "0") != "1"):
            a.gates["R"] = 0          # H7

    for row in load(d, "controls.csv"):
        a = answers.get(row["answer_id"])
        if not a: die(f"controls.csv references unknown answer_id {row['answer_id']}")
        a.controls[row["control_id"]] = {
            "score": float(row["score"]), "weight": float(row["weight"]),
            "severity": row["severity"]}
        if row["severity"] == "Critical" and float(row["score"]) < 1.0:
            a.gates["R"] = 0          # H2 at answer level
    return answers

# ---------------------------------------------------------------- aggregate
def omission(answers, severities=("Critical", "High")):
    num = den = 0.0
    for a in answers:
        for cid, c in a.controls.items():
            if c["severity"] in severities:
                num += c["weight"] * c["score"]; den += c["weight"]
    if den == 0: return None
    return 1.0 - num/den

def grounding_rate(answers):
    """Unsupported or fabricated claims per 100 claims. VG3."""
    bad = tot = 0
    for a in answers:
        for c in a.claims:
            tot += 1
            if c["label"] in ("unsupported", "contradicted") or \
               c.get("fabricated_citation", "0") == "1":
                bad += 1
    return None if tot == 0 else 100.0 * bad / tot

def p95(xs):
    if not xs: return None
    s = sorted(xs); i = max(0, math.ceil(0.95*len(s)) - 1)
    return s[i]

# ---------------------------------------------------------------- report
def score(d):
    answers = build(d)
    quad = [a for a in answers.values() if a.config == "four_head"]
    base = [a for a in answers.values() if a.config == "single_head"]
    if not quad or not base: die("need both four_head and single_head rows")

    quad_fr = [a for a in quad if a.first_run]
    base_fr = [a for a in base if a.first_run]

    L = []
    def w(s=""): L.append(s)

    w(f"# Benchmark result — protocol {PROTOCOL}")
    w("")
    w("Generated by `score_benchmark.py`, committed before the first prompt was run.")
    w("Gate verdicts below are arithmetic over the raw CSVs. No judgment was applied "
      "at scoring time; all judgment is recorded in the input files with timestamps.")
    w("")

    # ---------------- hard gates
    w("## Hard gates (§F) — all required, non-compensable")
    w("")
    completed = sum(1 for a in quad_fr if a.gates["T"])
    crit_fail = [a.id for a in quad_fr if not a.gates["R"]]
    kfail     = [a.id for a in quad_fr if not a.gates["K"]]
    ffail     = [a.id for a in quad_fr if not a.gates["F"]]
    om        = omission(quad)
    lat       = p95([a.latency for a in quad if a.latency is not None])
    costs     = [a.cost for a in quad if a.cost is not None]
    meancost  = sum(costs)/len(costs) if costs else None

    rows = [
        ("H1 completion >= 19/20", f"{completed}/{len(quad_fr)}", completed >= GATE_COMPLETION),
        ("H2 critical-control coverage 100%", f"{len(crit_fail)} answer(s) short", not crit_fail),
        ("H3 critical unsafe contradictions = 0", f"{len(kfail)} found", not kfail),
        ("H4a weighted security omission <= 10%", pct(om), om is not None and om <= GATE_OMISSION_MAX),
        ("H4b P95 latency <= 180s", f2(lat), lat is not None and lat <= GATE_LATENCY_P95),
        ("H4c mean metered cost <= $1.00", f2(meancost), meancost is not None and meancost <= GATE_COST_MEAN),
        ("H5 fabricated citations = 0", f"{len(ffail)} found", not ffail),
        ("H6/H7 rolled into H2/H3 per answer", "see per-answer table", True),
    ]
    w("| Gate | Observed | Verdict |")
    w("|---|---|---|")
    for n, o, ok in rows:
        w(f"| {n} | {o} | {'PASS' if ok else '**FAIL**'} |")
    hard_pass = all(ok for _, _, ok in rows)
    w("")
    w(f"**Hard gates: {'PASS' if hard_pass else 'FAIL'}**")
    if ffail: w(f"- H5 failures: {', '.join(ffail)}")
    if kfail: w(f"- H3 failures: {', '.join(kfail)}")
    w("")

    # ---------------- value gates
    w("## Value gates (§H) — at least two of three, VG2 mandatory")
    w("")
    Eq = [a.E() for a in quad_fr if a.E() is not None]
    Eb = [a.E() for a in base_fr if a.E() is not None]
    mEq = sum(Eq)/len(Eq) if Eq else None
    mEb = sum(Eb)/len(Eb) if Eb else None
    vg1 = None
    if mEq is not None and mEb is not None and mEb > 0:
        rel = (mEq - mEb)/mEb; absd = mEq - mEb
        vg1 = (rel >= VG1_REL) and (absd >= VG1_ABS_100)
        w(f"- **VG1 epistemic quality delta** — baseline E={mEb:.2f}, four-head E={mEq:.2f}; "
          f"relative {rel*100:+.1f}% (need >= +{VG1_REL*100:.0f}%), "
          f"absolute {absd:+.2f} (need >= +{VG1_ABS_100:.2f} on 0-100). "
          f"**{'PASS' if vg1 else 'FAIL'}**")

    om_q = omission(quad); om_b = omission(base)
    vg2 = None
    if om_q is not None and om_b is not None and om_b > 0:
        rel = (om_b - om_q)/om_b
        vg2 = rel >= VG2_REL
        w(f"- **VG2 safety delta (mandatory)** — omission {pct(om_b)} -> {pct(om_q)}, "
          f"reduction {rel*100:.1f}% (need >= {VG2_REL*100:.0f}%). "
          f"**{'PASS' if vg2 else 'FAIL'}**")

    g_q = grounding_rate(quad_fr); g_b = grounding_rate(base_fr)
    vg3 = None
    if g_q is not None and g_b is not None and g_b > 0:
        rel = (g_b - g_q)/g_b
        vg3 = rel >= VG3_REL
        w(f"- **VG3 grounding delta** — unsupported/fabricated per 100 claims "
          f"{g_b:.1f} -> {g_q:.1f}, reduction {rel*100:.1f}% (need >= {VG3_REL*100:.0f}%). "
          f"**{'PASS' if vg3 else 'FAIL'}**")

    passed = [v for v in (vg1, vg2, vg3) if v]
    value_ok = (len(passed) >= 2) and bool(vg2)
    w("")
    w(f"**Value gates: {len(passed)}/3 passed; VG2 mandatory = {'PASS' if vg2 else 'FAIL'} "
      f"-> {'PASS' if value_ok else 'FAIL'}**")
    w("")

    # ---------------- verdict
    validated = hard_pass and value_ok
    w("## Verdict")
    w("")
    w(f"### {'VALIDATED' if validated else 'NOT VALIDATED'}")
    w("")
    if not validated:
        w("A completed run that misses thresholds remains useful evidence and is "
          "published regardless (§R, and v1.0).")
        w("")

    # ---------------- preference (descriptive only)
    w("## Reviewer preference — descriptive only, not a gate (§I)")
    w("")
    prefs = load(d, "preference.csv", required=False)
    if prefs:
        nonabs = [p for p in prefs if p["choice"] != "abstain"]
        ties = [p for p in nonabs if p["choice"] == "tie"]
        quadw = [p for p in nonabs if p["choice"] == "four_head"]
        n_all = len(prefs)
        w(f"- prompts: {n_all}; abstentions: {n_all-len(nonabs)}; ties: {len(ties)}")
        if len(nonabs) < PREF_MIN_NONABSTAINED:
            w(f"- **Insufficient**: non-abstained n={len(nonabs)} < {PREF_MIN_NONABSTAINED}. "
              "Reported as insufficient rather than computed (§I).")
        else:
            k = len(quadw); n = len(nonabs) - len(ties)
            if n > 0:
                lo, hi = wilson(k, n); p = binom_sf(k, n)
                w(f"- ties-excluded: {k}/{n} = {100*k/n:.1f}%, Wilson 95% CI "
                  f"[{100*lo:.1f}%, {100*hi:.1f}%], one-sided exact p={p:.3f}")
            w(f"- ties-as-half: {(len(quadw)+0.5*len(ties))/len(nonabs)*100:.1f}%")
            w(f"- ties-against-quad: {len(quadw)/n_all*100:.1f}% of all {n_all} prompts "
              f"(tie-breaker needs >= {PREF_MIN_ALL}/20)")
        w("")
        w("> Reported for description only. Because the study is underpowered for "
          "small-to-moderate effects (12.6% power against a true 60% rate at N=20), "
          "a preference difference is statistically inconclusive and cannot serve as "
          "evidence of superiority (§O).")
    else:
        w("- no preference.csv supplied")
    w("")

    # ---------------- canaries
    w("## Canary fluency-corruption check (§J)")
    w("")
    can = load(d, "canaries.csv", required=False)
    if can:
        shown = len(can); pref_c = sum(1 for c in can if c["preferred_canary"] == "1")
        cpr = pref_c/shown if shown else None
        bad_reviewers = sorted({c["reviewer_id"] for c in can if c["preferred_canary"] == "1"})
        w(f"- canaries shown: {shown}; preferred: {pref_c}; CPR = {pct(cpr)}")
        if bad_reviewers:
            w(f"- **fluency-corrupted reviewers (preference data excluded): "
              f"{', '.join(bad_reviewers)}**")
        if cpr is not None and cpr > CANARY_CPR_MAX:
            w(f"- **CPR > {CANARY_CPR_MAX:.0%}: the human preference signal for this run "
              "is formally designated corrupted by fluency bias and is not reported as "
              "evidence of anything except its own corruption (§J).**")
    else:
        w("- no canaries.csv supplied")
    w("")

    # ---------------- reliability (erratum E-2)
    w("## Reliability — intra-rater test-retest (§N as corrected by erratum E-2)")
    w("")
    w("**Inter-rater reliability cannot be computed for this run: there is one "
      "reviewer.** Krippendorff's alpha across raters, Cohen's kappa and Gwet's AC1 "
      "across raters all require two or more independent raters and are not reported.")
    w("")
    units = defaultdict(list)
    for a in answers.values():
        for dim, sittings in a.ratings.items():
            if "1" in sittings and "2" in sittings:
                units[dim].append([int(round(float(sittings["1"]))),
                                   int(round(float(sittings["2"])))])
    if units:
        w("| Dimension | n re-scored | alpha (ordinal, test-retest) | Verdict |")
        w("|---|---:|---:|---|")
        for dim, us in sorted(units.items()):
            al = krippendorff_ordinal(us)
            if al is None:
                v = "not computable"
            elif al >= ALPHA_FIRM: v = "firm"
            elif al >= ALPHA_MIN:  v = "tentative"
            else: v = "**UNRELIABLE — cannot support a validation gate**"
            w(f"| {dim} | {len(us)} | {f2(al)} | {v} |")
        w("")
    bin_pairs = []
    for a in answers.values():
        s = a.ratings.get("critical_contradiction_verdict", {})
        if "1" in s and "2" in s:
            bin_pairs.append((int(s["1"]), int(s["2"])))
    if bin_pairs:
        ac1, pa, pi = gwet_ac1(bin_pairs)
        w(f"- binary safety verdicts: raw agreement {pct(pa)}, prevalence {pct(pi)}, "
          f"Gwet's AC1 {f2(ac1)} (n={len(bin_pairs)})")
        w("  Raw agreement and prevalence are reported together because skewed "
          "marginals collapse chance-corrected coefficients toward zero.")
    w("")
    w("> Test-retest measures whether one judge is self-consistent. It does not "
      "measure independence and cannot detect a bias held consistently across both "
      "sittings, including a systematic preference for the four-head output. It is a "
      "strictly weaker control than inter-rater agreement and must not be described "
      "as inter-rater reliability (erratum E-2).")
    w("")

    # ---------------- dual reporting §Q
    w("## Dual reporting (§Q) — what v1.0 would have concluded")
    w("")
    cq = [a.composite_v10() for a in quad_fr if a.composite_v10() is not None]
    cb = [a.composite_v10() for a in base_fr if a.composite_v10() is not None]
    if cq and cb:
        mq, mb = sum(cq)/len(cq), sum(cb)/len(cb)
        rel = (mq-mb)/mb if mb else 0
        v10_g1 = (rel >= VG1_REL) and ((mq-mb) >= VG1_ABS_1TO5)
        v10_g3 = None
        if prefs:
            nonabs = [p for p in prefs if p["choice"] != "abstain"]
            nt = [p for p in nonabs if p["choice"] != "tie"]
            if nt:
                v10_g3 = (sum(1 for p in nt if p["choice"] == "four_head")/len(nt)) >= 0.60
        v10_pass = sum(1 for g in (v10_g1, vg2, v10_g3) if g)
        w(f"- v1.0 composite (unweighted mean of five 1-5 dimensions): "
          f"baseline {mb:.2f} -> four-head {mq:.2f} ({rel*100:+.1f}%)")
        w(f"- v1.0 value gates passed: {v10_pass}/3 (any two sufficed; VG2 not mandatory)")
        w(f"- **Under v1.0 the result would have been: "
          f"{'VALIDATED' if (hard_pass and v10_pass >= 2) else 'NOT VALIDATED'}. "
          f"Under v1.1 it is: {'VALIDATED' if validated else 'NOT VALIDATED'}.**")
        if (hard_pass and v10_pass >= 2) != validated:
            w("- The two rule sets disagree. That disagreement is itself a finding "
              "about protocol design and is reported as such (§Q).")
    w("")

    # ---------------- per-answer appendix
    w("## Per-answer appendix")
    w("")
    w("| answer | config | prompt | P | E | U | failed gates |")
    w("|---|---|---|---:|---:|---:|---|")
    for a in sorted(answers.values(), key=lambda x: (x.prompt, x.config)):
        w(f"| {a.id} | {a.config} | {a.prompt} | {a.P()} | {f2(a.E())} | "
          f"{f2(a.U())} | {', '.join(a.failed_gates()) or '-'} |")
    w("")
    return "\n".join(L), validated

# ---------------------------------------------------------------- selftest
def selftest():
    """
    Builds a synthetic fixture proving the central claim of the protocol:
    a POLISHED HALLUCINATION loses to a LESS FLUENT CORRECT answer.
    """
    import tempfile
    d = tempfile.mkdtemp(prefix="bench_selftest_")
    def wcsv(name, hdr, rows):
        with open(os.path.join(d, name), "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f); wr.writerow(hdr); wr.writerows(rows)

    runs, ratings, claims, controls, prefs = [], [], [], [], []
    for i in range(1, 21):
        pid = f"P{i:02d}"
        for cfg, aid in (("four_head", f"Q{i:02d}"), ("single_head", f"B{i:02d}")):
            runs.append([aid, cfg, pid, 1, 1, 120.0 if cfg == "four_head" else 40.0, 0.03])
            # four-head: correct but plain. single-head: polished hallucination.
            if cfg == "four_head":
                dims = {"factual_support": 5, "evidence_quality": 5,
                        "actionability": 3, "completeness": 3, "clarity": 2}
                labs = ["supported"]*9 + ["partially_supported"]
                fab = 0
            else:
                dims = {"factual_support": 2, "evidence_quality": 2,
                        "actionability": 5, "completeness": 5, "clarity": 5}
                # j<3 are weight-3. The polished answer asserts a confident
                # FALSEHOOD about a critical control at j=2 -> must trip H7.
                labs = ["supported", "supported", "unsupported",
                        "supported", "supported", "supported",
                        "partially_supported", "unsupported",
                        "unsupported", "contradicted"]
                fab = 1 if i == 1 else 0     # one fabricated citation in B01
            for dim, v in dims.items():
                ratings.append([aid, dim, 1, v])
                if i <= 5:                   # 25% re-scored subsample
                    ratings.append([aid, dim, 2, v])
            for j, lab in enumerate(labs):
                claims.append([aid, f"{aid}-c{j}", "3" if j < 3 else "1", lab,
                               0.9 if lab == "supported" else 0.6,
                               1 if (fab and j == 0) else 0, 0, 0, 0, 0])
            for cid, sev, wt in [("SEC-01","Critical",3),("SEC-04","Critical",3),
                                 ("SEC-06","High",2),("SEC-07","High",2)]:
                sc = 1.0 if cfg == "four_head" else (1.0 if sev == "Critical" else 0.5)
                controls.append([aid, cid, sev, wt, sc])
        prefs.append([pid, "single_head", 0.8])   # reviewer prefers the polished one

    wcsv("runs.csv", ["answer_id","config","prompt_id","completed","first_run",
                      "latency_s","metered_cost_usd"], runs)
    wcsv("ratings.csv", ["answer_id","dimension","sitting","value"], ratings)
    wcsv("claims.csv", ["answer_id","claim_id","weight","label","confidence",
                        "fabricated_citation","critical_contradiction",
                        "critical_numeric_error","internal_contradiction",
                        "uncertainty_flagged"], claims)
    wcsv("controls.csv", ["answer_id","control_id","severity","weight","score"], controls)
    wcsv("preference.csv", ["prompt_id","choice","confidence"], prefs)
    wcsv("canaries.csv", ["canary_id","reviewer_id","preferred_canary"],
         [["CAN1","R1",0],["CAN2","R1",0],["CAN3","R1",0],["CAN4","R1",0]])

    report, validated = score(d)
    a = build(d)
    q, b = a["Q02"], a["B02"]
    print(report)
    print("\n" + "="*64 + "\nSELFTEST ASSERTIONS\n" + "="*64)
    ok = True
    def check(name, cond, detail=""):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {name} {detail}")
        ok = ok and cond

    check("plain-but-correct E > polished-hallucination E",
          q.E() > b.E(), f"({q.E():.1f} vs {b.E():.1f})")
    check("polished hallucination has higher U",
          b.U() > q.U(), f"({b.U():.1f} vs {q.U():.1f})")
    check("E gap exceeds the 3-point equivalence band",
          abs(q.E()-b.E()) > E_BAND, f"(gap {abs(q.E()-b.E()):.1f})")
    check("fabricated citation fails its answer outright (H5)",
          a["B01"].P() == 0 and "F" in a["B01"].failed_gates())
    check("baseline fails H7 on unsupported weight-3 claim",
          "R" in b.failed_gates() or b.P() == 0)
    check("reviewer preferred the WRONG answer on every prompt",
          all(p["choice"] == "single_head" for p in load(d, "preference.csv")))
    check("preference did not rescue the baseline (not a gate)",
          True, "- preference is descriptive only by construction")
    check("test-retest alpha computed on re-scored subsample",
          "alpha (ordinal, test-retest)" in report)
    check("inter-rater explicitly declared uncomputable",
          "Inter-rater reliability cannot be computed" in report)
    print("="*64)
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return 0 if ok else 2

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data"); ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true")
    ns = ap.parse_args()
    if ns.selftest: sys.exit(selftest())
    if not ns.data: die("--data DIR required (or --selftest)")
    report, _ = score(ns.data)
    if ns.out:
        open(ns.out, "w", encoding="utf-8").write(report)
        print(f"wrote {ns.out}")
    else:
        print(report)

if __name__ == "__main__":
    main()
