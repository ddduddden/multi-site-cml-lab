# HQ Engineering Review and Conclusions

[Portfolio](../../../README.md) / [HQ Implementation](README.md) / Engineering Review

> **Scope:** HQ Campus · Test window: 3–6 October 2026 · HQ-VP-10.01–10.14  
> **Status:** Fault tests completed 3–6 October; final configuration reconciliation completed 12 October 2026

## Contents

- [Routed paths](#routed-paths--hq-vp-10021004)
- [Access member and uplink failures](#access-member-and-uplink-failures--hq-vp-10051006)
- [Progressive Po30 failure](#progressive-po30-failure--hq-vp-1007)
- [Layer 2 isolation and split brain](#layer-2-isolation-and-split-brain--hq-vp-1008)
- [Upstream isolation and HSRP](#upstream-isolation-and-hsrp--hq-vp-1009)
- [Device and combined failures](#device-and-combined-failures--hq-vp-10101013)
- [Restoration and remaining checks](#restoration-and-remaining-checks--hq-vp-1014)
- [Priorities for the next revision](#priorities-for-the-next-revision)
- [Overall assessment](#overall-assessment)
- [Technical references](#technical-references)

Phase 10 tested how the as-built HQ campus behaved when links and devices failed. Several alternate paths worked as intended, while the isolation tests exposed limits in the current design. This review explains those findings, the troubleshooting behind them and the remaining work before sign-off.

## Routed paths | HQ-VP-10.02–10.04

*Evidence: [HQ-VP-10.02–10.03](../../../evidence/hq/failure-tests/10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md) · [HQ-VP-10.04](../../../evidence/hq/failure-tests/10.04/HQ-VP-10.04-cross-link-failure.md)*

Removing one routed ECMP link reduced the number of equal-cost paths, but the destination was still reachable through the remaining links. When the normal cross-link failed, OSPF used the surviving higher-cost route. On hq-d2, the route to hq-r1 Loopback0 changed from metric 101 to 121, then returned to 101 when the link was restored.

This supported my cost design from Phase 09: the planned alternate links were there when needed, but did not become the preferred paths during normal operation. IP SLA recorded some failed samples while the route changed, so the switchover was not loss-free. The alternate route worked, and the original route returned after recovery.

## Access member and uplink failures | HQ-VP-10.05–10.06

*Evidence: [HQ-VP-10.05](../../../evidence/hq/failure-tests/10.05/HQ-VP-10.05-etherchannel-member-failure.md) · [HQ-VP-10.06](../../../evidence/hq/failure-tests/10.06/HQ-VP-10.06-access-uplink-failure.md)*

The first Po20 member test followed the plan: I shut down the selected member on hq-d2 only. The far end initially continued showing its link up, before LACP suspended it. This was not just a timing quirk. The test recorded 0/20 replies, 177 failed SLA101 samples and a later 0/5 return check from hq-r2 to hq-a1. The sustained asymmetric loss was not explained.

I added a second run with both ends of the same member pair shut down. Po20 stayed operational on the other bundled member, with 20/20 replies in the retained settled-state ping. Both runs remain in the evidence. The bilateral rerun demonstrated member redundancy under a different fault condition; it did not make the original one-sided failure disappear.

The complete access Port-Channel test removed the whole logical uplink, leaving no member in that bundle to carry traffic. Rapid PVST+ provided the alternate Layer-2 path, and the intended HSRP gateway could remain Active. Traffic could therefore reach the same gateway through a different switch path. A change in the Layer-2 forwarding path did not require the gateway role itself to move.

## Progressive Po30 failure | HQ-VP-10.07

*Evidence: [HQ-VP-10.07](../../../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md)*

Po30 remained up as four members were reduced to three, two and one. With one member left, its STP cost rose from 3 to 4. On hq-d2, Po30 was still the root port for VLAN130, but hq-a1 now advertised a lower-cost path to the root. Root Guard therefore put hq-d2’s access-facing Po20 into root-inconsistent state rather than allowing it to take a root-port role. It reacted to the superior BPDU, not directly to the member loss. [1]

When the final member failed, Po30 went down completely. At that point a physical Layer-2 path through hq-a1 still existed, but Root Guard blocked it by design, preventing the access layer from becoming a transit path between the distribution switches. The switches could no longer exchange HSRP hellos on affected VLANs. Traffic also failed: SLA101 had already logged four failed samples at three-to-two links and seven more at two-to-one, then timed out at zero links. From hq-a1, hq-d2’s VLAN130 SVI returned 0/5 while it still showed up/up. The zero-link return route was not captured, so I cannot claim that the exact return path was proved in 10.07. Recovery also recorded further failed samples.

This showed me the limit of the design. The four Po30 members protect against individual link failures, but together they still form one logical connection between the distribution switches. Root Guard was deliberately configured on the access-facing Port-Channels to protect the intended distribution-layer root placement. I would keep that protection and look at an independent inter-distribution connection. An additional Layer-2 switch could be an option if designed into that connection; simply adding another access switch behind the same Root Guard protection would not solve the loss of Po30.

## Layer 2 isolation and split brain | HQ-VP-10.08

*Evidence: [HQ-VP-10.08](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md)*

Shutting down Po20 and Po30 on hq-d2 isolated it at Layer 2 while leaving its routed uplinks operational. The HSRP states and traffic failures that followed took some working out.

Once the switches lost contact over Layer 2, hq-d1 became HSRP Active, while the isolated hq-d2 also showed Active locally because it could no longer hear its peer. From hq-a1, however, hq-d2’s VLAN160 SVI was unreachable (0/5). The two devices showed split HSRP state; they were not both providing a usable gateway to the test source.

From hq-a1, the gateway remained reachable through hq-d1 and traffic to hq-r1 worked after the path settled, although SLA102 recorded nine failed samples during the change. Traffic to hq-r2 failed. All eight hq-d2 VLAN SVIs stayed up/up in the isolated state. Its VLAN160 subnet continued to be advertised into OSPF, and hq-r2’s routing and CEF checks selected hq-d2 for the return flow to 10.10.60.4 despite the missing Layer-2 path to hq-a1.

The return-route and CEF evidence supports a blackhole on the path back to the source; it is not a packet-level capture of the drop. The gateway check alone would have missed it. This is why I checked the routing information alongside sourced traffic.

I went away and read Cisco's documentation on Catalyst SVI autostate to understand why Vlan160 had stayed up. Under the documented default behaviour, the VLAN and SVI must be enabled, with at least one eligible Layer-2 port in the VLAN up and forwarding in STP. With no eligible forwarding port left, the SVI line protocol would normally go down. The IOSvL2 image kept it up, which did not match that expectation. This should therefore not be presented as normal Catalyst behaviour. [2]

This was one of the main learning points for me. It went beyond the straightforward failover examples from my CCNA study. The two locally Active HSRP states showed the split-brain condition, but they did not explain the different traffic results. Understanding that meant checking the SVI state, OSPF advertisement and hq-r2’s selected return route.

The network recovered once the links were restored, but the test had exposed a gap in traffic continuity despite the gateway remaining reachable.

## Upstream isolation and HSRP | HQ-VP-10.09

*Evidence: [HQ-VP-10.09](../../../evidence/hq/failure-tests/10.09/HQ-VP-10.09-d2-routed-isolation.md)*

Removing all five routed uplinks from hq-d2 left it without OSPF routes, while its Layer-2 connections stayed up. hq-d2 remained HSRP Active for VLAN199. From hq-a1, the virtual gateway was still reachable, but it no longer provided a working route to the edge routers.

Unlike the Layer-2 isolation in HQ-VP-10.08, the switches could still exchange HSRP hellos here. The problem was that hq-d2 remained Active after losing its upstream routes. No interface or object tracking was configured to reduce its effective priority when that happened.

Working through this and reading Cisco's guidance helped me understand what the tracking configuration would need to do. Tracking can lower the Active switch's priority, but the decrement must be large enough for the other switch to have the higher priority. That switch also needs preemption enabled to take over. [3]

A reachable gateway was not enough to keep traffic moving. This test confirmed the upstream-tracking gap already identified in the design rather than demonstrating automatic gateway failover. Tracking and preemption are future improvements and would need testing during failure and recovery.

## Device and combined failures | HQ-VP-10.10–10.13

*Evidence: [HQ-VP-10.10](../../../evidence/hq/failure-tests/10.10/HQ-VP-10.10-d1-device-failure.md) · [HQ-VP-10.11](../../../evidence/hq/failure-tests/10.11/HQ-VP-10.11-d2-device-failure.md) · [HQ-VP-10.12](../../../evidence/hq/failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md) · [HQ-VP-10.13](../../../evidence/hq/failure-tests/10.13/HQ-VP-10.13-diagonal-double-failure.md)*

The individual device tests covered the loss of each distribution switch and hq-r1. The retained checks show surviving HSRP, STP, routing or connectivity where captured, followed by restored service after restart. Coverage was not identical in each case: hq-d1’s final HSRP/OSPF state after the 10.10 restart was not captured, and 10.12 confirmed hq-r2 reachability and an OSPF cross-link neighbour but did not run the planned live-flow failover test away from hq-r1.

For the combined failure I stopped hq-d1 first, allowed the network to settle, then stopped hq-r2. In the remaining state, hq-d2 and hq-r1 had the cross-link route in both directions and the tested VLAN170 traffic succeeded. This showed the value of the diagonal link. The evidence covers the settled double-failure state, not transition loss or an exact convergence time.

## Restoration and remaining checks | HQ-VP-10.14

*Evidence: [HQ-VP-10.14](../../../evidence/hq/failure-tests/10.14/HQ-VP-10.14-final-restoration.md)*

The final restoration checks showed the HQ network back in its normal forwarding state. Po10 and Po20 each had both members, Po30 had all four, and the STP and HSRP roles matched the intended split. OSPF neighbours returned and the final connectivity checks passed. Temporary VLAN test addressing and IP SLA operations were removed.

At the end of the 6 October session, hq-a1 still had the temporary `logging buffered 65536 informational` setting and several final running/startup comparisons had not been retained. Those checks were completed on 12 October. The original hq-a1 logging setting was restored and saved, and all five devices were checked. The only remaining comparison differences were the known CML configuration-fetch VTY timeout artefacts. The follow-up CLI is retained in the [10.14 configuration evidence](../../../evidence/hq/failure-tests/10.14/10.14-config-excerpts.md), with the final CML export kept private.

## Priorities for the next revision

The main lesson from these tests is that redundancy has to be checked across the whole traffic path, in both directions. An interface being up or a gateway showing Active does not prove that traffic can reach its destination and get back.

For the next revision, I would focus on three areas:

1. HSRP upstream tracking. Test object or route-health tracking, with a priority decrement and preemption policy that move the gateway role when upstream connectivity is lost.
2. An independent inter-distribution connection. Evaluate a separate Layer-2 connection, potentially through an additional switch, while keeping Root Guard on the access-facing Port-Channels. The proposed topology would need to keep the distribution switches connected after Po30 fails, without relying on the access layer for transit. Test STP root placement, loop prevention and HSRP communication during failure and recovery.
3. Time synchronisation and continuous monitoring. Phase 10 lacked NTP synchronisation and continuous external monitoring, which limited how accurately events could be matched across devices and outages measured. For the next test cycle, configure NTP and verify that device clocks are synchronised before testing. Add central logging and continuous traffic probes alongside the manual CLI checks. Matching timestamps would help establish the event sequence, while the probe interval and capture method would determine the precision of the outage measurements.
These changes have not been implemented or tested in Phase 10. They would need to form part of a separate design revision and test cycle.

The unexpected IOSvL2 autostate behaviour also needs a clear follow-up: it is recorded as a platform-specific limitation here, not assumed to be normal Catalyst behaviour. A later test on a platform with standard SVI autostate would be needed before drawing wider conclusions about that failure mode.

## Overall assessment

The HQ design provided useful resilience during the tested routed-link, EtherChannel-member, access-uplink and device failures, within the limits of the traffic captures. The isolation tests also exposed gaps: loss of the only logical inter-distribution path, SVIs and OSPF advertisements remaining active after Layer-2 isolation in IOSvL2, and HSRP staying on a switch with no upstream routes.

The most useful part of this phase for me was working out why traffic stopped during those failures. It showed what worked, where the lab image behaved differently from normal Catalyst SVI autostate and what I want to address in a later revision. The fault tests and final configuration close-out are complete; the 10.08 failure and 10.12 inconclusive coverage remain documented in their reports. Availability and precise convergence times were not measured.

**Continue reading:** [Priorities for the next revision](#priorities-for-the-next-revision) · [Current acceptance status](phase-11-final-acceptance.md#overall-assessment) · [Choose another route](../../../README.md#explore-the-hq-project).

## Technical references

[1] Cisco, “Enhance STP with Root Guard,” Document ID 10588, updated 15 June 2026. Available at: <https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10588-74.html> (Accessed during Phase 10 testing, 3–6 October 2026).

[2] Cisco, “Understanding and Troubleshooting the Autostate Feature in Catalyst Switches,” Document ID 41141, updated 6 May 2005. Available at: <https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/41141-188.html> (Accessed during Phase 10 testing, 3–6 October 2026).

[3] Cisco, “Use HSRP Preempt and Track Commands,” Document ID 13780, updated 6 August 2026. Available at: <https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/13780-6.html> (Accessed during Phase 10 testing, 3–6 October 2026).

---

[← Phase 10 Test Plan](phase-10-test-plan.md) · [↑ Phase 10 Evidence Index](../../../evidence/hq/failure-tests/README.md) · [HQ implementation](README.md)
