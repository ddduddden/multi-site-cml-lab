# Phase 10: Failure and Resilience Test Plan

[Portfolio](../../../README.md) / [HQ Implementation](README.md) / Phase 10 Test Plan

**Site:** HQ campus · **Coverage:** `HQ-VP-10.01`–`HQ-VP-10.14`  
**Pre-test requirements:** 3 October 2026 · **Baseline:** [`1aa65c5`](https://github.com/ddduddden/multi-site-cml-lab/commit/1aa65c52ead4f23f09e9dbe7450b8f358acb0f0e)  
**Purpose:** A record of *planned checks and acceptance expectations*, not a rewritten account of the 3–6 October test results.

## Purpose and document boundaries

Phases 01–09 proved the individual routing and switching features. Phase 10 asks whether the combined HQ design keeps a usable traffic path after links or devices fail, and whether normal operation returns after restoration.

This plan records the test objectives and acceptance expectations set before execution. The [individual HQ-VP reports](../../../evidence/hq/failure-tests/README.md) describe what was actually run and observed; the [HQ troubleshooting record](troubleshooting.md) covers investigations. The [Testing Methodology](phase-10-testing-methodology.md) and [Engineering Review](phase-10-engineering-review.md) explain the approach and findings.

**Interpretation:** Where a fault exposes an unexpected limitation, preserve the original resilience requirement and record the discrepancy. Reproducing a fault, documenting a failure, or restoring service later does not by itself satisfy a traffic-continuity criterion. The existing evidence and its recorded result labels are not changed by this plan.

## Contents

| Section | Jump to |
| --- | --- |
| Test matrix | [HQ-VP-10.01–10.14](#test-matrix) |
| Method | [Baseline, traffic and evidence rules](#test-method) |
| Procedures | [Individual test specifications](#test-procedures) |
| Acceptance criteria | [How results are assessed](#acceptance-criteria) |
| Navigation | [Source documents and next steps](#navigation) |

## Test matrix

| Test | Failure or check | Pre-test acceptance focus | Report |
| --- | --- | --- | --- |
| [10.01](#hq-vp-1001-healthy-baseline) | Healthy baseline | Healthy, repeatable starting state | [HQ-VP-10.01 report](../../../evidence/hq/failure-tests/10.01/HQ-VP-10.01-healthy-baseline.md) |
| [10.02](#hq-vp-1002-single-routed-link-loss-and-ecmp-reduction) | Single routed-link loss and ECMP reduction | ECMP reduction with surviving traffic | [HQ-VP-10.02 report](../../../evidence/hq/failure-tests/10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) |
| [10.03](#hq-vp-1003-routed-link-failure-detection) | Routed-link failure detection | Observed adjacency detection and recovery | [HQ-VP-10.03 report](../../../evidence/hq/failure-tests/10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) |
| [10.04](#hq-vp-1004-cross-link-loss-and-higher-cost-alternate) | Cross-link loss and higher-cost alternate | Higher-cost alternate and preferred restoration | [HQ-VP-10.04 report](../../../evidence/hq/failure-tests/10.04/HQ-VP-10.04-cross-link-failure.md) |
| [10.05](#hq-vp-1005-po20-member-link-failure) | Po20 member-link failure | Po20 stays up with one member | [HQ-VP-10.05 report](../../../evidence/hq/failure-tests/10.05/HQ-VP-10.05-etherchannel-member-failure.md) |
| [10.06](#hq-vp-1006-access-port-channel-outage) | Access Port-Channel outage | Alternate access uplink; stable gateway owner | [HQ-VP-10.06 report](../../../evidence/hq/failure-tests/10.06/HQ-VP-10.06-access-uplink-failure.md) |
| [10.07](#hq-vp-1007-progressive-po30-degradation-and-complete-loss) | Progressive Po30 degradation and complete loss | Member-loss tolerance, zero-member impact | [HQ-VP-10.07 report](../../../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md) |
| [10.08](#hq-vp-1008-distribution-layer-2-isolation) | Distribution Layer 2 isolation | SVI withdrawal, usable gateway and return path | [HQ-VP-10.08 report](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) |
| [10.09](#hq-vp-1009-active-gateway-loses-routed-uplinks) | Active gateway loses routed uplinks | HSRP remains Active despite loss of routed uplinks | [HQ-VP-10.09 report](../../../evidence/hq/failure-tests/10.09/HQ-VP-10.09-d2-routed-isolation.md) |
| [10.10](#hq-vp-1010-hq-d1-device-outage) | hq-d1 device outage | Distribution takeover after D1 outage | [HQ-VP-10.10 report](../../../evidence/hq/failure-tests/10.10/HQ-VP-10.10-d1-device-failure.md) |
| [10.11](#hq-vp-1011-hq-d2-device-outage) | hq-d2 device outage | Distribution takeover after D2 outage | [HQ-VP-10.11 report](../../../evidence/hq/failure-tests/10.11/HQ-VP-10.11-d2-device-failure.md) |
| [10.12](#hq-vp-1012-hq-r1-device-outage) | hq-r1 device outage | Surviving hq-r2 path and live-flow failover verification | [HQ-VP-10.12 report](../../../evidence/hq/failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md) |
| [10.13](#hq-vp-1013-diagonal-double-device-failure) | Diagonal double-device failure | Settled-state traffic through diagonal pair | [HQ-VP-10.13 report](../../../evidence/hq/failure-tests/10.13/HQ-VP-10.13-diagonal-double-failure.md) |
| [10.14](#hq-vp-1014-final-restoration-and-hygiene) | Final restoration and hygiene | Forwarding, control plane and config restored | [HQ-VP-10.14 report](../../../evidence/hq/failure-tests/10.14/HQ-VP-10.14-final-restoration.md) |

**🟧 10-MINUTE ROUTE — CONTINUE READING**

[![Verification Records](https://img.shields.io/badge/Verification%20Records-bf6700?style=flat-square)](verification-plan.md) &emsp;<sup>➜</sup>&emsp; [![Test Results and Captures](https://img.shields.io/badge/Test%20Results%20and%20Captures-bf6700?style=flat-square)](../../../evidence/hq/failure-tests/README.md)

[![Choose Another Route ↗](https://img.shields.io/badge/CHOOSE%20ANOTHER%20ROUTE%20%E2%86%97-C2185B?style=flat-square)](../../../README.md#explore-the-hq-project)

## Test method

**Topology and rollback.** The campaign uses the existing five CML nodes: `hq-r1`, `hq-r2`, `hq-d1`, `hq-d2` and `hq-a1`. Confirm the working configuration, check running/startup differences, retain a private pre-test CML export and capture one complete baseline before injecting failures. Do not save shutdown states or use CML **Wipe** for a device failure.

**Traffic sources.** Use two sequential access-switch test modes, keeping `no ip routing` on `hq-a1`:

| Mode | Source on `hq-a1` | Gateway | Exercises |
| --- | --- | --- | --- |
| A | `Vlan199`, `10.10.99.4/26` | `10.10.99.1` | `hq-d2`-preferred management gateway |
| B (temporary) | `Vlan112`, `10.10.12.4/22` | `10.10.12.1` | `hq-d1`-preferred user gateway |

Confirm that a temporary source address is unused first. Switch sources one at a time, removing test SVIs and restoring the gateway after use. Record any alternative VLAN source used during testing. A switch-originated test verifies the gateway/routed path, not a physical user endpoint or application.

**Observation sequence.** For every injected fault: establish a healthy path → inject one controlled failure → capture protocol *and* forwarding state → test live destinations → restore → verify the preferred state. Capture both traffic directions where a return path might be asymmetric. Run a settled-state 20-packet ping to destinations that should still be reachable; the expected settled-state result is `20/20`. Record any packet loss during the transition. No zero-loss requirement applies.

**Probe discipline.** Use IP SLA ICMP echo operations from `hq-a1`: `101` to `hq-r2 Loopback0 10.255.10.130`; `102` to `hq-r1 Loopback0 10.255.10.129`; frequency one per second, timeout 800 ms and threshold 500 ms. For 10.12, use a temporary `103` to `hq-d2 Loopback0 10.255.10.132`. Record before/after counters and actual CLI source settings. IP SLA failure counts are **samples**, not precise outage durations; 500 ms is a probe threshold, not a failover acceptance bound. When unsupported or not configured, retain the sourced-ping result instead.

**Scope boundary.** A standalone `hq-r2` device failure is outside the scope of this plan; the two-device 10.13 case does not substitute for that test. Do not describe an excluded scenario as completed.

**Evidence handling.** Preserve one authentic source capture per device/batch where possible, including fault command, interface/protocol state, test traffic and recovery. Log messages should be tied to the test window; unsynchronised device clocks must not be used to invent cross-device event order. Reports link to the [existing evidence index](../../../evidence/hq/failure-tests/README.md); this plan creates no new evidence copies.

## Test procedures

### HQ-VP-10.01: Healthy baseline

**Objective.** Confirm that the five-device HQ topology and its routing, switching and gateway services are healthy before introducing any faults.

**Fault injection.** No failure. Compare running and startup configurations with the intended baseline; confirm the private CML rollback export and enable reliable console/event logging.

**Expected behaviour.** Po10/Po20/Po30 are fully bundled (2/2/4 members); five `FULL` OSPF neighbour entries appear on each Layer 3 device; the preferred HSRP/STP role split is correct; `hq-a1` has `Vlan199 10.10.99.4/26` and gateway `10.10.99.1`. Both edge loopbacks respond.

**Acceptance criteria.** Baseline is acceptable only if link membership, OSPF neighbours, learned routes, HSRP/STP ownership, management settings and sourced probes agree with the established Phase 07–09 state. Unexpected configuration differences are resolved or explicitly recorded before faults begin.

**Verification commands.** On switches: `show etherchannel summary`, `show spanning-tree root`, `show spanning-tree inconsistentports`, `show standby brief`; on Layer 3 devices: `show ip ospf neighbor`, `show ip route ospf`, `show ip interface brief`; on `hq-a1`: gateway/SVI configuration and pings to `10.255.10.129` and `.130`. Check `show archive config differences nvram:startup-config system:running-config` where supported.

**Evidence.** [HQ-VP-10.01 report](../../../evidence/hq/failure-tests/10.01/HQ-VP-10.01-healthy-baseline.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[↑ Test matrix](#test-matrix) · [Next 10.02 →](#hq-vp-1002-single-routed-link-loss-and-ecmp-reduction)

---

### HQ-VP-10.02: Single routed-link loss and ECMP reduction

**Objective.** Prove that a single failed direct routed link removes one usable OSPF/CEF next hop without removing connectivity to the live edge router.

**Fault injection.** With management-VLAN traffic running, identify one `hq-d2`→`hq-r2` direct path using CEF; shut the corresponding `hq-r2` interface after checking the actual CML/CDP endpoints; then restore it.

**Expected behaviour.** The direct four-path forwarding set contracts to three valid links; traffic to `hq-r2` recovers through the surviving direct links. Restoration returns the expected four direct paths.

**Acceptance criteria.** Record affected-interface state, the reduced and restored installed next-hop set, successful settled-state probes and any transition loss. No zero-loss or fixed-second convergence criterion applies.

**Verification commands.** `show ip cef exact-route 10.10.99.4 10.255.10.130`, `show ip route 10.255.10.130`, `show ip cef 10.255.10.130`, `show ip ospf neighbor`, `show ip interface brief`, `show ip sla statistics 101` (or sourced ping).

**Evidence.** [HQ-VP-10.02 report](../../../evidence/hq/failure-tests/10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.01](#hq-vp-1001-healthy-baseline) · [↑ Test matrix](#test-matrix) · [Next 10.03 →](#hq-vp-1003-routed-link-failure-detection)

---

### HQ-VP-10.03: Routed-link failure detection

**Objective.** Record how the routing adjacency reacts to the same physical fault used for 10.02, without manufacturing a second failure.

**Fault injection.** Use the 10.02 shutdown/recovery event; collect the affected devices’ OSPF state and buffered messages around the event.

**Expected behaviour.** The lost adjacency leaves `FULL` and later returns; a peer may react to interface-down notification, OSPF hello/dead timers, or an LSA received via another path. Do not assume all failures take a full 40-second dead interval.

**Acceptance criteria.** The adjacency transition and recovery must be recorded. Attribute a detection cause only where actual event messages support it; otherwise say the cause was not established.

**Verification commands.** `show ip ospf neighbor`, `show ip ospf interface <interface>`, `show logging | include OSPF|LINEPROTO|LINK-`, `show ip interface brief` on both affected ends.

**Evidence.** [HQ-VP-10.03 report](../../../evidence/hq/failure-tests/10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.02](#hq-vp-1002-single-routed-link-loss-and-ecmp-reduction) · [↑ Test matrix](#test-matrix) · [Next 10.04 →](#hq-vp-1004-cross-link-loss-and-higher-cost-alternate)

---

### HQ-VP-10.04: Cross-link loss and higher-cost alternate

**Objective.** Check that the topology retains a valid route when the normal `hq-d2`→`hq-r1` cross-link fails.

**Fault injection.** Shut `hq-r1 Gi0/4` (paired with `hq-d2 Gi3/0`), collect routing and probes, then restore it.

**Expected behaviour.** `hq-d2` reaches `hq-r1 Loopback0` indirectly through `hq-r2` and `hq-d1`. The route metric is expected to change from `101` to `121`, returning to `101` on recovery.

**Acceptance criteria.** The route, selected next hop and successful settled-state traffic must support the alternate path; full neighbour restoration and the preferred metric must be shown afterwards. Transition loss is recorded, not disqualifying by itself.

**Verification commands.** `show ip ospf neighbor`, `show ip route 10.255.10.129`, `show ip cef 10.255.10.129`, `traceroute 10.255.10.129` if captured, `show ip sla statistics 102` or sourced ping.

**Evidence.** [HQ-VP-10.04 report](../../../evidence/hq/failure-tests/10.04/HQ-VP-10.04-cross-link-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[![Orange route step 01 of 12 — next: 10.04 TEST REPORT](https://img.shields.io/badge/ORANGE%20ROUTE-01%2F12%20%20NEXT%3A%2010.04%20TEST%20REPORT-bf6700?style=flat-square)](../../../evidence/hq/failure-tests/10.04/HQ-VP-10.04-cross-link-failure.md)

[← 10.03](#hq-vp-1003-routed-link-failure-detection) · [↑ Test matrix](#test-matrix) · [Next 10.05 →](#hq-vp-1005-po20-member-link-failure)

---

### HQ-VP-10.05: Po20 member-link failure

**Objective.** Check that losing one physical member degrades bandwidth rather than bringing down the complete access uplink.

**Fault injection.** Measure member counters while `hq-a1` sends traffic to `hq-r2` via Po20. Shut the identified member on `hq-d2`; observe; restore it.

**Expected behaviour.** Po20 remains an operational LACP EtherChannel with one bundled member, carrying surviving traffic. Both members return after restoration.

**Acceptance criteria.** The bundle must remain up on its surviving member and traffic must recover. Capture the member state and probe results; preserve any recorded loss.

**Verification commands.** `show etherchannel summary` on `hq-a1`/`hq-d2`, `show interfaces <member>`, `show lacp neighbor` if needed, `show ip sla statistics 101`, sourced 20-packet ping.

**Evidence.** [HQ-VP-10.05 report](../../../evidence/hq/failure-tests/10.05/HQ-VP-10.05-etherchannel-member-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.04](#hq-vp-1004-cross-link-loss-and-higher-cost-alternate) · [↑ Test matrix](#test-matrix) · [Next 10.06 →](#hq-vp-1006-access-port-channel-outage)

---

### HQ-VP-10.06: Access Port-Channel outage

**Objective.** Prove that the access switch can use its other uplink while the designated HSRP Active gateway stays on the intended distribution switch.

**Fault injection.** Separately shut/restore `hq-a1 Po20` (management VLAN199 source), then `Po10`; repeat the Po10 case using a temporary VLAN112 source to exercise `hq-d1`-preferred gateway traffic. Never leave both access uplinks disabled.

**Expected behaviour.** Rapid PVST+ selects the surviving path via the other distribution switch and Po30; existing HSRP Active owners should not need to change. An unaffected-uplink control may show no interruption.

**Acceptance criteria.** Show the surviving access STP path, correct gateway ownership, connectivity to live loopbacks after reconvergence, and return to original port roles on recovery. Capture transient loss.

**Verification commands.** `show spanning-tree vlan 199`, `show spanning-tree vlan 112`, `show standby brief`, `show etherchannel summary`, `show ip sla statistics 101`/`102`, sourced ping.

**Evidence.** [HQ-VP-10.06 report](../../../evidence/hq/failure-tests/10.06/HQ-VP-10.06-access-uplink-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.05](#hq-vp-1005-po20-member-link-failure) · [↑ Test matrix](#test-matrix) · [Next 10.07 →](#hq-vp-1007-progressive-po30-degradation-and-complete-loss)

---

### HQ-VP-10.07: Progressive Po30 degradation and complete loss

**Objective.** Establish how the inter-distribution EtherChannel behaves as physical redundancy falls from four members to zero, including Root Guard and gateway effects.

**Fault injection.** Shut corresponding Po30 physical member pairs progressively (`hq-d1 Gi1/3`, `Gi1/2`, `Gi1/1`, `Gi1/0`, subject to confirmed endpoints). Capture each 3/2/1/0 stage, then restore in reverse order; repeat the complete-loss state for the other test source when required.

**Expected behaviour.** With at least one member, Po30 remains operational. With one member, its STP cost is expected to rise from `3` to `4`, with root-inconsistent on `hq-d1 Po10` for VLANs 120/140/160/199 and on `hq-d2 Po20` for 112/130/152/170/190; those states should clear when the second member is restored. At zero members, affected SVIs with no eligible forwarding Layer 2 port should go down. Check SVI state, HSRP peer visibility and surviving traffic paths against the predicted behaviour.

**Acceptance criteria.** For each step, record bundle membership, STP costs/roles and inconsistent ports; at complete failure, record gateway, SVI and return-route consequences. Record any service outage or split HSRP state and assess it against the acceptance criteria. Full baseline must return after restoration.

**Verification commands.** `show etherchannel summary`, `show spanning-tree vlan 112`, `show spanning-tree vlan 199`, `show spanning-tree inconsistentports`, `show standby brief`, `show ip interface brief`, `show ip route <source-prefix>`, sourced pings.

**Evidence.** [HQ-VP-10.07 report](../../../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.06](#hq-vp-1006-access-port-channel-outage) · [↑ Test matrix](#test-matrix) · [Next 10.08 →](#hq-vp-1008-distribution-layer-2-isolation)

---

### HQ-VP-10.08: Distribution Layer 2 isolation

**Objective.** Test whether a distribution switch that loses every campus Layer 2 connection stops presenting itself as a usable VLAN gateway and routed return path.

**Fault injection.** Shut both `hq-d2 Po20` and `Po30`, leaving all five routed uplinks operational. Check the VLAN gateway and the edge-loopback probes, then restore both Port-Channels.

**Expected behaviour.** Affected `hq-d2` routed VLAN SVIs should go down after losing their active Layer 2 paths, allowing `hq-d1` to take over the relevant HSRP gateway role. The corresponding campus prefix should no longer be preferred through an unusable `hq-d2` return path. Both live edge-loopback destinations should remain reachable through a functioning path.

**Acceptance criteria.** **Original resilience criterion:** affected SVI/routing state must reflect the loss of service, gateway takeover must work and settled-state traffic must have a viable **return** path. A reachable virtual gateway alone is not sufficient. **Reproducing a fault alone does not meet the traffic-continuity requirement.**

**Verification commands.** On `hq-d2`: `show ip interface brief`, `show standby brief`, `show interfaces trunk`, `show spanning-tree vlan 199`, `show ip route connected`, `show ip ospf neighbor`; on `hq-r2`: `show ip route 10.10.99.0`, `show ip cef 10.10.99.4`; on `hq-a1`: STP, VIP and sourced edge-loopback pings/IP SLA. Use Mode A (VLAN199). Record any alternative test source in the evidence.

**Evidence.** [HQ-VP-10.08 report](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[![Orange route step 06 of 12 — next: 10.08 TEST REPORT](https://img.shields.io/badge/ORANGE%20ROUTE-06%2F12%20%20NEXT%3A%2010.08%20TEST%20REPORT-bf6700?style=flat-square)](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md)

[← 10.07](#hq-vp-1007-progressive-po30-degradation-and-complete-loss) · [↑ Test matrix](#test-matrix) · [Next 10.09 →](#hq-vp-1009-active-gateway-loses-routed-uplinks)

---

### HQ-VP-10.09: Active gateway loses routed uplinks

**Objective.** Expose the upstream-health limitation when an HSRP Active distribution switch retains its campus links but loses every route to the edge.

**Fault injection.** Shut all five routed `hq-d2` uplinks (`Gi2/0`–`Gi2/3` and `Gi3/0`); leave Po20/Po30 up. Check management-VLAN connectivity, then restore all five.

**Expected behaviour.** Because HSRP uplink/object tracking is not configured, `hq-d2` is expected to remain Active and answer its local gateway while remote edge-loopback traffic fails. `hq-d1` still has routed reachability but remains HSRP Standby.

**Acceptance criteria.** The limitation is demonstrated only when HSRP status, lost OSPF routes, local VIP success, remote-destination failure and recovery are all recorded. Identify the HSRP tracking/preemption improvement as future work, not an already implemented fix.

**Verification commands.** `show ip ospf neighbor`, `show ip route 10.255.10.129`, `show ip route 10.255.10.130`, `show standby brief`, `show etherchannel summary`, VIP ping and loopback pings/IP SLA.

**Evidence.** [HQ-VP-10.09 report](../../../evidence/hq/failure-tests/10.09/HQ-VP-10.09-d2-routed-isolation.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.08](#hq-vp-1008-distribution-layer-2-isolation) · [↑ Test matrix](#test-matrix) · [Next 10.10 →](#hq-vp-1010-hq-d1-device-outage)

---

### HQ-VP-10.10: hq-d1 device outage

**Objective.** Test the survival of campus gateways and routed connectivity when the preferred distribution switch for VLAN112 is lost.

**Fault injection.** In CML, Stop `hq-d1` in two separate stop/start cycles: mode A on VLAN199 and mode B on VLAN112. Confirm recovery between cycles. Never Wipe.

**Expected behaviour.** `hq-d2` becomes the available gateway/STP path for affected VLANs, and both surviving edge loopbacks are reachable after convergence. On restoration, preferred roles return.

**Acceptance criteria.** Capture HSRP/STP takeover, OSPF neighbours and the edge route back to the test VLAN; show successful settled-state traffic and restoration. Note any cycle/source not actually covered.

**Verification commands.** On surviving nodes: `show standby brief`, `show spanning-tree vlan 112`, `show spanning-tree vlan 199`, `show ip ospf neighbor`, `show ip route <test-subnet>`, sourced ping/IP SLA.

**Evidence.** [HQ-VP-10.10 report](../../../evidence/hq/failure-tests/10.10/HQ-VP-10.10-d1-device-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.09](#hq-vp-1009-active-gateway-loses-routed-uplinks) · [↑ Test matrix](#test-matrix) · [Next 10.11 →](#hq-vp-1011-hq-d2-device-outage)

---

### HQ-VP-10.11: hq-d2 device outage

**Objective.** Test equivalent access and gateway survival after loss of the distribution switch that normally owns VLAN199.

**Fault injection.** Stop `hq-d2` in CML for mode A and mode B in separate stop/start cycles. Start and recover fully between cycles.

**Expected behaviour.** `hq-d1` carries the tested access VLANs and assumes available gateway/STP roles, with live edge loopbacks reachable after convergence. The preferred dual-distribution state returns after restart.

**Acceptance criteria.** Record the surviving HSRP/STP roles, route back to source, loopback probes, and recovered five-neighbour baseline. Distinguish tested sources from planned but unrun variants.

**Verification commands.** `show standby brief`, `show spanning-tree vlan 199`, `show spanning-tree vlan 112`, `show ip ospf neighbor`, `show ip route <test-subnet>`, sourced ping/IP SLA.

**Evidence.** [HQ-VP-10.11 report](../../../evidence/hq/failure-tests/10.11/HQ-VP-10.11-d2-device-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.10](#hq-vp-1010-hq-d1-device-outage) · [↑ Test matrix](#test-matrix) · [Next 10.12 →](#hq-vp-1012-hq-r1-device-outage)

---

### HQ-VP-10.12: hq-r1 device outage

**Objective.** Test continued use of `hq-r2` when `hq-r1` is stopped, and attempt to demonstrate a live flow moving off the failed router.

**Fault injection.** Original proposal: run from temporary `hq-a1 Vlan112` source `10.10.12.4`, first prove the chosen test flow uses `hq-r1`, and monitor a temporary probe to `hq-d2 Loopback0 10.255.10.132` (probe 103). Stop/Start `hq-r1` in CML and remove the temporary probe afterwards.

**Expected behaviour.** `hq-r1 Loopback0` necessarily fails while its router is stopped. A flow to a **surviving** destination that originally used `hq-r1` should be able to use an alternate route through `hq-r2`. The stopped router's routes and adjacencies return after restart.

**Acceptance criteria.** Verify surviving connectivity. To demonstrate live-flow failover, capture the forwarding path and traffic for the same flow before and after the failure. Record any missing coverage.

**Verification commands.** `show ip cef exact-route <source-ip> 10.255.10.132`, `show ip route 10.255.10.132`, `show ip ospf neighbor`, sourced ping/IP SLA where actually configured; verify both edge loopbacks after restoration.

**Evidence.** [HQ-VP-10.12 report](../../../evidence/hq/failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.11](#hq-vp-1011-hq-d2-device-outage) · [↑ Test matrix](#test-matrix) · [Next 10.13 →](#hq-vp-1013-diagonal-double-device-failure)

---

### HQ-VP-10.13: Diagonal double-device failure

**Objective.** Check whether the remaining diagonal distribution/edge pair sustains traffic after two separate node losses.

**Fault injection.** Use a single source VLAN to verify the surviving routed path. This test does not require a comparison of STP root behaviour. Stop `hq-d1` and allow the network to settle. Then stop `hq-r2`, leaving `hq-d2` ↔ `hq-r1` on their cross-link. Restore `hq-r2` first, then `hq-d1`; do not Wipe either node.

**Expected behaviour.** `hq-d2` provides the surviving gateway, and `hq-r1` remains reachable through the diagonal routed link. `hq-r2` destinations cannot answer while stopped.

**Acceptance criteria.** Prove connectivity through the surviving diagonal pair in the **settled** two-fault state, including route back to the source and service restoration. Do not claim zero loss or measured transition time unless continuously captured.

**Verification commands.** `show standby brief`, `show ip ospf neighbor`, `show ip route 10.255.10.129`, `show ip route <test-subnet>` on `hq-r1`, source-VLAN gateway and `hq-r1` loopback pings; check restoration on both nodes.

**Evidence.** [HQ-VP-10.13 report](../../../evidence/hq/failure-tests/10.13/HQ-VP-10.13-diagonal-double-failure.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.12](#hq-vp-1012-hq-r1-device-outage) · [↑ Test matrix](#test-matrix) · [Next 10.14 →](#hq-vp-1014-final-restoration-and-hygiene)

---

### HQ-VP-10.14: Final restoration and hygiene

**Objective.** Confirm that fault injection and temporary monitoring left no forwarding change behind and that the retained network can be restarted from a known healthy state.

**Fault injection.** Start all nodes, `no shutdown` all test interfaces, remove temporary access-switch SVIs and IP SLA schedules/operations (including proposed 103 if installed), reinstate `hq-a1 Vlan199 10.10.99.4/26` and gateway `10.10.99.1`; restore other temporary settings.

**Expected behaviour.** Po10/Po20/Po30 full membership, no inconsistent STP ports, intended HSRP/STP split, five `FULL` OSPF neighbours on each Layer 3 device and successful gateway/edge-loopback checks. No unintended running/startup or configuration drift.

**Acceptance criteria.** Reconcile running, startup and intended settings on **all five** devices, resolve any configuration differences before saving, and retain the final configurations and private CML backup. A successful forwarding check alone does not prove complete configuration sign-off.

**Verification commands.** `show etherchannel summary`, `show spanning-tree root`, `show spanning-tree inconsistentports`, `show standby brief`, `show ip ospf neighbor`, `show ip route ospf`, `show ip sla configuration`, `show ip interface brief`, sourced pings, running/startup configuration comparison.

**Evidence.** [HQ-VP-10.14 report](../../../evidence/hq/failure-tests/10.14/HQ-VP-10.14-final-restoration.md) · [Phase 10 index](../../../evidence/hq/failure-tests/README.md).

[← 10.13](#hq-vp-1013-diagonal-double-device-failure) · [↑ Test matrix](#test-matrix)

---

## Acceptance criteria

Assess each test against its acceptance criteria in HQ-VP-10.01–10.14. Confirm the expected protocol state, traffic forwarding and recovery using recorded checks. Results belong in the [Phase 10 evidence index](../../../evidence/hq/failure-tests/README.md); detailed findings belong in the [Engineering Review](phase-10-engineering-review.md).

**Result vocabulary.** The evidence index uses `PASS`, `FAIL` and `INCONCLUSIVE` for execution outcomes. These should be judged against each pre-test criterion. The earlier general HQ verification plan uses a separate lifecycle status scheme (`Verified`, `Blocked`, etc.); do not treat those as interchangeable without an explicit project decision.

## Navigation

[← HQ verification plan](verification-plan.md) · [↑ Test matrix](#test-matrix) · [Phase 10 results and evidence](../../../evidence/hq/failure-tests/README.md) · [HQ troubleshooting](troubleshooting.md) · [HQ implementation](README.md)
