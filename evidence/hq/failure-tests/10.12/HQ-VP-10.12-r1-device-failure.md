[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.12](README.md) / Test report

# HQ-VP-10.12 — hq-r1 Device Failure

Phase 10 — Failure and Resilience Testing

**Result: INCONCLUSIVE**

**Original test plan:** [HQ-VP-10.12 — hq-r1 device outage](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1012-hq-r1-device-outage)\
**Evidence:** [Retained CLI excerpt](10.12-retained-cli-excerpt.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that hq-r2 remains available when hq-r1 fails and determine whether the retained evidence demonstrates traffic moving to a surviving routed path.

The original plan called for a VLAN112 test source and a monitored flow confirmed to use hq-r1 before the failure. The retained test instead used VLAN199 (10.10.99.4) to check connectivity to both edge-router loopbacks.

## Healthy baseline

Before the failure, both loopbacks responded to 5/5 sourced pings from hq-a1.

The OSPF neighbour checks confirmed four direct adjacencies between hq-d1 and hq-r1, four between hq-d2 and hq-r2, and the two cross-link adjacencies.

## Device failure

I stopped hq-r1 in CML and checked the network after convergence.

- hq-r1 Loopback0 (10.255.10.129): **0/5 replies**, with ICMP unreachable responses.
- hq-r2 Loopback0 (10.255.10.130): **5/5 replies**.
- hq-d1 retained its FULL OSPF adjacency to hq-r2 over the cross-link.
- hq-d2 retained all four direct OSPF adjacencies to hq-r2.
- hq-d1 lost its four adjacencies to hq-r1, and hq-d2 lost its cross-link adjacency to hq-r1.

These checks confirmed that hq-r2 remained reachable while hq-r1 was unavailable. VLAN199 traffic reached hq-r2 through the surviving direct links from hq-d2, while the failed router's own loopback was no longer available. Neither check demonstrated a live flow switching from hq-r1 to hq-r2.

## Recovery

I restarted hq-r1 and checked connectivity as the network recovered.

Two early recovery checks to hq-r1 Loopback0 each returned 0/5 replies while the router was coming back. Once it had finished booting and OSPF had converged:

- hq-r1 Loopback0: **5/5 replies**, confirmed by an immediate repeat.
- hq-r2 Loopback0: **5/5 replies**.
- hq-r1 restored all five OSPF adjacencies to FULL.
- Its routed interfaces and Loopback0 returned to up/up.

## Result

**INCONCLUSIVE.** hq-r2 remained reachable throughout the recorded failure-state checks, and hq-r1 recovered its connectivity and OSPF neighbours after restarting.

However, the planned live-flow failover was not performed. Without a confirmed pre-failure forwarding path and the same flow tested after the failure, I cannot claim that traffic successfully moved from hq-r1 to hq-r2.

The retained evidence supports surviving-router reachability and successful restoration, but not the full original failover objective.

---

[◀ Test evidence](README.md) · [Retained CLI ▶](10.12-retained-cli-excerpt.md)
