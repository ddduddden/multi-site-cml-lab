# HQ Troubleshooting

[Portfolio](../../../README.md) / [HQ Implementation](README.md) / Troubleshooting

This file records **meaningful diagnostic investigations**.

It is not a diary of every mistake. The build log remains the chronology; a build-log or verification entry links here only when the observed behaviour requires real investigation.

## Troubleshooting Contents

[HQ-TS-001 — IOSvL2 Routing Mode](#hq-ts-001--iosvl2-routing-mode-on-hq-a1) | [HQ-TS-002 — IOSvL2 SVI State](#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation)

---

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-TS-NNN` | HQ troubleshooting record |
| `HQ-VP-XX.YY` | Related HQ verification test |
| `HQ-DEV-NNN` | Related HQ design deviation |

## When to create a troubleshooting record

**Normally does not need an `HQ-TS-NNN` record:**
- A mistyped command that is corrected immediately.
- A wrong interface selected and immediately corrected.
- A forgotten `no shutdown` noticed immediately.
- A minor syntax correction with no meaningful effect on the build.

**Normally does justify an `HQ-TS-NNN` record:**
- A protocol fails to establish even though the configuration appears correct.
- Failover or reconvergence differs from the expected behaviour.
- A platform or image behaves differently from the documented assumption.
- A routing decision cannot initially be explained.
- A feature limitation requires investigation before implementation can continue.

## Entry template

```text
## HQ-TS-NNN — Short title

Opened:
DD-MM-YYYY

Related verification:
- HQ-VP-XX.YY

Related build-log entry:
- DD-MM-YYYY — description

Symptom:
...

Expected behaviour:
...

Scope / impact:
...

Investigation:
1. ...
2. ...
3. ...

Root cause:
...

Correction:
...

Re-verification:
...

Evidence:
...

Related deviation:
- HQ-DEV-NNN, only if an accepted design deviation results

Status:
Open / Resolved
```

## Cross-reference rule

Resolving a troubleshooting record does not automatically mean the related verification test is `Verified`.

After the correction, the verification test must be run or re-run and its own `Observed result`, `Status`, and evidence updated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<a name="hq-ts-001--iosvl2-routing-mode-on-hq-a1"></a>

## HQ-TS-001 — IOSvL2 Routing Mode on `hq-a1` [→](#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation)

**Opened:**  
`30-09-2026`

**Related verification:**  
- `HQ-VP-07.05` — where the fault was observed and the correction re-verified
- `HQ-VP-05.01` — earlier as-built record of the `hq-a1` default gateway
- `HQ-VP-06.01` — the same IOSvL2 routing behaviour observed on `hq-d1` and `hq-d2`

**Related build-log entry:**  
- `30-09-2026` — Phase 07: disabled IP routing on `hq-a1`

**Symptom:**  
During `HQ-VP-07.05`, `hq-a1` (`10.10.99.4`) could reach its local HSRP gateway but could not reach the four `Loopback0` addresses, even though `ip default-gateway 10.10.99.1` was configured. `show ip route` displayed a routing table rather than the `Default gateway is …` view expected from the Layer 2 access-switch role.

**Expected behaviour:**  
`hq-a1` operates as a Layer 2 access switch. Management traffic for destinations beyond VLAN `199` should use `ip default-gateway 10.10.99.1`, as set out in the HQ Campus Design, Section 3, *Management SVI Allocation*.

**Scope / impact:**  
- `hq-a1` management traffic beyond the local VLAN. The default gateway had been configured since Phase 05 but was not being used while IPv4 routing remained enabled.
- No Phase 05 result is affected. Every `hq-a1` test in `HQ-VP-05.03`–`HQ-VP-05.05` used targets in the same VLAN as the source (`10.10.99.x` from `Vlan199`, and `10.10.12.x` from the temporary `Vlan112` SVI).
- `hq-d1` and `hq-d2` use the same IOSvL2 default routing behaviour, but that behaviour is appropriate for their multilayer distribution role and required no correction.

**Investigation:**  
1. `show ip route` on `hq-a1` returned the routing-table view, so IP routing was enabled even though no `ip routing` line appeared in the running configuration.
2. With IP routing enabled, IOS forwarded using the routing table rather than `ip default-gateway`. `hq-a1` held only its connected `Vlan199` route, so it had no route to the `10.255.10.x` routing identities.
3. `hq-d1` and `hq-d2`, which run the same IOSvL2 image, also route without an explicit `ip routing` line (`HQ-VP-06.01`). This corroborated the same observed IOSvL2 routing behaviour on the distribution switches.
4. OSPF was not the cause. The edge routers held `10.10.99.0/26` through OSPF (`HQ-VP-07.04`), so a return path existed.

**Root cause:**  
On the IOSvL2 image used in this lab (`vios_l2` `15.2(20200924:215240)`), IPv4 routing was operational in the initial lab state even though `ip routing` was not displayed in the normal running configuration. Cisco documents `ip default-gateway` for use when IP routing is disabled; while routing remained active, `hq-a1` forwarded according to its routing table instead of using the configured default gateway. Because it held only the connected VLAN `199` route, it had no routed path to the remote `Loopback0` addresses. This observed platform behaviour was not captured by the Phase 01 capability review.

**Correction:**  
`no ip routing` on `hq-a1`, retaining `ip default-gateway 10.10.99.1`. The running configuration now also shows `no ip cef` globally and `no ip route-cache` on `Vlan199`, consistent with routing being disabled. `hq-d1` and `hq-d2` were not changed.

**Re-verification:**  
- `HQ-VP-07.01` — `show ip route` on `hq-a1` reports `Default gateway is 10.10.99.1`.
- `HQ-VP-07.05` — `hq-a1` reached `10.10.99.1` and all four loopbacks at `5/5`.
- `HQ-VP-07.06` — `hq-a1 Vlan199` remained `up/up`, and the Layer 2 state was unchanged.

**Evidence:**  
Post-correction state: `evidence/hq/ospf/HQ-VP-07.01-loopback-ospf-process-identity.txt`; `evidence/hq/ospf/HQ-VP-07.05-end-to-end-reachability.txt`; `configs/hq/hq-a1-running-config.txt`. Pre-correction output was not retained as repository evidence.

**Related deviation:**  
None. The correction brings `hq-a1` into line with the design.

**Status:**  
Resolved

[↑ Troubleshooting Contents](#troubleshooting-contents) | [Next: HQ-TS-002 →](#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation)

---

<a name="hq-ts-002--iosvl2-svi-state-during-layer-2-isolation"></a>

## [←](#hq-ts-001--iosvl2-routing-mode-on-hq-a1) HQ-TS-002 — IOSvL2 SVI State During Layer-2 Isolation

**Featured orange route — 10.08 investigation.** Continue through this troubleshooting record to the linked engineering conclusion below.

**Opened:**
`04-10-2026`

**Related verification:**
- [`HQ-VP-10.07`](../../../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md) — progressive `Po30` member loss and complete inter-distribution failure
- [`HQ-VP-10.08`](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) — `hq-d2` Layer-2 isolation with routed uplinks left operational

**Related engineering review:**
- [Phase 10 — Engineering Review and Conclusions](phase-10-engineering-review.md) — discussion of the SVI state, HSRP and return-path findings

**Symptom:**
During `HQ-VP-10.07` and `HQ-VP-10.08`, routed SVIs remained `up/up` on an IOSvL2 distribution switch even after the affected VLAN no longer had a usable Layer-2 forwarding path.

In `HQ-VP-10.08`, `hq-d2 Po20` and `Po30` were administratively shut while all five routed OSPF uplinks remained operational. `show interfaces trunk` returned no active trunks and `show spanning-tree vlan 160` showed no spanning-tree instance, but `Vlan160` remained `up/up`.

The same behaviour was then recognised in the complete `Po30` failure from `HQ-VP-10.07`, where stranded SVIs remained operational despite the Layer-2 partition.

**Expected behaviour:**
I expected an SVI to lose line protocol when its VLAN no longer had a usable Layer-2 forwarding port.

If the stranded SVI had gone down, its connected route would also have been removed. HSRP on that interface would no longer have remained Active, and OSPF would not have continued advertising the affected connected subnet from that switch.

**Scope / impact:**
- The behaviour was observed on the IOSvL2 distribution switches used in the CML lab.
- During complete `Po30` loss, both distribution switches retained SVIs for VLANs that were isolated from the opposite side of the Layer-2 topology.
- This allowed both HSRP peers to become Active independently when the Layer-2 partition separated them.
- During `HQ-VP-10.08`, `hq-d2` retained `10.10.60.0/26` as a connected route and continued advertising it into OSPF even though it no longer had a Layer-2 path to the test host.
- `hq-r2` therefore continued selecting `hq-d2` for the return path, producing a data-plane blackhole.
- The behaviour affects the interpretation of both `HQ-VP-10.07` and `HQ-VP-10.08`.

**Investigation:**
1. I first confirmed that the failure was genuinely Layer 2. On `hq-d2`, both `Po20` and `Po30` were down, `show interfaces trunk` returned no active trunks, and `show spanning-tree vlan 160` showed no active instance.
2. I then checked the Layer-3 state. `Vlan160` remained `up/up` and `10.10.60.0/26` remained installed as a connected route.
3. All five routed OSPF adjacencies on `hq-d2` remained `FULL`, so the switch continued advertising the connected VLAN160 subnet.
4. The routing and CEF checks showed that `hq-r2` selected a return path through `hq-d2`. Together with the failed traffic tests, this supports the return-path blackhole identified in `HQ-VP-10.08`. No packet-level capture of the drop was retained.
5. Traffic testing showed the consequence directly: the local HSRP gateway remained reachable from `hq-a1`, while the monitored path through `hq-r2` failed.
6. Reviewing `HQ-VP-10.07` showed the same underlying SVI behaviour during complete loss of `Po30`. The Layer-2 partition separated the HSRP peers, but the stranded SVIs remained operational instead of dropping.
7. Recovery of the Layer-2 paths restored end-to-end connectivity without changing the routing decision on `hq-r2`, supporting the conclusion that the missing downstream Layer-2 path caused the failure.

`HQ-VP-10.07` exposed the same SVI behaviour, but `HQ-VP-10.08` established the return-path failure.

**Root cause:**
The IOSvL2 image used in this lab retained SVI line protocol in situations where the affected VLAN had no usable Layer-2 forwarding path.

Because the SVI remained `up/up`, IOS also retained the directly connected subnet. That allowed HSRP to remain operational locally and allowed OSPF to continue advertising a subnet that the switch could no longer reach through the Layer-2 topology.

The resulting blackhole was therefore produced by an interaction between:

1. the intentional Layer-2 topology and Root Guard policy;
2. the failure that removed the usable Layer-2 path; and
3. the observed IOSvL2 SVI state behaviour.

This is recorded as an **IOSvL2 platform observation**. It is not being claimed as general Cisco Catalyst behaviour or as a confirmed Cisco software defect.

**Correction:**
No corrective network configuration was applied during Phase 10.

The purpose of the failure tests is to measure the behaviour of the as-built HQ design before introducing remediation. The platform behaviour is documented so that it is not mistaken for a general physical-switch characteristic.

The finding will also be considered when the Branch campus is designed and when equivalent failure behaviour is tested on later platforms.

**Re-verification:**
- Restoring `Po20` and `Po30` returned the normal Layer-2 topology.
- `hq-d2` returned to its intended HSRP Active role for VLAN160 and `hq-d1` returned to Standby.
- `hq-a1` again selected `Po20` as the VLAN160 root path.
- All five `hq-d2` OSPF adjacencies remained `FULL`.
- Gateway, `hq-r1` and `hq-r2` reachability returned to `5/5`.
- The `hq-r2` route and CEF selection toward VLAN160 remained unchanged, but became usable again once the downstream Layer-2 path was restored.

**Evidence:**
- [HQ-VP-10.07 — Progressive Po30 failure](../../../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md) and [retained CLI/session evidence](../../../evidence/hq/failure-tests/10.07/README.md)
- [HQ-VP-10.08 — Layer 2 isolation and return-path blackhole](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) and [retained CLI/session evidence](../../../evidence/hq/failure-tests/10.08/README.md)
- [10.08 original event buffer](../../../evidence/hq/failure-tests/10.08/10.08-original-event-buffer.md) and [original recovery CLI](../../../evidence/hq/failure-tests/10.08/10.08-original-recovery-cli.md)

**Related deviation:**
None. The unexpected result is being recorded as platform-specific behaviour rather than an accepted change to the HQ design.

**Status:**
Open — investigation complete; the observed SVI behaviour has not been corrected.

[← Previous: HQ-TS-001](#hq-ts-001--iosvl2-routing-mode-on-hq-a1) | [↑ Troubleshooting Contents](#troubleshooting-contents) | [HQ Verification Plan →](verification-plan.md)

[![Orange route step 11 of 12 — next: 10.08 ENGINEERING REVIEW](https://img.shields.io/badge/ORANGE%20ROUTE-11%2F12%20%20NEXT%3A%2010.08%20ENGINEERING%20REVIEW-bf6700?style=flat-square)](phase-10-engineering-review.md#layer-2-isolation-and-split-brain--hq-vp-1008)

[↑ Phase 10 Test Index](../../../evidence/hq/failure-tests/README.md) · [← Original event buffer](../../../evidence/hq/failure-tests/10.08/10.08-original-event-buffer.md)
