# Phase 10 — Failure and Resilience Testing

Phase 10 evaluates the resilience of the HQ network under individual link failures, EtherChannel degradation, device outages and combined failure conditions.

Failure testing took place from 03-10-2026 to 06-10-2026, with final configuration reconciliation completed on 12-10-2026. Results are supported by summarised evidence, retained CLI captures and session records.

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd) — retained CLI captures and session records, committed before the HQ-VP reports.

[Portfolio](../../../README.md) / [Evidence Map](../README.md) / Phase 10

[Test plan](../../../docs/implementation/hq/phase-10-test-plan.md#test-matrix) · [Testing methodology](../../../docs/implementation/hq/phase-10-testing-methodology.md) · [Verification record](../../../docs/implementation/hq/verification-plan.md#phase-10--failure-testing)

## Test Results

| Test | Scenario | Result | Evidence |
|---|---|---|---|
| [HQ-VP-10.01 — Healthy baseline](10.01/HQ-VP-10.01-healthy-baseline.md) | Healthy baseline | PASS | [10.01 — CLI baseline capture](10.01/README.md) |
| [HQ-VP-10.02–10.03 — Routed-link failure and ECMP](10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) | Routed-link failure and ECMP | PASS | [10.02-10.03 — Failure and recovery CLI](10.02-10.03/README.md) |
| [HQ-VP-10.04 — Cross-link failure](10.04/HQ-VP-10.04-cross-link-failure.md) | Cross-link failure | PASS | [10.04 — Failure and recovery CLI](10.04/README.md) |
| [HQ-VP-10.05 — EtherChannel member failure](10.05/HQ-VP-10.05-etherchannel-member-failure.md) | EtherChannel member failure | PASS | [10.05 — CLI captures and session record](10.05/README.md) |
| [HQ-VP-10.06 — Access uplink failure](10.06/HQ-VP-10.06-access-uplink-failure.md) | Access uplink failure | PASS | [10.06 — Uplink failure captures](10.06/README.md) |
| [HQ-VP-10.07 — Po30 progressive failure](10.07/HQ-VP-10.07-po30-progressive-failure.md) | Po30 progressive failure | PASS | [10.07 — Event log and session record](10.07/README.md) |
| [HQ-VP-10.08 — `hq-d2` Layer 2 isolation](10.08/HQ-VP-10.08-d2-layer2-isolation.md) | `hq-d2` Layer 2 isolation | FAIL | [10.08 — CLI captures and session record](10.08/README.md) |
| [HQ-VP-10.09 — `hq-d2` routed isolation](10.09/HQ-VP-10.09-d2-routed-isolation.md) | `hq-d2` routed isolation | PASS | [10.09 — Session record](10.09/README.md) |
| [HQ-VP-10.10 — `hq-d1` device failure](10.10/HQ-VP-10.10-d1-device-failure.md) | `hq-d1` device failure | PASS | [10.10 — CLI excerpt](10.10/README.md) |
| [HQ-VP-10.11 — `hq-d2` device failure](10.11/HQ-VP-10.11-d2-device-failure.md) | `hq-d2` device failure | PASS | [10.11 — CLI excerpt](10.11/README.md) |
| [HQ-VP-10.12 — `hq-r1` device failure](10.12/HQ-VP-10.12-r1-device-failure.md) | `hq-r1` device failure | INCONCLUSIVE | [10.12 — CLI excerpt](10.12/README.md) |
| [HQ-VP-10.13 — Combined failures](10.13/HQ-VP-10.13-diagonal-double-failure.md) | Combined failures | PASS | [10.13 — Session record](10.13/README.md) |
| [HQ-VP-10.14 — Final restoration](10.14/HQ-VP-10.14-final-restoration.md) | Final restoration | PASS | [10.14 — Configuration evidence and session record](10.14/README.md) |

## Result Definitions

| Result | Meaning |
|---|---|
| **PASS** | The test met its defined verification criteria. |
| **FAIL** | The test did not meet its defined verification criteria. |
| **INCONCLUSIVE** | The available evidence was insufficient to determine a reliable result. |

## Notes

**HQ-VP-10.01 — Healthy baseline:** The report records BASELINE ESTABLISHED; the index PASS means the starting baseline was established, not that a failure/recovery test was run.

**HQ-VP-10.05 — EtherChannel member failure:** The one-sided Po20 member shutdown caused sustained loss on SLA101 (177 failed samples), while SLA102 recorded none. The cause remains unexplained. The bilateral rerun passed on the surviving member. The index PASS refers to the rerun, not the one-sided finding.

**HQ-VP-10.07 — Po30 progressive failure:** Complete loss of the distribution interconnect exposed a Layer 2 design limitation, with HSRP state changes during the outage.

**HQ-VP-10.08 — `hq-d2` Layer 2 isolation:** The expected SVI withdrawal and working return path did not occur. The retained evidence shows the subnet advertised into OSPF while return traffic was blackholed. The IOSvL2 finding remains in the report.

**HQ-VP-10.09 — `hq-d2` routed isolation:** The report confirmed the absence of HSRP upstream tracking. Its index PASS records the documented isolation/recovery checks; it does not imply uninterrupted routing through the isolated gateway.

**HQ-VP-10.12 — `hq-r1` device failure:** The surviving hq-r2 path was verified, but no live flow was shown rerouting away from hq-r1. The full planned failover check remains inconclusive.

**HQ-VP-10.13 — Combined failures:** Results describe connectivity after the network had settled. They do not establish a precise convergence time.

**HQ-VP-10.14 — Final restoration:** The forwarding baseline recovered on 06-10-2026. Final five-device configuration comparisons, the hq-a1 logging reset and a private CML export were completed on 12-10-2026. See the retained [configuration close-out evidence](10.14/10.14-config-excerpts.md).

**🟧 10-MINUTE ROUTE — CONTINUE READING**

[![Engineering Findings](https://img.shields.io/badge/Engineering%20Findings-bf6700?style=flat-square)](../../../docs/implementation/hq/phase-10-engineering-review.md) &emsp;<sup>➜</sup>&emsp; [![Final Acceptance](https://img.shields.io/badge/Final%20Acceptance-bf6700?style=flat-square)](../../../docs/implementation/hq/phase-11-final-acceptance.md)

[![Choose Another Route ↗](https://img.shields.io/badge/CHOOSE%20ANOTHER%20ROUTE%20%E2%86%97-C2185B?style=flat-square)](../../../README.md#explore-the-hq-project)

---

[◀ Phases 07–09](../ospf/README.md) · [↑ Evidence Map](../README.md) · [Phase 11 ▶](../final-acceptance/README.md)
