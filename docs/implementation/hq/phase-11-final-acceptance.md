# HQ Phase 11 — Final Acceptance and Engineering Close-Out

[Portfolio](../../../README.md) / [HQ Implementation](README.md) / Phase 11 Final Acceptance

**HQ campus** · Public configuration milestone [`1ee631b`](https://github.com/ddduddden/multi-site-cml-lab/commit/1ee631be011985dac4a1c6a7f97de1ff95d22c1c) · Final documentation review in progress

Phases 01–09 took HQ from the initial platform setup through to a working campus with redundant gateways and multiple routed paths. In Phase 10 I tested how those features worked together when links and devices failed. With that testing finished, Phase 11 brings the build and its results together and records the state of the lab at close-out.

## Key findings

- The alternate routed and access paths worked in the tested failure conditions. OSPF used surviving routes, and Rapid PVST+ provided another path to the same Active HSRP gateway.
- Po30 tolerated partial member loss, although some traffic samples failed. Complete loss showed the need for an independent connection between the distribution switches while keeping Root Guard’s protection.
- The isolation tests showed why gateway reachability alone was not enough. Layer 2 isolation exposed a return-path blackhole, while routed isolation confirmed the HSRP upstream-tracking gap.
- The one-sided Po20 failure remains unexplained. The Layer 2 isolation result remains FAIL, and the hq-r1 live-flow failover result remains INCONCLUSIVE.
- The normal forwarding state was restored and temporary test configuration removed after testing on 06-10-2026. The final configuration checks and logging reset were completed on 12-10-2026.
- The 16-10-2026 boot check required a manual VLAN 199 SVI reset on `hq-a1` before operational checks passed; the root cause remains unknown.

## Completing the HQ build

I built HQ around two edge routers, two distribution switches and one access switch. The VLANs, EtherChannels, Rapid PVST+ and HSRP established the campus switching and gateway roles. I then added the routed /31 links, loopbacks and OSPF Area 10, followed by verification of ECMP and the cost policy.

The earlier phases checked those features individually. Failure testing showed how they behaved together. Removing one routed link left other ECMP paths available. When a cross-link failed, OSPF used the surviving higher-cost route and returned to the preferred route after restoration. There were failed IP SLA samples during the changes, but the alternate routing worked.

The access-uplink tests showed another useful distinction. Traffic could reach the same Active HSRP gateway through a different Layer 2 path, so losing the preferred access uplink did not always require the gateway role to move. In the combined failure, I stopped hq-d1 and then hq-r2. Once the network had settled, the route tables showed the hq-d2–hq-r1 cross-link in both directions, and the tested VLAN170 traffic succeeded.

[Phase 10 Engineering Review](phase-10-engineering-review.md)

## What the failure tests showed

The Po20 test covered two ways of taking one member link out of service. Shutting hq-d2 Gi0/0 only caused sustained loss on one probe path: SLA101 recorded 177 failed samples, while SLA102 stayed OK with no failures. The cause remains unexplained. Shutting both hq-d2 Gi0/0 and the connected hq-a1 Gi1/0 interface then left Po20 working on its other member link, with 20/20 replies in the settled-state check. The report records PASS for this bilateral test, with the one-sided result retained as a separate finding.

[Po20 member failure](../../../evidence/hq/failure-tests/10.05/HQ-VP-10.05-etherchannel-member-failure.md)

Po30 showed why four physical links still need to be considered as one logical connection. The bundle stayed up with one member link left, although SLA101 recorded 11 failed samples before the final link was removed. With one link remaining, the higher STP cost allowed hq-a1 to advertise a better path to the root. Root Guard put the access-facing Port-Channels on both distribution switches into root-inconsistent state for the VLANs rooted on the other switch.

When Po30 went down completely, Root Guard prevented the access switch from becoming a transit path between the distribution switches. That was the intended protection, but there was no independent inter-distribution path left for the affected HSRP peers. From hq-a1, hq-d2’s VLAN130 SVI returned 0/5 replies even though it still showed up/up, and SLA101 timed out. The loss of Po30 had therefore affected forwarding as well as HSRP peer communication. I would keep Root Guard and address the missing alternative connection in a later design. The 10.07 report retains its PASS for the documented checks, with that limitation explained alongside it.

[Po30 progressive failure](../../../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md)

The hq-d2 Layer 2 isolation test took more investigation. Both switches showed locally Active HSRP states, and the gateway was reachable through hq-d1, but traffic to hq-r2 failed. Checking the SVI state, OSPF advertisement and hq-r2 return route explained the difference. The isolated hq-d2 still had up/up SVIs and was advertising the VLAN160 subnet. hq-r2 selected it for the return flow even though it had no working Layer 2 path back to the source.

That evidence supports a return-path blackhole, and 10.08 remains FAIL. The IOSvL2 SVI behaviour differed from the normal Catalyst autostate behaviour described in Cisco’s documentation. It remains a finding from this lab.

Removing hq-d2’s routed uplinks showed a separate issue. Its Layer 2 connections stayed up, so it could still hear its HSRP peer and remained Active. The gateway answered, but it no longer had a route to the edge loopbacks. This confirmed the upstream-tracking gap in the current configuration. Tracking, with a suitable priority decrement and preemption policy, is something I would add and test in the next revision.

[Layer 2 isolation](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md)  |  [Routed isolation](../../../evidence/hq/failure-tests/10.09/HQ-VP-10.09-d2-routed-isolation.md)

The hq-r1 device test confirmed that hq-r2 remained reachable while hq-r1 was stopped. Live-flow failover away from hq-r1 was not established, so 10.12 remains INCONCLUSIVE. The combined-failure test showed connectivity after the network had settled. The lab had no NTP synchronisation or continuous external monitoring, which limited how accurately events could be matched across devices and outages measured. The retained ping and IP SLA samples show traffic behaviour during the checks rather than precise convergence times or measured availability.

[hq-r1 device failure](../../../evidence/hq/failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md)  |  [Testing Methodology](phase-10-testing-methodology.md)

## Final restoration

After testing, the links and devices were restored and the normal roles and paths returned. Po10 and Po20 each had both member links, Po30 had all four, and STP showed no inconsistent ports. The HSRP roles matched the intended split, each Layer 3 device had five FULL OSPF neighbours, and hq-a1 reached its VLAN199 gateway and both edge loopbacks with 5/5 replies. The temporary VLAN source addresses and IP SLA operations were removed.

The final running/startup checks were completed across all five devices on 12-10-2026. On hq-a1, the original logging setting was restored and saved. The comparisons showed the known CML configuration-fetch VTY timeout difference, along with hq-a1’s logging reset before the save. The follow-up startup check confirmed that the custom logging setting had been cleared. This completed the configuration close-out.

[Final restoration report](../../../evidence/hq/failure-tests/10.14/HQ-VP-10.14-final-restoration.md)  |  [12-10-2026 configuration checks](../../../evidence/hq/failure-tests/10.14/10.14-config-excerpts.md)

Device management was also tightened up after the Phase 07 milestone. SSH access was standardised across all five devices and restricted to the management host through access lists. The switches’ local-user and enable secrets were updated from type 5 to type 9 hashes, bringing them into line with the routers. Management host routes were added where needed to provide a return path through hq-r1’s external management connection.

The Phase 07 export preserves the 30-09-2026 milestone. On 15-10-2026, the sanitised Phase 11 YAML and five matching device configuration files were published on the phase-11/final-acceptance branch in commit 1ee631b. They were prepared from the private export retained after the 12-10-2026 close-out. The public copy preserves the SSH settings and management connectivity, with credentials and the management host address replaced by placeholders or example values. The original export remains private.

[Public Phase 07 export](../../../lab/cml-lab-exports/hq/hq-phase-07-ospf-area10-2026-09-30.yaml)  |  [Export policy](../../../lab/cml-lab-exports/README.md)  |  [Final session record](../../../evidence/hq/failure-tests/10.14/10.14-session-record.md)  |  [Published Phase 11 export](../../../lab/cml-lab-exports/hq/hq-phase-11-final-acceptance-2026-10-15.yaml)  |  [Configuration milestone 1ee631b](https://github.com/ddduddden/multi-site-cml-lab/commit/1ee631be011985dac4a1c6a7f97de1ff95d22c1c)

## Operational check — 16-10-2026

The private five-device CML export was booted to check the final HQ configuration. The published export is sanitised and was not the source used for this runtime test.

On the first check, `hq-a1 Vlan199` remained `down/down`, and pings to the HSRP management gateway `10.10.99.1` failed (`0/5`). The VLAN database, Po10/Po20 LACP bundles, trunks and Rapid PVST+ state were checked. Entering `no shutdown` alone did not recover the SVI. After `shutdown` / `no shutdown`, it returned to `up/up`, and the gateway ping succeeded (`5/5`). The underlying cause was not established.

The subsequent checks were successful **after manual intervention**, not on a completely clean untouched boot. Both edge-router loopbacks replied `5/5` from `hq-a1`. On `hq-r1`, five OSPF neighbours were `FULL` and the route to `10.10.12.0/22` had four installed metric-`11` equal-cost paths. HSRP and EtherChannel state matched the intended roles, including all four Po30 members. The retained traceroute showed `10.10.99.3` (`hq-d2`) followed by `10.255.10.3`; no unrecorded later hop is inferred.

**Retained CLI:** [Startup checks and manual recovery](../../../evidence/hq/final-acceptance/HQ-Phase-11-Boot-Recovery-CLI.md) · [Post-recovery verification](../../../evidence/hq/final-acceptance/HQ-Phase-11-Final-Boot-Verification.txt).

**Evidence commit:** [`39b68a7` — Add Phase 11 boot evidence and HQ troubleshooting records](https://github.com/ddduddden/multi-site-cml-lab/commit/39b68a790a3b9ed0de55071fdf7f9b004d0638b2).

This startup finding does not establish the same cause as the IOSvL2 SVI behaviour investigated in [HQ-TS-002](troubleshooting.md#hq-ts-002--iosvl2-svi-state-during-layer-2-isolation). The completed Phase 10 FAIL and INCONCLUSIVE outcomes are unchanged.

## Overall assessment

The HQ build gave me a working campus to test beyond individual configuration exercises. The routed and access-path tests showed the alternate paths doing their job. Working through the isolation cases helped me understand how HSRP, spanning tree and the return route could combine to produce different traffic results.

The build, failure testing and configuration close-out are complete. The reports explain what worked and the findings I would carry into the next revision, particularly upstream tracking and an independent inter-distribution connection. Better time synchronisation and monitoring would also help with that next round of testing. Those changes remain future work.

**Status:** Final documentation and evidence review in progress; acceptance has not been declared.

[Reviewed baseline 0ba7114](https://github.com/ddduddden/multi-site-cml-lab/commit/0ba7114f25acf8793a04800b9381412ed7c55d28)  |  [Phase 10 results and evidence provenance](../../../evidence/hq/failure-tests/README.md)

---

[← HQ Verification Plan](verification-plan.md) · [↑ HQ Implementation](README.md) · [Phase 10 Engineering Review →](phase-10-engineering-review.md)
