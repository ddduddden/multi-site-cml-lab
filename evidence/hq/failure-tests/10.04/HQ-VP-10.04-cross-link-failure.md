[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.04](README.md) / Test report

# <a href="../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1004-cross-link-loss-and-higher-cost-alternate" title="Previous: 10.04 test plan" aria-label="Previous: 10.04 test plan"><img src="../../../../diagrams/orange-previous.svg" alt="" width="30" height="26"></a> HQ-VP-10.04 — Cross-Link Failure <a href="../../../../docs/implementation/hq/phase-10-engineering-review.md#routed-paths--hq-vp-10021004" title="Next: 10.04 engineering review" aria-label="Next: 10.04 engineering review"><img src="../../../../diagrams/orange-next.svg" alt="" width="30" height="26"></a>

**🟧 WORKED EXAMPLE · 02/06**


Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [HQ-VP-10.04 — Cross-link loss and higher-cost alternate](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1004-cross-link-loss-and-higher-cost-alternate)\
**Evidence:** [Failure CLI](10.04-failure.md) · [Recovery CLI](10.04-recovery.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that the OSPF cost design provides a working alternative if the direct cross-link between hq-d2 and hq-r1 fails.

The normal route to hq-r1 Loopback0 (10.255.10.129) was designed with metric 101. Removing that connection should force traffic through hq-r2 and hq-d1, increasing the metric to 121. Restoring the cross-link should return the preferred route.

The original acceptance criteria required the alternate route, selected next hops, successful settled-state traffic and full restoration of the preferred route and OSPF adjacency.

## Cross-link failure

I shut down hq-r1 Gi0/4, which connects to hq-d2 Gi3/0.

On hq-r1, the interface became administratively down/down and the OSPF adjacency to hq-d2 disappeared. The remaining four adjacencies to hq-d1 stayed FULL.

Although hq-d2 Gi3/0 continued reporting up/up in CML after the far-end shutdown, the OSPF neighbour adjacency was absent from the neighbour table. This suggests a CML link-state reporting artefact; the control-plane evidence confirmed the lost cross-link adjacency, while all four adjacencies to hq-r2 remained FULL.

Following OSPF convergence, the routing table reflected the expected path change.

## Alternative route and ECMP

hq-d2 installed an intra-area OSPF route to 10.255.10.129/32 with metric 121, using four equal-cost next hops towards hq-r2.

| Next hop | Interface |
| --- | --- |
| 10.255.10.3 | Gi2/0 |
| 10.255.10.15 | Gi2/1 |
| 10.255.10.17 | Gi2/2 |
| 10.255.10.19 | Gi2/3 |

The CEF output confirmed the same four next hops.

On hq-r2, the route to hq-r1 Loopback0 had metric 111, with next hop 10.255.10.4 through Gi0/4 towards hq-d1. Its CEF entry agreed.

Together, the routing and forwarding records support the alternative path:

**hq-d2 → hq-r2 → hq-d1 → hq-r1**

The four equal-cost links provide ECMP between hq-d2 and hq-r2, while the surviving cross-link from hq-r2 to hq-d1 provides the continuation towards hq-r1.

This confirmed that the higher-cost alternative had been installed as intended, rather than leaving the destination unreachable.

## Traffic verification

I monitored the existing IP SLA probes from hq-a1, particularly SLA102 towards hq-r1 Loopback0.

| Capture | SLA102 successes | SLA102 failures | Latest result |
| --- | ---: | ---: | --- |
| Previous 10.02–10.03 recovery | 1,273 | 0 | OK |
| 10.04 failure state | 2,000 | 5 | OK |
| 10.04 recovery | 2,252 | 5 | OK |

Five failed samples were present at the failure-state capture, but SLA102 had already returned to OK. The count remained unchanged in the recovery capture, with no additional failures recorded between those readings.

SLA101, monitoring hq-r2, retained its previous six failures across these readings.

These counters support successful probing after the route change, although the transition was not demonstrated to be loss-free. The counters are cumulative, and the zero-failure reading came from the preceding test rather than an immediate 10.04 baseline. They cannot establish an exact convergence time or attribute every failed sample solely to this shutdown.

## Restoration

I restored hq-r1 Gi0/4 with no shutdown.

The interface returned to up/up, and the OSPF adjacency between hq-r1 and hq-d2 returned to FULL. Both devices again showed their expected five OSPF neighbour entries.

On hq-d2, the route to 10.255.10.129/32 returned to:

- OSPF metric: 101
- Next hop: 10.255.10.7
- Outgoing interface: Gi3/0

CEF confirmed the same direct next hop, replacing the four metric-121 alternatives.

## Result and engineering assessment

**PASS.** The failure produced the expected higher-cost OSPF alternative, with four equal-cost next hops through hq-r2 and a surviving continuation through hq-d1. The retained probes showed successful reachability after the routing change, and restoring the cross-link returned the preferred metric-101 route and FULL adjacency.

The routing and CEF captures confirmed that the Phase 09 cost engineering worked as intended. The higher-cost alternatives were available when the direct cross-link failed, and the preferred route returned after restoration.

---

🟧 **NEXT STEP —** [10.04 engineering review](../../../../docs/implementation/hq/phase-10-engineering-review.md#routed-paths--hq-vp-10021004) [![Next stage](../../../../diagrams/orange-next.svg)](../../../../docs/implementation/hq/phase-10-engineering-review.md#routed-paths--hq-vp-10021004)

[◀ Test evidence](README.md) · [Failure CLI ▶](10.04-failure.md) · [Recovery CLI](10.04-recovery.md) · [Engineering Review](../../../../docs/implementation/hq/phase-10-engineering-review.md#routed-paths--hq-vp-10021004) · [↑ Phase 10 Test Index](../README.md)
