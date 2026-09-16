# HQ Campus Design

**Project:** Multi-Site Cisco CML Lab  
**Site:** HQ Campus  
**Status:** Intended design — implementation and verification in progress  
**Routing domain:** OSPF Area 10  
**Node count:** 5 network devices

> This document describes the intended HQ architecture. Platform-specific behaviour, implementation notes, commands, test evidence, and simulator limitations will be maintained separately.

---

## 1. Overview

The HQ campus uses a five-device, two-tier collapsed-core design:

- `hq-r1` — Edge Router 1
- `hq-r2` — Edge Router 2
- `hq-d1` — Distribution Switch 1
- `hq-d2` — Distribution Switch 2
- `hq-a1` — Access Switch

The internal HQ routing domain operates as **OSPF Area 10**.

The edge routers will later connect Area 10 to the **Area 0 inter-site backbone** and support future GRE/IPsec connectivity.

The design provides:

- Redundant Layer 2 access/distribution connectivity
- First-hop gateway redundancy
- Per-VLAN spanning-tree root control
- Routed Distribution-to-Edge connectivity
- OSPF equal-cost multipath
- Alternate routed paths
- VLSM addressing
- `/31` routed infrastructure interfaces
- `/32` loopbacks
- Dedicated native and parking VLANs
- A clear path toward monitoring, security, inter-site connectivity, and automation

Layer 2 multi-link connectivity uses **LACP EtherChannel**.

Layer 3 multi-link connectivity uses **independent routed interfaces with OSPF ECMP**.

These are separate design mechanisms and are documented as such.

---

## 2. High-Level Topology

The HQ campus topology is shown below.

![HQ Campus - OSPF Area 10](../diagrams/hq-campus-area10-topology.svg)

The two Distribution Switches provide the Layer 3 gateway and campus-routing functions for HQ. `hq-a1` is dual-homed to them using `Po10` and `Po20`, while `hq-d1` and `hq-d2` are interconnected by `Po30`.

Each Distribution Switch also has four routed point-to-point interfaces to its directly paired edge router for the intended OSPF ECMP design:

- `hq-d1` ↔ `hq-r1`
- `hq-d2` ↔ `hq-r2`

A further cross-connected routed interface is provided in each direction to create an alternate OSPF path:

- `hq-d1` ↔ `hq-r2`
- `hq-d2` ↔ `hq-r1`

The two edge routers will later connect HQ Area 10 to the Area 0 inter-site backbone.


---

## 3. VLAN and Gateway Design

### VLAN and VLSM Addressing Plan

**Site allocation:** `10.10.0.0/16`  
**OSPF area:** Area 10  
**HSRP addressing convention:** `.1` = HSRP virtual IP, `.2` = `hq-d1`, `.3` = `hq-d2` for each routed VLAN.

| VLAN | Name         | Function                          | IPv4 Prefix     | Usable Hosts | HSRP Virtual IP |
| ---: | ------------ | --------------------------------- | --------------- | -----------: | --------------- |
|  112 | `CORP-USERS` | Corporate users                   | `10.10.12.0/22` |         1022 | `10.10.12.1`    |
|  120 | `VOICE`      | IP telephony                      | `10.10.20.0/23` |          510 | `10.10.20.1`    |
|  130 | `SERVERS`    | Server/application services       | `10.10.30.0/25` |          126 | `10.10.30.1`    |
|  140 | `IOT-CCTV`   | IoT and surveillance              | `10.10.40.0/23` |          510 | `10.10.40.1`    |
|  152 | `GUEST`      | Guest access                      | `10.10.52.0/22` |         1022 | `10.10.52.1`    |
|  160 | `FACILITIES` | Printers/facilities               | `10.10.60.0/26` |           62 | `10.10.60.1`    |
|  170 | `BYOD-WLAN`  | BYOD/wireless                     | `10.10.70.0/23` |          510 | `10.10.70.1`    |
|  190 | `NATIVE`     | Dedicated native VLAN             | —               |            — | —               |
|  191 | `PARKING`    | Unused ports                      | —               |            — | —               |
|  199 | `NET-MGMT`   | Network infrastructure management | `10.10.99.0/26` |           62 | `10.10.99.1`    |

#### Address Allocation Rationale

Unallocated address ranges within `10.10.0.0/16` are intentionally reserved for future HQ VLANs and services. Keeping HQ user and service networks within this site-specific address block provides structured growth while preserving the ability to summarise HQ routes toward the OSPF Area 0 backbone.

The addressing plan also provides a readable relationship between VLAN IDs and IPv4 subnets where practical. For example, VLAN 112 uses `10.10.12.0/22`, VLAN 120 uses `10.10.20.0/23`, and VLAN 152 uses `10.10.52.0/22`. This convention improves operational readability without overriding valid VLSM boundaries or subnet-sizing requirements.

#### Capacity Rationale

`CORP-USERS` and `GUEST` are intentionally allocated `/22` networks because they represent the highest-growth and highest-device-density client segments in the HQ design.

The 1,022-host capacity of a `/22` represents available addressing headroom rather than an assumption that 1,022 endpoints are currently deployed. The larger prefixes provide room for growth while allowing the addressing plan to demonstrate genuine VLSM alongside `/23`, `/25`, and `/26` networks.

A `/22` also creates a comparatively large Layer 2 broadcast domain. In a larger production campus, a similar endpoint population could instead be divided across additional VLANs and smaller subnets. The use of `/22` networks here is therefore a deliberate lab design choice rather than an assumption that larger broadcast domains are always preferable.

#### OSPF Summarisation Policy

The entire `10.10.0.0/16` block is reserved exclusively for HQ Area 10 addressing.

When the Area 0 backbone is introduced, the HQ Area Border Routers are intended to summarise the Area 10 user and service networks toward Area 0 using the HQ site block rather than advertising each individual VLAN prefix separately.

This provides a clear hierarchical addressing model:

* HQ user and service networks — `10.10.0.0/16`
* Branch user and service networks — `10.20.0.0/16`
* Infrastructure and transit addressing — `10.255.0.0/16`

On Cisco IOS, an active OSPF area-range summary installs a Null0 discard route for the summary by default. This prevents routing loops for destinations that fall within the advertised summary but for which no more-specific route exists in the routing table. A valid more-specific route still takes precedence through normal longest-prefix matching.

For this reason, addresses within `10.10.0.0/16` must remain part of the controlled HQ addressing plan and must not be allocated casually elsewhere in the topology. This preserves both the operational meaning of the HQ summary and the clarity of the overall addressing hierarchy.

### Gateway and SVI Addressing Plan

The gateway addressing convention is standardised across every routed VLAN:

- First usable address — HSRP virtual IP
- Second usable address — `hq-d1`
- Third usable address — `hq-d2`

HSRP group numbers match their associated VLAN IDs.

| VLAN | Name | IPv4 Prefix | HSRP Group | HSRP Virtual IP | `hq-d1` SVI | `hq-d2` SVI | Preferred Active |
|---:|---|---|---:|---|---|---|---|
| 112 | `CORP-USERS` | `10.10.12.0/22` | 112 | `10.10.12.1` | `10.10.12.2/22` | `10.10.12.3/22` | `hq-d1` |
| 120 | `VOICE` | `10.10.20.0/23` | 120 | `10.10.20.1` | `10.10.20.2/23` | `10.10.20.3/23` | `hq-d2` |
| 130 | `SERVERS` | `10.10.30.0/25` | 130 | `10.10.30.1` | `10.10.30.2/25` | `10.10.30.3/25` | `hq-d1` |
| 140 | `IOT-CCTV` | `10.10.40.0/23` | 140 | `10.10.40.1` | `10.10.40.2/23` | `10.10.40.3/23` | `hq-d2` |
| 152 | `GUEST` | `10.10.52.0/22` | 152 | `10.10.52.1` | `10.10.52.2/22` | `10.10.52.3/22` | `hq-d1` |
| 160 | `FACILITIES` | `10.10.60.0/26` | 160 | `10.10.60.1` | `10.10.60.2/26` | `10.10.60.3/26` | `hq-d2` |
| 170 | `BYOD-WLAN` | `10.10.70.0/23` | 170 | `10.10.70.1` | `10.10.70.2/23` | `10.10.70.3/23` | `hq-d1` |
| 199 | `NET-MGMT` | `10.10.99.0/26` | 199 | `10.10.99.1` | `10.10.99.2/26` | `10.10.99.3/26` | `hq-d2` |

#### HSRP Policy

The preferred multilayer distribution switch uses an HSRP priority of `110`, while the standby multilayer distribution switch uses the default priority of `100`. Preemption is enabled on the preferred switch so that it can resume the Active role after recovering from a failure.

Gateway ownership is deliberately split between the two multilayer distribution switches:

- `hq-d1` is preferred Active for VLANs `112`, `130`, `152`, and `170`.
- `hq-d2` is preferred Active for VLANs `120`, `140`, `160`, and `199`.

The preferred HSRP Active switch for each VLAN is also intended to operate as the Rapid PVST+ root primary for that VLAN. The HSRP Standby switch is intended to operate as the STP root secondary.

This aligns the preferred Layer 2 forwarding path with the active Layer 3 default gateway while allowing both multilayer distribution switches to participate in normal forwarding.

#### Management SVI Allocation

VLAN 199 provides the in-band management subnet for network infrastructure.

The HSRP virtual gateway and multilayer distribution switch SVI addresses are allocated above. The management SVI address for `hq-a1` will be selected separately from the remaining usable addresses within `10.10.99.0/26` as part of the management-addressing convention.

`hq-a1` remains a Layer 2 access switch. Its management SVI provides IP reachability for device administration and does not provide inter-VLAN routing.

#### HSRP Versioning — Forward Design Note

The current HQ convention of matching the HSRP group number to the VLAN ID is compatible with the planned VLANs because every HQ group number falls within the HSRP version 1 range.

When the Branch Campus is designed, the same convention must not be copied automatically without checking the VLAN IDs. If future VLAN IDs exceed `255`, HSRP version 2 should be evaluated if the design is to preserve the VLAN-ID-to-HSRP-group-number relationship.

This requirement will be revisited during the Branch Campus design rather than changing the current HQ HSRP design unnecessarily.

### Reserved VLAN Policy

**VLAN 190 — `NATIVE`**

* Dedicated non-default native VLAN
* No SVI
* No intended endpoint traffic

**VLAN 191 — `PARKING`**

* Reserved for unused ports
* No SVI
* Unused ports are administratively shut down

**VLAN 1**

VLAN 1 carries no production traffic, no infrastructure management traffic, and is not used as the native VLAN.

---

## 4. Layer 3 Infrastructure Addressing

HQ Layer 3 infrastructure addressing is allocated from `10.255.10.0/24`, which forms part of the wider `10.255.0.0/16` infrastructure and transit address space.

Point-to-point routed interfaces use `/31` prefixes, while loopback interfaces use `/32` addresses.

### Point-to-Point Routed Interface Addressing

For consistency, the lower address in each `/31` is assigned to the multilayer distribution switch and the higher address is assigned to the edge router.

The design intentionally uses four independent routed links between each directly paired multilayer distribution switch and edge router to demonstrate OSPF equal-cost multipath across multiple physical paths.

Two additional cross-connected routed links provide alternate paths and are intended to use higher OSPF costs than the direct ECMP links.

| Link | Distribution Interface | Distribution IP | Edge Interface | Edge IP | Path Role |
|---|---|---|---|---|---|
| `hq-d1` ↔ `hq-r1` | `hq-d1 E2/0` | `10.255.10.0/31` | `hq-r1 E0/0` | `10.255.10.1/31` | Direct ECMP |
| `hq-d2` ↔ `hq-r2` | `hq-d2 E2/0` | `10.255.10.2/31` | `hq-r2 E0/0` | `10.255.10.3/31` | Direct ECMP |
| `hq-d1` ↔ `hq-r2` | `hq-d1 E3/0` | `10.255.10.4/31` | `hq-r2 E1/0` | `10.255.10.5/31` | Higher-cost cross-link |
| `hq-d2` ↔ `hq-r1` | `hq-d2 E3/0` | `10.255.10.6/31` | `hq-r1 E1/0` | `10.255.10.7/31` | Higher-cost cross-link |
| `hq-d1` ↔ `hq-r1` | `hq-d1 E2/1` | `10.255.10.8/31` | `hq-r1 E0/1` | `10.255.10.9/31` | Direct ECMP |
| `hq-d1` ↔ `hq-r1` | `hq-d1 E2/2` | `10.255.10.10/31` | `hq-r1 E0/2` | `10.255.10.11/31` | Direct ECMP |
| `hq-d1` ↔ `hq-r1` | `hq-d1 E2/3` | `10.255.10.12/31` | `hq-r1 E0/3` | `10.255.10.13/31` | Direct ECMP |
| `hq-d2` ↔ `hq-r2` | `hq-d2 E2/1` | `10.255.10.14/31` | `hq-r2 E0/1` | `10.255.10.15/31` | Direct ECMP |
| `hq-d2` ↔ `hq-r2` | `hq-d2 E2/2` | `10.255.10.16/31` | `hq-r2 E0/2` | `10.255.10.17/31` | Direct ECMP |
| `hq-d2` ↔ `hq-r2` | `hq-d2 E2/3` | `10.255.10.18/31` | `hq-r2 E0/3` | `10.255.10.19/31` | Direct ECMP |

#### /31 Addressing Rationale

The routed point-to-point links use `/31` prefixes because each subnet connects exactly two Layer 3 endpoints.

Cisco supports `/31` addressing on point-to-point IPv4 links in accordance with RFC 3021. In this use case, both addresses in the `/31` are usable by the two endpoints, avoiding the network and broadcast address overhead associated with traditional `/30` point-to-point subnets.

Using `/31` prefixes therefore reduces infrastructure address consumption while maintaining a simple and repeatable addressing convention.

#### ECMP and Cross-Link Allocation

The eight direct routed links form two intended four-link equal-cost path sets:

- `hq-d1` ↔ `hq-r1` — four independent routed links
- `hq-d2` ↔ `hq-r2` — four independent routed links

The two cross-connected links are:

- `hq-d1 E3/0` ↔ `hq-r2 E1/0`
- `hq-d2 E3/0` ↔ `hq-r1 E1/0`

These cross-links are intended to use deliberately higher OSPF costs so that they remain available as alternate paths rather than joining the normal four-link ECMP path sets.

Their final operational behaviour will be confirmed during implementation and failure testing before they are described as verified backup paths.

### Loopback Addressing

Loopback interfaces use `/32` addresses and provide stable Layer 3 identities that are independent of individual physical-link state.

| Device | Interface | IPv4 Address | Purpose |
|---|---|---|---|
| `hq-r1` | `Loopback0` | `10.255.10.129/32` | Stable identity / OSPF router ID |
| `hq-r2` | `Loopback0` | `10.255.10.130/32` | Stable identity / OSPF router ID |
| `hq-d1` | `Loopback0` | `10.255.10.131/32` | Stable identity / OSPF router ID |
| `hq-d2` | `Loopback0` | `10.255.10.132/32` | Stable identity / OSPF router ID |

#### Infrastructure Address Allocation Rationale

The low-numbered portion of `10.255.10.0/24` is used for routed point-to-point links, while loopback addresses are allocated separately within the same HQ infrastructure block.

This separation makes transit links and stable device identities easier to distinguish during configuration, verification, and troubleshooting.

Unused addresses within `10.255.10.0/24` remain reserved for future HQ infrastructure requirements rather than being allocated before a defined purpose exists.

Future tunnel-source and Area 0/WAN addressing will be designed during the corresponding project phase rather than being pre-allocated here.

---

## 5. Layer 2 Design

The HQ Layer 2 design provides redundant access-to-distribution connectivity using LACP EtherChannel while keeping the Layer 3 Distribution-to-Edge links independent for OSPF ECMP.

### EtherChannel Plan

Three Layer 2 EtherChannels are used within the HQ campus:

| Port-Channel | Connected Devices | Physical Member Interfaces | Members | Function | LACP Mode |
|---|---|---|---:|---|---|
| `Po10` | `hq-a1` ↔ `hq-d1` | `hq-a1 E0/0-E0/1` ↔ `hq-d1 E0/0-E0/1` | 2 | Access-to-Distribution trunk | Active / Active |
| `Po20` | `hq-a1` ↔ `hq-d2` | `hq-a1 E1/0-E1/1` ↔ `hq-d2 E0/0-E0/1` | 2 | Access-to-Distribution trunk | Active / Active |
| `Po30` | `hq-d1` ↔ `hq-d2` | `hq-d1 E1/0-E1/3` ↔ `hq-d2 E1/0-E1/3` | 4 | Distribution interconnect trunk | Active / Active |

`Po10` and `Po20` provide redundant Layer 2 uplinks from `hq-a1` to the two multilayer distribution switches.

`Po30` provides the Layer 2 interconnect between `hq-d1` and `hq-d2`.

LACP is used rather than a static EtherChannel so that member-link participation is negotiated dynamically.

The Layer 3 links between the multilayer distribution switches and edge routers are not EtherChannels. Each remains an independent routed interface for OSPF adjacency formation and ECMP.

### Trunk Policy

All HQ campus EtherChannels operate as IEEE 802.1Q trunks.

The trunk policy is standardised as follows:

- VLAN `190` is the configured native VLAN.
- VLAN `191` is reserved as the parking VLAN and is excluded from normal trunk forwarding.
- VLAN `1` carries no production or infrastructure-management traffic and is not used as the native VLAN.
- Allowed VLANs are explicitly defined rather than relying on the default all-VLAN trunk behaviour.

The intended allowed VLAN set is:

`112,120,130,140,152,160,170,190,199`

Using an explicit allowed-VLAN list limits each trunk to VLANs that have a defined purpose within the HQ design.

### Access Switch Port Allocation

`hq-a1` remains a Layer 2 access switch. Its physical interfaces are allocated as follows:

| Port(s) | Access VLAN | Voice VLAN | Function | Intended State |
|---|---:|---:|---|---|
| `E0/0-E0/1` | — | — | `Po10` members to `hq-d1` | Enabled |
| `E0/2-E0/3` | 191 | — | Unused / parking | Shutdown |
| `E1/0-E1/1` | — | — | `Po20` members to `hq-d2` | Enabled |
| `E1/2-E1/3` | 191 | — | Unused / parking | Shutdown |
| `E2/0` | 112 | 120 | Corporate workstation + IP phone | Enabled |
| `E2/1` | 112 | — | Corporate workstation | Enabled |
| `E2/2` | 130 | — | Server/application endpoint | Enabled |
| `E2/3` | 140 | — | IoT/CCTV endpoint | Enabled |
| `E3/0` | 152 | — | Guest endpoint | Enabled |
| `E3/1` | 160 | — | Printer/facilities endpoint | Enabled |
| `E3/2` | 170 | — | BYOD/WLAN test endpoint | Enabled |
| `E3/3` | 199 | — | Network-management endpoint | Enabled |

Unused access interfaces are assigned to VLAN `191` and administratively shut down.

The access-port allocation represents the intended design. Exact interface naming and availability will be confirmed against the selected CML switching image during implementation.

### Layer 2 Design Intent

The Layer 2 design deliberately separates two different redundancy mechanisms:

- LACP EtherChannel provides link aggregation and member-link resilience on switched campus links.
- OSPF ECMP provides Layer 3 multipath routing on the independent Distribution-to-Edge routed links.

This separation avoids presenting the routed ECMP links as a logical Port-Channel and keeps the purpose of each technology clear in both the design and later verification evidence.

---

## 6. HSRP and Rapid PVST+ Design

Section 3 defines the HQ HSRP addressing, group-number, priority, preemption, and versioning policies.

This section defines how the intended HSRP gateway roles are coordinated with Rapid PVST+ root placement so that Layer 2 forwarding is aligned with the preferred Layer 3 gateway.

### HSRP and STP Role Alignment

For the routed VLANs, the preferred HSRP Active multilayer distribution switch is also intended to operate as the Rapid PVST+ root primary. The peer multilayer distribution switch is intended to operate as the HSRP Standby and STP root secondary.

| VLANs | `hq-d1` Intended Role | `hq-d2` Intended Role |
|---|---|---|
| `112,130,152,170` | HSRP Active / STP Root Primary | HSRP Standby / STP Root Secondary |
| `120,140,160,199` | HSRP Standby / STP Root Secondary | HSRP Active / STP Root Primary |

This alignment keeps the preferred Layer 2 forwarding path directed toward the multilayer distribution switch that owns the active default gateway for the VLAN.

It also reduces unnecessary forwarding across the `hq-d1` ↔ `hq-d2` distribution interconnect during normal operation.

The HSRP priority and preemption settings that establish these preferred gateway roles are documented in Section 3 and are not repeated here.

### Native VLAN STP Placement

VLAN `190` is the dedicated native VLAN carried across the HQ campus trunks. It has no SVI and does not use HSRP, but it still requires deterministic spanning-tree root placement.

| VLAN | Function | `hq-d1` STP Role | `hq-d2` STP Role |
|---:|---|---|---|
| 190 | Native VLAN | Root Primary | Root Secondary |

Because VLAN `190` has no Layer 3 gateway to align with, `hq-d1` is selected as root primary as a fixed administrative convention. The purpose is deterministic root placement rather than Layer 3 traffic-path optimisation.

VLAN `191` is the parking VLAN. It is excluded from normal trunk forwarding and its unused access interfaces are administratively shut down. No campus-wide STP root role is therefore defined for VLAN `191`.

### Rapid PVST+ Policy

Rapid PVST+ is the intended spanning-tree mode for the HQ campus.

A separate spanning-tree instance is maintained for each participating VLAN, allowing root placement to be controlled on a per-VLAN basis.

The routed user, service, and management VLANs use the root-primary/root-secondary assignments shown above so that STP root ownership follows the preferred HSRP gateway ownership.

VLAN `190` uses the separate STP-only root placement defined above because it has no Layer 3 gateway.

The Layer 2 EtherChannels `Po10`, `Po20`, and `Po30` participate in the switched spanning-tree topology. The independent routed interfaces between the multilayer distribution switches and edge routers do not participate in Rapid PVST+.

Cisco's root-primary and root-secondary mechanism is preferred over selecting arbitrary bridge-priority values manually. Exact configuration syntax and resulting bridge priorities will be verified against the selected CML switching image during implementation.

MST remains a later design exercise and is not part of the current HQ implementation.

### Failover and Verification Intent

The implemented design will verify that the intended HSRP Active and STP root roles are established for each routed VLAN and that VLAN `190` uses the intended STP root placement.

Failure testing will also verify that gateway and Layer 2 forwarding roles change as expected when a preferred multilayer distribution switch or relevant Layer 2 path becomes unavailable.

These behaviours remain design intent until they have been demonstrated and captured as implementation evidence.

---

## 7. OSPF Area 10 and ECMP Design

HQ uses OSPFv2 Area `10` for its internal Layer 3 routing.

The HQ OSPF process uses process ID `10` as an administrative convention. The process ID is locally significant and is not required to match the OSPF area number or the process ID used by a neighbouring device.

The two HQ edge routers are intended to participate in Area `0` during the later backbone phase, at which point they will operate as Area Border Routers between Area `10` and Area `0`.

The HQ summarisation policy toward Area `0` is defined in Section 3 and is not duplicated here.

### OSPF Router Identity

Each Layer 3 HQ device uses its `Loopback0` address from Section 4 as an explicitly configured OSPF router ID.

Using an explicit router ID avoids relying on automatic router-ID selection and keeps the OSPF identity of each device independent of individual physical-interface state.

### OSPF Interface Participation

OSPF will be enabled on the required interfaces individually rather than by using a broad network statement that could unintentionally include additional interfaces.

The OSPF process uses a passive-by-default policy. Only interfaces that are intended to form OSPF neighbour relationships are made non-passive.

| Interface Type | Area | OSPF Adjacency | Policy |
|---|---:|---|---|
| Routed Distribution-to-Edge `/31` links | 10 | Yes | Non-passive |
| Routed user/service SVIs | 10 | No | Passive, prefix advertised |
| VLAN 199 management SVI | 10 | No | Passive, prefix advertised |
| `Loopback0` | 10 | No | Passive, `/32` advertised |
| VLAN 190 native VLAN | — | No | No Layer 3 interface / not in OSPF |
| VLAN 191 parking VLAN | — | No | No Layer 3 interface / not in OSPF |

The routed user, service, management, and loopback prefixes are therefore advertised into Area `10` without attempting to establish OSPF neighbours on those interfaces.

Only the ten routed Distribution-to-Edge links defined in Section 4 form OSPF adjacencies.

### Distribution-to-Distribution Routing Scope

`hq-d1` and `hq-d2` do not form an OSPF adjacency directly with each other. Their `Po30` connection is a Layer 2 trunk, and the routed VLAN SVIs carried across it are passive in OSPF.

HSRP and the routed OSPF cross-links therefore provide different forms of resilience. HSRP provides default-gateway redundancy for the campus VLANs, while the higher-cost Distribution-to-Edge cross-links provide alternate Layer 3 routing paths when direct routed connectivity toward an edge router is lost.

The cross-links do not replace HSRP, and HSRP does not provide an alternate OSPF transit path.

### Routed-Link OSPF Network Type

Each Distribution-to-Edge `/31` Ethernet link connects exactly two OSPF devices.

These interfaces are therefore intended to use the OSPF point-to-point network type rather than the default Ethernet broadcast network type.

Using the point-to-point network type reflects the actual two-device topology and avoids an unnecessary DR/BDR election on these links.

The network type will be configured consistently at both ends of every routed link.

### OSPF Cost and ECMP Policy

Explicit OSPF interface costs are used so that path preference is determined by the documented design rather than by platform-dependent interface bandwidth calculations.

The four direct routed links in each primary Distribution-to-Edge pair use equal OSPF costs.

The two cross-connected links use a deliberately higher cost.

| Path Set | Links | OSPF Cost per Interface | Intended Role |
|---|---:|---:|---|
| `hq-d1` ↔ `hq-r1` | 4 | 10 | Direct equal-cost path set |
| `hq-d2` ↔ `hq-r2` | 4 | 10 | Direct equal-cost path set |
| `hq-d1` ↔ `hq-r2` | 1 | 100 | Higher-cost cross-link |
| `hq-d2` ↔ `hq-r1` | 1 | 100 | Higher-cost cross-link |

The values `10` and `100` are administrative design values rather than representations of physical bandwidth. They create an explicit cost difference while keeping all four links within each direct path set equal.

OSPF is configured to permit a maximum of four equal-cost paths so that the intended four-link ECMP design is explicit rather than dependent on a platform default.

The higher cost of the cross-connected links is intended to make them less preferred than the direct links where a lower-cost direct path is available, rather than allowing them to join the normal four-link ECMP sets.

When Area `0` and the inter-site backbone are introduced, end-to-end OSPF costs will be reviewed again to confirm that the resulting SPF decisions still match the intended primary and alternate path hierarchy.

### ECMP Forwarding Behaviour

OSPF determines which paths qualify as equal-cost routes, while the forwarding plane determines how traffic is distributed across the installed next hops.

The presence of four equal-cost routes does not imply that a single traffic flow will be divided evenly across all four physical links.

ECMP verification will therefore distinguish between:

- successful installation of multiple equal-cost next hops in the routing table;
- forwarding behaviour across those next hops; and
- aggregate load sharing observed when multiple traffic flows are generated.

The exact forwarding and hashing behaviour of the selected CML image will be verified during implementation rather than assumed from the design.

### Failure and Convergence Test Intent

With all four direct links operational, routes that use a direct path set should be capable of installing up to four equal-cost next hops.

Failure testing will then remove one direct member at a time and verify that the remaining equal-cost paths continue to provide reachability.

A complete failure of a direct four-link path set will be used to test whether the higher-cost cross-connected paths provide the expected alternate routing behaviour where the surviving topology permits it.

The implementation phase will verify:

- intended OSPF neighbour formation on all ten routed links;
- no unintended OSPF neighbours on SVIs or loopbacks;
- point-to-point OSPF network type on the routed Ethernet links;
- explicit direct-link and cross-link costs;
- installation of up to four equal-cost next hops where intended;
- route removal and reconvergence after individual-link failures;
- alternate-path behaviour after loss of a complete direct path set; and
- restoration of the preferred paths when failed links return.

These behaviours remain design intent until they have been demonstrated and captured as implementation evidence.

---

## 8. Design Rationale

| Design Decision | Rationale |
|---|---|
| Two-tier collapsed core | Provides meaningful campus redundancy within the five-device HQ design |
| Single access switch | Preserves the five-device HQ limit |
| LACP at Layer 2 | Demonstrates logical link aggregation and member-link resilience |
| OSPF ECMP at Layer 3 | Demonstrates multipath routing across independent routed interfaces |
| Cross-connected routed paths | Enables path-cost and routing-reconvergence testing |
| `/31` routed interfaces | Efficient addressing for two-endpoint routed infrastructure |
| `/32` loopbacks | Provides stable device identities and explicit OSPF router IDs |
| VLSM | Sizes networks by function rather than assigning every VLAN a `/24` |
| Dedicated native VLAN | Keeps trunk native traffic separate from production user VLANs |
| Parking VLAN | Keeps unused access ports separate from production VLANs |
| HSRP/STP alignment | Aligns the preferred Layer 2 path with the active gateway |
| Split HSRP/STP ownership | Allows both multilayer distribution switches to participate in normal forwarding |
| Deterministic VLAN 190 STP root placement | Prevents native-VLAN root selection from being left to default bridge election behaviour |
| Rapid PVST+ | Provides per-VLAN spanning-tree instances and allows intentional root placement |
| Passive-by-default OSPF | Limits neighbour formation to intentional routed interfaces |
| Interface-specific OSPF activation | Reduces the risk of unintentionally enabling OSPF on additional interfaces |
| Explicit OSPF router IDs | Keeps OSPF device identity independent of automatic interface-based selection |
| OSPF point-to-point network type | Matches the two-device routed-link topology and avoids unnecessary DR/BDR elections |
| Explicit OSPF interface costs | Makes the intended direct-path and alternate-path preference deterministic |
| Four-path OSPF ECMP limit | Makes the intended four-link equal-cost design explicit rather than relying on a platform default |
| Separate implementation evidence | Keeps design intent separate from platform-specific behaviour and proof |

---

## 9. Current Design Status

The following are **design decisions**:

- Five-device HQ topology
- Two-tier collapsed-core campus design
- OSPFv2 Area `10`
- OSPF process ID `10` as a local administrative convention
- VLAN and VLSM plan
- HSRP addressing and group-number convention
- Split HSRP gateway ownership between `hq-d1` and `hq-d2`
- Rapid PVST+ with HSRP-aligned root placement
- Deterministic STP root placement for native VLAN `190`
- LACP EtherChannels at Layer 2
- Routed Distribution-to-Edge interfaces
- `/31` point-to-point addressing
- `/32` loopbacks
- Explicit `Loopback0` OSPF router IDs
- Passive-by-default OSPF policy
- Interface-specific OSPF activation
- OSPF point-to-point network type on routed Distribution-to-Edge links
- Four-path OSPF ECMP intent
- Explicit OSPF cost `10` on direct ECMP links
- Explicit OSPF cost `100` on cross-connected alternate links
- OSPF maximum equal-cost path limit of `4`
- Higher-cost cross-connected routed paths
- No direct OSPF adjacency between `hq-d1` and `hq-d2`
- Separation of Layer 2 EtherChannel redundancy from Layer 3 OSPF ECMP

The following require implementation evidence before they are considered **as-built**:

- Final platform/image selection
- Exact interface availability and naming
- EtherChannel formation and member state
- Trunk VLAN state
- HSRP Active/Standby roles and failover
- Rapid PVST+ root and blocking behaviour
- VLAN `190` STP root placement
- OSPF router IDs
- OSPF adjacency formation on all ten routed links
- Passive-interface behaviour on SVIs and loopbacks
- OSPF point-to-point network type
- Direct-link and cross-link OSPF costs
- Installation of up to four equal-cost next hops
- ECMP forwarding behaviour
- Individual-link failure and reconvergence
- Complete direct-path-set failure behaviour
- Higher-cost alternate-path behaviour
- Restoration of preferred paths after recovery

Implementation detail and evidence will be maintained separately as the build progresses.

---

## 10. Next Design Phase

After the HQ baseline is implemented and verified, the project will progress toward:

- Monitoring and logging
- Layer 2 security controls
- ACL policy
- Area 0 backbone design
- Branch/Area 20
- GRE
- GRE over IPsec
- Dual-tunnel resilience
- WAN failover / wider ECMP testing
- Python and Ansible automation

The HQ design should remain stable unless implementation evidence identifies a genuine platform or architectural constraint.
