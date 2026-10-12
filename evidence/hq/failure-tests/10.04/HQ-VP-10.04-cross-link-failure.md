[Phase 10](../README.md) / [10.04](cross-link-failure-evidence.md)

[← Previous](cross-link-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](cross-link-failure-evidence.md) · [Next →](10.04-failure.md)

---

# [←](../10.02-10.03/HQ-VP-10.02-10.03-routed-link-ecmp.md "Previous VP") HQ-VP-10.04 — Cross-Link Failure [→](../10.05/HQ-VP-10.05-etherchannel-member-failure.md "Next VP")

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](cross-link-failure-evidence.md)

Failure
-------

Before the failure, hq-d2 reached hq-r1 Loopback0 through the direct cross-link:

- Metric 101.
- Next hop 10.255.10.7.
- Outgoing interface Gi3/0.

hq-r1 Gi0/4 was shut down.

What happened
-------------

After convergence:

- hq-d2's route changed from metric 101 to metric 121.
- hq-r2's route showed the surviving continuation through hq-d1.
- The route tables show the surviving path as:
  hq-d2 -> hq-r2 -> hq-d1 -> hq-r1.
- SLA102 recorded five failed samples before returning to OK.
- hq-d2 Gi3/0 still showed up/up in this CML run after the shutdown was applied
  at the hq-r1 end.

The cross-link was the normal route from hq-d2 to
hq-r1 Loopback0. Losing it forced the longer route through hq-r2 and hq-d1.

Recovery
--------

Restoring hq-r1 Gi0/4 returned the direct metric-101 route.

Result
------

PASS. OSPF moved to the higher-cost alternate route when the direct cross-link
was lost, then returned to the lower-cost route after recovery.

---

[← Previous](cross-link-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](cross-link-failure-evidence.md) · [Next →](10.04-failure.md)
