[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.06](README.md) / Test report

# HQ-VP-10.06 — Access Uplink Failure

Phase 10 — Failure and Resilience Testing

**Result: PASS**

**Original test plan:** [HQ-VP-10.06 — Access Port-Channel outage](../../../../docs/implementation/hq/phase-10-test-plan.md#hq-vp-1006-access-port-channel-outage)\
**Evidence:** [CLI captures and original source records](README.md)\
**Evidence commit:** [a8624b1](https://github.com/ddduddden/multi-site-cml-lab/commit/a8624b176298e3b0132daedf082c2aae0c704ebd)

## Test objective

Verify that hq-a1 can retain access to its intended HSRP gateway after losing either distribution uplink.

Po10 connects hq-a1 to hq-d1, while Po20 connects it to hq-d2. I had aligned the Rapid PVST+ root placement with the preferred HSRP Active gateway for each VLAN group.

The test covered VLAN199, which prefers hq-d2, and VLAN112, which prefers hq-d1. I expected STP to select the surviving uplink while the original Active gateway remained reachable through the other distribution switch and Po30.

## Mode A — VLAN199 (NET-MGMT)

### Po20 failure

I shut Po20, the preferred access uplink for VLAN199.

The EtherChannel summary confirmed Po20 was down while Po10 remained operational. Rapid PVST+ moved the VLAN199 root-port role to Po10, increasing the root-path cost from 3 to 6.

Both distribution switches retained their original HSRP roles. hq-d2 remained Active for VLAN199, so traffic reached the same gateway over Po10 and Po30 rather than requiring an HSRP takeover.

Connectivity after convergence was successful:

- VLAN199 gateway 10.10.99.1: 5/5 replies.
- hq-r2 Loopback0 (10.255.10.130): 20/20 replies.
- Both IP SLA probes reported their latest result as OK.

The cumulative SLA counters do not establish whether any packets were lost during the transition.

I restored Po20 before continuing. The retained interface log confirms its return to service.

### Po10 failure — alternate uplink test

With VLAN199 back on its preferred Po20 path, I shut Po10 to check that losing the alternate uplink would not disturb forwarding.

The capture confirmed:

- Po10 was down while Po20 remained operational.
- Po20 retained the VLAN199 STP root-port role with a root-path cost of 3.
- The gateway responded to 5/5 pings.
- hq-r2 Loopback0 responded to 20/20 sourced pings.
- SLA101 and SLA102 each remained at 12 cumulative failures, with no increase during the control.

Po10 was then restored. Both Port-Channels returned to their operational state before the VLAN112 test.

## Mode B — VLAN112 (CORP-USERS)

For the second test, I changed the source VLAN to exercise the opposite gateway preference.

Before assigning 10.10.12.4/22 to hq-a1, I checked the address from hq-d1. The ping returned 0/3 replies and ARP remained incomplete.

I configured the temporary VLAN112 SVI, changed the default gateway to 10.10.12.1 and recreated IP SLA operations 101 and 102 using VLAN112 as their source.

The baseline confirmed Po10 as the VLAN112 STP root port with a root-path cost of 3. The gateway and both edge-router loopbacks were reachable.

I then shut Po10. The resulting state showed:

- Po10 down and Po20 operational.
- VLAN112 selecting Po20 as its STP root port.
- Root-path cost increasing from 3 to 6.
- hq-d1 remaining HSRP Active for VLAN112.

The traffic checks confirmed the surviving path was usable.

| Check | Recorded result |
| --- | --- |
| Gateway 10.10.12.1 | 5/5 replies |
| hq-r1 Loopback0 (10.255.10.129) | 20/20 replies |
| SLA101 — hq-r2 | 302 successes, 0 failures |
| SLA102 — hq-r1 | 311 successes, 0 failures |

Both IP SLA probes were running before Po10 was shut. Neither recorded a failed sample across the monitored transition, although brief loss between samples cannot be ruled out.

This demonstrated that VLAN112 could reach its preferred gateway through Po20 and Po30 without requiring an HSRP takeover.

## Restoration

I restored Po10 and removed the temporary VLAN112 SVI, its gateway setting and both test IP SLA operations. The original VLAN199 probes were not reinstated as part of this cleanup.

The final checks confirmed:

- Po10 and Po20 operational, with both members bundled.
- VLAN112 using Po10 and VLAN199 using Po20 as their root ports.
- Both VLANs restored to their normal root-path cost of 3.
- The intended HSRP Active and Standby roles restored.
- No STP inconsistent ports.
- hq-a1 returned to VLAN199 management with gateway 10.10.99.1.

The restored gateway and both edge-router loopbacks each responded to 5/5 sourced pings.

## Result

**PASS.** Both access uplink failures demonstrated successful forwarding over the surviving Layer 2 path, with the intended HSRP gateway remaining Active. The Po10 no-impact control also behaved as expected.

The important distinction was that an STP path change did not require an HSRP gateway failover. Traffic could reach the same Active gateway through the other distribution switch and Po30.

The retained pings and SLA checks support connectivity under the tested failure conditions, including zero failed samples across the monitored Mode B transition. They do not establish an exact convergence time or prove that every transition was loss-free. Packet loss during the final Po10 restoration was not measured.

Within those limits, the test demonstrated that either access Port-Channel could be removed while retaining the tested gateway and routed connectivity.

---

[◀ Test evidence](README.md) · [Mode A Po20 failure ▶](HQ-VP-10.06-mode-a-po20-access-uplink-failure.md) · [Po10 control](HQ-VP-10.06-mode-a-po10-no-impact-control.md) · [Mode B evidence](HQ-VP-10.06-mode-b-vlan112-setup-baseline.md) · [Recovery](HQ-VP-10.06-final-recovery-restored-baseline.md)
