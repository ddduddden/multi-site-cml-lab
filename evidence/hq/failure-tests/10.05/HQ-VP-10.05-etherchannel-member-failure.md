[Phase 10](../README.md) / [10.05](etherchannel-member-failure-evidence.md)

[← Previous](etherchannel-member-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](etherchannel-member-failure-evidence.md) · [Next →](10.05-hq-a1-event-log-recovered-from-later-buffer.md)

---

HQ-VP-10.05 — EtherChannel Member Failure
=========================================

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](etherchannel-member-failure-evidence.md)

Member selection
----------------
Po20 member pairs:

- hq-a1 Gi1/0 <-> hq-d2 Gi0/0.
- hq-a1 Gi1/1 <-> hq-d2 Gi0/1.

During sample traffic, hq-d2 Gi0/0 showed the larger counter increase:

- Gi0/0: +118.
- Gi0/1: +17.

The Gi1/0 <-> Gi0/0 pair was selected for the test.

First run — one-sided shutdown
------------------------------
The selected member was first shut on hq-d2 Gi0/0 only.

- Ping (target not recorded): 0/20 replies.
- SLA101: Timeout, 49 successes / 177 failures.
- SLA102: OK, 230 successes / 0 failures.
- A later hq-r2 check to hq-a1 management address 10.10.99.4 was still 0/5.
- The member at the other end did not drop straight away.
- LACP later suspended it after LACP messages stopped arriving.
- The log recorded `%EC-5-L3DONTBNDL2`.

Outcome: FINDING. The one-sided shutdown produced sustained asymmetric failure
behaviour rather than a clean physical-link loss. The bilateral rerun below was
therefore used for the intended link-loss check.

Bilateral rerun
---------------
The same member pair was then removed at both ends.

- Po20 stayed up and in use.
- The failed physical member was down.
- The other physical member stayed bundled in Po20.
- Port-channel20 stayed up/up.
- Ping (target not recorded): 20/20 replies.
- SLA101: 80 successes / 5 failures, latest result OK.
- SLA102: 82 successes / 5 failures, latest result OK.

No pre-rerun SLA reading was retained, so those five failed samples on each
probe cannot be attributed solely to the bilateral shutdown.

Recovery
--------
After both interfaces were restored, both members rejoined Po20.

Result
------
PASS. Po20 stayed operational on one member during the bilateral link failure.
The one-sided run is kept separately because it showed a different LACP
failure-detection behaviour.

---

[← Previous](etherchannel-member-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](etherchannel-member-failure-evidence.md) · [Next →](10.05-hq-a1-event-log-recovered-from-later-buffer.md)
