# HQ Verification Plan

[Portfolio](../../../README.md) / [HQ Implementation](README.md) / Verification Plan

This document defines what the HQ implementation must prove before a feature is treated as verified as-built.

It is a **controlled living document**. Verification IDs remain permanent, and the records reflect the CML behaviour observed during implementation and testing.

Phases 01–09 retain their individual verification records. Phases 06/07 and 08/09 were completed in combined build and test windows, with separate IDs maintained for each phase. Phase 10 records the completed failure testing and its findings. Phase 11 records final operational checks and the accepted HQ V1 engineering close-out.

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-VP-XX.YY` | HQ verification test — phase `XX`, test `YY` |
| `HQ-TS-NNN` | Related HQ troubleshooting record |
| `HQ-DEV-NNN` | Related HQ design deviation |

## Standard test record

Each verification test uses the same structure:

```text
Objective
Expected result
Configuration involved
Verification command(s)
Observed result
Status
Evidence
Notes / Troubleshooting
```

Each verification test uses the `Status` field to record its result.

| Status | Meaning |
|---|---|
| `Not started` | The test has not been run yet. |
| `In progress` | The test or related investigation is currently underway. |
| `Verified` | The expected behaviour has been demonstrated and recorded. |
| `Blocked` | The test cannot currently be completed because an unresolved issue, dependency, or platform limitation is preventing progress. |
| `Deviated` | The implementation intentionally differs from the design and an accepted `HQ-DEV-NNN` record exists for the test. |

There is no separate Pass/Fail field for Phases 01–09. `Blocked` means the test cannot currently be completed; it does not mean the test has permanently failed. Phase 10 uses PASS, FAIL and INCONCLUSIVE in its separate test reports.

## Git traceability

Git commit references are included throughout the verification plan to provide a record of each implementation milestone. They allow changes to be traced back to the corresponding configuration, documentation and verification evidence, rather than presenting only the finished network.

Browse the [HQ Evidence Map](../../../evidence/hq/README.md) for the complete evidence index.

## Contents

[Explore the Test Investigations](../../../evidence/hq/README.md#follow-the-evidence)

[← Test planning](phase-10-test-plan.md)

[![Choose Another Route ↗](https://img.shields.io/badge/CHOOSE%20ANOTHER%20ROUTE%20%E2%86%97-C2185B?style=flat-square)](../../../README.md#explore-the-hq-project)

| Phase | Scope | Detail |
|---:|---|---|
| [01](#phase-01--platform-baseline) | Platform Baseline | [View phase](#phase-01--platform-baseline) |
| [02](#phase-02--layer-2--vlan-baseline) | Layer 2 / VLAN Baseline | [View phase](#phase-02--layer-2--vlan-baseline) |
| [03](#phase-03--lacp-etherchannel) | LACP EtherChannel | [View phase](#phase-03--lacp-etherchannel) |
| [04](#phase-04--rapid-pvst) | Rapid PVST+ | [View phase](#phase-04--rapid-pvst) |
| [05](#phase-05--svis-and-hsrp) | SVIs and HSRP | [View phase](#phase-05--svis-and-hsrp) |
| [06](#phase-06--routed-31-underlay) | Routed `/31` Underlay | [View phase](#phase-06--routed-31-underlay) |
| [07](#phase-07--loopbacks-and-ospf-area-10) | Loopbacks and OSPF Area 10 | [View phase](#phase-07--loopbacks-and-ospf-area-10) |
| [08](#phase-08--ecmp) | ECMP | [View phase](#phase-08--ecmp) |
| [09](#phase-09--ospf-cost-engineering) | OSPF Cost Engineering | [View phase](#phase-09--ospf-cost-engineering) |
| [10](#phase-10--failure-testing) | Failure Testing | [View phase](#phase-10--failure-testing) |
| [11](#phase-11--final-acceptance) | Final Acceptance | [View phase](#phase-11--final-acceptance) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 01 — Platform Baseline

[HQ-VP-01.01](#hq-device-inventory--hq-vp-0101) | [HQ-VP-01.02](#image-and-software-version-inventory--hq-vp-0102) | [HQ-VP-01.03](#interface-inventory-and-topology-fit--hq-vp-0103) | [HQ-VP-01.04](#platform-capability-review--hq-vp-0104)

**Completed:** `20-09-2026`

**Git traceability:** [`9d99722` — Document and verify HQ platform baseline](https://github.com/ddduddden/multi-site-cml-lab/commit/9d9972296d28a4456f54e4ed38fdb70b45f2060f).

**Objective:** Establish exactly what is running before assuming anything about node type, image, interface naming, interface count, licensing, or planned feature availability.

---

### HQ Device Inventory — HQ-VP-01.01

**Objective:**\
Confirm that all five intended HQ devices exist in CML with the expected hostnames and roles.

**Expected result:**\
`hq-r1`, `hq-r2`, `hq-d1`, `hq-d2`, and `hq-a1` are present and console-accessible.

**Configuration involved:**\
None.

**Verification command(s):**\
Confirm the five CML nodes and labels in the topology, then capture basic device identity from the CLI.

**Observed result:**\
All five intended HQ devices were present in the CML topology with the expected hostnames. `hq-r1` and `hq-r2` were available as IOSv edge routers; `hq-d1` and `hq-d2` as IOSvL2 multilayer distribution switches; and `hq-a1` as the IOSvL2 access switch. All five devices were booted and console-accessible.

**Status:**\
Verified

**Evidence:** [HQ-VP-01.01 — captures](../../../evidence/hq/platform-baseline/README.md#hq-vp-0101)

**Notes / Troubleshooting:**\
No troubleshooting record required.

---

### Image and Software Version Inventory — HQ-VP-01.02

**Objective:**\
Confirm the software image and version running on each HQ device.

**Expected result:**\
The image and software version are identified for all five devices before configuration begins.

**Configuration involved:**\
None.

**Verification command(s):**\
`show version`

**Observed result:**\
`hq-r1` and `hq-r2` were running Cisco IOSv Software Version `15.9(3)M12`, RELEASE SOFTWARE `(fc1)`. `hq-d1`, `hq-d2`, and `hq-a1` were running Cisco IOSvL2 (`vios_l2`) Experimental Version `15.2(20200924:215240)` `[sweickge-sep24-2020-l2iol-release 135]`. These were the expected image types for the planned HQ device roles.

**Status:**\
Verified

**Evidence:** [HQ-VP-01.02 — captures](../../../evidence/hq/platform-baseline/README.md#hq-vp-0102)

**Notes / Troubleshooting:**\
No troubleshooting record required.

---

### Interface Inventory and Topology Fit — HQ-VP-01.03

**Objective:**\
Confirm the available interface names and counts can support the intended HQ topology.

**Expected result:**\
Each device has the required interfaces for its planned role, and the actual interface names are recorded before configuration.

**Configuration involved:**\
Physical CML links were added only after the interface inventory was verified; no production feature configuration was applied.

**Verification command(s):**\
`show ip interface brief`; compare the available interfaces with the interface allocations in the HQ Campus Design.

**Observed result:**\
`hq-r1` and `hq-r2` each had eight GigabitEthernet interfaces available (`Gi0/0`–`Gi0/7`). `hq-d1`, `hq-d2`, and `hq-a1` each had sixteen GigabitEthernet interfaces available (`Gi0/0`–`Gi3/3`). This was enough for the planned HQ topology. The 18 CML links were then added and checked against the interface allocations in the **HQ Campus Design**.

**Status:**\
Verified

**Evidence:** [HQ-VP-01.03 — captures](../../../evidence/hq/platform-baseline/README.md#hq-vp-0103)

**Notes / Troubleshooting:**\
No troubleshooting record required.

---

### Platform Capability Review — HQ-VP-01.04

**Objective:**\
Identify any known platform or image constraint that would block the planned HQ features before implementation begins.

**Expected result:**\
No unresolved capability issue blocks the planned use of Layer 2 LACP, Rapid PVST+, HSRP, OSPF, routed interfaces, or the later ECMP design.

**Configuration involved:**\
Testing was carried out on `hq-d1` (IOSvL2) and `hq-r1` (IOSv). Temporary test configuration was removed afterwards.

**Verification command(s):**\
Platform-appropriate `show` commands and context-sensitive CLI help were used to check support for the required features. Cleanup was confirmed with `show running-config` and interface-state checks.

**Observed result:**\
Testing on `hq-d1` and `hq-r1` confirmed that the IOSvL2 and IOSv images support the main features required by the HQ design, including LACP, Rapid PVST+, HSRP, routed interfaces, OSPF and ECMP. Temporary test configuration was removed afterwards and the devices were returned to their baseline state. No platform limitation was found that would prevent the planned HQ build.

**Status:**\
Verified

**Evidence:** [HQ-VP-01.04 — captures](../../../evidence/hq/platform-baseline/README.md#hq-vp-0104)

**Notes / Troubleshooting:**\
These checks confirm platform support only. Operational protocol behaviour, failover, convergence, path selection, and summarisation will be tested during the later implementation phases. No troubleshooting record required.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 02 — Layer 2 / VLAN Baseline

[HQ-VP-02.01](#vlan-database--hq-vp-0201) | [HQ-VP-02.02](#access-port-assignments--hq-vp-0202) | [HQ-VP-02.03](#parking-vlan-policy--hq-vp-0203)

**Completed:** `21-09-2026`

**Git traceability:** [`e6f7201` — Complete HQ Phase 02 Layer 2 VLAN baseline](https://github.com/ddduddden/multi-site-cml-lab/commit/e6f7201131b7bef53612278bd5cdf2d98b3fbf5f).

**Objective:** Establish the VLAN database, intended access-port assignments, and parking-VLAN policy before EtherChannel/trunk implementation begins.

Native-VLAN and trunk verification belongs to Phase 03 because the production trunks are created and verified with the EtherChannels there.

---

### VLAN Database — HQ-VP-02.01

**Objective:**\
Confirm that all intended HQ VLANs exist on each switch that requires them.

**Expected result:**\
Required VLAN IDs and names match the approved HQ design on `hq-d1`, `hq-d2`, and `hq-a1`.

**Configuration involved:**\
VLAN creation and naming on the applicable switches.

**Verification command(s):**\
`show vlan brief`

**Observed result:**\
All ten approved HQ VLANs were present and active on `hq-d1`, `hq-d2`, and `hq-a1`, with VLAN IDs and names matching the approved design.

VLAN `1` remained present as the platform default but was not used for production or management access. VLAN `190` remains reserved as the native VLAN for the Phase 03 trunk implementation.

**Status:**\
Verified

**Evidence:** [HQ-VP-02.01 — captures](../../../evidence/hq/layer2-vlan-baseline/README.md#hq-vp-0201)

**Notes / Troubleshooting:**\
No troubleshooting record required.

---

### Access-Port Assignments — HQ-VP-02.02

**Objective:**\
Confirm every intended HQ access port has the correct access VLAN and, where required, voice VLAN.

**Expected result:**\
Access-port and voice-VLAN assignments match the approved HQ access-switch port plan.

**Configuration involved:**\
Access-mode, access-VLAN, and voice-VLAN configuration on the intended access ports.

**Verification command(s):**\
`show vlan brief`; `show interfaces switchport`

**Observed result:**\
`hq-a1` access-port assignments matched the approved HQ port plan. All eight endpoint-facing interfaces were configured as static access ports with the correct access VLANs, and `Gi2/0` was additionally assigned voice VLAN `120` (`VOICE`).

All endpoint-facing interfaces were administratively enabled and remained operationally down because no endpoints were connected during verification.

**Status:**\
Verified

**Evidence:** [HQ-VP-02.02 — captures](../../../evidence/hq/layer2-vlan-baseline/README.md#hq-vp-0202)

**Notes / Troubleshooting:**\
No troubleshooting record required.

---

### Parking-VLAN Policy — HQ-VP-02.03

**Objective:**\
Confirm `hq-a1` interfaces that are not yet in service during Phase 02 are separated from production VLANs and administratively disabled.

**Expected result:**\
All `hq-a1` interfaces not yet in service are assigned to VLAN `191` (`PARKING`) and administratively shut down. Future `Po10` and `Po20` member interfaces remain parked until Phase 03.

**Configuration involved:**\
Parking-VLAN assignment and administrative shutdown of `hq-a1` interfaces not yet in service.

**Verification command(s):**\
`show vlan brief`; `show ip interface brief`; `show interfaces switchport`

**Observed result:**\
All `hq-a1` interfaces not yet in service during Phase 02 were assigned to VLAN `191` (`PARKING`) and administratively shut down.

The future `Po10` and `Po20` member interfaces remain parked until Phase 03, when they will be reconfigured for their intended EtherChannel trunk roles.

**Status:**\
Verified

**Evidence:** [HQ-VP-02.03 — captures](../../../evidence/hq/layer2-vlan-baseline/README.md#hq-vp-0203)

**Notes / Troubleshooting:**\
No troubleshooting record required.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 03 — LACP EtherChannel

[HQ-VP-03.01](#etherchannel-formation-and-lacp-state--hq-vp-0301) | [HQ-VP-03.02](#port-channel-trunk-policy--hq-vp-0302) | [HQ-VP-03.03](#operational-trunk-and-vlan-state--hq-vp-0303) | [HQ-VP-03.04](#etherchannel-member-link-failure-and-recovery--hq-vp-0304)

**Completed:** `22-09-2026`

**Git traceability:** [`7db4f05` — Complete HQ Phase 03 LACP EtherChannel](https://github.com/ddduddden/multi-site-cml-lab/commit/7db4f05124b244752e461084b1eeb7aaf7dcd132).

**Objective:** Build and verify `Po10`, `Po20`, and `Po30`, including LACP formation, member participation, 802.1Q trunking, native-VLAN consistency, allowed-VLAN policy, and member-link resilience.

Phase 03 verifies the Layer 2 EtherChannel and trunk infrastructure before deterministic Rapid PVST+ root placement or Layer 3 gateway services are introduced.

Per-VLAN Layer 3 gateway reachability is intentionally deferred to Phase 05, after the production SVIs and HSRP gateways exist.

---

### EtherChannel Formation and LACP State — HQ-VP-03.01

**Objective:**\
Confirm that `Po10`, `Po20`, and `Po30` form successfully using LACP and contain the intended physical member interfaces.

**Expected result:**\
`Po10`, `Po20`, and `Po30` are operational LACP EtherChannels with all intended physical members bundled correctly and no unexpected suspended or standalone members.

**Configuration involved:**\
LACP `active` mode on the intended physical members and creation of `Po10`, `Po20`, and `Po30`.

**Verification command(s):**\
`show etherchannel summary`; `show lacp neighbor`

**Observed result:**\
`Po10`, `Po20`, and `Po30` formed successfully as Layer 2 LACP EtherChannels. All intended physical members were bundled in their respective Port-Channels with no suspended or standalone members. LACP neighbor output confirmed Active-mode peers on all three bundles.

**Status:**\
Verified

**Evidence:** [HQ-VP-03.01 — captures](../../../evidence/hq/etherchannel/README.md#hq-vp-0301)

**Notes / Troubleshooting:**\
No troubleshooting record required.

---

### Port-Channel Trunk Policy — HQ-VP-03.02

**Objective:**\
Confirm that all three logical Port-Channels use the approved HQ 802.1Q trunk policy and that the physical members operate consistently with their logical bundle.

**Expected result:**\
All three Port-Channels operate as 802.1Q trunks using native VLAN `190` and allowed VLANs `112,120,130,140,152,160,170,190,199`, with VLAN `191` excluded and no conflicting member configuration.

**Configuration involved:**\
Trunk configuration on `Po10`, `Po20`, and `Po30`, including the explicit native VLAN and allowed-VLAN list.

**Verification command(s):**\
`show interfaces trunk`; `show etherchannel summary`

**Observed result:**\
`Po10`, `Po20`, and `Po30` operated as 802.1Q trunks using native VLAN `190`. Each Port-Channel carried the approved allowed-VLAN list `112,120,130,140,152,160,170,190,199`, with VLAN `191` excluded.

**Status:**\
Verified

**Evidence:** [HQ-VP-03.02 — captures](../../../evidence/hq/etherchannel/README.md#hq-vp-0302)

**Notes / Troubleshooting:**\
The effective Port-Channel and trunk behaviour was confirmed from observed IOSvL2 output. No troubleshooting record required.

---

### Operational Trunk and VLAN State — HQ-VP-03.03

**Objective:**\
Confirm that the configured Port-Channels are operational trunks and that the intended VLANs are active on the Layer 2 trunk infrastructure.

**Expected result:**\
`Po10`, `Po20`, and `Po30` report an operational trunk state with the approved VLAN set active. Final per-VLAN STP forwarding behaviour is deferred to Phase 04.

**Configuration involved:**\
No additional configuration beyond the completed Phase 03 EtherChannel and trunk configuration.

**Verification command(s):**\
`show interfaces trunk`; `show etherchannel summary`

**Observed result:**\
All three Port-Channels were operational trunks and the complete approved VLAN set was shown as allowed and active. At the time of verification, `hq-d2 Po20` showed no VLANs in the spanning-tree forwarding state; deterministic per-VLAN spanning-tree forwarding behaviour remains intentionally deferred to Phase 04.

**Status:**\
Verified

**Evidence:** [HQ-VP-03.03 — captures](../../../evidence/hq/etherchannel/README.md#hq-vp-0303)

**Notes / Troubleshooting:**\
Per-VLAN gateway reachability remains deferred until Phase 05. No troubleshooting record required.

---

### EtherChannel Member-Link Failure and Recovery — HQ-VP-03.04

**Objective:**\
Confirm that loss of a physical EtherChannel member does not bring down the logical Port-Channel while other valid members remain available, and that the failed member rejoins correctly after recovery.

**Expected result:**\
A controlled member-link failure removes only the affected member while the Port-Channel remains operational; the restored member automatically rejoins the bundle.

**Configuration involved:**\
Controlled administrative failure and restoration of selected physical EtherChannel members.

**Verification command(s):**\
`show etherchannel summary`

**Observed result:**\
A single physical member was administratively removed and restored on each of `Po10`, `Po20`, and `Po30`. In every test the affected member left the bundle while the logical Port-Channel remained operational using the surviving members. After restoration, each member automatically rejoined its EtherChannel. During `Po30` recovery, the restored member briefly entered LACP hot-standby state before returning to the bundled state.

**Status:**\
Verified

**Evidence:** [HQ-VP-03.04 — captures](../../../evidence/hq/etherchannel/README.md#hq-vp-0304)

**Notes / Troubleshooting:**\
No troubleshooting record required. The complete Port-Channel, device and combined failure scenarios are recorded in the [Phase 10 results](../../../evidence/hq/failure-tests/README.md).

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 04 — Rapid PVST+

[HQ-VP-04.01](#rapid-pvst-mode-and-root-placement--hq-vp-0401) | [HQ-VP-04.02](#access-layer-forwarding-and-alternate-paths--hq-vp-0402) | [HQ-VP-04.03](#stp-path-failure-and-recovery--hq-vp-0403)

**Completed:** `24-09-2026`

**Git traceability:** [`2094b28` — Complete HQ Phase 04 Rapid PVST+](https://github.com/ddduddden/multi-site-cml-lab/commit/2094b28d5f8a4b38719723c927ad3232ea69f09e).

**Objective:**\
Verify Rapid PVST+ mode, deterministic root placement, forwarding paths, alternate-path behaviour, and recovery after controlled EtherChannel failures.

---

### Rapid PVST+ Mode and Root Placement — HQ-VP-04.01

**Objective:**\
Confirm that Rapid PVST+ is operating across the HQ switching topology and that the intended root-primary and root-secondary placement is established for each participating VLAN.

**Expected result:**\
Rapid PVST+ is active, with `hq-d1` root for VLANs `112,130,152,170,190` and `hq-d2` root for VLANs `120,140,160,199`. The other multilayer distribution switch holds the secondary role for each group.

**Configuration involved:**\
Rapid PVST+ mode and the approved root-primary/root-secondary assignments on `hq-d1` and `hq-d2`.

**Verification command(s):**\
`show spanning-tree summary`; `show spanning-tree root`; `show spanning-tree bridge`; representative `show spanning-tree vlan <vlan-id>` checks.

**Observed result:**\
`show spanning-tree summary` confirmed Rapid PVST+ mode on all three HQ switches. Root placement matched the approved design: `hq-d1` was root for VLANs `112,130,152,170,190`, while `hq-d2` was root for VLANs `120,140,160,199`. Root switches used base priority `24576`, secondaries `28672`, and `hq-a1` retained the default `32768`. `hq-a1` used `Po10` toward the `hq-d1` group and `Po20` toward the `hq-d2` group.

**Status:**\
Verified

**Evidence:** [HQ-VP-04.01 — captures](../../../evidence/hq/spanning-tree/README.md#hq-vp-0401)

**Notes / Troubleshooting:**\
VLAN `1` remains locally present on the multilayer distribution switches because unused ports remain assigned to it. It is not carried on the production trunks and is outside the Phase 04 root-placement policy.

An early VLAN `112` capture showed a transient root-state mismatch immediately after the STP changes. The condition cleared without configuration changes and the final topology matched the design.

No troubleshooting record required.

---

### Access-Layer Forwarding and Alternate Paths — HQ-VP-04.02

**Objective:**\
Confirm that Rapid PVST+ produces the expected forwarding paths and places the redundant EtherChannel into the alternate state.

**Expected result:**\
`hq-a1` uses the preferred path toward the correct root bridge for each VLAN group, while the other EtherChannel remains available as the alternate path.

**Configuration involved:**\
No additional configuration beyond the completed Rapid PVST+ root-placement policy.

**Verification command(s):**\
`show spanning-tree vlan <vlan-id>` on `hq-a1`, `hq-d1`, and `hq-d2`.

**Observed result:**\
Representative VLANs confirmed the expected forwarding paths. VLAN `112` used `Po10` toward `hq-d1`, while VLAN `120` used `Po20` toward `hq-d2`, with the opposite Port-Channel held as the alternate path. The resulting topology was loop-free and matched the intended design.

**Status:**\
Verified

**Evidence:** [HQ-VP-04.02 — captures](../../../evidence/hq/spanning-tree/README.md#hq-vp-0402)

**Notes / Troubleshooting:**\
VLANs `112` and `120` were used as representative examples for the two root-placement groups. The blocked path was located at `hq-a1`; during Phase 03, before deterministic root placement was configured, `hq-d2 Po20` showed no VLANs in the spanning-tree forwarding state.

No troubleshooting record required.

---

### STP Path Failure and Recovery — HQ-VP-04.03

**Objective:**\
Confirm that Rapid PVST+ uses the alternate EtherChannel when a preferred path fails and returns to the normal forwarding path after recovery.

**Expected result:**\
Loss of either EtherChannel causes the alternate path to become active for the affected VLAN group. Restoring the EtherChannel returns the topology to its normal state.

**Configuration involved:**\
Controlled shutdown and restoration of `Po10` with VLAN `112`, and `Po20` with VLAN `120`, to verify failover in both directions.

**Verification command(s):**\
`show spanning-tree vlan <vlan-id>`; `show interfaces trunk`; `show etherchannel summary`

**Observed result:**\
Failure of `Po10` for VLAN `112` and `Po20` for VLAN `120` caused the alternate Port-Channel to become the forwarding path while the root bridge remained unchanged. In both tests, the root-path cost increased from `3` to `6` during failure and returned to `3` after recovery.

**Status:**\
Verified

**Evidence:** [HQ-VP-04.03 — captures](../../../evidence/hq/spanning-tree/README.md#hq-vp-0403)

**Notes / Troubleshooting:**\
The logical Port-Channels were shut down so the tests exercised complete EtherChannel failure rather than repeating the member-link resilience already verified in Phase 03.

Whole-switch and combined Layer 2/Layer 3 failures are covered in the [Phase 10 results](../../../evidence/hq/failure-tests/README.md).

No troubleshooting record required.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 05 — SVIs and HSRP

[HQ-VP-05.01](#svi-addressing-and-layer-3-baseline--hq-vp-0501) | [HQ-VP-05.02](#hsrp-configuration-and-normal-operating-state--hq-vp-0502) | [HQ-VP-05.03](#hsrpstp-alignment-and-gateway-reachability--hq-vp-0503) | [HQ-VP-05.04](#hsrp-gateway-failover--hq-vp-0504) | [HQ-VP-05.05](#hsrp-preemption-and-preferred-state-restoration--hq-vp-0505)

**Completed:** `27-09-2026`

**Git traceability:** [`9e17f45` — Complete HQ Phase 05 SVIs and HSRP](https://github.com/ddduddden/multi-site-cml-lab/commit/9e17f4594ca03d354264e553a7f0109f12685366).

**Objective:** Build and verify the HQ routed VLAN interfaces and first-hop gateway redundancy, including SVI addressing, HSRP operating state, STP/HSRP alignment, gateway reachability, failover, and recovery to the preferred state.

`hq-a1` uses VLAN `199` for in-band management, with address `10.10.99.4/26` and default gateway `10.10.99.1`.

---

### SVI Addressing and Layer 3 Baseline — HQ-VP-05.01

**Objective:**\
Confirm the production SVI addressing on `hq-d1` and `hq-d2`, establish the VLAN 199 management SVI on `hq-a1`, and verify that only the intended VLANs provide Layer 3 interfaces.

**Expected result:**\
All eight routed VLANs use the approved `.1` VIP / `.2 hq-d1` / `.3 hq-d2` convention and subnet masks. `hq-a1` uses `10.10.99.4/26` on VLAN `199` with default gateway `10.10.99.1`. VLANs `190` and `191` have no Layer 3 interfaces.

**Configuration involved:**\
SVI addressing on `hq-d1` and `hq-d2`, plus the VLAN 199 management SVI and default-gateway configuration on `hq-a1`.

**Verification command(s):**\
`show ip interface brief`; `show running-config | section ^interface Vlan`; `show running-config | include ^ip default-gateway` on `hq-a1`.

**Observed result:**\
All eight SVIs on `hq-d1` and `hq-d2` were up/up with the approved addresses and masks. Neither switch had a VLAN `190` or `191` SVI. Following temporary-SVI removal, `hq-a1` retained only `Vlan199`, up/up at `10.10.99.4/26`, with default gateway `10.10.99.1`.

**Status:**\
Verified

**Evidence:** [HQ-VP-05.01 — captures](../../../evidence/hq/hsrp/README.md#hq-vp-0501)

**Notes / Troubleshooting:**\
The final baseline was captured on `27-09-2026`. Temporary `hq-a1 Vlan112` removal is also referenced by `HQ-VP-05.05`.

Forward note (`30-09-2026`): [`HQ-TS-001`](troubleshooting.md#hq-ts-001--iosvl2-routing-mode-on-hq-a1) found that IPv4 routing was operational on `hq-a1` under the IOSvL2 image's initial state, so the configured `ip default-gateway` was not used until `no ip routing` was applied in Phase 07. All Phase 05 `hq-a1` tests used targets in the same VLAN as their source, so the recorded Phase 05 results are unaffected.

---

### HSRP Configuration and Normal Operating State — HQ-VP-05.02

**Objective:**\
Confirm that every routed VLAN has the intended HSRP group, virtual IP, priority, preemption policy, and Active/Standby ownership.

**Expected result:**\
All eight HSRP groups use the approved virtual IPs and VLAN-matching group numbers. Each preferred peer is Active at priority `110`, with the standby peer at priority `100`. Preemption is enabled on the preferred peer only.

**Configuration involved:**\
HSRP configuration on the eight routed VLAN SVIs on `hq-d1` and `hq-d2`.

**Verification command(s):**\
`show running-config | section ^interface Vlan`; `show standby brief`

**Observed result:**\
Final captures confirmed the approved virtual IPs and group numbers, priority `110` on each preferred peer, priority `100` on the standby peer, and preemption only on the preferred peer. `hq-d1` was Active for VLANs `112,130,152,170`; `hq-d2` was Active for VLANs `120,140,160,199`.

**Status:**\
Verified

**Evidence:** [HQ-VP-05.02 — captures](../../../evidence/hq/hsrp/README.md#hq-vp-0502)

**Notes / Troubleshooting:**\
An unintended HSRP group `0` on `hq-d2` and redundant preemption on the non-preferred peers were removed before the final state was recaptured. No troubleshooting or deviation record required.

---

### HSRP/STP Alignment and Gateway Reachability — HQ-VP-05.03

**Objective:**\
Confirm that HSRP Active ownership matches the Rapid PVST+ root-primary placement and that the virtual gateways are reachable through the access-layer topology.

**Expected result:**\
The HSRP Active peer is also the Rapid PVST+ root switch for each routed VLAN. For representative VLANs `112` and `199`, `hq-a1` can reach the virtual gateway and both distribution-switch SVI addresses.

**Configuration involved:**\
HSRP and Rapid PVST+ on `hq-d1` and `hq-d2`, with gateway testing from `hq-a1` using its permanent `Vlan199` management SVI and temporary `Vlan112` SVI (`10.10.12.4/22`).

**Verification command(s):**\
`show ip interface brief`; `ping` from `hq-a1`. HSRP state is cross-referenced to `HQ-VP-05.02`; STP root placement and access-layer root ports to `HQ-VP-04.01`.

**Observed result:**\
HSRP Active ownership matched the recorded STP root placement. All six gateway targets returned `5/5`. The Phase 04 evidence shows `hq-a1` using root port `Po10` for VLAN `112` and `Po20` for VLAN `199`.

**Status:**\
Verified

**Evidence:** [HQ-VP-05.03 — captures](../../../evidence/hq/hsrp/README.md#hq-vp-0503)

**Notes / Troubleshooting:**\
STP state comes from the earlier Phase 04 capture, rather than a simultaneous ping capture. The temporary `Vlan112` SVI remained through failover testing; final removal is recorded in `HQ-VP-05.05`.

---

### HSRP Gateway Failover — HQ-VP-05.04

**Objective:**\
Confirm that gateway service recovers through the Standby peer when the preferred Active SVI becomes unavailable.

**Expected result:**\
The Standby peer becomes Active, retains the same virtual IP and provides gateway reachability after convergence. Tests cover VLAN `112` with `hq-d1` unavailable and VLAN `199` with `hq-d2` unavailable.

**Configuration involved:**\
Controlled shutdown of `hq-d1 Vlan112` and, separately, `hq-d2 Vlan199`, with gateway testing from `hq-a1`.

**Verification command(s):**\
`show standby brief`; `ping` from `hq-a1`; `show ip interface brief` on `hq-d2` to confirm the VLAN `199` shutdown state.

**Observed result:**\
Shutting down `hq-d1 Vlan112` caused `hq-d2` to become Active for group `112`; a post-failover ping returned `5/5`. Shutting down `hq-d2 Vlan199` caused `hq-d1` to become Active for group `199`; both post-failover pings returned `5/5`. The virtual IPs remained unchanged.

**Status:**\
Verified

**Evidence:** [HQ-VP-05.04 — captures](../../../evidence/hq/hsrp/README.md#hq-vp-0504)

**Notes / Troubleshooting:**\
The VLAN `199` sequence includes an early capture taken before convergence; later evidence confirms `hq-d2 Vlan199` down and `hq-d1` Active. The tests were completed before redundant non-preferred preemption was removed; that cleanup does not change the recorded failover results. Final HSRP state is recorded in `HQ-VP-05.02`. Whole-device and combined STP/HSRP failures are documented in the [Phase 10 results](../../../evidence/hq/failure-tests/README.md).

---

### HSRP Preemption and Preferred-State Restoration — HQ-VP-05.05

**Objective:**\
Confirm that restoration of the preferred gateway returns HSRP ownership to the intended peer and that temporary access-switch test configuration is removed.

**Expected result:**\
Preemption restores the planned Active/Standby ownership and HSRP/STP alignment. `hq-a1` retains its permanent `Vlan199` management SVI, with the temporary `Vlan112` SVI removed.

**Configuration involved:**\
Restoration of `hq-d1 Vlan112` and `hq-d2 Vlan199`, followed by removal of the temporary `hq-a1 Vlan112` SVI.

**Verification command(s):**\
`show standby brief`; `show ip interface brief`; `show spanning-tree root`; `ping` from `hq-a1`.

**Observed result:**\
VLAN `112` returned to `hq-d1` Active / `hq-d2` Standby, and VLAN `199` returned to `hq-d2` Active / `hq-d1` Standby. Recovery pings returned `4/5`, then `5/5` in both tests. All eight groups returned to planned ownership, the final STP root-port split matched the design, the temporary `Vlan112` SVI was removed, and `Vlan199` remained up/up at `10.10.99.4/26`.

**Status:**\
Verified

**Evidence:** [HQ-VP-05.05 — captures](../../../evidence/hq/hsrp/README.md#hq-vp-0505)

**Notes / Troubleshooting:**\
One earlier VLAN `112` recovery ping could not be reliably linked to the final test run, so it was excluded from the evidence. The bridge MAC addresses differed from the Phase 04 capture after the CML environment was restored. CML assigns MAC addresses automatically, and recreated or wiped nodes can receive new addresses; however, the configured STP priorities and intended `Po10`/`Po20` roles were unchanged, so the planned root and forwarding design remained the same. Final as-built preemption policy is recorded in `HQ-VP-05.02`.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 06 — Routed `/31` Underlay

[HQ-VP-06.01](#routed-31-interface-addressing-and-state--hq-vp-0601) | [HQ-VP-06.02](#direct-31-point-to-point-reachability--hq-vp-0602) | [HQ-VP-06.03](#pre-ospf-underlay-baseline--hq-vp-0603)

**Completed:** `30-09-2026`

**Git traceability:** [`6608742` — Add HQ Phase 06 and 07 verification artifacts](https://github.com/ddduddden/multi-site-cml-lab/commit/66087426a6aa619e0177abca1238fad7c3213d70).

**Build window:** Combined with Phase 07. The saved end-of-Phase-06 state was restored and recaptured before documentation close-out so the underlay could be evidenced independently of OSPF.

**Objective:** Build and verify all ten routed Distribution-to-Edge `/31` links before dynamic routing is enabled.

The historical Phase 06 milestone contains the routed `/31` underlay but no configured loopbacks or OSPF process. `Loopback0` identities were introduced with Phase 07 and are therefore verified there.

**Device state reference:** The end-of-Phase-06 CML export is retained privately as the pre-OSPF rollback point and is not committed. The committed `configs/hq/` files represent the Phase 07 milestone.

---

### Routed `/31` Interface Addressing and State — HQ-VP-06.01

**Objective:**\
Confirm that all ten Distribution-to-Edge links use the documented routed interfaces, `/31` addressing, and address-ownership convention, with both ends operational.

**Expected result:**\
The four direct links between `hq-d1` and `hq-r1`, the four direct links between `hq-d2` and `hq-r2`, and the two cross-links use the documented `10.255.10.0/24` allocations. Every endpoint uses mask `255.255.255.254`, the lower address is assigned to the distribution switch, and all routed endpoints are `up/up`. Distribution-side routed interfaces use `no switchport`.

**Configuration involved:**\
`/31` addressing on `hq-r1`/`hq-r2 Gi0/0`–`Gi0/4`; routed-port conversion and addressing on `hq-d1`/`hq-d2 Gi2/0`–`Gi2/3` and `Gi3/0`.

**Verification command(s):**\
`show ip interface brief`; `show interfaces description`; `show ip route connected`; `show running-config interface <routed-interface>`.

**Observed result:**\
All ten routed links were `up/up` and matched the documented `/31` address ownership. `hq-d1` held `.0`, `.8`, `.10`, `.12`, plus cross-link `.4`; `hq-r1` held `.1`, `.9`, `.11`, `.13`, plus cross-link `.7`. `hq-d2` held `.2`, `.14`, `.16`, `.18`, plus cross-link `.6`; `hq-r2` held `.3`, `.15`, `.17`, `.19`, plus cross-link `.5`. Every endpoint used a `/31` mask, the distribution interfaces were routed with `no switchport`, and the connected routing tables contained the expected `/31` networks and local `/32` interface routes.

**Status:**\
Verified

**Evidence:** [HQ-VP-06.01 — captures](../../../evidence/hq/layer3-underlay/README.md#hq-vp-0601)

**Notes / Troubleshooting:**\
The IOSvL2 switches routed correctly even though no explicit `ip routing` line was present in the running configuration; the operational routing table was used as the authoritative check. This observed IOSvL2 routing behaviour is recorded in [`HQ-TS-001`](troubleshooting.md#hq-ts-001--iosvl2-routing-mode-on-hq-a1), where it affected `hq-a1`. On the multilayer distribution switches it is the intended behaviour and needed no correction.

---

### Direct `/31` Point-to-Point Reachability — HQ-VP-06.02

**Objective:**\
Confirm bidirectional IPv4 reachability across every routed `/31` before OSPF is introduced.

**Expected result:**\
Each Layer 3 device can ping the directly connected address at the opposite end of each of its five routed links. An initial `4/5` while ARP resolves is acceptable if the immediate repeat returns `5/5`.

**Configuration involved:**\
No additional configuration beyond `HQ-VP-06.01`.

**Verification command(s):**\
`ping <far-end-interface-address>` from `hq-r1`, `hq-r2`, `hq-d1`, and `hq-d2`.

**Observed result:**\
All twenty directional pings succeeded. Several first router-side attempts returned `4/5` while ARP resolved, and every immediate repeat returned `5/5`; all distribution-side attempts returned `5/5` on the first recorded check. This confirmed direct IPv4 reachability across all eight direct links and both cross-links before dynamic routing was introduced.

**Status:**\
Verified

**Evidence:** [HQ-VP-06.02 — captures](../../../evidence/hq/layer3-underlay/README.md#hq-vp-0602)

**Notes / Troubleshooting:**\
The initial ARP misses were expected first-packet behaviour and did not require a troubleshooting record.

---

### Pre-OSPF Underlay Baseline — HQ-VP-06.03

**Objective:**\
Confirm that the verified routed underlay is captured before an OSPF process exists.

**Expected result:**\
`show running-config | section ^router ospf` returns no matching configuration on `hq-r1`, `hq-r2`, `hq-d1`, or `hq-d2`.

**Configuration involved:**\
None beyond the completed routed `/31` underlay.

**Verification command(s):**\
`show running-config | section ^router ospf`

**Observed result:**\
The command returned no OSPF router section on all four Layer 3 devices. This establishes a clean pre-OSPF baseline for the Phase 07 routing-domain evidence.

**Status:**\
Verified

**Evidence:** [HQ-VP-06.03 — captures](../../../evidence/hq/layer3-underlay/README.md#hq-vp-0603)

**Notes / Troubleshooting:**\
The saved Phase 06 state predates the four `Loopback0` identities. Rather than recreating an intermediate state that was not actually built, the loopbacks are recorded as part of Phase 07.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 07 — Loopbacks and OSPF Area 10

[HQ-VP-07.01](#loopback-and-ospf-process-identity--hq-vp-0701) | [HQ-VP-07.02](#ospf-interface-participation-network-type-and-cost--hq-vp-0702) | [HQ-VP-07.03](#ospf-area-10-adjacencies--hq-vp-0703) | [HQ-VP-07.04](#ospf-link-state-database-and-learned-routing--hq-vp-0704) | [HQ-VP-07.05](#routed-and-end-to-end-reachability--hq-vp-0705) | [HQ-VP-07.06](#layer-2-and-gateway-regression--hq-vp-0706)

**Completed:** `30-09-2026`

**Build window:** Combined with Phase 06. Phase 07 starts from the verified routed `/31` underlay and introduces the four loopback identities and the complete OSPF Area 10 interface policy.

**Objective:** Verify loopback identities, explicit OSPF router IDs, passive-interface policy, intended adjacencies, Area 10 route advertisement, and routed reachability while preserving the previously verified Layer 2 and HSRP state.

Phase 07 applies the complete approved OSPF interface policy, including point-to-point network type and explicit interface costs. Route tables captured here may already show multiple next hops, but ECMP behaviour is deliberately interpreted in Phase 08 and cost-driven path selection in Phase 09.

**As-built configuration reference:** `configs/hq/hq-r1-running-config.txt`, `hq-r2-running-config.txt`, `hq-d1-running-config.txt`, `hq-d2-running-config.txt`, and `hq-a1-running-config.txt`.

**Git traceability:** [`6608742` — Add HQ Phase 06 and 07 verification artifacts](https://github.com/ddduddden/multi-site-cml-lab/commit/66087426a6aa619e0177abca1238fad7c3213d70).

---

### Loopback and OSPF Process Identity — HQ-VP-07.01

**Objective:**\
Confirm the four `Loopback0` identities and that OSPF process `10` uses them as explicit router IDs with a single normal Area `10` and an operational maximum-path value of four.

**Expected result:**\

| Device | `Loopback0` / Router ID |
|---|---|
| `hq-r1` | `10.255.10.129/32` |
| `hq-r2` | `10.255.10.130/32` |
| `hq-d1` | `10.255.10.131/32` |
| `hq-d2` | `10.255.10.132/32` |

Each device reports one normal area and `Maximum path: 4`. `hq-a1` remains a Layer 2 access switch and uses `ip default-gateway 10.10.99.1`.

**Configuration involved:**\
`Loopback0` addressing and interface-level Area 10 participation; `router ospf 10` with explicit `router-id` on the four Layer 3 devices.

**Verification command(s):**\
`show ip interface brief`; `show ip protocols`; `show running-config | section ^router ospf`; `show running-config interface Loopback0`; on `hq-a1`, `show ip route` and `show running-config | include ^ip routing|^ip default-gateway`.

**Observed result:**\
All four loopbacks were `up/up` with the documented `/32` addresses. OSPF process `10` used `.129`, `.130`, `.131`, and `.132` as the respective router IDs, each device reported one normal area and `Maximum path: 4`, and no broad `network` statements were present. No explicit `maximum-paths 4` line was present in the running configuration; `show ip protocols` confirmed that the operational maximum-path value on this image was `4`. `hq-a1` showed routing disabled with default gateway `10.10.99.1`.

**Status:**\
Verified

**Evidence:** [HQ-VP-07.01 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0701)

**Notes / Troubleshooting:**\
No deviation is required for the omitted `maximum-paths 4` line because the captured operational value matches the design.

---

### OSPF Interface Participation, Network Type and Cost — HQ-VP-07.02

**Objective:**\
Confirm that OSPF participates only on the intended interfaces, uses the passive-by-default policy, forms adjacencies only on routed Distribution-to-Edge links, and applies the approved point-to-point network type and interface costs.

**Expected result:**\
`hq-r1` and `hq-r2` each have six Area 10 interfaces: `Loopback0` plus `Gi0/0`–`Gi0/4`. `hq-d1` and `hq-d2` each have fourteen: `Loopback0`, five routed links, and eight SVIs. `Loopback0` and the SVIs are passive; only the five routed links per device are non-passive. All ten Ethernet `/31` links use OSPF point-to-point network type. Direct-link endpoints use cost `10`; the four cross-link endpoints use cost `100`.

**Configuration involved:**\
`passive-interface default`; `no passive-interface` on the five routed links per device; interface-level `ip ospf 10 area 10`; `ip ospf network point-to-point`; `ip ospf cost 10` / `100`.

**Verification command(s):**\
`show ip ospf interface brief`; `show ip protocols`; `show running-config | section ^router ospf`; `show running-config interface <routed-interface>`.

**Observed result:**\
Both routers showed six Area 10 interfaces and both distribution switches fourteen. The loopbacks and all eight distribution SVIs were passive; only the five routed links per Layer 3 device were non-passive. Every routed Ethernet interface reported state `P2P`. The eight direct links used cost `10` at both ends and the two cross-links cost `100` at both ends. The distribution SVIs remained advertised in Area 10 without forming neighbours.

**Status:**\
Verified

**Evidence:** [HQ-VP-07.02 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0702)

**Notes / Troubleshooting:**\
An initial implementation typo placed the five `hq-d2` routed interfaces in Area `0`. They were corrected to Area `10` before the final evidence capture. This was an immediately identified implementation correction, not an accepted design deviation or a separate troubleshooting investigation.

---

### OSPF Area 10 Adjacencies — HQ-VP-07.03

**Objective:**\
Confirm that all ten intended point-to-point adjacencies reach `FULL` and that no unintended adjacency forms between the two distribution switches or on passive interfaces.

**Expected result:**\
Each Layer 3 device has exactly five `FULL/  -` neighbours. Across all four devices, the twenty neighbour-table entries represent ten unique routed-link adjacencies. `hq-d1` and `hq-d2` do not form a direct OSPF adjacency.

**Configuration involved:**\
No additional configuration beyond `HQ-VP-07.01` and `HQ-VP-07.02`.

**Verification command(s):**\
`show ip ospf neighbor`

**Observed result:**\
Each of `hq-r1`, `hq-r2`, `hq-d1`, and `hq-d2` showed exactly five neighbours in `FULL/  -` state. The direct four-link sets and each cross-link were present on the intended interfaces, producing ten unique adjacencies. No distribution-to-distribution adjacency was present.

**Status:**\
Verified

**Evidence:** [HQ-VP-07.03 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0703)

**Notes / Troubleshooting:**\
No deliberate adjacency-failure test was included in Phase 07. Routing and device failures were examined separately in the [Phase 10 tests](../../../evidence/hq/failure-tests/README.md).

---

### OSPF Link-State Database and Learned Routing — HQ-VP-07.04

**Objective:**\
Confirm a consistent Area 10 link-state database and the expected intra-area learning of remote HQ prefixes.

**Expected result:**\
The Area 10 database contains exactly four Router LSAs, advertised by `10.255.10.129`–`10.255.10.132`, with no Network, Summary, or External LSAs. The expected Router LSA link counts are `11` for each edge router and `19` for each multilayer distribution switch.

The edge routers each learn 16 intra-area routes: the eight HQ VLAN prefixes, three remote loopbacks, and five remote `/31`s. The distribution switches each learn 8: three remote loopbacks and five remote `/31`s. They retain their eight VLANs as connected routes. All learned routes are intra-area (`O`), and loopbacks appear as `/32`s.

**Configuration involved:**\
No additional configuration beyond `HQ-VP-07.01` and `HQ-VP-07.02`.

**Verification command(s):**\
`show ip ospf database`; `show ip route ospf`.

**Observed result:**\
All four devices held identical databases: four Router LSAs from `10.255.10.129`–`10.255.10.132` with matching sequence numbers and checksums, link counts of `11`, `11`, `19`, and `19`, and no Network, Summary, or External LSAs.

`hq-r1` and `hq-r2` each installed 16 OSPF routes: all eight VLAN networks, three remote loopbacks, and five remote transit links. `hq-d1` and `hq-d2` each installed 8 OSPF routes: three remote loopbacks and five remote transit links. They kept the eight VLAN networks as connected routes. Every learned route was intra-area, and every loopback was a `/32`.

Several routes already displayed multiple equal-cost next hops; those observations are retained here but are evaluated formally in Phase 08.

**Status:**\
Verified

**Evidence:** [HQ-VP-07.04 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0704)

**Notes / Troubleshooting:**\
The observed link counts are consistent with standard OSPFv2 Router-LSA construction: on each numbered point-to-point link, the router-to-router relationship and the attached IP subnet are represented separately. `Loopback0` contributes one stub-network entry. Five numbered point-to-point links therefore account for ten entries; adding `Loopback0` gives each edge router a link count of `11`, while the eight additional passive SVI prefixes give each distribution switch a link count of `19`.

The captured metrics also show that the cost-`100` cross-links can be the shortest path to some destinations. Their path-selection behaviour is intentionally analysed in Phase 09 rather than reinterpreted during Phase 07.

The routing tables also showed five equal-cost paths at metric `111` between the two edge-router loopbacks and between the two distribution-switch loopbacks. OSPF could install only four of those paths, and the one left out differed between devices:

- `hq-r1`: For the route to `10.255.10.130/32` (`hq-r2 Loopback0`), installed its four direct links and left out cross-link `Gi0/4`.
- `hq-r2`: For the route to `10.255.10.129/32` (`hq-r1 Loopback0`), installed the cross-link and left out direct link `Gi0/3`.
- `hq-d1`: For the route to `10.255.10.132/32` (`hq-d2 Loopback0`), installed the cross-link and left out direct link `Gi2/3`.
- `hq-d2`: For the route to `10.255.10.131/32` (`hq-d1 Loopback0`), installed the cross-link and left out direct link `Gi2/3`.

---

### Routed and End-to-End Reachability — HQ-VP-07.05

**Objective:**\
Confirm routed reachability between all four Layer 3 devices using their `Loopback0` addresses, and from the Layer 2 access-switch management SVI through the HSRP gateway to all four routing identities.

**Expected result:**\
Each Layer 3 device reaches the other three `Loopback0` addresses using its own `Loopback0` as the source. `hq-a1` reaches HSRP gateway `10.10.99.1` and routing identities `.129`–`.132` while remaining a Layer 2 access switch.

**Configuration involved:**\
No additional OSPF configuration. `hq-a1` uses `Vlan199 10.10.99.4/26`, explicit `no ip routing`, and `ip default-gateway 10.10.99.1`.

**Verification command(s):**\
`ping <remote-loopback-address> source Loopback0` on the four Layer 3 devices; `show ip route`; `show running-config | include ^ip routing|^ip default-gateway`; pings from `hq-a1` to the HSRP VIP and all four loopbacks.

**Observed result:**\
All twelve loopback-sourced pings between the four Layer 3 devices returned `5/5`. From `hq-a1`, the HSRP virtual gateway and all four routing identities responded at `100%`, confirming management traffic could leave VLAN `199` through HSRP and return through Area `10`. During the initial check, `hq-a1` could reach its local HSRP gateway but not the four remote routing identities. [`HQ-TS-001`](troubleshooting.md#hq-ts-001--iosvl2-routing-mode-on-hq-a1) identified the observed IOSvL2 routing mode as the cause: with IP routing enabled, `ip default-gateway` was not used. After `no ip routing` was applied, all four remote reachability checks succeeded.

**Status:**\
Verified

**Evidence:** [HQ-VP-07.05 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0705)

**Notes / Troubleshooting:**\
The earlier mistyped `10.10.10.x` ping destinations were discarded as irrelevant operator input. The investigation and correction of the `hq-a1` routing mode are recorded in [`HQ-TS-001`](troubleshooting.md#hq-ts-001--iosvl2-routing-mode-on-hq-a1).

---

### Layer 2 and Gateway Regression — HQ-VP-07.06

**Objective:**\
Confirm that the Layer 3 underlay and OSPF work did not change the verified Phase 03–05 EtherChannel, Rapid PVST+, HSRP, or access-switch management state.

**Expected result:**\
`Po10`, `Po20`, and `Po30` remain operational with their intended LACP members. STP root placement remains `hq-d1` for VLANs `112,130,152,170,190` and `hq-d2` for VLANs `120,140,160,199`. HSRP ownership remains `hq-d1` Active for `112,130,152,170` and `hq-d2` Active for `120,140,160,199`. `hq-a1 Vlan199` remains `10.10.99.4/26` and `up/up`.

**Configuration involved:**\
None. This is a regression check of the previously verified Layer 2 and first-hop redundancy state.

**Verification command(s):**\
`show etherchannel summary`; `show spanning-tree root`; `show standby brief`; `show ip interface brief`.

**Observed result:**\
All EtherChannels remained operational with their intended members bundled. STP root placement and the access-switch `Po10`/`Po20` root-port split matched the Phase 04 design. HSRP Active/Standby ownership and preferred-only preemption remained aligned with Phase 05. `hq-a1 Vlan199` remained `up/up` at `10.10.99.4/26`.

**Status:**\
Verified

**Evidence:** [HQ-VP-07.06 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0706)

**Notes / Troubleshooting:**\
This is a state regression check only. The earlier Phase 03–05 failure tests are not repeated.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 08 — ECMP

[HQ-VP-08.01](#ecmp-route-installation--hq-vp-0801) | [HQ-VP-08.02](#cef-path-selection--hq-vp-0802) | [HQ-VP-08.03](#aggregate-ecmp-forwarding--hq-vp-0803) | [HQ-VP-08.04](#ecmp-contraction-and-restoration--hq-vp-0804) | [HQ-VP-08.05](#four-path-maximum--hq-vp-0805)

**Completed:** `30-09-2026`

**Objective:** Prove that the intended equal-cost OSPF routes are installed and usable; do not infer ECMP merely from topology.

Phase 08 verifies the ECMP behaviour already exposed by the Phase 07 OSPF configuration. No permanent configuration change was made.

**As-built configuration reference:** The Phase 07 files in `configs/hq/` remain the current as-built configuration reference.

**Git traceability:** [`79d27bf` — Add HQ Phase 08 and 09 verification evidence](https://github.com/ddduddden/multi-site-cml-lab/commit/79d27bfa3351bb6ffbf9363ee66675251e9aa1a2).

---

### ECMP Route Installation — HQ-VP-08.01

**Objective:**\
Confirm that the intended four-route OSPF ECMP sets are installed in the routing table.

**Expected result:**\
Selected campus and directly paired edge/distribution loopback routes install four equal-cost next hops at metric `11`. OSPF retains an operational maximum-path value of `4`.

**Configuration involved:**\
No Phase 08 configuration change. The test uses the Phase 07 OSPF interface costs and process state.

**Verification command(s):**\
`show ip ospf neighbor`; selected `show ip route <prefix>` checks; Phase 07 `show ip protocols` evidence.

**Observed result:**\
`hq-r1` and `hq-r2` each installed four metric-`11` routes to `10.10.12.0/22`. `hq-d2` installed four metric-`11` routes to `hq-r2 Loopback0`, while the equivalent `hq-d1` to `hq-r1 Loopback0` state is retained in Phase 07 evidence. The metric matches direct-link cost `10` plus destination SVI or loopback cost `1`. Phase 07 evidence records `Maximum path: 4`.

**Status:**\
Verified

**Evidence:** [HQ-VP-08.01 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0801)

**Notes / Troubleshooting:**\
Per-flow forwarding is verified separately in `HQ-VP-08.02` and `HQ-VP-08.03`.

---

### CEF Path Selection — HQ-VP-08.02

**Objective:**\
Confirm that CEF `exact-route` prediction matches the interface actually used to forward the test traffic.

**Expected result:**\
For each tested flow, the interface predicted by `show ip cef exact-route` carries the dominant output increase during the associated 100-ping test.

**Configuration involved:**\
No configuration change. Interface counters were cleared only for measurement.

**Verification command(s):**\
`show ip cef exact-route 10.10.99.4 <destination>` on `hq-d2`; clear and inspect `Gi2/0`–`Gi2/3` counters; 100-ping tests from `hq-a1`.

**Observed result:**\
Three test flows were run from `10.10.99.4`. CEF selected `hq-d2 Gi2/2` for `10.255.10.130`, `Gi2/3` for `10.255.10.5`, and `Gi2/2` for `10.255.10.4`. In every case the selected interface carried the dominant output increase during the test. Exact counter values are retained in the evidence file.

**Status:**\
Verified

**Evidence:** [HQ-VP-08.02 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0802)

**Notes / Troubleshooting:**\
A separate router-generated reply observation did not affect the forwarding result and is retained in the evidence file. In Phase 10, `exact-route` predictions were treated as routing-path evidence, not standalone proof of the interface used by router-generated traffic.

---

### Aggregate ECMP Forwarding — HQ-VP-08.03

**Objective:**\
Confirm that more than one installed ECMP route is used by the test traffic.

**Expected result:**\
More than one installed ECMP member carries the test traffic. Equal distribution across all four members is not required.

**Configuration involved:**\
No configuration change.

**Verification command(s):**\
Reuse the flow tests, CEF, and counter checks from `HQ-VP-08.02`.

**Observed result:**\
The three tested flows used two members of the four-route ECMP set. `hq-d2 Gi2/2` carried the flows to `10.255.10.130` and `10.255.10.4`, while `Gi2/3` carried the flow to `10.255.10.5`. No tested flow selected `Gi2/0` or `Gi2/1`.

**Status:**\
Verified

**Evidence:** [HQ-VP-08.03 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0803)

**Notes / Troubleshooting:**\
The same three flow captures are used for both checks. `HQ-VP-08.03` keeps the forwarding summary, while the detailed CEF and counter output is kept in `HQ-VP-08.02`.

---

### ECMP Contraction and Restoration — HQ-VP-08.04

**Objective:**\
Confirm that removal and restoration of equal-cost direct links causes the installed ECMP route set to contract and rebuild cleanly.

**Expected result:**\
A selected four-route campus prefix contracts `4→3→2→1` as direct links are removed, remains metric `11` while at least one cost-`10` direct link survives, and restores `1→2→3→4` as the links return.

**Configuration involved:**\
Temporary shutdown and restoration of `hq-r1 Gi0/3`, `Gi0/2`, `Gi0/1`, and `Gi0/0`. No permanent configuration change.

**Verification command(s):**\
`show ip ospf neighbor`; `show ip route 10.10.12.0`; controlled `shutdown` and `no shutdown`.

**Observed result:**\
`hq-r1`'s route to `10.10.12.0/22` contracted from four metric-`11` next hops to three, two, and one as the direct links were removed. Restoring the links rebuilt the route set from one to four.

**Status:**\
Verified

**Evidence:** [HQ-VP-08.04 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0804)

**Notes / Troubleshooting:**\
A brief one-sided OSPF neighbour state was seen during one shutdown and is kept in the evidence file. Stable route checks were taken after both sides had converged.

---

### Four-Path Maximum — HQ-VP-08.05

**Objective:**\
Confirm the lab-observed four-path OSPF installation behaviour when five equal-cost paths are available.

**Expected result:**\
Only four next hops are installed. If one installed next hop is removed, the route still installs four equal-cost next hops and a previously omitted equal-cost route can enter.

**Configuration involved:**\
No `maximum-paths` command was added. Phase 07 established the operational maximum-path value as `4`.

**Verification command(s):**\
`show ip route 10.255.10.130`; remove one installed next hop; repeat the route check after convergence.

**Observed result:**\
`hq-r1` initially installed four metric-`111` next hops to `10.255.10.130/32` over `Gi0/0`–`Gi0/3`. `Gi0/4` provided a fifth equal-cost path at metric `111`. After `Gi0/3` was shut and OSPF converged, the route still installed four metric-`111` next hops and `Gi0/4` entered the routing table.

The omitted route was not fixed. Phase 07 showed `hq-r2` omitting `Gi0/3` for `10.255.10.129/32`; after the mirrored recovery in this test window it omitted `Gi0/0`. Final `hq-r1` state again omitted `Gi0/4` for `10.255.10.130/32`.

**Status:**\
Verified

**Evidence:** [HQ-VP-08.05 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0805)

**Notes / Troubleshooting:**\
For this far-side loopback, `Gi0/4` had the same total OSPF cost as the other paths, so it could join the ECMP route set.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 09 — OSPF Cost Engineering

[HQ-VP-09.01](#normal-cost-driven-selection--hq-vp-0901) | [HQ-VP-09.02](#higher-cost-alternate-activation--hq-vp-0902) | [HQ-VP-09.03](#preferred-route-restoration--hq-vp-0903)

**Completed:** `30-09-2026`

**Objective:** Prove that preferred direct routes and higher-cost alternate routes are selected according to the approved OSPF cost design and become usable when the preferred direct set is unavailable.

Phase 09 verifies the cost policy already configured in Phase 07. No permanent configuration change was made.

**As-built configuration reference:** The Phase 07 files in `configs/hq/` remain the current as-built configuration reference.

**Git traceability:** [`79d27bf` — Add HQ Phase 08 and 09 verification evidence](https://github.com/ddduddden/multi-site-cml-lab/commit/79d27bfa3351bb6ffbf9363ee66675251e9aa1a2).

---

### Normal Cost-Driven Selection — HQ-VP-09.01

**Objective:**\
Confirm that normal OSPF route selection follows the configured total path cost.

**Expected result:**\
The routing table installs the lowest-cost route or equal-cost route set for each selected destination.

**Configuration involved:**\
No configuration change. Phase 07 direct-link cost `10`, cross-link cost `100`, SVI cost `1`, and loopback cost `1` remain in use.

**Verification command(s):**\
Selected `show ip route` checks on `hq-r1`, cross-referenced with the Phase 07 interface-cost evidence.

**Observed result:**\
`10.10.12.0/22` used four direct metric-`11` routes rather than the metric-`101` cross-link alternative. `hq-d2 Loopback0` used the cross-link at metric `101`, which was lower than the metric-`121` route through `hq-d1`. The far-side `hq-d2`–`hq-r2` `/31` prefixes used the cross-link at metric `110`, lower than the metric-`120` alternative through `hq-d1`.

The final `hq-r1` routing table showed five far-side infrastructure prefixes using only `Gi0/4`: `10.255.10.2/31`, `10.255.10.14/31`, `10.255.10.16/31`, `10.255.10.18/31`, and `10.255.10.132/32`.

**Status:**\
Verified

**Evidence:** [HQ-VP-09.01 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0901)

**Notes / Troubleshooting:**\
The five-way metric-`111` loopback case is verified separately in `HQ-VP-08.05`.

---

### Higher-Cost Alternate Activation — HQ-VP-09.02

<a href="../../hq-campus-design.md#intended-behaviour-during-routed-link-failures" title="Previous: Stop 1 · Design intent" aria-label="Previous: Stop 1 · Design intent"><img src="../../../diagrams/orange-previous.svg" alt="" width="30" height="26"></a> **🟧 10-MINUTE ROUTE · EXPLORE THE EVIDENCE · 02/07** <a href="phase-10-test-plan.md" title="Next: Stop 3 · Phase 10 test plan" aria-label="Next: Stop 3 · Phase 10 test plan"><img src="../../../diagrams/orange-next.svg" alt="" width="30" height="26"></a>

*Phase verification* · **About a minute** | Every Phase 01–09 check is recorded in this format, with supporting Git commits and evidence linked to the relevant phases. Here Phase 09 removes each four-link direct set to exercise the cross-links from Stop 1. Read *Expected result* and *Observed result*. Matching build-log entry: [Phase 09](build-log.md#phase-09--ospf-cost-engineering).

**Objective:**\
Confirm that removing a complete four-link direct set causes OSPF to use the surviving higher-cost alternate route, while traffic remains reachable through the opposite edge/distribution pair.

**Expected result:**\
The affected edge router reaches a selected campus prefix at metric `101`. The distribution switch that loses its direct links reaches the affected edge loopback at metric `211` through the opposite edge/distribution pair. End-to-end reachability remains available.

**Configuration involved:**\
Temporary shutdown of the four direct links on each tested edge/distribution pair. No permanent configuration change.

**Verification command(s):**\
`show ip ospf neighbor`; selected `show ip route` checks; sourced ping and traceroute tests; `show standby brief` during the `hq-r1`↔`hq-d1` test.

**Observed result:**\
With all four `hq-r1`↔`hq-d1` direct links down, `hq-r1` reached `10.10.12.0/22` at metric `101` through `hq-d2`. `hq-d1` reached `hq-r1 Loopback0` at metric `211` through `hq-r2→hq-d2→hq-r1`; the sourced ping succeeded `10/10` and traceroute followed that path.

`hq-d1` remained HSRP Active for VLANs `112`, `130`, `152`, and `170` because interface tracking is not configured. Its cross-link to `hq-r2` remained available, so routed traffic for those VLANs could continue.

The mirrored `hq-r2`↔`hq-d2` test produced the same metric pattern. `hq-r2` used a metric-`101` campus route through `hq-d1`, while `hq-d2` reached `hq-r2 Loopback0` at metric `211` through `hq-r1→hq-d1→hq-r2`. `hq-a1` reached `10.255.10.130` at `10/10`, and the traceroute from `hq-d2` followed the expected alternate path.

**Status:**\
Verified

**Evidence:** [HQ-VP-09.02 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0902)

**Notes / Troubleshooting:**\
HSRP state was captured during the `hq-r1`↔`hq-d1` test. During the mirrored `hq-r2`↔`hq-d2` test, one traceroute probe showed `*`; the same alternate hops remained visible and the selected route and `10/10` reachability were stable. Complete routed-uplink isolation of an Active HSRP distribution switch was tested in [HQ-VP-10.09](../../../evidence/hq/failure-tests/10.09/HQ-VP-10.09-d2-routed-isolation.md).

🟧 **NEXT STEP —** [Stop 3 · Phase 10 test plan](phase-10-test-plan.md) [![Next stop](../../../diagrams/orange-next.svg)](phase-10-test-plan.md)

---

### Preferred-Route Restoration — HQ-VP-09.03

**Objective:**\
Confirm that restoration of lower-cost direct connectivity removes the higher-cost alternate route and returns the routing state to the Phase 07 baseline.

**Expected result:**\
Restoring a cost-`10` direct link replaces the metric-`101` alternate route. Full restoration returns the normal four-route ECMP state, five OSPF neighbours per Layer 3 device, the expected OSPF route counts, and the Phase 07 configuration baseline.

**Configuration involved:**\
Restoration of the interfaces temporarily shut during Phase 08/09 testing. No permanent configuration change.

**Verification command(s):**\
`no shutdown`; `show ip ospf neighbor`; selected `show ip route` checks; final `show ip route ospf`; final `show ip interface brief | exclude unassigned`; comparison with the committed Phase 07 configuration files.

**Observed result:**\
Restoring `hq-r1 Gi0/0` replaced the metric-`101` route to `10.10.12.0/22` with a direct metric-`11` route. Restoring the remaining direct links rebuilt the four-route ECMP state. The mirrored `hq-r2`↔`hq-d2` restoration returned both devices to five `FULL` neighbours and restored the four metric-`11` routes.

The final health check showed five OSPF neighbours on all four Layer 3 devices, 16 learned OSPF routes on each edge router, and 8 on each distribution switch. All intended routed interfaces, SVIs, and loopbacks were `up/up`.

The post-test CML export was compared with the committed Phase 07 device configurations, and no unexpected configuration changes were found.

**Status:**\
Verified

**Evidence:** [HQ-VP-09.03 — captures](../../../evidence/hq/ospf/README.md#hq-vp-0903)

**Notes / Troubleshooting:**\
No troubleshooting was required during final restoration.

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 10 — Failure Testing

**Testing completed:** 06-10-2026\
**Configuration close-out:** 12-10-2026\
**Status:** Completed with documented findings and limitations.

**Objective:** Verify how the HQ network responds to link, Port-Channel and device failures, and whether the expected paths and normal operation are restored.

The tests confirmed alternate routes and access paths under several failure conditions. They also exposed limitations not identified in the earlier verification phases.

[`HQ-VP-10.08`](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) remains **FAIL** because the Layer 2 isolation test exposed a return-path blackhole. [`HQ-VP-10.12`](../../../evidence/hq/failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md) remains **INCONCLUSIVE** because live-flow failover was not demonstrated. The sustained asymmetric failure behaviour during the initial one-sided Po20 member shutdown in [`HQ-VP-10.05`](../../../evidence/hq/failure-tests/10.05/HQ-VP-10.05-etherchannel-member-failure.md) is also retained, although its bilateral rerun passed.

The investigation behind the Layer 2 isolation findings is recorded in [`HQ-TS-002`](troubleshooting.md#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation).

Normal forwarding was restored on 06-10-2026, with final configuration reconciliation completed on 12-10-2026.

**Records:** [Failure Test Plan](phase-10-test-plan.md) · [Testing Methodology](phase-10-testing-methodology.md) · [Results and Evidence](../../../evidence/hq/failure-tests/README.md) · [Engineering Review](phase-10-engineering-review.md).

**Git traceability:** [`a8624b1` — test(hq): preserve Phase 10 failure-testing evidence](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd).

[↑ Back to contents](#contents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Phase 11 — Final Acceptance

**Final operational check:** 16-10-2026\
**Startup recheck:** 26-10-2026\
**Status:** **ACCEPTED** — documented HQ V1 engineering milestone; limitations retained (26-10-2026).

**Objective:** Check the final HQ operational state, record any startup intervention, and confirm that the documentation and retained evidence describe the completed network accurately.

The private five-device CML export was booted and checked against the HQ design. On `hq-r1`, OSPF showed five `FULL` neighbours and four equal-cost, metric-`11` routes to `10.10.12.0/22`. HSRP Active/Standby roles matched the design, and the LACP bundles were operational. From `hq-a1`, both edge-router loopbacks replied `5/5`. The recorded traceroute towards `hq-r2` showed `10.10.99.3` (`hq-d2`) followed by `10.255.10.3`.

**Startup finding:** On 16 October, `hq-a1`'s VLAN199 SVI remained `down/down` despite the VLAN, trunk and spanning-tree configuration appearing correct. A manual `shutdown` / `no shutdown` brought it `up/up`, and the management gateway replied `5/5`. A 26 October startup recheck reproduced the `down/down` state, `0/5` gateway pings and unsuccessful `no shutdown` attempt. The same administrative reset restored `up/up` and `5/5` gateway replies. The cause was not established; **neither check demonstrated intervention-free startup**. The 26 October capture did not repeat the wider routing and HSRP checks.

The outstanding Phase 10 findings remain documented. HQ V1 was accepted on 26 October 2026 as a completed engineering milestone with these limitations retained. This decision does not change the recorded Phase 10 outcomes or demonstrate an intervention-free startup.

**Evidence index:** [Phase 11 captures](../../../evidence/hq/final-acceptance/README.md).

**Evidence:** [Phase 11 — Boot recovery CLI](../../../evidence/hq/final-acceptance/HQ-Phase-11-Boot-Recovery-CLI.md) documents the initial VLAN 199 failure, investigation and manual reset. [Phase 11 — Final operational checks](../../../evidence/hq/final-acceptance/HQ-Phase-11-Final-Boot-Verification.txt) retains the subsequent OSPF, HSRP, LACP and connectivity output. Both captures were made on 16-10-2026. The separate [26 October startup recheck](../../../evidence/hq/final-acceptance/HQ-Phase-11-26-Oct-Boot-Retest.md) records the repeated failure and manual recovery without extending the original 16 October operational claims.

**Engineering close-out:** [Phase 11 final acceptance and engineering review](phase-11-final-acceptance.md).

**Git traceability:** [`1ee631b` — Publish HQ final configuration milestone for Phase 11](https://github.com/ddduddden/multi-site-cml-lab/commit/1ee631be011985dac4a1c6a7f97de1ff95d22c1c) · [`39b68a7` — Add Phase 11 boot evidence and HQ troubleshooting records](https://github.com/ddduddden/multi-site-cml-lab/commit/39b68a790a3b9ed0de55071fdf7f9b004d0638b2). The public export is sanitised; the operational boot check used the private export.

[↑ Back to contents](#contents)

---

[← HQ Build Log](build-log.md) · [↑ Contents](#contents) · [Phase 10 Test Plan →](phase-10-test-plan.md)
