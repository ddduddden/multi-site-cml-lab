[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.07](README.md) / Test report

# HQ-VP-10.07 — Po30 Progressive Failure

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [HQ-VP-10.07 — Progressive Po30 degradation and complete loss](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1007-progressive-po30-degradation-and-complete-loss)\
**Evidence:** [Session record](10.07-session-record.md) · [Event log](10.07-event-log-verbatim-extract.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)\
**Related troubleshooting:** [HQ-TS-002 — IOSvL2 SVI state](../../../../docs/implementation/hq/troubleshooting.md#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation)

## Test objective

Verify how Po30 behaves as its four physical links are progressively removed, including the effects on STP, Root Guard, HSRP and connectivity. Confirm that the normal operating state returns when the links are restored.

Po30 is the four-link EtherChannel between hq-d1 and hq-d2. I removed its members in stages, from four links down to zero, before restoring them one at a time.

## Healthy baseline

VLAN130 (SERVERS) was used for the test with a temporary address of 10.10.30.4/25 on hq-a1.

Before assigning the address, I checked its availability. The ping returned 0/3 replies and there was no ARP entry.

The initial IP SLA readings were:

- SLA101: 30 successful probes / 0 failures.
- SLA102: 35 successful probes / 0 failures.

## Progressive Po30 failure

### Four to three links

I shut Gi1/3 at both ends of Po30.

Po30 stayed up with three members bundled. STP showed no inconsistent ports, and neither SLA probe recorded a failure.

### Three to two links

I shut Gi1/2 next.

Po30 remained up with two members bundled, and STP still showed no inconsistent ports.

- SLA101: 4 failed samples.
- SLA102: 0 failed samples.

A return-path check from hq-r2 to 10.10.30.4 selected Gi0/3, with next hop 10.255.10.18. This supported the checked return flow passing through hq-d2 and Po30.

### Two to one link

I shut Gi1/1, leaving Gi1/0 as the only Po30 member.

Po30 stayed up, but its STP cost increased from 3 to 4. For VLAN130, hq-d2 still reached the root through Po30 at cost 4. hq-a1 already had a cost of 3 through hq-d1, so hq-a1 Po20 became the designated port and sent hq-d2 a superior BPDU.

Root Guard placed hq-d2 Po20 and hq-d1 Po10 into root-inconsistent state for the VLANs rooted on the opposite distribution switch.

At this stage, SLA101 had 11 cumulative failed samples while SLA102 still had none.

The logs also showed a brief HSRP state change on Vlan160. The event is retained in the raw evidence, but its cause was not established.

### One to zero links

I removed the final Po30 member, Gi1/0.

The resulting state showed:

- Po30 down, with all four members down.
- Root Guard still blocking the access-facing path between the distribution switches.
- VLAN120 and VLAN130 SVIs still reporting up/up in IOSvL2.
- HSRP peer communication lost, with both distribution switches locally Active for affected groups because they could no longer see each other.

VLAN130 checks from hq-a1 confirmed the split:

- hq-d1 SVI 10.10.30.2: 5/5 replies.
- hq-d2 SVI 10.10.30.3: 0/5 replies.
- SLA101: latest result Timeout.
- SLA102: latest result OK.

Although hq-a1 still had links to both distribution switches, Root Guard prevented it from becoming an unintended Layer 2 transit path when Po30 was lost. The two sides therefore remained separated at Layer 2.

The SLA101 failure was consistent with the return-path blackhole demonstrated in [10.08](../10.08/HQ-VP-10.08-d2-layer2-isolation.md), although hq-r2's VLAN130 route was not captured at the zero-link checkpoint in 10.07.

## Recovery

I restored the Po30 members one at a time.

With the first link back, Po30 formed again and the HSRP peers could see each other. Root Guard remained active because the one-link Po30 cost was still 4. SLA101 added 55 failed samples between the last zero-link check and the first check after restoration began.

The second link brought Po30's STP cost back to 3. Root Guard cleared and normal STP roles returned, although SLA101 had accumulated another 6 failed samples. The logs also recorded a brief HSRP state change on Vlan199 around this point; its cause was not established.

Restoring the third link added another 6 failed SLA101 samples.

With all four links restored:

- Po30 had all four members bundled.
- STP showed no inconsistent ports.
- Normal VLAN120 and VLAN130 root paths returned.
- SLA101: 159 successful probes / 0 failures.
- SLA102: 159 successful probes / 0 failures.

The SLA counters appeared to reset during the long test. The session notes attribute this to an hourly statistics-bucket rollover rather than a device restart, although the supporting rollover CLI was not retained.

## Result

**PASS.** Po30 remained operational with three, two and one physical link bundled. As the bundle reduced to one member, the higher STP cost triggered Root Guard on the affected access-facing ports. When Po30 was completely lost, Root Guard prevented hq-a1 from becoming an unintended transit path between the distribution switches.

The complete outage also separated the HSRP peers, left both distribution switches locally Active for affected groups and caused SLA101 to time out. The PASS confirms the observed EtherChannel and Root Guard behaviour, not uninterrupted routed connectivity throughout the test.

Restoring Po30 brought back its four bundled links, the expected STP roles and successful SLA readings.

The test also confirmed that Po30 is the only direct Layer 2 connection between hq-d1 and hq-d2.

---

[◀ Test evidence](README.md) · [Session record ▶](10.07-session-record.md) · [Event log](10.07-event-log-verbatim-extract.md)
