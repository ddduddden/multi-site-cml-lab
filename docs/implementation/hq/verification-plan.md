# HQ Verification Plan

This document defines what the HQ implementation must prove before a feature is treated as verified as-built.

It is a **controlled living document**. Once a verification ID is assigned it remains permanent. Expected results and exact verification commands may be refined when the actual CML platform behaviour is confirmed.

Only phases 01 and 02 are detailed initially. Phases 03–11 contain only their agreed objective until the project reaches them.

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

There is no separate Pass/Fail field. `Blocked` means the test cannot currently be completed; it does not mean the test has permanently failed.

## Contents

| Phase | Scope | Detail |
|---:|---|---|
| 01 | Platform baseline | Detailed below |
| 02 | Layer 2 / VLAN baseline | Detailed below |
| 03 | LACP EtherChannel | Objective only |
| 04 | Rapid PVST+ | Objective only |
| 05 | SVIs and HSRP | Objective only |
| 06 | Routed `/31`s and loopbacks | Objective only |
| 07 | OSPF Area 10 | Objective only |
| 08 | ECMP | Objective only |
| 09 | OSPF cost engineering | Objective only |
| 10 | Failure testing | Objective only |
| 11 | Final acceptance | Objective only |

---

## Phase 01 — Platform baseline

**Objective:** Establish exactly what is running before assuming anything about node type, image, interface naming, interface count, licensing, or planned feature availability.

### HQ-VP-01.01 — HQ device inventory

- **Objective:** Confirm that all five intended HQ devices exist in CML with the expected hostnames and roles.
- **Expected result:** `hq-r1`, `hq-r2`, `hq-d1`, `hq-d2`, and `hq-a1` are present and console-accessible.
- **Configuration involved:** None.
- **Verification command(s):** Record the CML node definition for each device and capture basic device identity from the CLI.
- **Observed result:** Pending
- **Status:** Not started
- **Evidence:** —
- **Notes / Troubleshooting:** —

### HQ-VP-01.02 — Image and software version inventory

- **Objective:** Record the image/software version actually running on each HQ device.
- **Expected result:** Image and version are known for all five devices and any mismatch with the current design assumptions is identified before configuration proceeds.
- **Configuration involved:** None.
- **Verification command(s):** `show version`
- **Observed result:** Pending
- **Status:** Not started
- **Evidence:** —
- **Notes / Troubleshooting:** —

### HQ-VP-01.03 — Interface inventory and topology fit

- **Objective:** Confirm the available interface names and counts can support the intended HQ topology.
- **Expected result:** Each device has the required interfaces for its planned role, and the actual interface names are recorded before configuration.
- **Configuration involved:** None.
- **Verification command(s):** Use the platform-appropriate interface summary command(s) and compare the result with the topology/interface plan.
- **Observed result:** Pending
- **Status:** Not started
- **Evidence:** —
- **Notes / Troubleshooting:** —

### HQ-VP-01.04 — Platform capability review

- **Objective:** Identify any known platform or image constraint that would block the planned HQ features before implementation begins.
- **Expected result:** No unresolved capability issue blocks the planned use of Layer 2 LACP, Rapid PVST+, HSRP, OSPF, routed interfaces, or the later ECMP design.
- **Configuration involved:** None unless a non-disruptive capability check is explicitly required.
- **Verification command(s):** Record relevant platform/version information and confirm feature availability using platform-appropriate CLI help or official Cisco documentation before feature configuration.
- **Observed result:** Pending
- **Status:** Not started
- **Evidence:** —
- **Notes / Troubleshooting:** —

---

## Phase 02 — Layer 2 / VLAN baseline

**Objective:** Establish the VLAN database, intended access-port assignments, and parking-VLAN policy before EtherChannel/trunk implementation begins.

> Native-VLAN and trunk verification belongs to Phase 03 because the production trunks are created and verified with the EtherChannels there.

### HQ-VP-02.01 — VLAN database

- **Objective:** Confirm that all intended HQ VLANs exist on each switch that requires them.
- **Expected result:** Required VLAN IDs and names match the approved HQ design on `hq-d1`, `hq-d2`, and `hq-a1`.
- **Configuration involved:** VLAN creation and naming on the applicable switches.
- **Verification command(s):** `show vlan brief`
- **Observed result:** Pending
- **Status:** Not started
- **Evidence:** —
- **Notes / Troubleshooting:** —

### HQ-VP-02.02 — Access-port assignments

- **Objective:** Confirm every intended HQ access port has the correct access VLAN and, where required, voice VLAN.
- **Expected result:** Access-port and voice-VLAN assignments match the approved HQ access-switch port plan.
- **Configuration involved:** Access-mode, access-VLAN, and voice-VLAN configuration on the intended access ports.
- **Verification command(s):** Verify switchport mode, access-VLAN assignment, and voice-VLAN assignment where applicable using the platform-appropriate switchport display command.
- **Observed result:** Pending
- **Status:** Not started
- **Evidence:** —
- **Notes / Troubleshooting:** —

### HQ-VP-02.03 — Parking-VLAN policy

- **Objective:** Confirm unused access ports are separated from production VLANs and administratively disabled as designed.
- **Expected result:** All currently unused access ports are assigned to VLAN `191` (`PARKING`) and administratively shut down, matching `docs/hq-campus-design.md`.
- **Configuration involved:** Parking-VLAN assignment and administrative shutdown of unused access ports.
- **Verification command(s):** Verify VLAN membership and administrative state using platform-appropriate interface/VLAN display commands.
- **Observed result:** Pending
- **Status:** Not started
- **Evidence:** —
- **Notes / Troubleshooting:** —

---

## Phase 03 — LACP EtherChannel

**Objective:** Build and verify Po10, Po20, and Po30, including member state, 802.1Q trunking, native-VLAN consistency, allowed-VLAN forwarding, and member-link failure behaviour.

_No individual verification IDs assigned yet._

## Phase 04 — Rapid PVST+

**Objective:** Verify intended root placement, forwarding/blocking state, and spanning-tree behaviour during defined failures.

_No individual verification IDs assigned yet._

## Phase 05 — SVIs and HSRP

**Objective:** Verify SVI addressing, HSRP active/standby roles, preemption, gateway reachability, and failover.

_No individual verification IDs assigned yet._

## Phase 06 — Routed `/31`s and loopbacks

**Objective:** Build and verify all routed point-to-point interfaces and loopback identities before dynamic routing is enabled.

_No individual verification IDs assigned yet._

## Phase 07 — OSPF Area 10

**Objective:** Verify router IDs, passive-interface policy, intended adjacencies, Area 10 route advertisement, and routing reachability.

_No individual verification IDs assigned yet._

## Phase 08 — ECMP

**Objective:** Prove that the intended equal-cost OSPF paths are actually installed and usable; do not infer ECMP merely from topology.

_No individual verification IDs assigned yet._

## Phase 09 — OSPF cost engineering

**Objective:** Prove that preferred direct paths and higher-cost cross-connected alternatives are selected according to the approved design and become usable during the intended failures.

_No individual verification IDs assigned yet._

## Phase 10 — Failure testing

**Objective:** Execute the agreed failure matrix for member links, Port-Channels, routed interfaces, multilayer distribution switches, edge routers, and routing recovery.

_No individual verification IDs assigned yet._

## Phase 11 — Final acceptance

**Objective:** Confirm that all required implementation records, verification outcomes, troubleshooting records, deviations, configs, and evidence support describing HQ as verified as-built.

_No individual verification IDs assigned yet._
