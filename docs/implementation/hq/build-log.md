# HQ Build Log

Chronological record of significant HQ implementation steps.

Detailed verification results are recorded in [`verification-plan.md`](verification-plan.md). Meaningful faults are recorded in [`troubleshooting.md`](troubleshooting.md), and accepted design differences in [`deviations.md`](deviations.md).

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-VP-XX.YY` | HQ verification test — phase `XX`, test `YY` |
| `HQ-TS-NNN` | HQ troubleshooting record |
| `HQ-DEV-NNN` | HQ accepted design deviation |

---

## Phase 01 — HQ Platform Baseline

**Completed:** `20-09-2026`

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

- `HQ-VP-01.01` — HQ Device Inventory
- `HQ-VP-01.02` — Image and Software Version Inventory
- `HQ-VP-01.03` — Interface Inventory and Topology Fit
- `HQ-VP-01.04` — Platform Capability Review

### Result

**Phase 01 verified.** No platform capability blocker was identified for the approved HQ design.

Production VLAN, EtherChannel, Rapid PVST+, HSRP, routed-link, and OSPF configuration has not yet started.

### Evidence

[`evidence/hq/platform-baseline/`](../../../evidence/hq/platform-baseline/)

### Git traceability

Phase completion commit: [`9d99722`](https://github.com/ddduddden/multi-site-cml-lab/commit/9d9972296d28a4456f54e4ed38fdb70b45f2060f) (PR #5).

### Next

**Phase 02 — Layer 2 / VLAN Baseline**

---

## Phase 02 — Layer 2 / VLAN Baseline

**Completed:** `21-09-2026`

### Implemented

- Created and named the approved HQ VLAN database on `hq-d1`, `hq-d2`, and `hq-a1`.
- Configured the intended `hq-a1` endpoint-facing access ports, including voice VLAN `120` on `Gi2/0`.
- Assigned all `hq-a1` interfaces not yet in service to VLAN `191` (`PARKING`) and administratively shut them down, including the future `Po10` and `Po20` members until Phase 03.
- Left VLAN `1` present as the platform default with no production or management access ports assigned.

### Verification

- `HQ-VP-02.01` — VLAN Database
- `HQ-VP-02.02` — Access-Port Assignments
- `HQ-VP-02.03` — Parking-VLAN Policy

### Result

**Phase 02 verified.** The approved VLAN database, access-port assignments, voice-VLAN assignment, and parking-VLAN policy were demonstrated and recorded.

EtherChannel/trunking and later Layer 2 and Layer 3 features remain for subsequent phases.

### Evidence

[`evidence/hq/layer2-vlan-baseline/`](../../../evidence/hq/layer2-vlan-baseline/)

### Git traceability

Phase completion commit: [`e6f7201`](https://github.com/ddduddden/multi-site-cml-lab/commit/e6f7201131b7bef53612278bd5cdf2d98b3fbf5f) (PR #6).

### Next

**Phase 03 — LACP EtherChannel**

---

## Phase 03 — LACP EtherChannel

**Completed:** `22-09-2026`

### Implemented

- Built `Po10` between `hq-a1` and `hq-d1` using two LACP member links.
- Built `Po20` between `hq-a1` and `hq-d2` using two LACP member links.
- Built `Po30` between `hq-d1` and `hq-d2` using four LACP member links.
- Configured all three Port-Channels as 802.1Q trunks with native VLAN `190`.
- Applied the approved allowed-VLAN list `112,120,130,140,152,160,170,190,199`.
- Reconfigured the former Phase 02 parked `Po10` and `Po20` member interfaces for their production EtherChannel roles.

### Verification

- `HQ-VP-03.01` — EtherChannel Formation and LACP State
- `HQ-VP-03.02` — Port-Channel Trunk Policy
- `HQ-VP-03.03` — Operational Trunk and VLAN State
- `HQ-VP-03.04` — EtherChannel Member-Link Failure and Recovery

### Result

**Phase 03 verified.** `Po10`, `Po20`, and `Po30` formed successfully with all intended LACP members bundled. The approved trunk policy was operational across all three Port-Channels, and each bundle remained operational during a controlled single-member failure and recovered correctly after restoration.

Deterministic Rapid PVST+ root placement and forwarding behaviour remain for Phase 04.

### Evidence

[`evidence/hq/etherchannel/`](../../../evidence/hq/etherchannel/)

### Git traceability

Phase completion commit: [`7db4f05`](https://github.com/ddduddden/multi-site-cml-lab/commit/7db4f05124b244752e461084b1eeb7aaf7dcd132) (PR #7).

### Next

**Phase 04 — Rapid PVST+**

---

## Phase 04 — Rapid PVST+

**Completed:** `24-09-2026`

### Implemented

- Enabled Rapid PVST+ on `hq-a1`, `hq-d1`, and `hq-d2`.
- Configured `hq-d1` as root primary for VLANs `112,130,152,170,190`.
- Configured `hq-d2` as root primary for VLANs `120,140,160,199`.
- Configured each multilayer distribution switch as root secondary for the other's VLAN group.
- Configured deterministic `hq-d1` root placement for native VLAN `190`.
- Preserved the existing Phase 03 EtherChannel and trunk configuration.
- Applied Root Guard on the distribution-to-access Port-Channels (`hq-d1 Po10` and `hq-d2 Po20`) to protect the intended distribution-layer STP root placement from a superior BPDU arriving from the access layer.
- Corrected the VLAN `152` name on `hq-a1` to `GUEST` after a minor naming issue was identified during evidence review. No functional behaviour was affected.

### Verification

- `HQ-VP-04.01` — Rapid PVST+ Mode and Root Placement
- `HQ-VP-04.02` — Access-Layer Forwarding and Alternate Paths
- `HQ-VP-04.03` — STP Path Failure and Recovery

### Result

**Phase 04 verified.** Rapid PVST+ operated across all three HQ switches and matched the approved root-placement design. Representative VLAN checks confirmed the expected forwarding paths, and controlled failures of `Po10` and `Po20` proved alternate-path recovery in both directions.

SVI addressing and HSRP gateway redundancy remain for Phase 05.

### Evidence

[`evidence/hq/spanning-tree/`](../../../evidence/hq/spanning-tree/)

### Git traceability

Phase completion commit: [`2094b28`](https://github.com/ddduddden/multi-site-cml-lab/commit/2094b28d5f8a4b38719723c927ad3232ea69f09e) (PR #8).

### Next

**Phase 05 — SVIs and HSRP**

---

## Phase 05 — SVIs and HSRP

**Completed:** `27-09-2026`

### Implemented

- Configured the approved SVIs and HSRP gateways on `hq-d1` and `hq-d2`, using `.2` / `.3` physical addresses and `.1` virtual gateways.
- Applied HSRP group numbers matching each routed VLAN, priority `110` on the preferred peer and `100` on the standby peer, with preemption retained only on the preferred peer.
- Aligned HSRP ownership with the Phase 04 Rapid PVST+ root placement.
- Configured `hq-a1 Vlan199` as `10.10.99.4/26` with default gateway `10.10.99.1`, and used a temporary `Vlan112` SVI for gateway testing.
- Configured VTP `transparent` on all three switches so VLAN definitions were locally represented in the exported CML configuration.
- Corrected unintended HSRP group `0` configuration on `hq-d2`.
- Verified failover and recovery for representative VLANs `112` and `199`, then removed the temporary `hq-a1 Vlan112` SVI.
- Restored recent unsaved configuration after an unexpected VMware/CML interruption before verification continued; no fault was identified with the Phase 05 SVI or HSRP design.
- Updated the operating workflow so significant configuration milestones are written to startup configuration, followed by a CML configuration fetch and retained versioned YAML exports.

### Verification

- `HQ-VP-05.01` — SVI Addressing and Layer 3 Baseline
- `HQ-VP-05.02` — HSRP Configuration and Normal Operating State
- `HQ-VP-05.03` — HSRP/STP Alignment and Gateway Reachability
- `HQ-VP-05.04` — HSRP Gateway Failover
- `HQ-VP-05.05` — HSRP Preemption and Preferred-State Restoration

### Result

**Phase 05 verified.** The approved SVI addressing, normal HSRP ownership, STP/HSRP alignment and gateway reachability were demonstrated. Controlled failure of the preferred SVI for representative VLANs `112` and `199` transferred gateway ownership to the peer, and restoration returned each VLAN to its planned preferred Active peer. The temporary `hq-a1 Vlan112` test SVI was removed after testing.

During final review, redundant preemption statements were removed from the non-preferred priority-`100` peers so the as-built HSRP configuration matched the approved design. Final normal-state captures confirmed the intended preferred-only preemption policy and unchanged Active/Standby ownership; the completed failover tests were not repeated.

Routed `/31` Distribution-to-Edge links and loopbacks remain for Phase 06.

### Evidence

[`evidence/hq/hsrp/`](../../../evidence/hq/hsrp/)

### Git traceability

Phase completion commit: [`9e17f45`](https://github.com/ddduddden/multi-site-cml-lab/commit/9e17f4594ca03d354264e553a7f0109f12685366) (PR #9).

### Next

**Phase 06 — Routed `/31`s and Loopbacks**

---

## Phase 06 — Routed `/31` Underlay

**Completed:** `30-09-2026`

**Build window:** Combined with Phase 07.

### Implemented

- Converted `hq-d1` and `hq-d2` `Gi2/0`–`Gi2/3` and `Gi3/0` to routed ports.
- Addressed the ten Distribution-to-Edge links as `/31` point-to-point networks from the approved `10.255.10.0/24` infrastructure range.
- Used four direct routed links from `hq-d1` to `hq-r1`, four from `hq-d2` to `hq-r2`, and one cross-link from each distribution switch to the opposite edge router.
- Applied operational descriptions containing peer interface, subnet, and direct/cross-link role.
- Verified connected routes and direct peer reachability before any OSPF process existed.
- Preserved the historical phase boundary shown by the saved CML state: `Loopback0` identities were not yet configured at the end of Phase 06 and were introduced with Phase 07.

### Verification

- `HQ-VP-06.01` — Routed `/31` Interface Addressing and State
- `HQ-VP-06.02` — Direct `/31` Point-to-Point Reachability
- `HQ-VP-06.03` — Pre-OSPF Underlay Baseline

### Result

**Phase 06 verified.** All ten routed links were `up/up`, used the approved `/31` addressing, and provided bidirectional directly connected reachability. The pre-OSPF capture confirmed no OSPF router process existed on any of the four Layer 3 devices.

The original phase index placed the loopbacks in Phase 06, but the retained milestone state shows that they were actually introduced at the start of Phase 07. The phase was therefore renamed *Routed `/31` Underlay*, and the implementation record follows the observed build history rather than reconstructing a state that did not exist.

### Evidence

[`evidence/hq/layer3-underlay/`](../../../evidence/hq/layer3-underlay/)

### Milestone artifacts

The end-of-Phase-06 CML export is retained privately as the pre-OSPF rollback point and is not committed. The Phase 06 evidence was captured from that restored state. The committed `configs/hq/` files represent the Phase 07 milestone.

### Git traceability

Phase 06 verification evidence is included in the combined Phase 06–07 evidence snapshot: commit [`6608742`](https://github.com/ddduddden/multi-site-cml-lab/commit/66087426a6aa619e0177abca1238fad7c3213d70).

### Next

**Phase 07 — Loopbacks and OSPF Area 10**

---

## Phase 07 — Loopbacks and OSPF Area 10

**Completed:** `30-09-2026`

**Build window:** Combined with Phase 06.

### Implemented

- Added `Loopback0` identities `10.255.10.129/32`–`10.255.10.132/32` to `hq-r1`, `hq-r2`, `hq-d1`, and `hq-d2`.
- Configured OSPFv2 process `10` with explicit router IDs matching those loopbacks.
- Enabled OSPF through interface-level `ip ospf 10 area 10` configuration rather than broad network statements.
- Applied `passive-interface default` and made only the five routed Distribution-to-Edge interfaces per Layer 3 device non-passive.
- Kept the eight distribution SVIs and all four loopbacks passive while advertising their prefixes into Area `10`.
- Configured all ten routed Ethernet links as OSPF point-to-point.
- Applied cost `10` to the eight direct links and cost `100` to the two cross-links at both ends.
- Confirmed with `show ip protocols` that the operational OSPF maximum-path value on this image was `4`; no explicit `maximum-paths 4` line was present in the running configuration.
- Corrected an early Area `0` interface assignment on `hq-d2` so all five routed interfaces participated in Area `10` before final verification.
- Disabled IP routing on `hq-a1` with `no ip routing`, retaining `ip default-gateway 10.10.99.1`. The initial management reachability check showed that `hq-a1` could reach its HSRP gateway but not the four remote routing identities while IOSvL2 routing was active; `HQ-TS-001` records the investigation and correction.
- Captured a sanitised Phase 07 CML milestone export and readable per-device running configurations for the public repository.

### Verification

- `HQ-VP-07.01` — Loopback and OSPF Process Identity
- `HQ-VP-07.02` — OSPF Interface Participation, Network Type and Cost
- `HQ-VP-07.03` — OSPF Area 10 Adjacencies
- `HQ-VP-07.04` — OSPF Link-State Database and Learned Routing
- `HQ-VP-07.05` — Routed and End-to-End Reachability
- `HQ-VP-07.06` — Layer 2 and Gateway Regression

### Result

**Phase 07 verified.** Each Layer 3 device formed exactly five `FULL` point-to-point OSPF neighbours, giving ten unique routed-link adjacencies across Area `10`. All four Router LSAs were present, the expected HQ prefixes were learned, and all twelve sourced inter-device reachability checks succeeded.

`hq-a1` successfully reached the HSRP gateway and all four loopbacks while operating with `no ip routing` and `ip default-gateway 10.10.99.1`. Final regression captures confirmed the existing EtherChannel, Rapid PVST+, HSRP, and management-SVI state remained intact.

Route tables already expose multiple next hops and cost-driven path differences, but those behaviours remain deliberately reserved for the dedicated Phase 08 ECMP and Phase 09 cost-engineering verification.

### Evidence

[`evidence/hq/ospf/`](../../../evidence/hq/ospf/)

### Milestone artifacts

- `configs/hq/hq-r1-running-config.txt`
- `configs/hq/hq-r2-running-config.txt`
- `configs/hq/hq-d1-running-config.txt`
- `configs/hq/hq-d2-running-config.txt`
- `configs/hq/hq-a1-running-config.txt`
- `lab/cml-lab-exports/hq/hq-phase-07-ospf-area10-2026-09-30.yaml`

### Git traceability

Phase 07 as-built configs, verification evidence, and milestone CML export: commit [`6608742`](https://github.com/ddduddden/multi-site-cml-lab/commit/66087426a6aa619e0177abca1238fad7c3213d70).

### Next

**Phase 08 — ECMP**

---

## Phase 08 — ECMP

**Completed:** `30-09-2026`

### Implemented

- Made no permanent configuration change.
- Verified the four-route ECMP behaviour exposed by the Phase 07 OSPF design.
- Confirmed selected metric-`11` four-route sets in the routing table.
- Verified CEF-selected forwarding with interface counters.
- Confirmed that more than one installed ECMP member carried the test traffic.
- Contracted and restored a selected ECMP route set from four routes to one and back to four.
- Verified the lab-observed four-path OSPF installation limit with a fifth equal-cost route available.

### Verification

- `HQ-VP-08.01` — ECMP Route Installation
- `HQ-VP-08.02` — CEF Path Selection
- `HQ-VP-08.03` — Aggregate ECMP Forwarding
- `HQ-VP-08.04` — ECMP Contraction and Restoration
- `HQ-VP-08.05` — Four-Path Maximum

### Result

**Phase 08 verified.** The intended four-route OSPF ECMP sets were present in the routing table, and the forwarding tests showed that more than one installed path was actually used. Controlled link removal contracted the selected route set from four routes to one, and restoration rebuilt it to four.

The test also showed five equal-cost paths from `hq-r1` to `hq-r2 Loopback0` (`10.255.10.130/32`). With the lab-observed maximum-path value of four, OSPF kept four next hops installed, and the previously omitted route entered the routing table when one installed path was removed.

### Evidence

[`evidence/hq/ospf/`](../../../evidence/hq/ospf/)

### Milestone artifacts

No new milestone artifact. Phase 08 changed no intended device configuration; the Phase 07 configs and CML export remain current.

### Git traceability

Phase 08/09 verification evidence commit: `79d27bf`.

### Next

**Phase 09 — OSPF Cost Engineering**

---

## Phase 09 — OSPF Cost Engineering

**Completed:** `30-09-2026`

### Implemented

- Made no permanent configuration change.
- Verified that normal OSPF route selection follows the approved cost policy.
- Confirmed that selected campus and infrastructure routes followed the expected OSPF costs: metric `11` on the direct paths and metrics `101` and `110` on the higher-cost cross-link paths.
- Removed each four-link direct edge/distribution set in turn and verified the surviving higher-cost routes.
- Confirmed alternate reachability with sourced pings and traceroutes.
- Restored all direct links and verified return to the normal ECMP and OSPF state.
- Compared the post-test CML export with the committed Phase 07 configuration files and found no unexpected configuration changes.

### Verification

- `HQ-VP-09.01` — Normal Cost-Driven Selection
- `HQ-VP-09.02` — Higher-Cost Alternate Activation
- `HQ-VP-09.03` — Preferred-Route Restoration

### Result

**Phase 09 verified.** Normal routing followed the configured OSPF cost policy. When a complete four-link direct set was removed, OSPF moved the affected routes onto the surviving higher-cost routes through the opposite edge/distribution pair, and reachability remained available.

Restoring the direct links returned the selected campus routes to metric `11`, rebuilt the four-route ECMP sets, and returned all four Layer 3 devices to five `FULL` OSPF neighbours. The final health check matched the Phase 07 operating baseline.

### Evidence

[`evidence/hq/ospf/`](../../../evidence/hq/ospf/)

### Milestone artifacts

No new milestone artifact. Phase 09 changed no intended device configuration; the Phase 07 configs and CML export remain current.

### Git traceability

Phase 08/09 verification evidence commit: `79d27bf`.

### Next

**Phase 10 — Failure Testing**
