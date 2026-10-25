[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.08](README.md) / Test report

# HQ-VP-10.08 — hq-d2 Layer-2 Isolation

**🟧 FOLLOW THE EVIDENCE · 05/06**

[![Orange previous arrow](../../../../diagrams/orange-previous.svg)](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1008-distribution-layer-2-isolation) [Previous · 10.08 test plan](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1008-distribution-layer-2-isolation) &emsp; [Next · 10.08 session investigation](10.08-session-record.md) [![Orange next arrow](../../../../diagrams/orange-next.svg)](10.08-session-record.md)


Phase 10 — Failure and Resilience Testing

**Result: FAIL**

**Original test plan:** [HQ-VP-10.08 — Distribution Layer 2 isolation](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1008-distribution-layer-2-isolation)\
**Evidence:** [Session record](10.08-session-record.md) · [Recovery CLI](10.08-original-recovery-cli.md) · [Original event buffer](10.08-original-event-buffer.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)\
**Related troubleshooting:** [HQ-TS-002 — IOSvL2 SVI state](../../../../docs/implementation/hq/troubleshooting.md#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation)

## Test objective

Verify how hq-d2 behaves when it loses both campus Layer 2 connections but keeps its routed uplinks. The test checks whether the VLAN gateway, SVI and OSPF routing state reflect the isolation, and whether traffic still has a working return path.

VLAN160 (FACILITIES) was used because hq-d2 is its preferred HSRP Active gateway. The test source was hq-a1 at 10.10.60.4/26, with virtual gateway 10.10.60.1. The distribution SVI addresses were 10.10.60.2 on hq-d1 and 10.10.60.3 on hq-d2.

## Healthy baseline

Before assigning 10.10.60.4/26 to hq-a1, I checked the address. The ping returned 0/3 replies and ARP remained incomplete.

During setup, I corrected an unintended configuration change on hq-d2 before starting the failure test.

After moving the test source to hq-a1, SLA101 recorded one startup failed sample. I recreated the probes once the path had settled, giving a clean baseline:

- SLA101: 146 successful probes / 0 failures.
- SLA102: 147 successful probes / 0 failures.

The baseline checks confirmed:

- Po20 and Po30 operational on hq-d2, with Vlan160 up/up.
- hq-d2 HSRP Active and hq-d1 Standby for VLAN160.
- Five FULL OSPF adjacencies on hq-d2.
- hq-a1 using Po20 as its STP root port, with Po10 as the alternate.
- VLAN160 gateway and both edge-router loopbacks reachable from hq-a1, each with 5/5 replies.

## Layer 2 isolation

I shut Po20 and Po30 on hq-d2, leaving all five routed uplinks operational.

After the shutdown:

- hq-a1 moved to Po10 through hq-d1.
- hq-d2 Vlan160 continued reporting up/up.
- hq-d2 remained locally HSRP Active, while hq-d1 also became locally Active because the peers could no longer see each other.
- hq-d2 retained all five FULL OSPF adjacencies.

The Layer 2 connections were gone, but hq-d2 still appeared healthy from the routed side.

### OSPF and the return path

Because Vlan160 stayed up/up on hq-d2, 10.10.60.0/26 remained in its connected routing table and continued to be advertised into OSPF. hq-r2 retained four metric-11 paths through hq-d2, and its checked CEF return flow towards 10.10.60.4 still selected hq-d2.

The later recovery capture showed that hq-r2's route entries had already been present for hours, rather than being withdrawn and relearned during this test.

Further checks on hq-d2 found no active campus trunks, no STP instance for VLAN160 and no member ports in the VLAN. Despite this, Vlan160 remained up/up, keeping its connected route in the routing table and the subnet advertised through OSPF.

### Traffic verification

From hq-a1 at 10.10.60.4, the failure-state checks returned:

| Destination | Recorded result |
|---|---|
| VLAN160 gateway 10.10.60.1 | 5/5 replies |
| hq-d1 SVI 10.10.60.2 | 5/5 replies |
| hq-d2 SVI 10.10.60.3 | 0/5 replies |
| hq-r2 Loopback0 10.255.10.130 | 0/5 replies |
| hq-r1 Loopback0 10.255.10.129 | 5/5 replies |

SLA101 went into Timeout. SLA102 returned to OK, but recorded 9 failed samples during the failure window.

Traffic from hq-a1 could leave through hq-d1. Replies from hq-r2 still followed the route through hq-d2, which no longer had a usable Layer 2 path back to the test host.

**The resulting return-path blackhole:**

```text
hq-a1 → hq-d1 → routed network → hq-r2

hq-r2 → hq-d2 → no Layer 2 path back to hq-a1
```

OSPF was using the route hq-d2 continued to advertise. The unexpected behaviour was that IOSvL2 kept the SVI and connected route up after its Layer 2 connections had been removed.

## Recovery

I restored Po20 and Po30 on hq-d2. Both Port-Channels returned to service, with all four Po30 members bundled. hq-d2 returned to HSRP Active and hq-d1 to Standby, hq-a1 selected Po20 again, and STP showed no inconsistent ports. hq-d2 continued to have five FULL OSPF adjacencies.

The retained IP SLA readings were:

| Capture | SLA101 | SLA102 |
|---|---|---|
| Before recovery | 186 successes / 2,626 failures / Timeout | 2,805 successes / 9 failures / OK |
| After recovery | 445 successes / 2,687 failures / OK | 3,117 successes / 15 failures / OK |

SLA102 added another 6 failed samples during recovery.

The VLAN160 gateway, hq-d2 SVI and both edge-router loopbacks each returned 5/5 replies after restoration. One hq-d2 SVI reply was much slower than the others (min/avg/max 3/204/1006 ms), with no confirmed cause.

## Platform behaviour

Cisco documents normal Catalyst SVI autostate as requiring at least one Layer 2 port in the VLAN to be up and forwarding. This is intended to prevent routing protocols from using an SVI that cannot forward traffic. The up/up SVI in this test is therefore recorded as the IOSvL2/CML behaviour observed in the lab, not as the expected behaviour of Catalyst switches generally.

## Result

**FAIL.** The VLAN160 gateway failed over to hq-d1, but traffic to hq-r2 was blackholed on the return path. The expected SVI withdrawal and working return path were not demonstrated.

The hq-d2 VLAN160 SVI and connected route remained up, so hq-d2 continued advertising the subnet into OSPF even though it could no longer forward traffic back to the test host at Layer 2. The traffic checks captured the failure, and the recovery checks confirmed that connectivity returned.


---

**🟧 NEXT STEP — 10.08 session investigation**

[Continue to 10.08 session investigation](10.08-session-record.md) [![Orange next arrow](../../../../diagrams/orange-next.svg)](10.08-session-record.md)

[◀ Test evidence](README.md) · [Session record ▶](10.08-session-record.md) · [Recovery CLI](10.08-original-recovery-cli.md) · [Original event buffer](10.08-original-event-buffer.md) · [↑ Phase 10 Test Index](../README.md)
