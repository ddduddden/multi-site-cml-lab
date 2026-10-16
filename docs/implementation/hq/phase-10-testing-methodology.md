# Testing Methodology

[HQ implementation](README.md) / [Phase 10 Test Plan](phase-10-test-plan.md) / [Engineering Review](phase-10-engineering-review.md) / [Phase 10 Evidence Index](../../../evidence/hq/failure-tests/README.md)

> **Scope:** HQ Campus · Test window: 03-10-2026 to 06-10-2026 · HQ-VP-10.01–10.14  
> **Status:** Fault tests completed 03-10-2026 to 06-10-2026; final configuration reconciliation completed 12-10-2026

## Contents

- [Overview](#overview)
- [Establishing the baseline](#establishing-the-baseline)
- [Introducing a fault and checking recovery](#introducing-a-fault-and-checking-recovery)
- [How the tests progressed](#how-the-tests-progressed)
- [Checking traffic as well as protocol state](#checking-traffic-as-well-as-protocol-state)
- [Recording the results](#recording-the-results)

## Overview

Phases 01–09 established the HQ network and verified its individual features. In Phase 10 I wanted to see what happened when those features had to work together during a failure. I worked through a series of link and device outages, starting with single links and building up to the loss of whole Port-Channels and, eventually, two devices at once.

The five-node HQ campus uses two edge routers, two Multilayer Distribution Switches and one access switch. Its LACP EtherChannels, Rapid PVST+, HSRP, OSPF and ECMP paths had already been configured and tested. The question now was whether traffic would keep moving when a preferred path disappeared, what would happen when there was no suitable alternative, and whether the original paths and roles would return after recovery.

This document explains how I carried out those tests. The individual HQ-VP-10.01–10.14 reports record the results and link to the evidence kept for each test. That evidence includes captured CLI, condensed excerpts and session notes; not every command was retained as a verbatim transcript. The separate engineering review covers the findings and what I would change in the next design revision.

### Establishing the baseline

I started with HQ-VP-10.01 to record the network in its normal working state before introducing any failures. The retained baseline covers the Port-Channels and member links, spanning-tree roles, HSRP Active and Standby roles, OSPF neighbours and basic connectivity from hq-a1. I used routing and forwarding checks in the relevant later test captures, but the 10.01 CLI record does not include an installed-route capture. This gave me a starting point without pretending every check had been saved.

I kept the same five-node topology throughout the tests and saved a separate sanitised CML export for reference. CML Free’s five-node limit meant I could not add a test PC, so I used temporary VLAN SVI addresses on hq-a1 to send traffic from the subnet being tested. In the captured setups for VLAN112, VLAN160 and VLAN170, I checked the proposed address with ping and ARP before assigning it.

### Introducing a fault and checking recovery

Before each test I checked the relevant healthy path and recorded the starting protocol state. I then made the planned change: shutting an interface or Port-Channel, removing a member link, or stopping a selected device in CML. After the change, I checked the physical and logical state again and sent traffic through the remaining path. An interface showing up, or HSRP showing Active, was never enough on its own to call the test successful.

I used shutdown commands for most link and Port-Channel failures, and stopped nodes in CML for the device tests. Those were repeatable fault conditions, but not quite the same as pulling a physical cable or losing hardware. In HQ-VP-10.05, the one-ended shutdown specified in the plan caused sustained traffic loss rather than a cleanly isolated member failure; the cause was not established.

Once I had captured the failure state, I restored the component and checked the Port-Channel, STP, HSRP and routing state that was available to verify. I then tested traffic again and removed the temporary addressing and probes. The buffered-logging reset and final configuration comparisons were completed on 12-10-2026 and recorded under HQ-VP-10.14. Capturing failures before restoring them mattered because a clean recovery could otherwise hide the problem.

| Stage | What I did |
|---|---|
| Baseline | Record the normal path, protocol roles, routes and test traffic. |
| Introduce the fault | Shut the planned link or Port-Channel, or stop the selected CML device. |
| Check the response | Compare interfaces, STP, HSRP, OSPF and routes; test actual forwarding. |
| Restore | Bring the failed link or device back and watch the protocols settle. |
| Confirm the baseline | Check the intended paths and roles are back, then clear test-only changes. |

### How the tests progressed

I began with the routed failures in HQ-VP-10.02–10.04, removing individual ECMP links and then a cross-link. These tests checked whether OSPF used the remaining paths and whether the original cost-based selection returned after restoration. HQ-VP-10.05 then followed the planned one-sided shutdown of a Po20 member. It produced 0/20 replies in the retained ping and sustained SLA101 failures, with no established cause. I added a bilateral shutdown of the same member pair as a separate rerun. That demonstrated Po20 operating on the remaining link, but did not erase the first result.

For HQ-VP-10.06 I chose one VLAN from each side of the distribution design. I had split the STP root and HSRP Active roles between hq-d1 and hq-d2, so each switch was primary for one group of VLANs. That split is shown below:

**HQ VLAN gateway and root split**

| Preferred switch | Gateway/STP-root VLANs |
|---|---|
| hq-d1 | 112, 130, 152, 170 |
| hq-d2 | 120, 140, 160, 199 |

The native VLAN 190 has hq-d1 as its STP root and no HSRP gateway.

Because of that split, I ran HQ-VP-10.06 in two modes. In Mode A (VLAN199), I shut Po20 and checked that hq-a1 could still reach the gateway on hq-d2 through Po10 and Po30, with hq-d2 remaining HSRP Active. In Mode B (VLAN112), I shut Po10 and checked the path to the gateway on hq-d1 through Po20 and Po30, with hq-d1 remaining Active. For Mode B I gave hq-a1 a temporary Vlan112 address, changed its default gateway to 10.10.12.1 and moved the IP SLA probe sources to Vlan112. Both modes tested another Layer-2 path to the same Active gateway, not an HSRP takeover. The diagram’s test-source box refers to 10.06; VLAN160 and VLAN170 were used for later tests.

After the access-uplink checks, HQ-VP-10.07 took Po30 down one member at a time, from four members to none. HQ-VP-10.08 and 10.09 then tested two kinds of isolation on hq-d2: removing its Layer-2 connections while keeping routed uplinks up, and then the reverse. I compared HSRP and routing state with sourced traffic in both cases. The recorded return-route and CEF analysis belongs to 10.08; that return-path check was not captured for 10.09.

The last fault tests, HQ-VP-10.10–10.13, covered each distribution switch and one edge router, followed by hq-d1 and hq-r2 stopping in sequence. HQ-VP-10.14 demonstrated that normal forwarding was restored on 06-10-2026. The remaining configuration comparisons and logging reset were completed on 12-10-2026.

### Checking traffic as well as protocol state

I used interface and EtherChannel summaries, spanning-tree output, HSRP status, OSPF neighbour and route tables, and CEF where it helped explain a path. Alongside those checks I ran sourced pings and used the IP SLA operations on hq-a1 to probe the two edge-router loopbacks at one-second intervals during monitored tests. Comparing the routing and protocol state with the traffic checks helped explain why packets could leave the source but the replies could not get back, as in HQ-VP-10.08.

To check packet loss, I used the recorded ping totals and IP SLA success and failure counters. They show whether probes failed during the samples, but they do not give an exact outage or convergence time. HQ-VP-10.13 in particular records connectivity after the combined failure had settled, not loss during the transition. I have not added a convergence time that I did not measure.

### Recording the results

I kept the test reports separate from captured CLI, condensed excerpts, event logs and session notes. HQ-VP-10.09 and 10.13 rely on session records rather than full transcripts; 10.10–10.12 have condensed captures, and the complete first-run CLI for 10.05 was not retained. I have not recreated missing output. The less tidy results, including failed IP SLA samples and unexpected LACP behaviour, stay in the record because they are part of what happened.

Changes from the original plan need to be visible. The planned 20/20 settled-state pings were not used consistently: later device tests mainly recorded 5-packet checks, and 10.09–10.14 did not retain continuous IP SLA coverage. Instead of running every fault in both planned source modes, I tested selected VLANs across the sequence: 130, 160, 152, 140, 170 and 120, alongside VLAN199 and VLAN112. The bilateral 10.05 test was an added rerun; 10.07 did not repeat complete Po30 loss in Mode B or capture the zero-link return route; 10.10 and 10.11 each had one device stop/start cycle rather than the two planned. The VLAN112 live-flow/probe-103 check in 10.12 was not performed, and 10.13 does not have the planned Mode A transition record. I have left those gaps in the evidence instead of treating unperformed checks as passed.

The original 03-10-2026 Test Plan stays unchanged. I am assessing the documented outcomes against its original acceptance criteria, while recording the checks that were changed or not captured during execution. Restored reachability does not by itself turn an unmet traffic-continuity criterion into a pass. The Phase 10 result index uses the following outcome labels:

| Result | Meaning |
|---|---|
| PASS | The original acceptance criteria were met and supported by the retained checks. |
| FAIL | At least one original acceptance criterion was not met, even when the cause was understood. |
| INCONCLUSIVE | The retained evidence was not enough to confirm either PASS or FAIL. |

The PASS, FAIL and INCONCLUSIVE labels describe the Phase 10 test outcome; they are not a direct replacement for the repository’s earlier Verified/Blocked/Deviated phase-status fields. The separate Engineering Review discusses what I learnt. This document records how I tested and what evidence I actually kept.

---

[← Phase 10 Test Plan](phase-10-test-plan.md) · [↑ Phase 10 Evidence Index](../../../evidence/hq/failure-tests/README.md) · [HQ implementation](README.md)
