# HQ Troubleshooting

This file records **meaningful diagnostic investigations**.

It is not a diary of every mistake. The build log remains the chronology; a build-log or verification entry links here only when the observed behaviour requires real investigation.

## Project reference key

| Reference | Meaning |
|---|---|
| `HQ-TS-NNN` | HQ troubleshooting record |
| `HQ-VP-XX.YY` | Related HQ verification test |
| `HQ-DEV-NNN` | Related HQ design deviation |

## When to create a troubleshooting record

**Normally does not need an `HQ-TS-NNN` record:**
- A mistyped command that is corrected immediately.
- A wrong interface selected and immediately corrected.
- A forgotten `no shutdown` noticed immediately.
- A minor syntax correction with no meaningful effect on the build.

**Normally does justify an `HQ-TS-NNN` record:**
- A protocol fails to establish even though the configuration appears correct.
- Failover or reconvergence differs from the expected behaviour.
- A platform or image behaves differently from the documented assumption.
- A routing decision cannot initially be explained.
- A feature limitation requires investigation before implementation can continue.

## Entry template

```text
## HQ-TS-NNN — Short title

Opened:
DD-MM-YYYY

Related verification:
- HQ-VP-XX.YY

Related build-log entry:
- DD-MM-YYYY — description

Symptom:
...

Expected behaviour:
...

Scope / impact:
...

Investigation:
1. ...
2. ...
3. ...

Root cause:
...

Correction:
...

Re-verification:
...

Evidence:
...

Related deviation:
- HQ-DEV-NNN, only if an accepted design deviation results

Status:
Open / Resolved
```

## Cross-reference rule

Resolving a troubleshooting record does not automatically mean the related verification test is `Verified`.

After the correction, the verification test must be run or re-run and its own `Observed result`, `Status`, and evidence updated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## HQ-TS-001 — IOSvL2 Routing Mode on `hq-a1`

**Opened:**  
`30-09-2026`

**Related verification:**  
- `HQ-VP-07.05` — where the fault was observed and the correction re-verified
- `HQ-VP-05.01` — earlier as-built record of the `hq-a1` default gateway
- `HQ-VP-06.01` — the same IOSvL2 routing behaviour observed on `hq-d1` and `hq-d2`

**Related build-log entry:**  
- `30-09-2026` — Phase 07: disabled IP routing on `hq-a1`

**Symptom:**  
During `HQ-VP-07.05`, `hq-a1` (`10.10.99.4`) could reach its local HSRP gateway but could not reach the four `Loopback0` addresses, even though `ip default-gateway 10.10.99.1` was configured. `show ip route` displayed a routing table rather than the `Default gateway is …` view expected from the Layer 2 access-switch role.

**Expected behaviour:**  
`hq-a1` operates as a Layer 2 access switch. Management traffic for destinations beyond VLAN `199` should use `ip default-gateway 10.10.99.1`, as set out in the HQ Campus Design, Section 3, *Management SVI Allocation*.

**Scope / impact:**  
- `hq-a1` management traffic beyond the local VLAN. The default gateway had been configured since Phase 05 but was not being used while IPv4 routing remained enabled.
- No Phase 05 result is affected. Every `hq-a1` test in `HQ-VP-05.03`–`HQ-VP-05.05` used targets in the same VLAN as the source (`10.10.99.x` from `Vlan199`, and `10.10.12.x` from the temporary `Vlan112` SVI).
- `hq-d1` and `hq-d2` use the same IOSvL2 default routing behaviour, but that behaviour is appropriate for their multilayer distribution role and required no correction.

**Investigation:**  
1. `show ip route` on `hq-a1` returned the routing-table view, so IP routing was enabled even though no `ip routing` line appeared in the running configuration.
2. With IP routing enabled, IOS forwarded using the routing table rather than `ip default-gateway`. `hq-a1` held only its connected `Vlan199` route, so it had no route to the `10.255.10.x` routing identities.
3. `hq-d1` and `hq-d2`, which run the same IOSvL2 image, also route without an explicit `ip routing` line (`HQ-VP-06.01`). This corroborated the same observed IOSvL2 routing behaviour on the distribution switches.
4. OSPF was not the cause. The edge routers held `10.10.99.0/26` through OSPF (`HQ-VP-07.04`), so a return path existed.

**Root cause:**  
On the IOSvL2 image used in this lab (`vios_l2` `15.2(20200924:215240)`), IPv4 routing was operational in the initial lab state even though `ip routing` was not displayed in the normal running configuration. Cisco documents `ip default-gateway` for use when IP routing is disabled; while routing remained active, `hq-a1` forwarded according to its routing table instead of using the configured default gateway. Because it held only the connected VLAN `199` route, it had no routed path to the remote `Loopback0` addresses. This observed platform behaviour was not captured by the Phase 01 capability review.

**Correction:**  
`no ip routing` on `hq-a1`, retaining `ip default-gateway 10.10.99.1`. The running configuration now also shows `no ip cef` globally and `no ip route-cache` on `Vlan199`, consistent with routing being disabled. `hq-d1` and `hq-d2` were not changed.

**Re-verification:**  
- `HQ-VP-07.01` — `show ip route` on `hq-a1` reports `Default gateway is 10.10.99.1`.
- `HQ-VP-07.05` — `hq-a1` reached `10.10.99.1` and all four loopbacks at `5/5`.
- `HQ-VP-07.06` — `hq-a1 Vlan199` remained `up/up`, and the Layer 2 state was unchanged.

**Evidence:**  
Post-correction state: `evidence/hq/ospf/HQ-VP-07.01-loopback-ospf-process-identity.txt`; `evidence/hq/ospf/HQ-VP-07.05-end-to-end-reachability.txt`; `configs/hq/hq-a1-running-config.txt`. Pre-correction output was not retained as repository evidence.

**Related deviation:**  
None. The correction brings `hq-a1` into line with the design.

**Status:**  
Resolved
