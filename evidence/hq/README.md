# HQ Evidence Map

[Portfolio](../../README.md) / HQ Evidence Map

Use this index to find a check, open its evidence and return to the verification record. Phase 10 has separate test reports and planned acceptance criteria.

Phases 01–09 use the recorded status **Verified**. Phase 10 uses **PASS**, **FAIL** and **INCONCLUSIVE**.

| Phase | Test | Check | Recorded status / result | Evidence | Verification record / planned check |
|---|---|---|---|---|---|
| 01 | HQ-VP-01.01 | HQ Device Inventory | Verified | [Captures](platform-baseline/README.md#hq-vp-0101) | [Verification record](../../docs/implementation/hq/verification-plan.md#hq-device-inventory--hq-vp-0101) |
| 01 | HQ-VP-01.02 | Image and Software Version Inventory | Verified | [Captures](platform-baseline/README.md#hq-vp-0102) | [Verification record](../../docs/implementation/hq/verification-plan.md#image-and-software-version-inventory--hq-vp-0102) |
| 01 | HQ-VP-01.03 | Interface Inventory and Topology Fit | Verified | [Captures](platform-baseline/README.md#hq-vp-0103) | [Verification record](../../docs/implementation/hq/verification-plan.md#interface-inventory-and-topology-fit--hq-vp-0103) |
| 01 | HQ-VP-01.04 | Platform Capability Review | Verified | [Captures](platform-baseline/README.md#hq-vp-0104) | [Verification record](../../docs/implementation/hq/verification-plan.md#platform-capability-review--hq-vp-0104) |
| 02 | HQ-VP-02.01 | VLAN Database | Verified | [Captures](layer2-vlan-baseline/README.md#hq-vp-0201) | [Verification record](../../docs/implementation/hq/verification-plan.md#vlan-database--hq-vp-0201) |
| 02 | HQ-VP-02.02 | Access-Port Assignments | Verified | [Captures](layer2-vlan-baseline/README.md#hq-vp-0202) | [Verification record](../../docs/implementation/hq/verification-plan.md#access-port-assignments--hq-vp-0202) |
| 02 | HQ-VP-02.03 | Parking-VLAN Policy | Verified | [Captures](layer2-vlan-baseline/README.md#hq-vp-0203) | [Verification record](../../docs/implementation/hq/verification-plan.md#parking-vlan-policy--hq-vp-0203) |
| 03 | HQ-VP-03.01 | EtherChannel Formation and LACP State | Verified | [Captures](etherchannel/README.md#hq-vp-0301) | [Verification record](../../docs/implementation/hq/verification-plan.md#etherchannel-formation-and-lacp-state--hq-vp-0301) |
| 03 | HQ-VP-03.02 | Port-Channel Trunk Policy | Verified | [Captures](etherchannel/README.md#hq-vp-0302) | [Verification record](../../docs/implementation/hq/verification-plan.md#port-channel-trunk-policy--hq-vp-0302) |
| 03 | HQ-VP-03.03 | Operational Trunk and VLAN State | Verified | [Captures](etherchannel/README.md#hq-vp-0303) | [Verification record](../../docs/implementation/hq/verification-plan.md#operational-trunk-and-vlan-state--hq-vp-0303) |
| 03 | HQ-VP-03.04 | EtherChannel Member-Link Failure and Recovery | Verified | [Captures](etherchannel/README.md#hq-vp-0304) | [Verification record](../../docs/implementation/hq/verification-plan.md#etherchannel-member-link-failure-and-recovery--hq-vp-0304) |
| 04 | HQ-VP-04.01 | Rapid PVST+ Mode and Root Placement | Verified | [Captures](spanning-tree/README.md#hq-vp-0401) | [Verification record](../../docs/implementation/hq/verification-plan.md#rapid-pvst-mode-and-root-placement--hq-vp-0401) |
| 04 | HQ-VP-04.02 | Access-Layer Forwarding and Alternate Paths | Verified | [Captures](spanning-tree/README.md#hq-vp-0402) | [Verification record](../../docs/implementation/hq/verification-plan.md#access-layer-forwarding-and-alternate-paths--hq-vp-0402) |
| 04 | HQ-VP-04.03 | STP Path Failure and Recovery | Verified | [Captures](spanning-tree/README.md#hq-vp-0403) | [Verification record](../../docs/implementation/hq/verification-plan.md#stp-path-failure-and-recovery--hq-vp-0403) |
| 05 | HQ-VP-05.01 | SVI Addressing and Layer 3 Baseline | Verified | [Captures](hsrp/README.md#hq-vp-0501) | [Verification record](../../docs/implementation/hq/verification-plan.md#svi-addressing-and-layer-3-baseline--hq-vp-0501) |
| 05 | HQ-VP-05.02 | HSRP Configuration and Normal Operating State | Verified | [Captures](hsrp/README.md#hq-vp-0502) | [Verification record](../../docs/implementation/hq/verification-plan.md#hsrp-configuration-and-normal-operating-state--hq-vp-0502) |
| 05 | HQ-VP-05.03 | HSRP/STP Alignment and Gateway Reachability | Verified | [Captures](hsrp/README.md#hq-vp-0503) | [Verification record](../../docs/implementation/hq/verification-plan.md#hsrpstp-alignment-and-gateway-reachability--hq-vp-0503) |
| 05 | HQ-VP-05.04 | HSRP Gateway Failover | Verified | [Captures](hsrp/README.md#hq-vp-0504) | [Verification record](../../docs/implementation/hq/verification-plan.md#hsrp-gateway-failover--hq-vp-0504) |
| 05 | HQ-VP-05.05 | HSRP Preemption and Preferred-State Restoration | Verified | [Captures](hsrp/README.md#hq-vp-0505) | [Verification record](../../docs/implementation/hq/verification-plan.md#hsrp-preemption-and-preferred-state-restoration--hq-vp-0505) |
| 06 | HQ-VP-06.01 | Routed `/31` Interface Addressing and State | Verified | [Captures](layer3-underlay/README.md#hq-vp-0601) | [Verification record](../../docs/implementation/hq/verification-plan.md#routed-31-interface-addressing-and-state--hq-vp-0601) |
| 06 | HQ-VP-06.02 | Direct `/31` Point-to-Point Reachability | Verified | [Captures](layer3-underlay/README.md#hq-vp-0602) | [Verification record](../../docs/implementation/hq/verification-plan.md#direct-31-point-to-point-reachability--hq-vp-0602) |
| 06 | HQ-VP-06.03 | Pre-OSPF Underlay Baseline | Verified | [Captures](layer3-underlay/README.md#hq-vp-0603) | [Verification record](../../docs/implementation/hq/verification-plan.md#pre-ospf-underlay-baseline--hq-vp-0603) |
| 07 | HQ-VP-07.01 | Loopback and OSPF Process Identity | Verified | [Captures](ospf/README.md#hq-vp-0701) | [Verification record](../../docs/implementation/hq/verification-plan.md#loopback-and-ospf-process-identity--hq-vp-0701) |
| 07 | HQ-VP-07.02 | OSPF Interface Participation, Network Type and Cost | Verified | [Captures](ospf/README.md#hq-vp-0702) | [Verification record](../../docs/implementation/hq/verification-plan.md#ospf-interface-participation-network-type-and-cost--hq-vp-0702) |
| 07 | HQ-VP-07.03 | OSPF Area 10 Adjacencies | Verified | [Captures](ospf/README.md#hq-vp-0703) | [Verification record](../../docs/implementation/hq/verification-plan.md#ospf-area-10-adjacencies--hq-vp-0703) |
| 07 | HQ-VP-07.04 | OSPF Link-State Database and Learned Routing | Verified | [Captures](ospf/README.md#hq-vp-0704) | [Verification record](../../docs/implementation/hq/verification-plan.md#ospf-link-state-database-and-learned-routing--hq-vp-0704) |
| 07 | HQ-VP-07.05 | Routed and End-to-End Reachability | Verified | [Captures](ospf/README.md#hq-vp-0705) | [Verification record](../../docs/implementation/hq/verification-plan.md#routed-and-end-to-end-reachability--hq-vp-0705) |
| 07 | HQ-VP-07.06 | Layer 2 and Gateway Regression | Verified | [Captures](ospf/README.md#hq-vp-0706) | [Verification record](../../docs/implementation/hq/verification-plan.md#layer-2-and-gateway-regression--hq-vp-0706) |
| 08 | HQ-VP-08.01 | ECMP Route Installation | Verified | [Captures](ospf/README.md#hq-vp-0801) | [Verification record](../../docs/implementation/hq/verification-plan.md#ecmp-route-installation--hq-vp-0801) |
| 08 | HQ-VP-08.02 | CEF Path Selection | Verified | [Captures](ospf/README.md#hq-vp-0802) | [Verification record](../../docs/implementation/hq/verification-plan.md#cef-path-selection--hq-vp-0802) |
| 08 | HQ-VP-08.03 | Aggregate ECMP Forwarding | Verified | [Captures](ospf/README.md#hq-vp-0803) | [Verification record](../../docs/implementation/hq/verification-plan.md#aggregate-ecmp-forwarding--hq-vp-0803) |
| 08 | HQ-VP-08.04 | ECMP Contraction and Restoration | Verified | [Captures](ospf/README.md#hq-vp-0804) | [Verification record](../../docs/implementation/hq/verification-plan.md#ecmp-contraction-and-restoration--hq-vp-0804) |
| 08 | HQ-VP-08.05 | Four-Path Maximum | Verified | [Captures](ospf/README.md#hq-vp-0805) | [Verification record](../../docs/implementation/hq/verification-plan.md#four-path-maximum--hq-vp-0805) |
| 09 | HQ-VP-09.01 | Normal Cost-Driven Selection | Verified | [Captures](ospf/README.md#hq-vp-0901) | [Verification record](../../docs/implementation/hq/verification-plan.md#normal-cost-driven-selection--hq-vp-0901) |
| 09 | HQ-VP-09.02 | Higher-Cost Alternate Activation | Verified | [Captures](ospf/README.md#hq-vp-0902) | [Verification record](../../docs/implementation/hq/verification-plan.md#higher-cost-alternate-activation--hq-vp-0902) |
| 09 | HQ-VP-09.03 | Preferred-Route Restoration | Verified | [Captures](ospf/README.md#hq-vp-0903) | [Verification record](../../docs/implementation/hq/verification-plan.md#preferred-route-restoration--hq-vp-0903) |
| 10 | [HQ-VP-10.01](failure-tests/10.01/HQ-VP-10.01-healthy-baseline.md) | Healthy baseline | PASS | [Test evidence](failure-tests/10.01/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1001-healthy-baseline) |
| 10 | [HQ-VP-10.02](failure-tests/10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) | Routed-link failure and ECMP | PASS | [Test evidence](failure-tests/10.02-10.03/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1002-single-routed-link-loss-and-ecmp-reduction) |
| 10 | [HQ-VP-10.03](failure-tests/10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) | Routed-link failure and ECMP | PASS | [Test evidence](failure-tests/10.02-10.03/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1003-routed-link-failure-detection) |
| 10 | [HQ-VP-10.04](failure-tests/10.04/HQ-VP-10.04-cross-link-failure.md) | Cross-link failure | PASS | [Test evidence](failure-tests/10.04/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1004-cross-link-loss-and-higher-cost-alternate) |
| 10 | [HQ-VP-10.05](failure-tests/10.05/HQ-VP-10.05-etherchannel-member-failure.md) | EtherChannel member failure | PASS | [Test evidence](failure-tests/10.05/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1005-po20-member-link-failure) |
| 10 | [HQ-VP-10.06](failure-tests/10.06/HQ-VP-10.06-access-uplink-failure.md) | Access uplink failure | PASS | [Test evidence](failure-tests/10.06/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1006-access-port-channel-outage) |
| 10 | [HQ-VP-10.07](failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md) | Po30 progressive failure | PASS | [Test evidence](failure-tests/10.07/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1007-progressive-po30-degradation-and-complete-loss) |
| 10 | [HQ-VP-10.08](failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) | `hq-d2` Layer 2 isolation | FAIL | [Test evidence](failure-tests/10.08/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1008-distribution-layer-2-isolation) |
| 10 | [HQ-VP-10.09](failure-tests/10.09/HQ-VP-10.09-d2-routed-isolation.md) | `hq-d2` routed isolation | PASS | [Test evidence](failure-tests/10.09/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1009-active-gateway-loses-routed-uplinks) |
| 10 | [HQ-VP-10.10](failure-tests/10.10/HQ-VP-10.10-d1-device-failure.md) | `hq-d1` device failure | PASS | [Test evidence](failure-tests/10.10/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1010-hq-d1-device-outage) |
| 10 | [HQ-VP-10.11](failure-tests/10.11/HQ-VP-10.11-d2-device-failure.md) | `hq-d2` device failure | PASS | [Test evidence](failure-tests/10.11/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1011-hq-d2-device-outage) |
| 10 | [HQ-VP-10.12](failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md) | `hq-r1` device failure | INCONCLUSIVE | [Test evidence](failure-tests/10.12/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1012-hq-r1-device-outage) |
| 10 | [HQ-VP-10.13](failure-tests/10.13/HQ-VP-10.13-diagonal-double-failure.md) | Combined failures | PASS | [Test evidence](failure-tests/10.13/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1013-diagonal-double-device-failure) |
| 10 | [HQ-VP-10.14](failure-tests/10.14/HQ-VP-10.14-final-restoration.md) | Final restoration | PASS | [Test evidence](failure-tests/10.14/README.md) | [Planned check](../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1014-final-restoration-and-hygiene) |

Phase 10 results need to be read with the [result notes](failure-tests/README.md#notes), particularly the rerun in 10.05, the tracking limitation in 10.09 and the settled-state checks in 10.13.

## Phase 11 — Final Acceptance

Phase 11 is a narrative close-out, with final documentation review still in progress. The boot checks succeeded after a manual management SVI reset; the cause of the initial failure remains unresolved.

[Boot recovery and final operational checks](final-acceptance/README.md) · [Verification record](../../docs/implementation/hq/verification-plan.md#phase-11--final-acceptance) · [Final acceptance document](../../docs/implementation/hq/phase-11-final-acceptance.md)

---

[↑ Portfolio](../../README.md) · [HQ Implementation](../../docs/implementation/hq/README.md)
