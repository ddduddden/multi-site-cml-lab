[Phase 10](../README.md) / [10.07](po30-progressive-failure-evidence.md)

[← Previous](po30-progressive-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](po30-progressive-failure-evidence.md) · [Next →](10.07-event-log-verbatim-extract.md)

---

# [←](../10.06/HQ-VP-10.06-access-uplink-failure.md "Previous VP") HQ-VP-10.07 — Po30 Progressive Failure [→](../10.08/HQ-VP-10.08-d2-layer2-isolation.md "Next VP")

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](po30-progressive-failure-evidence.md)
Related troubleshooting: HQ-TS-002

Starting state
--------------

Po30 is the four-link EtherChannel between hq-d1 and hq-d2.

VLAN130 (SERVERS) was used for the test with temporary hq-a1 address
10.10.30.4/25.

Temporary-address availability check
------------------------------------

Before assigning 10.10.30.4/25 to hq-a1:

- 10.10.30.4: 0/3 replies.
- No ARP entry was present.

Clean IP SLA baseline:

- SLA101: 30 successful probes / 0 failures.
- SLA102: 35 successful probes / 0 failures.

4 -> 3 links
------------

The Gi1/3 link was removed at both ends.

Po30 stayed up with three links bundled. STP showed no inconsistent ports and
neither SLA probe recorded a failure.

3 -> 2 links
------------

Gi1/2 was removed next.

Po30 stayed up with two links bundled and STP still showed no inconsistent
ports.

- SLA101: 4 failed samples.
- SLA102: 0 failed samples.

A return-path check from hq-r2 to 10.10.30.4 used Gi0/3 with next hop
10.255.10.18, so that checked return flow was going through hq-d2 and Po30.

2 -> 1 link
-----------

Gi1/1 was removed next, leaving Gi1/0 as the only Po30 member.

Po30 stayed up, but its STP cost changed from 3 to 4.

For VLAN130, hq-d2 still reached the root through Po30 at cost 4. hq-a1 already
had a cost of 3 through hq-d1, so hq-a1 Po20 became the designated port and sent
hq-d2 a superior BPDU.

Root Guard then put hq-d2 Po20 into root-inconsistent state for the VLANs rooted
on hq-d1. The same thing happened in the other direction on hq-d1 for the VLANs
rooted on hq-d2.

Root Guard was active on:

- hq-d2 Po20: VLANs 112, 130, 152, 170 and 190.
- hq-d1 Po10: VLANs 120, 140, 160 and 199.

At this stage:

- SLA101: 11 cumulative failed samples.
- SLA102: 0 failed samples.

The logs also show a brief HSRP state change on Vlan160 during this part of the
test. It is kept in the raw evidence, but no cause was proved.

1 -> 0 links
------------

The final Po30 member was removed.

At this point:

- Po30 was down.
- All four Po30 links were down.
- Root Guard still blocked the access-facing path between the distribution
  switches.
- VLAN120 and VLAN130 SVIs still showed up/up in IOSvL2.
- HSRP peer communication was lost.
- Both distribution switches became locally Active for affected groups because
  they could no longer see the peer.

VLAN130 checks from hq-a1:

- hq-d1 SVI 10.10.30.2: 5/5 replies.
- hq-d2 SVI 10.10.30.3: 0/5 replies.

SLA101 went into Timeout while SLA102 remained OK.

The access switch still had links to both distribution switches. With Po30 gone,
Root Guard correctly stopped hq-a1 becoming an unintended transit path between
them, so the two sides were split at Layer 2.

The SLA101 failure is consistent with the return-path blackhole proved in 10.08.
Not captured: hq-r2's VLAN130 route at the zero-link checkpoint in 10.07.

Recovery
--------

The Po30 links were restored one at a time.

With the first link back:

- Po30 came back up.
- The HSRP peers could see each other again.
- Root Guard remained because the one-link Po30 cost was still 4.
- SLA101 added 55 failed samples between the last zero-link check and the first
  check after the link returned.

With the second link back:

- Po30 cost returned to 3.
- Root Guard cleared.
- Normal STP roles returned.
- SLA101 added another 6 failed samples.

The logs also show a brief HSRP state change on Vlan199 around this point. No
cause was proved.

Restoring the third link added another 6 failed SLA101 samples.

With all four links restored:

- Po30 was back to four bundled links.
- STP showed no inconsistent ports.
- Normal VLAN120 and VLAN130 root paths were back.
- SLA101: 159 successful probes / 0 failures.
- SLA102: 159 successful probes / 0 failures.

The SLA counters appeared to reset during the long test. The session notes record
this as an hourly statistics-bucket rollover rather than a device restart; the
underlying rollover CLI was not retained.

Result
------

PASS. Po30 stayed usable with three, two and one physical link remaining.

With all Po30 members down, Root Guard correctly stopped hq-a1 becoming
an unintended transit path between the distribution switches.

Design notes
------------

Po30 gives member redundancy, but there is no second direct Layer-2 path
between hq-d1 and hq-d2 in this topology. The two sides therefore stayed
separated until Po30 was restored.

A future campus revision could add a second direct
inter-distribution Layer-2 path so the loss of one logical EtherChannel does not
remove the only direct Layer-2 connection between the distribution switches.

---

[← Previous](po30-progressive-failure-evidence.md) · [↑ Phase 10 Index](../README.md) · [Test evidence](po30-progressive-failure-evidence.md) · [Next →](10.07-event-log-verbatim-extract.md)
