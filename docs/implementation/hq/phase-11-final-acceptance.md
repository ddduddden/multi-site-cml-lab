# HQ Phase 11 Final Acceptance and Engineering Close-Out

[Portfolio](../../../README.md) / [HQ Implementation](README.md) / Phase 11 Final Acceptance

HQ Campus

Phases 01–09 took HQ from the initial platform setup through to a working campus with redundant gateways and multiple routed paths. In Phase 10 I tested how those features worked together when links and devices failed. With that testing finished, Phase 11 brings the build and its results together and records the state of the lab at close-out.

## Key findings

- The routed-link and access-uplink tests demonstrated working alternate paths. OSPF used surviving routes, and Rapid PVST+ provided another path to the same Active HSRP gateway.

- Po30 remained operational during partial member loss, although some traffic samples failed. Complete loss showed the need for an independent connection between the distribution switches while keeping Root Guard’s protection.

- The isolation tests showed why gateway reachability alone was not enough. Layer 2 isolation exposed a return-path blackhole, while routed isolation confirmed the HSRP upstream-tracking gap.

- The one-sided Po20 failure remains unexplained. The Layer 2 isolation result remains FAIL, and the hq-r1 live-flow failover result remains INCONCLUSIVE.

- The normal forwarding state was restored and temporary test configuration removed after testing on 6 October. The final configuration checks and logging reset were completed on 12 October.

- The 16 October startup check required a manual reset of hq-a1’s VLAN199 SVI. A 26 October recheck reproduced the same failure and recovery; the cause remains unknown.

🟧 [← Return to Stop 7 · Final Acceptance](#overall-assessment)

## Completing the HQ build

I built HQ around two edge routers, two distribution switches and one access switch. The VLANs, EtherChannels, Rapid PVST+ and HSRP established the campus switching and gateway roles. I then added the routed /31 links, loopbacks and OSPF Area 10, followed by verification of ECMP and the cost policy.

## What the failure tests showed

The earlier phases checked those features individually. Failure testing showed how they behaved together. Removing one routed link left other ECMP paths available. When a cross-link failed, OSPF used the surviving higher-cost route and returned to the preferred route after restoration. There were failed IP SLA samples during the changes, but the alternate routing worked.

Traffic could also reach the same Active HSRP gateway through a different Layer 2 path. Losing the preferred access uplink did not always require the gateway role to move.

[Phase 10 Engineering Review](phase-10-engineering-review.md)

The Po20 test covered two ways of taking one member link out of service. Shutting down only hq-d2 Gi0/0 caused sustained loss on one probe path: SLA101 recorded 177 failed samples, while SLA102 stayed OK with no failures. The cause remains unexplained. In the bilateral rerun, shutting down both hq-d2 Gi0/0 and the connected hq-a1 Gi1/0 interface left Po20 working on its other member link, with 20/20 replies in the settled-state check. The report records PASS for this bilateral test, with the one-sided result retained as a separate finding.

[Po20 member failure](../../../evidence/hq/failure-tests/10.05/HQ-VP-10.05-etherchannel-member-failure.md)

Po30 had four member links, but they still formed a single logical connection between the distribution switches. The bundle stayed up with one member link left, although SLA101 recorded 11 failed samples before the final link was removed. With one link remaining, Po30’s higher STP cost made the path advertised by hq-a1 more attractive. Root Guard put the access-facing Port-Channels on both distribution switches into root-inconsistent state for the VLANs rooted on the other switch.

When Po30 went down completely, Root Guard prevented the access switch from becoming a transit path between the distribution switches. That was the intended protection, but there was no independent inter-distribution path left for the affected HSRP peers. From hq-a1, hq-d2’s VLAN130 SVI returned 0/5 replies even though it still showed up/up, and SLA101 timed out. The loss of Po30 had therefore affected forwarding as well as HSRP peer communication. I would keep Root Guard and address the missing alternative connection in a later design. The 10.07 report retains its PASS for the documented checks, with that limitation explained alongside it.

[Po30 progressive failure](../../../evidence/hq/failure-tests/10.07/HQ-VP-10.07-po30-progressive-failure.md)

The hq-d2 Layer 2 isolation test took more investigation. Both switches showed locally Active HSRP states, and the gateway was reachable through hq-d1, but traffic to hq-r2 failed. Checking the SVI state, OSPF advertisement and hq-r2 return route explained the difference. The isolated hq-d2 still had up/up SVIs and was advertising the VLAN160 subnet. hq-r2 selected it for the return flow even though it had no working Layer 2 path back to the source.

That evidence supports a return-path blackhole, and 10.08 remains FAIL. The IOSvL2 SVI behaviour differed from the normal Catalyst autostate behaviour described in Cisco’s documentation. I would need to test this on a platform with standard SVI autostate before drawing a wider conclusion.

Removing hq-d2’s routed uplinks showed a separate issue. Its Layer 2 connections stayed up, so it could still hear its HSRP peer and remained Active. The gateway answered, but it no longer had a route to the edge loopbacks. This confirmed the upstream-tracking gap in the current configuration. Tracking, with a suitable priority decrement and preemption policy, is something I would add and test in the next revision.

[Layer 2 isolation](../../../evidence/hq/failure-tests/10.08/HQ-VP-10.08-d2-layer2-isolation.md) | [Routed isolation](../../../evidence/hq/failure-tests/10.09/HQ-VP-10.09-d2-routed-isolation.md)

The hq-r1 device test confirmed that hq-r2 remained reachable while hq-r1 was stopped. Live-flow failover away from hq-r1 was not established, so 10.12 remains INCONCLUSIVE. In the combined failure, I stopped hq-d1 and then hq-r2. Once the network had settled, the route tables showed the hq-d2–hq-r1 cross-link in both directions, and the tested VLAN170 traffic succeeded.

The lab had no NTP synchronisation or continuous external monitoring, which limited how accurately events could be matched across devices and outages measured. The retained ping and IP SLA samples show traffic behaviour during the checks rather than precise convergence times or measured availability.

[hq-r1 device failure](../../../evidence/hq/failure-tests/10.12/HQ-VP-10.12-r1-device-failure.md) | [Combined failure](../../../evidence/hq/failure-tests/10.13/HQ-VP-10.13-diagonal-double-failure.md) | [Testing Methodology](phase-10-testing-methodology.md)

## Final restoration and configuration close-out

After testing, the links and devices were restored and the normal roles and paths returned. Po10 and Po20 each had both member links, Po30 had all four, and STP showed no inconsistent ports. The HSRP roles matched the intended split, each Layer 3 device had five FULL OSPF neighbours, and hq-a1 reached its VLAN199 gateway and both edge loopbacks with 5/5 replies. The temporary VLAN source addresses and IP SLA operations were removed.

The final running/startup checks were completed across all five devices on 12 October. On hq-a1, the original logging setting was restored and saved, and a follow-up startup check confirmed that the custom setting had been cleared. The only remaining differences were the known VTY timeout artefacts caused by CML configuration fetching. This completed the configuration close-out.

[Final restoration report](../../../evidence/hq/failure-tests/10.14/HQ-VP-10.14-final-restoration.md) | [12 October configuration checks](../../../evidence/hq/failure-tests/10.14/10.14-config-excerpts.md)

Device management was also tightened up after the Phase 07 milestone. SSH access was standardised across all five devices and restricted to the management host through access lists. The switches’ local-user and enable secrets were updated from type 5 to type 9 hashes, bringing them into line with the routers. Management host routes were added where needed to provide a return path through hq-r1’s external management connection.

The Phase 07 export preserves the 30 September milestone. On 15 October, the sanitised Phase 11 YAML and five matching device configuration files were published in commit 1ee631b. They were prepared from the private export retained after the 12 October close-out. The public copy retains the SSH configuration, access restrictions and management routes, with credentials and the management host address replaced by placeholders or example values. The original export remains private.

[Phase 07 export](../../../lab/cml-lab-exports/hq/hq-phase-07-ospf-area10-2026-09-30.yaml) | [Phase 11 export](../../../lab/cml-lab-exports/hq/hq-phase-11-final-acceptance-2026-10-15.yaml) | [Export policy](../../../lab/cml-lab-exports/README.md) | [Configuration milestone 1ee631b](https://github.com/ddduddden/multi-site-cml-lab/commit/1ee631be011985dac4a1c6a7f97de1ff95d22c1c)

## Operational check on 16 October

On 16 October, the private five-device CML export was booted to check the final HQ configuration. This check used the private export, so it does not establish the startup behaviour of the sanitised public copy.

On the first check, hq-a1’s VLAN199 SVI remained down/down, and pings to the management gateway at 10.10.99.1 failed with 0/5 replies. The VLAN database, Po10 and Po20 bundles, trunks and Rapid PVST+ state were checked. Entering no shutdown alone did not recover the SVI. A shutdown/no shutdown cycle brought it up, after which the gateway returned 5/5 replies. The cause of the initial SVI state was not established.

The operational checks passed after the manual SVI reset. Both edge-router loopbacks returned 5/5 replies from hq-a1. On hq-r1, all five OSPF neighbours were FULL and the route to 10.10.12.0/22 had four equal-cost paths at metric 11. HSRP and EtherChannel state matched the intended roles, including all four Po30 members. The retained traceroute recorded 10.10.99.3 on hq-d2 followed by 10.255.10.3.

The startup finding is recorded separately from the Layer 2 isolation behaviour investigated in Phase 10, as a common cause has not been established.

[Startup checks and recovery](../../../evidence/hq/final-acceptance/HQ-Phase-11-Boot-Recovery-CLI.md) | [Operational checks](../../../evidence/hq/final-acceptance/HQ-Phase-11-Final-Boot-Verification.txt) | [Evidence commit 39b68a7](https://github.com/ddduddden/multi-site-cml-lab/commit/39b68a790a3b9ed0de55071fdf7f9b004d0638b2)

## Startup recheck — 26 October

A further CML boot reproduced the VLAN199 startup problem on `hq-a1`. The SVI was `down/down` and the management gateway returned `0/5` even though the VLAN was active, the Po10/Po20 EtherChannels were bundled, and Po20 was the VLAN199 root forwarding port. Running and startup SVI configuration matched. Entering `no shutdown` alone did not change the state. A deliberate `shutdown` / `no shutdown` reset brought the SVI `up/up` and the gateway answered `5/5`.

This is a second observed occurrence with the same recovery procedure. The cause remains unresolved; a clean, intervention-free boot has not been demonstrated. The recheck establishes recovery of the management gateway, **not** a fresh set of full-network routing, HSRP or failover results. The more extensive operational checks above remain those retained on 16 October.

[26 October recheck and recovery evidence](../../../evidence/hq/final-acceptance/HQ-Phase-11-26-Oct-Boot-Retest.md)

## Overall assessment

<a href="phase-10-engineering-review.md#layer-2-isolation-and-split-brain--hq-vp-1008" title="Previous: Stop 6 · Troubleshooting and engineering review" aria-label="Previous: Stop 6 · Troubleshooting and engineering review"><img src="../../../diagrams/orange-previous.svg" alt="" width="30" height="26"></a> **🟧 10-MINUTE ROUTE · EXPLORE THE EVIDENCE · 07/07**

*Final acceptance, limitations and future development.* Where HQ V1 stands at close-out and what the next revision would change. Open findings are listed under [Key findings](#key-findings). About 1 minute.

The HQ build gave me a working campus to test beyond individual configuration exercises. The routed and access-path tests showed the alternate paths doing their job. Working through the isolation cases helped me understand how HSRP, spanning tree and the return route could combine to produce different traffic results.

The build, failure testing and configuration close-out are complete. The reports record the working design and the findings I would carry into the next revision. HSRP upstream tracking would allow the gateway role to respond to a loss of upstream connectivity, while an independent inter-distribution connection would provide an alternative when Po30 is lost. Both changes would need to be tested during failure and recovery, with Root Guard retained on the access-facing Port-Channels.

Before the next test cycle, I would also add NTP synchronisation and continuous monitoring. That would make it easier to compare events across devices and measure the traffic impact of a failure. These are the next steps I would take to develop the HQ design; they remain future work.

**Status: ACCEPTED — HQ V1 engineering milestone, with documented findings and limitations retained.** Acceptance recorded 26 October 2026.

**Final acceptance:** HQ V1 is accepted as a completed engineering and portfolio milestone. The network build, failure testing, configuration reconciliation and final operational checks have been documented, with supporting evidence retained in GitHub. The outstanding findings remain part of the accepted record, including the 10.08 FAIL, 10.12 INCONCLUSIVE result, unexplained one-sided Po20 behaviour and the VLAN199 startup issue reproduced on 16 and 26 October. The operational checks passed after manual recovery; an intervention-free startup has not been demonstrated. Further resilience improvements belong to the next design revision.

[Phase 10 results](../../../evidence/hq/failure-tests/README.md) | [Reviewed repository baseline 653ce7a](https://github.com/ddduddden/multi-site-cml-lab/commit/653ce7af76fe4e8a24460b5cae217e064675f1b2)

---

[← HQ Verification Plan](verification-plan.md) · [↑ HQ Implementation](README.md) · [Phase 10 Engineering Review →](phase-10-engineering-review.md)

**END OF THE 10-MINUTE ROUTE**

Follow two contrasting results in depth, explore the network visually, or choose another route.

[![Explore the Test Investigations ↗](https://img.shields.io/badge/EXPLORE%20THE%20TEST%20INVESTIGATIONS%20%E2%86%97-bf6700?style=flat-square)](../../../evidence/hq/README.md#explore-the-test-investigations) [![Explore the Interactive Portfolio ↗](https://img.shields.io/badge/EXPLORE%20THE%20INTERACTIVE%20PORTFOLIO%20%E2%86%97-0969da?style=flat-square)](https://dominicdudden.co.uk)

[![Choose Another Route ↗](https://img.shields.io/badge/CHOOSE%20ANOTHER%20ROUTE%20%E2%86%97-C2185B?style=flat-square)](../../../README.md#explore-the-hq-project)
