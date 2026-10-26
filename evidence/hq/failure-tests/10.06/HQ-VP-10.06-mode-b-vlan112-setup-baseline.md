[Portfolio](../../../../README.md) / [Evidence Map](../../README.md) / [Phase 10](../README.md) / [10.06](README.md) / Capture / record

# HQ-VP-10.06 — Mode B VLAN112 setup baseline

HQ-VP-10.06 — Access Uplink Failure
===================================

Mode B VLAN112 temporary probe setup and baseline
-------------------------------------------------

Capture date: 03-10-2026

Source: Device console capture, 03-10-2026.

Editorial note:
Selected verbatim CLI excerpts are retained. The intervening Po10 recovery
check duplicated evidence already retained in the Mode A control file and is
omitted here. Section labels are editorial.

Address availability check — hq-d1
----------------------------------

hq-d1#ping 10.10.12.4 repeat 3
Type escape sequence to abort.
Sending 3, 100-byte ICMP Echos to 10.10.12.4, timeout is 2 seconds:
...
Success rate is 0 percent (0/3)

hq-d1#show ip arp 10.10.12.4
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.10.12.4              0   Incomplete      ARPA   
hq-d1#

Mode B configuration and baseline — hq-a1
-----------------------------------------

hq-a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#no ip sla schedule 101
hq-a1(config)#no ip sla schedule 102
hq-a1(config)#end
hq-a1#
hq-a1#

hq-a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#interface Vlan112
hq-a1(config-if)# ip address 10.10.12.4 255.255.252.0
hq-a1(config-if)# no shutdown
hq-a1(config-if)#exit
hq-a1(config)#no ip default-gateway 10.10.99.1
hq-a1(config)#ip default-gateway 10.10.12.1
hq-a1(config)#end
hq-a1#
hq-a1#
hq-a1#

hq-a1#show ip interface brief | include Vlan112|Vlan199
Vlan112                10.10.12.4      YES manual up                    up      
Vlan199                10.10.99.4      YES NVRAM  up                    up      

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

hq-a1#ping 10.10.12.1 source 10.10.12.4 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.12.1, timeout is 2 seconds:
Packet sent with a source address of 10.10.12.4 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 4/205/1005 ms

hq-a1#ping 10.255.10.129 source 10.10.12.4 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.255.10.129, timeout is 2 seconds:
Packet sent with a source address of 10.10.12.4 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 4/6/9 ms

hq-a1#ping 10.255.10.130 source 10.10.12.4 repeat 5
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.255.10.130, timeout is 2 seconds:
Packet sent with a source address of 10.10.12.4 
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 6/7/8 ms
hq-a1#

Mode B IP SLA configuration and initial state — hq-a1
-----------------------------------------------------

hq-a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#no ip sla 101
hq-a1(config)#no ip sla 102
hq-a1(config)#
hq-a1(config)#ip sla 101
hq-a1(config-ip-sla)# icmp-echo 10.255.10.130 source-interface Vlan112
hq-a1(config-ip-sla-echo)# tag HQ-R2-Loopback0
hq-a1(config-ip-sla-echo)# threshold 500
hq-a1(config-ip-sla-echo)# timeout 800
hq-a1(config-ip-sla-echo)# frequency 1
hq-a1(config-ip-sla-echo)#exit
hq-a1(config)#
hq-a1(config)#ip sla 102
hq-a1(config-ip-sla)# icmp-echo 10.255.10.129 source-interface Vlan112
hq-a1(config-ip-sla-echo)# tag HQ-R1-Loopback0
hq-a1(config-ip-sla-echo)# threshold 500
hq-a1(config-ip-sla-echo)# timeout 800
hq-a1(config-ip-sla-echo)# frequency 1
hq-a1(config-ip-sla-echo)#exit
hq-a1(config)#
hq-a1(config)#ip sla schedule 101 life forever start-time now
hq-a1(config)#ip sla schedule 102 life forever start-time now
hq-a1(config)#end
hq-a1#

hq-a1#show ip sla statistics 101
IPSLAs Latest Operation Statistics

IPSLA operation id: 101
        Latest RTT: 8 milliseconds
Latest operation start time: 19:46:03 UTC Sat Oct 3 2026
Latest operation return code: OK
Number of successes: 1
Number of failures: 0
Operation time to live: Forever

hq-a1#show ip sla statistics 102
IPSLAs Latest Operation Statistics

IPSLA operation id: 102
        Latest RTT: 8 milliseconds
Latest operation start time: 19:46:07 UTC Sat Oct 3 2026
Latest operation return code: OK
Number of successes: 4
Number of failures: 0
Operation time to live: Forever

hq-a1#

---

[◀ Previous record](HQ-VP-10.06-mode-a-po20-access-uplink-failure.md) · [↑ Test evidence](README.md) · [Next record ▶](HQ-VP-10.06-mode-b-po10-failure-state.md)
