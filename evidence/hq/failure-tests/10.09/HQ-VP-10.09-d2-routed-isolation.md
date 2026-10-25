[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.09](README.md) / Test report

# HQ-VP-10.09 — hq-d2 Routed Isolation

Phase 10 — Failure and Resilience Testing

**Result: PASS — Design limitation confirmed**

**Original test plan:** [HQ-VP-10.09 — Active gateway loses routed uplinks](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1009-active-gateway-loses-routed-uplinks)\
**Evidence:** [Session record](10.09-session-record.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Confirm the behaviour of an HSRP Active distribution switch when all its routed uplinks fail but its Layer 2 campus connections remain operational.

For VLAN199, hq-d2 is the preferred HSRP Active gateway. However, the HQ configuration does not include HSRP uplink or object tracking.

Without uplink or object tracking, hq-d2 was expected to remain Active even after losing its OSPF routes. The gateway would still answer locally, but it would no longer have a working path to the edge routers.

The purpose was to confirm this limitation, not to demonstrate automatic gateway failover.

## Healthy baseline

Before the failure, hq-a1 was using VLAN199 with address 10.10.99.4 and gateway 10.10.99.1.

The retained baseline confirmed:

- hq-d2 had five FULL OSPF adjacencies.
- Po20 and Po30 were operational.
- hq-d2 was HSRP Active for VLAN199.
- The gateway and both edge-router loopbacks responded to 5/5 pings.

## Routed isolation

I shut all five routed uplinks on hq-d2:

Gi2/0, Gi2/1, Gi2/2, Gi2/3 and Gi3/0.

Po20 and Po30 were deliberately left operational, preserving the campus Layer 2 connections and HSRP peer communication.

After the shutdown:

- hq-d2 had no OSPF neighbours.
- Routes to both edge-router loopbacks were absent from its routing table.
- hq-d2 remained HSRP Active for VLAN199.
- Po20 and Po30 stayed operational.

Traffic checks from hq-a1 showed the consequence.

| Destination | Recorded result |
| --- | --- |
| VLAN199 gateway 10.10.99.1 | 5/5 replies |
| hq-r1 Loopback0 (10.255.10.129) | 0/5, ICMP unreachable |
| hq-r2 Loopback0 (10.255.10.130) | 0/5, ICMP unreachable |

Meanwhile, hq-d1 remained HSRP Standby for VLAN199 and could still reach both edge-router loopbacks (5/5 each).

The network therefore had an alternative distribution switch with routed connectivity, but the access switch continued using the isolated Active gateway.

## Why the gateway did not fail over

HSRP was operating according to its configured priorities. hq-d2 remained available on the campus VLAN and continued exchanging HSRP messages, so losing OSPF connectivity did not by itself cause it to relinquish the Active role.

This exposed the difference between gateway availability and upstream reachability.

From hq-a1, the virtual gateway still responded successfully. However, hq-d2 had no routes to the remote destinations, so the local gateway could not provide the required routed service.

The design would need an upstream-health tracking mechanism to reduce hq-d2's HSRP priority when its routed connectivity failed.

With the existing priorities of 110 on hq-d2 and 100 on hq-d1, a tracking decrement greater than 10 would make hq-d1 the higher-priority switch. Preemption would also need to be enabled on hq-d1 for it to take over while the current Active switch remained operational.

This is a proposed improvement, not a configuration tested or implemented during Phase 10.

## Recovery

After restoring all five routed links:

- hq-d2 returned to five FULL OSPF adjacencies.
- hq-d2 remained HSRP Active for VLAN199.
- hq-a1 again reached the gateway and both edge-router loopbacks (5/5 each).

Normal routed connectivity was restored without changing the HSRP Active gateway.

## Result

**PASS — Design limitation confirmed.**

The test demonstrated the expected behaviour of the current configuration. hq-d2 remained HSRP Active after losing all routed connectivity, allowing local gateway communication to succeed while remote traffic failed.

This was not a successful traffic-continuity or gateway-failover result. It confirmed that the existing HSRP design does not account for upstream route availability.

The available evidence is a retained test-session record rather than a complete CLI transcript. It confirms the failure and recovery states, but does not establish a convergence time or measured transition loss.

HSRP tracking and preemption remain future design improvements requiring their own verification.

---

[◀ Test evidence](README.md) · [Session record ▶](10.09-session-record.md) · [Engineering Review](../../../../docs/implementation/hq/phase-10-engineering-review.md#upstream-isolation-and-hsrp--hq-vp-1009)
