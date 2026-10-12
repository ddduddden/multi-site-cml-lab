[Phase 10](../README.md) / [10.02-10.03](routed-link-ecmp-evidence.md)

[← Previous](routed-link-ecmp-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](routed-link-ecmp-evidence.md) · [Next →](10.02-10.03-failure.md)

---

# [←](../10.01/HQ-VP-10.01-healthy-baseline.md "Previous VP") HQ-VP-10.02 / 10.03 — Routed Link Failure and ECMP Reduction [→](../10.04/HQ-VP-10.04-cross-link-failure.md "Next VP")

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](routed-link-ecmp-evidence.md)

Failure
-------
The tested flow originally used:

- hq-d2 Gi2/2 -> hq-r2 Gi0/2.
- Next hop 10.255.10.17.

hq-r2 Gi0/2 was shut down.

What happened
-------------
After convergence:

- The direct ECMP set reduced from four paths to three.
- CEF moved the tested flow to hq-d2 Gi2/3, next hop 10.255.10.19.
- SLA101 recorded six failed samples before returning to OK.
- SLA102 recorded no failed samples.
- hq-d2 Gi2/2 still showed up/up in this CML run after the shutdown was applied
  at the hq-r2 end.

The logs show two separate events:

- hq-r2 reported its local interface down/detached.
- hq-d2 later logged `Dead timer expired` for that neighbour.

The six one-second SLA failures show that traffic moved before the 40-second
OSPF dead timer expired. This points to the OSPF topology change reaching hq-d2
over the surviving links before the failed neighbour was finally removed.

Recovery
--------
After hq-r2 Gi0/2 was restored:

- The ECMP set returned to four paths.
- The tested flow returned to hq-d2 Gi2/2, next hop 10.255.10.17.

Result
------
PASS. One direct ECMP path was removed, the tested flow moved to a surviving
path, and the four-path set returned after recovery.

Measurement: six failed SLA probe samples; exact outage duration was not
measured.

---

[← Previous](routed-link-ecmp-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](routed-link-ecmp-evidence.md) · [Next →](10.02-10.03-failure.md)
