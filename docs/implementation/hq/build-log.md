# HQ Build Log

[Portfolio](../../../README.md) / [HQ Implementation](README.md) / HQ Build Log

Chronological record of significant HQ implementation steps.

Detailed verification results are recorded in [verification-plan.md](verification-plan.md). Meaningful faults are recorded in [troubleshooting.md](troubleshooting.md), and accepted design differences in [deviations.md](deviations.md).

## Project reference key

- HQ-VP-XX.YY — HQ verification test, phase XX, test YY
- HQ-TS-NNN — HQ troubleshooting record
- HQ-DEV-NNN — HQ accepted design deviation

## Phase index

| Phase | Build record | Status |
|---:|---|---|
| 01 | [HQ Platform Baseline](#phase-01--hq-platform-baseline) | Verified |
| 02 | [Layer 2 / VLAN Baseline](#phase-02--layer-2--vlan-baseline) | Verified |
| 03 | [LACP EtherChannel](#phase-03--lacp-etherchannel) | Verified |
| 04 | [Rapid PVST+](#phase-04--rapid-pvst) | Verified |
| 05 | [SVIs and HSRP](#phase-05--svis-and-hsrp) | Verified |
| 06 | [Routed /31 Underlay](#phase-06--routed-31-underlay) | Verified |
| 07 | [Loopbacks and OSPF Area 10](#phase-07--loopbacks-and-ospf-area-10) | Verified |
| 08 | [ECMP](#phase-08--ecmp) | Verified |
| 09 | [OSPF Cost Engineering](#phase-09--ospf-cost-engineering) | Verified |
| 10 | [Failure and Resilience Testing](#phase-10--failure-and-resilience-testing) | Completed — mixed outcomes |
| 11 | [Final configuration milestone](#phase-11--final-configuration-milestone) | **Accepted** — findings retained |

## Phase 01 — HQ Platform Baseline

**Completed:** 20-09-2026

### Implemented

- Built and booted the five-node HQ CML baseline.
- Applied the intended device hostnames and baseline console configuration.
- Confirmed the intended device roles and identities.
- Recorded the running IOSv and IOSvL2 software versions.
- Verified interface names and counts against the HQ Campus Design.
- Cabled the 18 planned physical links.
- Checked IOSv and IOSvL2 support for the features required by the design.
- Removed temporary capability-test configuration and confirmed the baseline was restored.

### Verification

- [HQ-VP-01.01](verification-plan.md#hq-device-inventory--hq-vp-0101) — HQ Device Inventory
- [HQ-VP-01.02](verification-plan.md#image-and-software-version-inventory--hq-vp-0102) — Image and Software Version Inventory
- [HQ-VP-01.03](verification-plan.md#interface-inventory-and-topology-fit--hq-vp-0103) — Interface Inventory and Topology Fit
- [HQ-VP-01.04](verification-plan.md#platform-capability-review--hq-vp-0104) — Platform Capability Review

### Result

**Phase 01 verified.** No platform capability blocker was identified for the approved HQ design.

Production VLAN, EtherChannel, Rapid PVST+, HSRP, routed-link, and OSPF configuration has not yet started.

### Evidence

[evidence/hq/platform-baseline/](../../../evidence/hq/platform-baseline/README.md)

### Git traceability

Phase completion commit: [9d99722](https://github.com/ddduddden/multi-site-cml-lab/commit/9d9972296d28a4456f54e4ed38fdb70b45f2060f) (PR \#5).

[↑ Back to phase index](#phase-index)

---

## Phase 02 — Layer 2 / VLAN Baseline

**Completed:** 21-09-2026

### Implemented

- Created and named the approved HQ VLAN database on hq-d1, hq-d2, and hq-a1.
- Configured the intended hq-a1 endpoint-facing access ports, including voice VLAN 120 on Gi2/0.
- Assigned all hq-a1 interfaces not yet in service to VLAN 191 (PARKING) and administratively shut them down, including the future Po10 and Po20 members until Phase 03.
- Left VLAN 1 present as the platform default with no production or management access ports assigned.

### Verification

- [HQ-VP-02.01](verification-plan.md#vlan-database--hq-vp-0201) — VLAN Database
- [HQ-VP-02.02](verification-plan.md#access-port-assignments--hq-vp-0202) — Access-Port Assignments
- [HQ-VP-02.03](verification-plan.md#parking-vlan-policy--hq-vp-0203) — Parking-VLAN Policy

### Result

**Phase 02 verified.** The approved VLAN database, access-port assignments, voice-VLAN assignment, and parking-VLAN policy were demonstrated and recorded.

EtherChannel/trunking and later Layer 2 and Layer 3 features remain for subsequent phases.

### Evidence

[evidence/hq/layer2-vlan-baseline/](../../../evidence/hq/layer2-vlan-baseline/README.md)

### Git traceability

Phase completion commit: [e6f7201](https://github.com/ddduddden/multi-site-cml-lab/commit/e6f7201131b7bef53612278bd5cdf2d98b3fbf5f) (PR \#6).

[↑ Back to phase index](#phase-index)

---

## Phase 03 — LACP EtherChannel

**Completed:** 22-09-2026

### Implemented

- Built Po10 between hq-a1 and hq-d1 using two LACP member links.
- Built Po20 between hq-a1 and hq-d2 using two LACP member links.
- Built Po30 between hq-d1 and hq-d2 using four LACP member links.
- Configured all three Port-Channels as 802.1Q trunks with native VLAN 190.
- Applied the approved allowed-VLAN list 112,120,130,140,152,160,170,190,199.
- Reconfigured the former Phase 02 parked Po10 and Po20 member interfaces for their production EtherChannel roles.

### Verification

- [HQ-VP-03.01](verification-plan.md#etherchannel-formation-and-lacp-state--hq-vp-0301) — EtherChannel Formation and LACP State
- [HQ-VP-03.02](verification-plan.md#port-channel-trunk-policy--hq-vp-0302) — Port-Channel Trunk Policy
- [HQ-VP-03.03](verification-plan.md#operational-trunk-and-vlan-state--hq-vp-0303) — Operational Trunk and VLAN State
- [HQ-VP-03.04](verification-plan.md#etherchannel-member-link-failure-and-recovery--hq-vp-0304) — EtherChannel Member-Link Failure and Recovery

### Result

**Phase 03 verified.** Po10, Po20, and Po30 formed successfully with all intended LACP members bundled. The approved trunk policy was operational across all three Port-Channels, and each bundle remained operational during a controlled single-member failure and recovered correctly after restoration.

Deterministic Rapid PVST+ root placement and forwarding behaviour remain for Phase 04.

### Evidence

[evidence/hq/etherchannel/](../../../evidence/hq/etherchannel/README.md)

### Git traceability

Phase completion commit: [7db4f05](https://github.com/ddduddden/multi-site-cml-lab/commit/7db4f05124b244752e461084b1eeb7aaf7dcd132) (PR \#7).

[↑ Back to phase index](#phase-index)

---

## Phase 04 — Rapid PVST+

**Completed:** 24-09-2026

### Implemented

- Enabled Rapid PVST+ on hq-a1, hq-d1, and hq-d2.
- Configured hq-d1 as root primary for VLANs 112,130,152,170,190.
- Configured hq-d2 as root primary for VLANs 120,140,160,199.
- Configured each multilayer distribution switch as root secondary for the other's VLAN group.
- Configured deterministic hq-d1 root placement for native VLAN 190.
- Preserved the existing Phase 03 EtherChannel and trunk configuration.
- Applied Root Guard on the distribution-to-access Port-Channels (hq-d1 Po10 and hq-d2 Po20) to protect the intended distribution-layer STP root placement from a superior BPDU arriving from the access layer.
- Corrected the VLAN 152 name on hq-a1 to GUEST after a minor naming issue was identified during evidence review. No functional behaviour was affected.

### Verification

- [HQ-VP-04.01](verification-plan.md#rapid-pvst-mode-and-root-placement--hq-vp-0401) — Rapid PVST+ Mode and Root Placement
- [HQ-VP-04.02](verification-plan.md#access-layer-forwarding-and-alternate-paths--hq-vp-0402) — Access-Layer Forwarding and Alternate Paths
- [HQ-VP-04.03](verification-plan.md#stp-path-failure-and-recovery--hq-vp-0403) — STP Path Failure and Recovery

### Result

**Phase 04 verified.** Rapid PVST+ operated across all three HQ switches and matched the approved root-placement design. Representative VLAN checks confirmed the expected forwarding paths, and controlled failures of Po10 and Po20 proved alternate-path recovery in both directions.

SVI addressing and HSRP gateway redundancy remain for Phase 05.

### Evidence

[evidence/hq/spanning-tree/](../../../evidence/hq/spanning-tree/README.md)

### Git traceability

Phase completion commit: [2094b28](https://github.com/ddduddden/multi-site-cml-lab/commit/2094b28d5f8a4b38719723c927ad3232ea69f09e) (PR \#8).

[↑ Back to phase index](#phase-index)

---

## Phase 05 — SVIs and HSRP

**Completed:** 27-09-2026

### Implemented

- Configured the approved SVIs and HSRP gateways on hq-d1 and hq-d2, using .2 / .3 physical addresses and .1 virtual gateways.
- Applied HSRP group numbers matching each routed VLAN, priority 110 on the preferred peer and 100 on the standby peer, with preemption retained only on the preferred peer.
- Aligned HSRP ownership with the Phase 04 Rapid PVST+ root placement.
- Configured hq-a1 Vlan199 as 10.10.99.4/26 with default gateway 10.10.99.1, and used a temporary Vlan112 SVI for gateway testing.
- Configured VTP transparent on all three switches so VLAN definitions were locally represented in the exported CML configuration.
- Corrected unintended HSRP group 0 configuration on hq-d2.
- Verified failover and recovery for representative VLANs 112 and 199, then removed the temporary hq-a1 Vlan112 SVI.
- Restored recent unsaved configuration after an unexpected VMware/CML interruption before verification continued; no fault was identified with the Phase 05 SVI or HSRP design.
- Updated the operating workflow so significant configuration milestones are written to startup configuration, followed by a CML configuration fetch and retained versioned YAML exports.

### Verification

- [HQ-VP-05.01](verification-plan.md#svi-addressing-and-layer-3-baseline--hq-vp-0501) — SVI Addressing and Layer 3 Baseline
- [HQ-VP-05.02](verification-plan.md#hsrp-configuration-and-normal-operating-state--hq-vp-0502) — HSRP Configuration and Normal Operating State
- [HQ-VP-05.03](verification-plan.md#hsrpstp-alignment-and-gateway-reachability--hq-vp-0503) — HSRP/STP Alignment and Gateway Reachability
- [HQ-VP-05.04](verification-plan.md#hsrp-gateway-failover--hq-vp-0504) — HSRP Gateway Failover
- [HQ-VP-05.05](verification-plan.md#hsrp-preemption-and-preferred-state-restoration--hq-vp-0505) — HSRP Preemption and Preferred-State Restoration

### Result

**Phase 05 verified.** The approved SVI addressing, normal HSRP ownership, STP/HSRP alignment and gateway reachability were demonstrated. Controlled failure of the preferred SVI for representative VLANs 112 and 199 transferred gateway ownership to the peer, and restoration returned each VLAN to its planned preferred Active peer. The temporary hq-a1 Vlan112 test SVI was removed after testing.

During final review, redundant preemption statements were removed from the non-preferred priority-100 peers so the as-built HSRP configuration matched the approved design. Final normal-state captures confirmed the intended preferred-only preemption policy and unchanged Active/Standby ownership; the completed failover tests were not repeated.

Routed /31 Distribution-to-Edge links and loopbacks remain for Phase 06.

### Evidence

[evidence/hq/hsrp/](../../../evidence/hq/hsrp/README.md)

### Git traceability

Phase completion commit: [9e17f45](https://github.com/ddduddden/multi-site-cml-lab/commit/9e17f4594ca03d354264e553a7f0109f12685366) (PR \#9).

[↑ Back to phase index](#phase-index)

---

## Phase 06 — Routed /31 Underlay

**Completed:** 30-09-2026

**Build window:** Combined with Phase 07.

### Implemented

- Converted hq-d1 and hq-d2 Gi2/0–Gi2/3 and Gi3/0 to routed ports.
- Addressed the ten Distribution-to-Edge links as /31 point-to-point networks from the approved 10.255.10.0/24 infrastructure range.
- Used four direct routed links from hq-d1 to hq-r1, four from hq-d2 to hq-r2, and one cross-link from each distribution switch to the opposite edge router.
- Applied operational descriptions containing peer interface, subnet, and direct/cross-link role.
- Verified connected routes and direct peer reachability before any OSPF process existed.
- Preserved the historical phase boundary shown by the saved CML state: Loopback0 identities were not yet configured at the end of Phase 06 and were introduced with Phase 07.

### Verification

- [HQ-VP-06.01](verification-plan.md#routed-31-interface-addressing-and-state--hq-vp-0601) — Routed /31 Interface Addressing and State
- [HQ-VP-06.02](verification-plan.md#direct-31-point-to-point-reachability--hq-vp-0602) — Direct /31 Point-to-Point Reachability
- [HQ-VP-06.03](verification-plan.md#pre-ospf-underlay-baseline--hq-vp-0603) — Pre-OSPF Underlay Baseline

### Result

**Phase 06 verified.** All ten routed links were up/up, used the approved /31 addressing, and provided bidirectional directly connected reachability. The pre-OSPF capture confirmed no OSPF router process existed on any of the four Layer 3 devices.

The original phase index placed the loopbacks in Phase 06, but the retained milestone state shows that they were actually introduced at the start of Phase 07. The phase was therefore renamed *Routed /31 Underlay*, and the implementation record follows the observed build history rather than reconstructing a state that did not exist.

### Evidence

[evidence/hq/layer3-underlay/](../../../evidence/hq/layer3-underlay/README.md)

### Milestone artifacts

The end-of-Phase-06 CML export is retained privately as the pre-OSPF rollback point and is not committed. The Phase 06 evidence was captured from that restored state. The committed configs/hq/ files represent the Phase 07 milestone.

### Git traceability

Phase 06 verification evidence is included in the combined Phase 06–07 evidence snapshot: commit [6608742](https://github.com/ddduddden/multi-site-cml-lab/commit/66087426a6aa619e0177abca1238fad7c3213d70).

[↑ Back to phase index](#phase-index)

---

## Phase 07 — Loopbacks and OSPF Area 10

**Completed:** 30-09-2026

**Build window:** Combined with Phase 06.

### Implemented

- Added Loopback0 identities 10.255.10.129/32–10.255.10.132/32 to hq-r1, hq-r2, hq-d1, and hq-d2.
- Configured OSPFv2 process 10 with explicit router IDs matching those loopbacks.
- Enabled OSPF through interface-level ip ospf 10 area 10 configuration rather than broad network statements.
- Applied passive-interface default and made only the five routed Distribution-to-Edge interfaces per Layer 3 device non-passive.
- Kept the eight distribution SVIs and all four loopbacks passive while advertising their prefixes into Area 10.
- Configured all ten routed Ethernet links as OSPF point-to-point.
- Applied cost 10 to the eight direct links and cost 100 to the two cross-links at both ends.
- Confirmed with show ip protocols that the operational OSPF maximum-path value on this image was 4; no explicit maximum-paths 4 line was present in the running configuration.
- Corrected an early Area 0 interface assignment on hq-d2 so all five routed interfaces participated in Area 10 before final verification.
- Disabled IP routing on hq-a1 with no ip routing, retaining ip default-gateway 10.10.99.1. The initial management reachability check showed that hq-a1 could reach its HSRP gateway but not the four remote routing identities while IOSvL2 routing was active; HQ-TS-001 records the investigation and correction.
- Captured a sanitised Phase 07 CML milestone export and readable per-device running configurations for the public repository.

### Verification

- [HQ-VP-07.01](verification-plan.md#loopback-and-ospf-process-identity--hq-vp-0701) — Loopback and OSPF Process Identity
- [HQ-VP-07.02](verification-plan.md#ospf-interface-participation-network-type-and-cost--hq-vp-0702) — OSPF Interface Participation, Network Type and Cost
- [HQ-VP-07.03](verification-plan.md#ospf-area-10-adjacencies--hq-vp-0703) — OSPF Area 10 Adjacencies
- [HQ-VP-07.04](verification-plan.md#ospf-link-state-database-and-learned-routing--hq-vp-0704) — OSPF Link-State Database and Learned Routing
- [HQ-VP-07.05](verification-plan.md#routed-and-end-to-end-reachability--hq-vp-0705) — Routed and End-to-End Reachability
- [HQ-VP-07.06](verification-plan.md#layer-2-and-gateway-regression--hq-vp-0706) — Layer 2 and Gateway Regression

### Result

**Phase 07 verified.** Each Layer 3 device formed exactly five FULL point-to-point OSPF neighbours, giving ten unique routed-link adjacencies across Area 10. All four Router LSAs were present, the expected HQ prefixes were learned, and all twelve sourced inter-device reachability checks succeeded.

hq-a1 successfully reached the HSRP gateway and all four loopbacks while operating with no ip routing and ip default-gateway 10.10.99.1. Final regression captures confirmed the existing EtherChannel, Rapid PVST+, HSRP, and management-SVI state remained intact.

Route tables already expose multiple next hops and cost-driven path differences, but those behaviours remain deliberately reserved for the dedicated Phase 08 ECMP and Phase 09 cost-engineering verification.

### Evidence

[evidence/hq/ospf/](../../../evidence/hq/ospf/README.md)

### Milestone artifacts

- configs/hq/hq-r1-running-config.txt
- configs/hq/hq-r2-running-config.txt
- configs/hq/hq-d1-running-config.txt
- configs/hq/hq-d2-running-config.txt
- configs/hq/hq-a1-running-config.txt
- lab/cml-lab-exports/hq/hq-phase-07-ospf-area10-2026-09-30.yaml

### Git traceability

Phase 07 as-built configs, verification evidence, and milestone CML export: commit [6608742](https://github.com/ddduddden/multi-site-cml-lab/commit/66087426a6aa619e0177abca1238fad7c3213d70).

[↑ Back to phase index](#phase-index)

---

## Phase 08 — ECMP

**Completed:** 30-09-2026

### Implemented

- Made no permanent configuration change.
- Verified the four-route ECMP behaviour exposed by the Phase 07 OSPF design.
- Confirmed selected metric-11 four-route sets in the routing table.
- Verified CEF-selected forwarding with interface counters.
- Confirmed that more than one installed ECMP member carried the test traffic.
- Contracted and restored a selected ECMP route set from four routes to one and back to four.
- Verified the lab-observed four-path OSPF installation limit with a fifth equal-cost route available.

### Verification

- [HQ-VP-08.01](verification-plan.md#ecmp-route-installation--hq-vp-0801) — ECMP Route Installation
- [HQ-VP-08.02](verification-plan.md#cef-path-selection--hq-vp-0802) — CEF Path Selection
- [HQ-VP-08.03](verification-plan.md#aggregate-ecmp-forwarding--hq-vp-0803) — Aggregate ECMP Forwarding
- [HQ-VP-08.04](verification-plan.md#ecmp-contraction-and-restoration--hq-vp-0804) — ECMP Contraction and Restoration
- [HQ-VP-08.05](verification-plan.md#four-path-maximum--hq-vp-0805) — Four-Path Maximum

### Result

**Phase 08 verified.** The intended four-route OSPF ECMP sets were present in the routing table, and the forwarding tests showed that more than one installed path was actually used. Controlled link removal contracted the selected route set from four routes to one, and restoration rebuilt it to four.

The test also showed five equal-cost paths from hq-r1 to hq-r2 Loopback0 (10.255.10.130/32). With the lab-observed maximum-path value of four, OSPF kept four next hops installed, and the previously omitted route entered the routing table when one installed path was removed.

### Evidence

[evidence/hq/ospf/](../../../evidence/hq/ospf/README.md)

### Milestone artifacts

No new milestone artifact. Phase 08 changed no intended device configuration; the Phase 07 configs and CML export remain current.

### Git traceability

Phase 08/09 verification evidence commit: [79d27bf](https://github.com/ddduddden/multi-site-cml-lab/commit/79d27bfa3351bb6ffbf9363ee66675251e9aa1a2).

[↑ Back to phase index](#phase-index)

---

## Phase 09 — OSPF Cost Engineering

**Completed:** 30-09-2026

### Implemented

- Made no permanent configuration change.
- Verified that normal OSPF route selection follows the approved cost policy.
- Confirmed that selected campus and infrastructure routes followed the expected OSPF costs: metric 11 on the direct paths and metrics 101 and 110 on the higher-cost cross-link paths.
- Removed each four-link direct edge/distribution set in turn and verified the surviving higher-cost routes.
- Confirmed alternate reachability with sourced pings and traceroutes.
- Restored all direct links and verified return to the normal ECMP and OSPF state.
- Compared the post-test CML export with the committed Phase 07 configuration files and found no unexpected configuration changes.

### Verification

- [HQ-VP-09.01](verification-plan.md#normal-cost-driven-selection--hq-vp-0901) — Normal Cost-Driven Selection
- [HQ-VP-09.02](verification-plan.md#higher-cost-alternate-activation--hq-vp-0902) — Higher-Cost Alternate Activation
- [HQ-VP-09.03](verification-plan.md#preferred-route-restoration--hq-vp-0903) — Preferred-Route Restoration

### Result

**Phase 09 verified.** Normal routing followed the configured OSPF cost policy. When a complete four-link direct set was removed, OSPF moved the affected routes onto the surviving higher-cost routes through the opposite edge/distribution pair, and reachability remained available.

Restoring the direct links returned the selected campus routes to metric 11, rebuilt the four-route ECMP sets, and returned all four Layer 3 devices to five FULL OSPF neighbours. The final health check matched the Phase 07 operating baseline.

### Evidence

[evidence/hq/ospf/](../../../evidence/hq/ospf/README.md)

### Milestone artifacts

No new milestone artifact. Phase 09 changed no intended device configuration; the Phase 07 configs and CML export remain current.

### Git traceability

Phase 08/09 verification evidence commit: [79d27bf](https://github.com/ddduddden/multi-site-cml-lab/commit/79d27bfa3351bb6ffbf9363ee66675251e9aa1a2).

🟧 [← Return to Stop 2 · Phase Verification](verification-plan.md#higher-cost-alternate-activation--hq-vp-0902)

[↑ Back to phase index](#phase-index)

---

## Phase 10 — Failure and Resilience Testing

**Testing completed:** 06-10-2026\
**Configuration reconciliation completed:** 12-10-2026

### Testing

- Executed the planned failure scenarios covering routed links, LACP members, complete Port-Channel outages, distribution and edge-router failures, and combined device failures.
- Checked protocol state alongside traffic forwarding, using routed connectivity tests, sourced pings, IP SLA observations and retained CLI evidence.
- Investigated unexpected behaviour, including the one-sided Po20 member failure, complete Po30 loss, Layer 2 isolation and loss of routed connectivity from an Active HSRP gateway.
- Restored the HQ topology to its normal forwarding state and removed temporary test configuration.
- Completed the outstanding configuration comparisons and logging restoration on 12-10-2026.

### Result

**Phase 10 completed.** The planned failure-testing sequence was executed, and the original acceptance criteria were retained when assessing the results.

Most scenarios demonstrated the intended recovery behaviour, but not every test passed. [HQ-VP-10.08](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) recorded a failure following Layer 2 isolation, while [HQ-VP-10.12](../../../evidence/hq/failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md) remained inconclusive because the planned live-flow failover check was not completed.

The tests also identified limitations involving the single logical Po30 connection, IOSvL2 SVI behaviour and HSRP upstream tracking. These findings remain documented rather than being treated as successful resilience tests.

Final restoration was confirmed on 06-10-2026, with outstanding configuration reconciliation completed on 12-10-2026.

### Evidence

- [Phase 10 Test Plan](phase-10-test-plan.md)
- [Testing Methodology](phase-10-testing-methodology.md)
- [Engineering Review and Conclusions](phase-10-engineering-review.md)
- [Test Results and Evidence Index](../../../evidence/hq/failure-tests/README.md)

### Git traceability

- [Retained CLI evidence — a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
- [Phase 10 completion merge — 0ba7114](https://github.com/ddduddden/multi-site-cml-lab/commit/0ba7114f25acf8793a04800b9381412ed7c55d28) (PR #13)

[↑ Back to phase index](#phase-index)

---

## Phase 11 — Final configuration milestone

**Prepared:** 15-10-2026\
**Source:** Private final export associated with the configuration close-out on 12-10-2026

The final export was prepared as a sanitised public milestone, and the five running-configuration files in configs/hq/ were refreshed from that same copy. The original Phase 07 YAML and Phase 10 evidence remain unchanged.

The final configuration includes standardised SSH access, management-host access lists and return routes, and type 9 local-user and enable secrets on all five devices. The three switches had used type 5 secrets in the Phase 07 milestone. The external-management connector and hq-r1 Gi0/5 DHCP connection are retained, alongside the access-port PortFast/BPDU Guard settings and parked, shut-down spare distribution ports.

Credentials and username references were sanitised. The management host address was replaced consistently with 192.0.2.10 in the SSH access lists and three host routes. The remaining device configuration and all 19 topology links were preserved from the supplied export. Its five Cisco devices form the HQ campus; the additional object provides external management.

YAML parsing and link-endpoint checks passed. Each published device file matches its configuration in the YAML. Comparison with the Phase 07 export confirmed that HQ routed-interface, OSPF, SVI and Port-Channel configuration is unchanged. No temporary IP SLA operations, temporary hq-a1 source SVIs or custom buffered-logging setting remain. Those were file checks, not a new CML execution test. At the time of publication on 15-10-2026, the CML boot had not been retested. A runtime test using the private export followed on 16-10-2026 (see below).

### Milestone artifacts

- [Final CML export](../../../lab/cml-lab-exports/hq/hq-phase-11-final-acceptance-2026-10-15.yaml)
- [hq-r1 configuration](../../../configs/hq/hq-r1-running-config.txt)
- [hq-r2 configuration](../../../configs/hq/hq-r2-running-config.txt)
- [hq-d1 configuration](../../../configs/hq/hq-d1-running-config.txt)
- [hq-d2 configuration](../../../configs/hq/hq-d2-running-config.txt)
- [hq-a1 configuration](../../../configs/hq/hq-a1-running-config.txt)

### Git traceability

Final sanitised CML export and five matching device configurations: [commit 1ee631b](https://github.com/ddduddden/multi-site-cml-lab/commit/1ee631be011985dac4a1c6a7f97de1ff95d22c1c).

This commit records the published configuration milestone. Final documentation review and Phase 11 acceptance are separate close-out activities.

The filename records preparation of the public copy on 15-10-2026. It does not move the original tests or configuration close-out to that date. The Phase 11 operational check on 16-10-2026 is recorded below. Final documentation review and engineering acceptance were completed on 26 October 2026.

### Operational check — 16-10-2026

A private copy of the final five-device CML configuration was booted for operational verification. This is separate from the sanitised public configuration milestone published on 15-10-2026.

On `hq-a1`, `Vlan199` remained `down/down` after boot. The VLAN was active, Po10 and Po20 were bundled and trunking, and the VLAN 199 spanning-tree path was forwarding, but gateway pings failed (`0/5`). Entering `no shutdown` alone did not recover the interface. A manual `shutdown` followed by `no shutdown` brought it `up/up`. The gateway then replied `5/5`, as did both edge-router loopbacks. The underlying cause was not established; this was not a clean, intervention-free boot.

Post-recovery checks recorded operational HSRP roles and EtherChannels. On `hq-r1`, five OSPF neighbours were `FULL`, and `10.10.12.0/22` had four installed equal-cost metric-`11` paths. The traceroute to `hq-r2`'s loopback showed `10.10.99.3` followed by `10.255.10.3`; it was not used to claim an unrecorded final destination hop.

**Evidence:** [Boot failure and manual recovery](../../../evidence/hq/final-acceptance/HQ-Phase-11-Boot-Recovery-CLI.md) · [Post-recovery operational CLI](../../../evidence/hq/final-acceptance/HQ-Phase-11-Final-Boot-Verification.txt)

**Git traceability:** [`39b68a7` — Add Phase 11 boot evidence and HQ troubleshooting records](https://github.com/ddduddden/multi-site-cml-lab/commit/39b68a790a3b9ed0de55071fdf7f9b004d0638b2).

### Follow-up startup check — 26-10-2026

A further CML boot reproduced the `hq-a1` VLAN199 SVI startup fault. The SVI was `down/down` and the management gateway returned `0/5`, although the VLAN was active and Po20 was operational and forwarding. Running and startup SVI configuration matched. `no shutdown` alone did not recover it; `shutdown` followed by `no shutdown` brought the SVI `up/up` and restored gateway reachability (`5/5`). The cause remains undetermined, and no wider routing/HSRP acceptance run was recorded during this recheck.

**Evidence:** [26 October startup recheck and CLI](../../../evidence/hq/final-acceptance/HQ-Phase-11-26-Oct-Boot-Retest.md).

The [Phase 11 engineering close-out](phase-11-final-acceptance.md) records HQ V1 as an accepted engineering milestone on 26 October 2026. The Phase 10 FAIL and INCONCLUSIVE results and other open findings remain documented; the 16 October operational checks and 26 October management-gateway recheck both required manual SVI recovery; a clean startup was not demonstrated.

[↑ Back to phase index](#phase-index)

---

[← HQ Campus Design](../../hq-campus-design.md) · [↑ Phase index](#phase-index) · [HQ Verification Plan →](verification-plan.md)
