# Phase 10 — Failure and Resilience Testing

Phase 10 evaluates the resilience of the HQ network under individual link failures, EtherChannel degradation, device outages and combined failure conditions.

Testing was completed between 3–6 October 2026. Results are supported by summarised evidence, retained CLI captures and session records.

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd) — retained CLI captures and session records, committed before the HQ-VP reports.

[Portfolio](../../../README.md) / Phase 10

## Test Results

| Test | Scenario | Result | Evidence |
|---|---|---|---|
| [HQ-VP-10.01 — Healthy baseline](10.01/HQ-VP-10.01-healthy-baseline.md) | Healthy baseline | PASS | [10.01 — CLI baseline capture](10.01/healthy-baseline-evidence.md) |
| [HQ-VP-10.02–10.03 — Routed-link failure and ECMP](10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) | Routed-link failure and ECMP | PASS | [10.02-10.03 — Failure and recovery CLI](10.02-10.03/routed-link-ecmp-evidence.md) |
| [HQ-VP-10.04 — Cross-link failure](10.04/HQ-VP-10.04-cross-link-failure.md) | Cross-link failure | PASS | [10.04 — Failure and recovery CLI](10.04/cross-link-failure-evidence.md) |
| [HQ-VP-10.05 — EtherChannel member failure](10.05/HQ-VP-10.05-etherchannel-member-failure.md) | EtherChannel member failure | PASS | [10.05 — CLI captures and session record](10.05/etherchannel-member-failure-evidence.md) |
| [HQ-VP-10.06 — Access uplink failure](10.06/HQ-VP-10.06-access-uplink-failure.md) | Access uplink failure | PASS | [10.06 — Uplink failure captures](10.06/access-uplink-failure-evidence.md) |
| [HQ-VP-10.07 — Po30 progressive failure](10.07/HQ-VP-10.07-po30-progressive-failure.md) | Po30 progressive failure | PASS | [10.07 — Event log and session record](10.07/po30-progressive-failure-evidence.md) |
| [HQ-VP-10.08 — D2 Layer 2 isolation](10.08/HQ-VP-10.08-d2-layer2-isolation.md) | D2 Layer 2 isolation | PASS | [10.08 — CLI captures and session record](10.08/d2-layer2-isolation-evidence.md) |
| [HQ-VP-10.09 — D2 routed isolation](10.09/HQ-VP-10.09-d2-routed-isolation.md) | D2 routed isolation | PASS | [10.09 — Session record](10.09/d2-routed-isolation-evidence.md) |
| [HQ-VP-10.10 — D1 device failure](10.10/HQ-VP-10.10-d1-device-failure.md) | D1 device failure | PASS | [10.10 — CLI excerpt](10.10/d1-device-failure-evidence.md) |
| [HQ-VP-10.11 — D2 device failure](10.11/HQ-VP-10.11-d2-device-failure.md) | D2 device failure | PASS | [10.11 — CLI excerpt](10.11/d2-device-failure-evidence.md) |
| [HQ-VP-10.12 — R1 device failure](10.12/HQ-VP-10.12-r1-device-failure.md) | R1 device failure | PASS | [10.12 — CLI excerpt](10.12/r1-device-failure-evidence.md) |
| [HQ-VP-10.13 — Combined failures](10.13/HQ-VP-10.13-diagonal-double-failure.md) | Combined failures | PASS | [10.13 — Session record](10.13/diagonal-double-failure-evidence.md) |
| [HQ-VP-10.14 — Final restoration](10.14/HQ-VP-10.14-final-restoration.md) | Final restoration | PASS | [10.14 — Configuration evidence and session record](10.14/final-restoration-evidence.md) |

## Result Definitions

| Result | Meaning |
|---|---|
| **PASS** | The test met its defined verification criteria. |
| **FAIL** | The test did not meet its defined verification criteria. |
| **INCONCLUSIVE** | The available evidence was insufficient to determine a reliable result. |

## Notes

**HQ-VP-10.05 — EtherChannel member failure:** The port-channel remained operational following a single-member shutdown. The supporting evidence also records transient IP SLA failures during testing.

**HQ-VP-10.07 — Po30 progressive failure:** Complete loss of the distribution interconnect exposed a Layer 2 design limitation, with HSRP state changes during the outage.

**HQ-VP-10.08 — D2 Layer 2 isolation:** The affected SVI remained operational and OSPF continued advertising the subnet despite the downstream Layer 2 failure. Return traffic was blackholed. This is a confirmed design limitation.

**HQ-VP-10.09 — D2 routed isolation:** Testing highlighted limitations in the existing HSRP configuration, including the absence of tracking.

**HQ-VP-10.13 — Combined failures:** Results describe connectivity after the network had settled. They do not establish a precise convergence time.

**HQ-VP-10.14 — Final restoration:** Temporary configurations were removed, the baseline restored and final connectivity checks passed.

---

[↑ Portfolio](../../../README.md)
