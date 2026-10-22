# HQ Phase 11 — Access-Switch Boot Recovery

[Portfolio](../../../README.md) / [Evidence Map](../README.md) / [Phase 11](README.md) / Boot Recovery

**Device:** `hq-a1` (IOSvL2)  
**Session:** 16 October 2026  
**Scope:** VLAN 199 management SVI startup checks, intervention and connectivity verification  
**Companion evidence:** [Final operational CLI checks](HQ-Phase-11-Final-Boot-Verification.txt) — retained separately from the startup investigation

## Observed behaviour

Following the CML boot, `Po10` and `Po20` showed their intended LACP members bundled, but `hq-a1 Vlan199` reported `down/down`. Pings to the HSRP management gateway (`10.10.99.1`) failed (`0/5`). The captured checks showed VLAN 199 active, the expected trunk allowed-VLAN and STP forwarding state, and the configured management SVI address. An initial `no shutdown` did not restore the SVI.

A subsequent explicit `shutdown` followed by `no shutdown` on `interface Vlan199` restored the interface to `up/up`. The gateway ping then returned `5/5`, followed by `5/5` pings to both edge-router loopbacks (`10.255.10.129` and `10.255.10.130`). The retained traceroute showed hops via `10.10.99.3` and `10.255.10.3`.

**Finding:** The checks succeeded after a manual SVI reset. The underlying cause of the initial SVI state was not established; this is **not evidence of a clean, intervention-free startup**.

## Original CLI capture

The following is the complete CLI text copied from `capture of boot recover.docx`, in the original sequence. Failed checks, repeated commands and unsuccessful input are retained. No CLI results have been reconstructed or omitted.

<details>
<summary>Expand full hq-a1 CLI transcript</summary>

```text
hq-a1>en
Password: 
hq-a1#terminal length 0
hq-a1#show etherchannel summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      N - not in use, no aggregation
        f - failed to allocate aggregator

        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port

        A - formed by Auto LAG


Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
10     Po10(SU)        LACP      Gi0/0(P)    Gi0/1(P)    
20     Po20(SU)        LACP      Gi1/0(P)    Gi1/1(P)    

hq-a1#ping 10.10.99.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)
hq-a1#
hq-a1#
hq-a1#
hq-a1#terminal length 0
hq-a1#show etherchannel summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      N - not in use, no aggregation
        f - failed to allocate aggregator

        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port

        A - formed by Auto LAG


Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
10     Po10(SU)        LACP      Gi0/0(P)    Gi0/1(P)    
20     Po20(SU)        LACP      Gi1/0(P)    Gi1/1(P)    

hq-a1#ping 10.10.99.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)
hq-a1#show ip interface brief | include Vlan199
Vlan199                10.10.99.4      YES TFTP   down                  down    
hq-a1#show spanning-tree vlan 199

VLAN0199
  Spanning tree enabled protocol rstp
  Root ID    Priority    24775
             Address     5254.003a.90d2
             Cost        3
             Port        66 (Port-channel20)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32967  (priority 32768 sys-id-ext 199)
             Address     5254.00bc.4c19
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi3/3               Desg FWD 4         128.16   P2p Edge 
Po10                Altn BLK 3         128.65   P2p 
Po20                Root FWD 3         128.66   P2p 


hq-a1#ping 10.10.99.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.2, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)
hq-a1#int vlan 199
       ^
% Invalid input detected at '^' marker.

hq-a1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#int vlan 199
hq-a1(config-if)#no shutdown
hq-a1(config-if)#end
hq-a1#terminal length 0
hq-a1#show etherchannel summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      N - not in use, no aggregation
        f - failed to allocate aggregator

        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port

        A - formed by Auto LAG


Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
10     Po10(SU)        LACP      Gi0/0(P)    Gi0/1(P)    
20     Po20(SU)        LACP      Gi1/0(P)    Gi1/1(P)    

hq-a1#ping 10.10.99.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)
hq-a1#show vlan id 199

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
199  NET-MGMT                         active    Gi3/3, Po10, Po20

VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
199  enet  100199     1500  -      -      -        -    -        0      0   

Remote SPAN VLAN
----------------
Disabled

Primary Secondary Type              Ports
------- --------- ----------------- ------------------------------------------

hq-a1#show interfaces trunk

Port        Mode             Encapsulation  Status        Native vlan
Po10        on               802.1q         trunking      190
Po20        on               802.1q         trunking      190

Port        Vlans allowed on trunk
Po10        112,120,130,140,152,160,170,190,199
Po20        112,120,130,140,152,160,170,190,199

Port        Vlans allowed and active in management domain
Po10        112,120,130,140,152,160,170,190,199
Po20        112,120,130,140,152,160,170,190,199

Port        Vlans in spanning tree forwarding state and not pruned
Po10        112,130,152,170,190
Po20        120,140,160,199
hq-a1#show running-config interface Vlan199
Building configuration...

Current configuration : 83 bytes
!
interface Vlan199
 ip address 10.10.99.4 255.255.255.192
 no ip route-cache
end

hq-a1#show vlan id 199

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
199  NET-MGMT                         active    Gi3/3, Po10, Po20

VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
199  enet  100199     1500  -      -      -        -    -        0      0   

Remote SPAN VLAN
----------------
Disabled

Primary Secondary Type              Ports
------- --------- ----------------- ------------------------------------------

hq-a1#show interfaces trunk

Port        Mode             Encapsulation  Status        Native vlan
Po10        on               802.1q         trunking      190
Po20        on               802.1q         trunking      190

Port        Vlans allowed on trunk
Po10        112,120,130,140,152,160,170,190,199
Po20        112,120,130,140,152,160,170,190,199

Port        Vlans allowed and active in management domain
Po10        112,120,130,140,152,160,170,190,199
Po20        112,120,130,140,152,160,170,190,199

Port        Vlans in spanning tree forwarding state and not pruned
Po10        112,130,152,170,190
Po20        120,140,160,199
hq-a1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#interface Vlan199
hq-a1(config-if)#shutdown
hq-a1(config-if)#no shutdown
hq-a1(config-if)#end
hq-a1#show ip interface brief | include Vlan199
Vlan199                10.10.99.4      YES TFTP   up                    up      
hq-a1#ping 10.10.99.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 4/206/1008 ms
hq-a1#
hq-a1#
hq-a1#
hq-a1#terminal length 0
hq-a1#show ip interface brief | include Vlan199
Vlan199                10.10.99.4      YES TFTP   up                    up      
hq-a1#ping 10.255.10.129
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.255.10.129, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 6/8/10 ms
hq-a1#ping 10.255.10.130
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.255.10.130, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 5/6/8 ms
hq-a1#traceroute 10.255.10.130
Type escape sequence to abort.
Tracing the route to 10.255.10.130
VRF info: (vrf in name/id, vrf out name/id)
  1 10.10.99.3 6 msec 4 msec 5 msec
  2 10.255.10.3 6 msec *  6 msec
hq-a1#
hq-a1#
hq-a1#
```

</details>

---

[◀ Evidence index](README.md) · [↑ Phase 11 evidence](README.md) · [Final operational checks ▶](HQ-Phase-11-Final-Boot-Verification.txt)
