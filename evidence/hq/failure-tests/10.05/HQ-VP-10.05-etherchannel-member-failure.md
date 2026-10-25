[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.05](README.md) / Test report

# HQ-VP-10.05 — EtherChannel Member Failure

Phase 10 — Failure and Resilience Testing

**Result: PASS**

PASS applies to the bilateral member-loss rerun; the one-sided failure remains unresolved.

**Original test plan:** [HQ-VP-10.05 — Po20 member-link failure](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1005-po20-member-link-failure)\
**Evidence:** [Session record](10.05-session-record.md) · Retained event logs\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that Po20 can remain operational when one of its two member links is shut down, while recording the different behaviour observed in the one-sided attempt and the bilateral rerun.

## Member selection

Po20 connects hq-a1 to hq-d2 through two physical member pairs:

- hq-a1 Gi1/0 ↔ hq-d2 Gi0/0.
- hq-a1 Gi1/1 ↔ hq-d2 Gi0/1.

During sample traffic, the counters on hq-d2 increased by **118** on Gi0/0 and **17** on Gi0/1. I chose the busier Gi1/0–Gi0/0 pair for the member-loss test because it showed the greater increase.

## First run — one-sided shutdown

I shut hq-d2 Gi0/0 without shutting its peer on hq-a1.

- The initial ping returned 0/20 replies; its target was not recorded.
- SLA101 returned 49 successes / 177 failures, latest result Timeout.
- SLA102 returned 230 successes / 0 failures, latest result OK.
- A later ping from hq-r2 to hq-a1 management address 10.10.99.4 returned 0/5.
- The peer member on hq-a1 did not drop immediately. LACP subsequently suspended Gi1/0, with `%EC-5-L3DONTBNDL2` recorded in the retained hq-a1 log.

Further checks showed that hq-d2 could reach hq-r2 (5/5), while the routing and CEF entries on hq-r2 selected hq-d2 for the return path to 10.10.99.4. That return ping still failed (0/5).

The one-sided shutdown caused sustained connectivity loss affecting hq-r2 while hq-r1 remained reachable. The exact cause was not established, so this remains an unresolved finding; an EtherChannel hashing explanation was not proven.

## Bilateral rerun

The same member pair was subsequently shut at both ends to simulate a member-link failure.

- Po20 stayed up/in use (SU) with the surviving member bundled.
- hq-a1 Gi1/0 and hq-d2 Gi0/0 were down; Gi1/1 and Gi0/1 remained bundled.
- Port-channel20 stayed up/up.
- The retained ping returned 20/20 replies; its target was not recorded.
- SLA101 returned 80 successes / 5 failures, latest result OK.
- SLA102 returned 82 successes / 5 failures, latest result OK.

The recorded SLA totals differ from the first run, but the complete probe reset or restart sequence was not retained. There was also no immediately preceding baseline for the rerun, so its five cumulative failures on each probe cannot be attributed solely to the bilateral shutdown.

## Recovery

After restoring both physical interfaces, the retained EtherChannel summary showed both member links bundled again on hq-a1 and hq-d2 (P flags). A recovery ping returned 5/5 replies, and both SLA operations reported their latest result as OK.

## Result

**PASS.** Po20 remained operational on its surviving member during the bilateral shutdown and returned to full membership afterwards.

The first, one-sided attempt produced unresolved sustained connectivity loss. The successful bilateral rerun demonstrated EtherChannel resilience during a simulated member-link failure but did not explain the loss of connectivity to hq-r2 while hq-r1 remained reachable during the one-sided shutdown. An exact disruption time was not established.

---

[◀ Test evidence](README.md) · [Session record ▶](10.05-session-record.md) · [↑ Phase 10 Test Index](../README.md)
