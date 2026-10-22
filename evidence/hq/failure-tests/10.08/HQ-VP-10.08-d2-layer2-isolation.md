[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.08](README.md) / Test report

# HQ-VP-10.08 — hq-d2 Layer-2 Isolation

Phase 10 — Failure and Resilience Testing

**Evidence commit:** [`a8624b1`](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)
Evidence: [captured CLI and session records](README.md)
Related troubleshooting: [HQ-TS-002](../../../../docs/implementation/hq/troubleshooting.md#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation)

Test setup
----------
VLAN160 (FACILITIES) was used for the test.

- Subnet: 10.10.60.0/26.
- HSRP virtual IP address (VIP): 10.10.60.1.
- hq-d1: 10.10.60.2.
- hq-d2: 10.10.60.3.
- Temporary hq-a1 address: 10.10.60.4.

Temporary-address availability check
------------------------------------
Before assigning 10.10.60.4/26 to hq-a1:

- 10.10.60.4: 0/3 replies.
- ARP remained incomplete.

During setup, the temporary VLAN160 test configuration was first entered on
hq-d2 instead of hq-a1. This temporarily removed hq-d2 Vlan130 and changed
Vlan160 from 10.10.60.3 to 10.10.60.4. hq-d2 was restored before the failure
test started.

After the test source moved to hq-a1, SLA101 recorded one startup failed sample.
The probes were recreated once the path had settled.

Clean baseline:

- SLA101: 146 successful probes / 0 failures.
- SLA102: 147 successful probes / 0 failures.

Before the failure
------------------
- Po20 and Po30 were up on hq-d2.
- hq-d2 Vlan160 was up/up.
- hq-d2 was HSRP Active.
- hq-d1 was HSRP Standby.
- hq-d2 had five OSPF neighbours in Full state.
- hq-a1 used Po20 as the root path, with Po10 as the alternate path.

Reachability from hq-a1:

- VIP: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.

Failure
-------
Po20 and Po30 were shut on hq-d2. The five routed links were deliberately left
up.

After the shutdown:

- hq-a1 moved to Po10 through hq-d1.
- hq-d2 Vlan160 still showed up/up.
- hq-d2 stayed locally HSRP Active but could no longer see its peer.
- hq-d1 also became locally Active because it could no longer see hq-d2.
- hq-d2 still had all five OSPF neighbours in Full state.

Layer 2 had failed on hq-d2, but from the routed side it still looked healthy.

OSPF and the return path
------------------------
Because Vlan160 stayed up/up on hq-d2:

- 10.10.60.0/26 stayed in the connected routing table.
- hq-d2 continued advertising the subnet into OSPF.
- hq-r2 kept four metric-11 paths through hq-d2.
- The checked CEF return flow to 10.10.60.4 still selected hq-d2.

The later recovery capture shows the hq-r2 route entries had already been
present for hours, so they were not withdrawn and relearned during this test.

Extra checks on hq-d2 showed:

- no active campus trunks;
- no STP instance for VLAN160;
- VLAN160 active with no member ports;
- Vlan160 still up/up.

So this was not just STP taking time to settle. IOSvL2 kept the SVI and
connected
route up even though hq-d2 had no working Layer-2 path back into the VLAN.

Traffic result
--------------
From hq-a1 at 10.10.60.4:

- VIP 10.10.60.1: 5/5 replies.
- hq-d1 SVI 10.10.60.2: 5/5 replies.
- hq-d2 SVI 10.10.60.3: 0/5 replies.
- hq-r2 Loopback0 10.255.10.130: 0/5 replies.
- hq-r1 Loopback0 10.255.10.129: 5/5 replies.

SLA101 went into Timeout.

SLA102 returned to OK, but was not without loss. It recorded 9 failed samples
during the failure window.

Why hq-r2 failed
----------------
Traffic from hq-a1 could leave through hq-d1.

The reply from hq-r2 still followed the route through hq-d2. It reached hq-d2,
but hq-d2 no longer had a usable Layer-2 path back to 10.10.60.4.

The result was a return-path blackhole:

hq-a1 -> hq-d1 -> routed network -> hq-r2
hq-r2 -> hq-d2 -> no Layer-2 path back to hq-a1

OSPF was following the route hq-d2 was still advertising. The unusual part was
IOSvL2 keeping the SVI and connected route up after the Layer-2 paths were gone.

Recovery
--------
Po20 and Po30 were restored on hq-d2.

After recovery:

- both Port-Channels were back up;
- Po30 had all four links bundled again;
- hq-d2 returned to HSRP Active and hq-d1 to Standby;
- STP showed no inconsistent ports;
- hq-d2 still had five OSPF neighbours in Full state;
- hq-a1 returned to Po20 as the root path.

IP SLA before recovery:

- SLA101: 186 successes / 2626 failures / Timeout.
- SLA102: 2805 successes / 9 failures / OK.

After recovery:

- SLA101: 445 successes / 2687 failures / OK.
- SLA102: 3117 successes / 15 failures / OK.

SLA102 added another 6 failed samples during recovery.

Reachability was restored:

- VIP: 5/5 replies.
- hq-d2 SVI: 5/5 replies.
- hq-r2 Loopback0: 5/5 replies.
- hq-r1 Loopback0: 5/5 replies.

One reply to the hq-d2 SVI was much slower than the others
(min/avg/max 3/204/1006 ms). No cause was proved.

Result
------
FAIL. The VLAN160 gateway failed over to hq-d1, but traffic to hq-r2 was
blackholed on the return path. The expected SVI withdrawal and working return
path were not demonstrated.

hq-d2's VLAN160 SVI and connected route stayed up, so the subnet continued to
be advertised into OSPF even though hq-d2 no longer had a usable Layer-2 path
back to the test host.

Platform note: Cisco documents normal Catalyst SVI autostate as requiring at
least one Layer-2 port in the VLAN to be up and forwarding. The feature is
intended to stop routing protocols using an SVI that cannot forward at Layer 2
and to avoid routing black holes. The up/up SVI seen here is therefore kept as
IOSvL2/CML behaviour observed in this lab, not a general Catalyst expectation.

---

[◀ Evidence index](README.md) · [↑ Test evidence](README.md) · [Next record ▶](10.08-session-record.md)
