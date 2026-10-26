# Explore the Evidence — HQ V1

[Portfolio](../../README.md) / [HQ Evidence Map](README.md) / Explore the Evidence

🟧 **10-MINUTE ROUTE · EXPLORE THE EVIDENCE**

This is the broader tour of how I planned, built, verified and failure-tested the HQ campus. It covers the engineering record as a whole, not just one or two interesting failures. The links open the source documents; the summaries here explain what to look for without having to read every page or CLI capture.

**GitHub is the source of truth.** The interactive site helps explain the network visually, while the original plans, test results and evidence remain in this repository.

| Stop | Time | Where to look |
|---|---:|---|
| [01 · Design and scope](#01--design-and-scope) | 1 min | What was planned and why |
| [02 · Implementation and verification](#02--implementation-and-verification) | 1 min | How the build was recorded and checked |
| [03 · Failure-test planning](#03--failure-test-planning) | 1½ min | What each test was supposed to prove |
| [04 · Test matrix and reports](#04--test-matrix-and-reports) | 1½ min | Actual PASS, FAIL and INCONCLUSIVE outcomes |
| [05 · Original evidence](#05--original-evidence) | 1½ min | CLI and traffic results behind the conclusions |
| [06 · Troubleshooting and engineering review](#06--troubleshooting-and-engineering-review) | 2 min | What the unexpected results revealed |
| [07 · Acceptance and next steps](#07--acceptance-and-next-steps) | 1½ min | What is closed and what remains open |

## 01 · Design and scope

**The starting point:** [HQ Campus Design](../../docs/hq-campus-design.md) · [Behind the Design](../../docs/hq-behind-the-design.md)

HQ was designed as the first campus of a larger multi-site lab. Its two edge routers, two distribution switches and access switch fit inside the five-node CML Free limit. The design records the VLAN and addressing plan, HSRP/STP alignment, routed `/31` links, OSPF Area 10, ECMP and deliberate higher-cost alternatives. The narrative explains the choices and trade-offs, not just the final topology.

## 02 · Implementation and verification

**The build trail:** [HQ Implementation](../../docs/implementation/hq/README.md) · [Build Log](../../docs/implementation/hq/build-log.md) · [Verification Plan](../../docs/implementation/hq/verification-plan.md)

Phases 01–09 record the progression from basic Layer 2 configuration through gateway redundancy and routed path engineering. Each verification ID links the planned check to retained CLI or other evidence. The Build Log also ties engineering changes to Git history, so a reviewer can follow how the configuration developed rather than judging one final export.

## 03 · Failure-test planning

**Before the faults:** [Testing Methodology](../../docs/implementation/hq/phase-10-testing-methodology.md) · [Phase 10 Test Plan](../../docs/implementation/hq/phase-10-test-plan.md)

The test plan keeps the original objectives and acceptance expectations separate from the results. The methodology describes baselines, traffic sources, probe interpretation, failure injection, recovery and the limits of a five-node simulation. In particular, a successful recovery does not turn an earlier failed continuity test into a pass.

## 04 · Test matrix and reports

**The results:** [Phase 10 Test Matrix and Report Index](failure-tests/README.md)

Phase 10 covers **14 test IDs across 13 report entries**, including the shared 10.02–10.03 record. From that index, compare a successful alternative route ([10.04 — PASS](failure-tests/10.04/HQ-VP-10.04-cross-link-failure.md)), a retained return-path failure ([10.08 — FAIL](failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md)), and a result whose evidence did not close every criterion ([10.12 — INCONCLUSIVE](failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md)). The result labels and limitations have not been tidied away for presentation.

## 05 · Original evidence

**Follow a claim back to a capture:** [HQ Evidence Map](README.md#verification-records) · [10.04 failure CLI](failure-tests/10.04/10.04-failure.md) · [10.08 session record](failure-tests/10.08/10.08-session-record.md)

The test reports summarise the observations. Their linked evidence records show the routing tables, protocol state, interface behaviour, forwarding checks and traffic probes used to reach each conclusion. For example, 10.04 links the higher-cost OSPF alternative to actual route and CEF entries; 10.08 links apparent routing health to failed return traffic. Raw captures remain distinguishable from later interpretation.

## 06 · Troubleshooting and engineering review

**What the results meant:** [Troubleshooting Register](../../docs/implementation/hq/troubleshooting.md) · [Phase 10 Engineering Review](../../docs/implementation/hq/phase-10-engineering-review.md)

The review joins the individual observations into an engineering picture. It covers the Po20 one-sided member loss, progressive Po30 behaviour, Layer 2 isolation, HSRP upstream-tracking limitations and the difference between a healthy-looking control plane and an actually usable traffic path. The troubleshooting entries keep the investigation and remaining questions beside the test evidence.

## 07 · Acceptance and next steps

**The close-out:** [Phase 11 Final Acceptance](../../docs/implementation/hq/phase-11-final-acceptance.md) · [Final Acceptance Evidence](final-acceptance/README.md)

The final acceptance record explains the restoration checks, saved configurations and boot verification. The retained boot verification records that the `hq-a1` management SVI required manual recovery after startup. The final acceptance record should state the disposition of that observation, whether resolved or accepted as a limitation, rather than imply every condition has been cleared. The Phase 10 **10.08 FAIL** and **10.12 INCONCLUSIVE** outcomes also remain part of the record.

---

## Go deeper — two worked examples

The route above gives the complete engineering overview. These two examples go into considerably more detail, including the test plan, result, engineering assessment and original evidence.

| Worked example | Start | What makes it useful |
|---|---|---|
| **10.04 · PASS** | [Start at the original test plan](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1004-cross-link-loss-and-higher-cost-alternate) | OSPF selects a higher-cost alternative and restores the preferred route |
| **10.08 · FAIL** | [Start at the original test plan](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1008-distribution-layer-2-isolation) | The Layer 2 isolation and OSPF return-path blackhole are investigated rather than hidden |

[How the worked-example navigation operates](README.md#follow-the-evidence) · [Interactive network portfolio](https://dominicdudden.co.uk)

[![Choose Another Route ↗](https://img.shields.io/badge/CHOOSE%20ANOTHER%20ROUTE%20%E2%86%97-C2185B?style=flat-square)](../../README.md#explore-the-hq-project)
