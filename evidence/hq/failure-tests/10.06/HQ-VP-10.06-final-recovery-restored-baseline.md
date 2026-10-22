[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.06](README.md) / Capture / record

# HQ-VP-10.06 — Final recovery restored baseline

<details>
<summary><strong>Original retained CLI / source capture</strong></summary>

```text
HQ-VP-10.06 — Access Uplink Failure
===================================

Final recovery and restored baseline
------------------------------------

Capture date: 03-10-2026

Source: Device console capture, 03-10-2026.

Editorial note:
Selected verbatim CLI excerpts are retained. The filtered event log is
stored separately to keep the recovery evidence concise. Repeated hq-d2 HSRP
output and blank prompts are omitted. Section labels are editorial.

Temporary Mode B cleanup and hq-a1 recovery
-------------------------------------------

hq-a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#interface Port-channel10
hq-a1(config-if)# no shutdown
hq-a1(config-if)#end
hq-a1#
hq-a1#

hq-a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#no ip sla schedule 101
hq-a1(config)#no ip sla schedule 102
hq-a1(config)#no ip sla 101
hq-a1(config)#no ip sla 102
hq-a1(config)#no interface Vlan112
hq-a1(config)#no ip default-gateway 10.10.12.1
hq-a1(config)#ip default-gateway 10.10.99.1
hq-a1(config)#end
hq-a1#
hq-a1#

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

hq-a1#show spanning-tree vlan 112

VLAN0112
  Spanning tree enabled protocol rstp
  Root ID    Priority    24688
             Address     5254.0044.1293
             Cost        3
             Port        65 (Port-channel10)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32880  (priority 32768 sys-id-ext 112)
             Address     5254.0002.4b8d
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi2/0               Desg FWD 4         128.9    P2p Edge 
Gi2/1               Desg FWD 4         128.10   P2p Edge 
Po10                Root FWD 3         128.65   P2p 
Po20                Altn BLK 3         128.66   P2p 

hq-a1#show spanning-tree vlan 199

VLAN0199
  Spanning tree enabled protocol rstp
  Root ID    Priority    24775
             Address     5254.006a.22f2
             Cost        3
             Port        66 (Port-channel20)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32967  (priority 32768 sys-id-ext 199)
             Address     5254.0002.4b8d
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi3/3               Desg FWD 4         128.16   P2p Edge 
Po10                Altn BLK 3         128.65   P2p 
Po20                Root FWD 3         128.66   P2p 

hq-a1#show ip interface brief | include Vlan112|Vlan199
Vlan199                10.10.99.4      YES NVRAM  up                    up      

hq-a1#show running-config | include ^ip default-gateway
ip default-gateway 10.10.99.1

hq-a1#ping 10.10.99.1 source 10.10.99.4 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
Packet sent with a source address of 10.10.99.4 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 4/5/9 ms

hq-a1#ping 10.255.10.129 source 10.10.99.4 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.255.10.129, timeout is 2 seconds:
Packet sent with a source address of 10.10.99.4 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 6/7/9 ms

hq-a1#ping 10.255.10.130 source 10.10.99.4 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.255.10.130, timeout is 2 seconds:
Packet sent with a source address of 10.10.99.4 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 5/6/7 ms

Final HSRP and STP consistency — hq-d1
--------------------------------------

hq-d1#

hq-d1#show standby brief
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Vl112       112  110 P Active  local           10.10.12.3      10.10.12.1
Vl120       120  100   Standby 10.10.20.3      local           10.10.20.1
Vl130       130  110 P Active  local           10.10.30.3      10.10.30.1
Vl140       140  100   Standby 10.10.40.3      local           10.10.40.1
Vl152       152  110 P Active  local           10.10.52.3      10.10.52.1
Vl160       160  100   Standby 10.10.60.3      local           10.10.60.1
Vl170       170  110 P Active  local           10.10.70.3      10.10.70.1
Vl199       199  100   Standby 10.10.99.3      local           10.10.99.1

hq-d1#show spanning-tree inconsistentports

Name                 Interface                Inconsistency
-------------------- ------------------------ ------------------

Number of inconsistent ports (segments) in the system : 0

hq-d1#

Final HSRP and STP consistency — hq-d2
--------------------------------------

hq-d2#show standby brief
                     P indicates configured to preempt.
                     |
Interface   Grp  Pri P State   Active          Standby         Virtual IP
Vl112       112  100   Standby 10.10.12.2      local           10.10.12.1
Vl120       120  110 P Active  local           10.10.20.2      10.10.20.1
Vl130       130  100   Standby 10.10.30.2      local           10.10.30.1
Vl140       140  110 P Active  local           10.10.40.2      10.10.40.1
Vl152       152  100   Standby 10.10.52.2      local           10.10.52.1
Vl160       160  110 P Active  local           10.10.60.2      10.10.60.1
Vl170       170  100   Standby 10.10.70.2      local           10.10.70.1
Vl199       199  110 P Active  local           10.10.99.2      10.10.99.1
hq-d2#

hq-d2#show spanning-tree inconsistentports

Name                 Interface                Inconsistency
-------------------- ------------------------ ------------------

Number of inconsistent ports (segments) in the system : 0

hq-d2#
```

</details>

---

[◀ Previous record](HQ-VP-10.06-mode-b-po10-traffic-continuity.md) · [↑ Test evidence](README.md) · [Next record ▶](HQ-VP-10.06-hq-a1-interface-event-log.md)
