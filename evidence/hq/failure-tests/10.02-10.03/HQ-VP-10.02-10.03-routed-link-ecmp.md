[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.02-10.03](README.md) / Test report

# HQ-VP-10.02 / 10.03 — Routed Link Failure and ECMP Reduction

<a href="../README.md" title="Previous: Stop 4 · Recorded results" aria-label="Previous: Stop 4 · Recorded results"><img src="../../../../diagrams/orange-previous.svg" alt="" width="30" height="26"></a> **🟧 10-MINUTE ROUTE · EXPLORE THE EVIDENCE · 05/07** <a href="10.02-10.03-failure.md" title="Next: Stop 5 continued · Original CLI" aria-label="Next: Stop 5 continued · Original CLI"><img src="../../../../diagrams/orange-next.svg" alt="" width="30" height="26"></a>

*A real test report* · **Just over a minute** | The first routed failure test checks a prediction from Stop 1: lose one direct link, lose one next hop, keep the destination. Read *Routed-link failure* and *Result*. The CLI comes next.

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plans:** [HQ-VP-10.02 — Routed-link failure](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1002-single-routed-link-loss-and-ecmp-reduction) · [HQ-VP-10.03 — Failure detection](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1003-routed-link-failure-detection)\
**Evidence:** [Failure and recovery CLI](README.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that losing one of the four direct routed links between hq-d2 and hq-r2 reduces the available ECMP paths without losing connectivity.

HQ-VP-10.03 used the same shutdown to examine OSPF neighbour detection and recovery, rather than introducing a separate failure.

## Routed-link failure

The test targeted the connection between hq-d2 Gi2/2 and hq-r2 Gi0/2, with next hop 10.255.10.17.

I shut hq-r2 Gi0/2. The resulting state showed:

- The OSPF route on hq-d2 retained metric 11.
- The installed ECMP set reduced from four next hops to three.
- `show ip cef exact-route` selected the surviving hq-d2 Gi2/3 connection, next hop 10.255.10.19, for traffic from 10.10.99.4 to hq-r2 Loopback0.
- SLA101, monitoring that source and destination, recorded six cumulative failed samples and a latest result of OK.
- SLA102 recorded zero failures.

The remaining three routed links provided the expected alternate forwarding paths.

## OSPF failure detection

The shutdown exposed different interface and neighbour behaviour at the two ends.

On hq-r2, Gi0/2 became administratively down/down. Its log recorded the adjacency leaving FULL because the interface went down.

On hq-d2, Gi2/2 continued reporting up/up in CML, although the affected OSPF adjacency was absent from the settled neighbour table.

The hq-d2 log also recorded an OSPF dead-timer expiry. Clock synchronisation between the devices was not established, so the timestamps could not reliably place that event relative to the hq-r2 shutdown.

## Recovery

The recovery captures confirmed:

- The adjacency returned to FULL at both ends.
- Routing and CEF returned to four equal-cost next hops.
- `show ip cef exact-route` selected hq-d2 Gi2/2, next hop 10.255.10.17, for the tested source and destination.
- Both IP SLA probes reported OK, with no increase in their recorded failure counts.

## Result

**PASS.** The routed-link failure reduced the ECMP set from four paths to three, with CEF selecting a surviving next hop. The original four-path set and OSPF adjacency were restored.

The six cumulative SLA101 failures were retained, but no immediate pre-shutdown counter reading was captured to attribute every failed sample to this fault. The evidence also does not establish an exact outage or convergence time.

Both tests met their recorded routing and neighbour-state acceptance criteria without requiring separate fault injections.

---

🟧 **NEXT STEP —** [Stop 5 continued · Original CLI](10.02-10.03-failure.md) [![Next stop](../../../../diagrams/orange-next.svg)](10.02-10.03-failure.md)

[◀ Test evidence](README.md) · [Failure CLI ▶](10.02-10.03-failure.md) · [Recovery CLI](10.02-10.03-recovery.md) · [↑ Phase 10 Test Index](../README.md)
