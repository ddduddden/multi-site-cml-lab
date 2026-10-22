[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.01](README.md) / Test report

# HQ-VP-10.01 — Healthy Baseline

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Raw CLI: [hq-a1 baseline capture](10.01-hq-a1-baseline-cli.md)

Baseline
--------
Before failure testing started:

- Po10 and Po20 were up on hq-a1 with both members bundled.
- Po30 was up between hq-d1 and hq-d2 with all four members bundled.
- STP root placement on hq-a1 matched the design.
- STP showed no inconsistent ports.
- HSRP ownership matched the design.
- hq-d1, hq-d2, hq-r1 and hq-r2 each had five OSPF neighbours in Full state.
- hq-a1 management was on VLAN199 (NET-MGMT) at 10.10.99.4/26.
- hq-a1 buffered logging was at debugging level with an 8192-byte buffer.

Reachability:

- HSRP management VIP 10.10.99.1: 5/5 replies.
- hq-r1 Loopback0 10.255.10.129: 5/5 replies.

Retention note: the 10.01 CLI capture directly preserves hq-a1 Po10/Po20,
STP root paths, management state, logging and the HSRP VIP ping. The Po30,
STP inconsistent-port, HSRP ownership, OSPF-neighbour and hq-r1 Loopback0
baseline observations above were recorded during the session, but their command
output was not retained in the 10.01 capture.

Not retained: the hq-r2 Loopback0 baseline ping capture; the check was run.

Result
------
BASELINE ESTABLISHED. Phase 10 started from the intended healthy HQ state.

---

[◀ Evidence index](README.md) · [↑ Test evidence](README.md) · [Next record ▶](10.01-hq-a1-baseline-cli.md)
