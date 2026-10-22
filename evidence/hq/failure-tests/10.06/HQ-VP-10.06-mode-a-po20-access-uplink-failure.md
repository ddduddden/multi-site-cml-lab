[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.06](README.md) / Capture / record

# Mode A Po20 access uplink failure

<details>
<summary><strong>Original retained CLI / source capture</strong></summary>

```text
HQ-VP-10.06 — Access Uplink Failure
===================================

Mode A VLAN199 Po20 failure
---------------------------

Capture date: 03-10-2026

Source: Device console capture, 03-10-2026.

Editorial note:
Selected verbatim CLI excerpts are retained. Earlier unrelated log entries,
blank prompts and repeated pastes are omitted. Section labels are editorial.

Baseline HSRP ownership — hq-d1 / hq-d2
---------------------------------------

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
hq-d1#

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

Failure action and Layer 2 state — hq-a1
----------------------------------------

hq-a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#interface Port-channel20
hq-a1(config-if)# shutdown
hq-a1(config-if)#end

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
20     Po20(SD)        LACP      Gi1/0(D)    Gi1/1(D)    

hq-a1#show spanning-tree vlan 199

VLAN0199
  Spanning tree enabled protocol rstp
  Root ID    Priority    24775
             Address     5254.006a.22f2
             Cost        6
             Port        65 (Port-channel10)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32967  (priority 32768 sys-id-ext 199)
             Address     5254.0002.4b8d
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi3/3               Desg FWD 4         128.16   P2p Edge 
Po10                Root FWD 3         128.65   P2p 

hq-a1#show ip interface brief | include Port-channel10|Port-channel20
Port-channel10         unassigned      YES unset  up                    up      
Port-channel20         unassigned      YES unset  administratively down down

HSRP ownership during failure — hq-d1 / hq-d2
---------------------------------------------

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
hq-d1#

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

Traffic continuity and probe state — hq-a1
------------------------------------------

hq-a1#
hq-a1#

hq-a1#ping 10.10.99.1 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 6/8/11 ms

hq-a1#ping 10.255.10.130 source 10.10.99.4 repeat 20
Type escape sequence to abort.
Sending 20, 100-byte ICMP Echos to 10.255.10.130, timeout is 2 seconds:
Packet sent with a source address of 10.10.99.4 
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 7/9/18 ms

hq-a1#show ip sla statistics 101
IPSLAs Latest Operation Statistics

IPSLA operation id: 101
        Latest RTT: 11 milliseconds
Latest operation start time: 19:05:05 UTC Sat Oct 3 2026
Latest operation return code: OK
Number of successes: 541
Number of failures: 10
Operation time to live: Forever

hq-a1#show ip sla statistics 102
IPSLAs Latest Operation Statistics

IPSLA operation id: 102
        Latest RTT: 6 milliseconds
Latest operation start time: 19:05:06 UTC Sat Oct 3 2026
Latest operation return code: OK
Number of successes: 542
Number of failures: 10
Operation time to live: Forever

hq-a1#
```

</details>

---

[◀ Previous record](HQ-VP-10.06-mode-a-po10-no-impact-control.md) · [↑ Test evidence](README.md) · [Next record ▶](HQ-VP-10.06-mode-b-vlan112-setup-baseline.md)
