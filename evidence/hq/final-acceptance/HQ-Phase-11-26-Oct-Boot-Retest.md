# Phase 11 — 26 October Startup Recheck

[Portfolio](../../../README.md) / [Phase 11 Evidence](README.md) / 26 October Startup Recheck

**Device:** `hq-a1` (IOSvL2)  
**Session:** 26 October 2026  
**Scope:** Repeat check of the VLAN199 SVI startup fault and its manual recovery, following the 16 October finding  
**Outcome:** Failure and recovery **reproduced**. Root cause **not established**.

## Observations

The recheck found `Vlan199` (`10.10.99.4/26`) `down/down`, and the management gateway `10.10.99.1` returned `0/5` pings. VLAN199 existed and was active; Po10 and Po20 both had two LACP members bundled. The trunk output permitted VLAN199 on both Port-Channels, with Po20 forwarding and Po10 blocking for that VLAN. The running and startup SVI configurations agreed. The SVI had no configured `shutdown`.

The detailed STP output showed Po20 as the root forwarding port. It also listed access port Gi3/3 as designated forwarding, even though `show interfaces GigabitEthernet3/3` reported `down/down (notconnect)`. Po20 was independently `up/up` and its counters showed received traffic; those counters do not prove that VLAN199 user traffic was passing. The filtered log showed earlier VLAN199 state changes during startup, but did not establish the reason for the later `down/down` state.

Issuing `no shutdown` on `interface Vlan199` alone left the SVI `down/down`, with gateway pings still `0/5`. A subsequent explicit `shutdown` and `no shutdown` brought the SVI to `up/up`, and the gateway replied `5/5`. An intermediate mistyped `notshutdown` was rejected by IOS and did not alter the configuration.

This reproduces the startup symptom and manual recovery recorded on 16 October. **It does not establish the underlying cause, identify a confirmed IOSvL2 software defect, or prove clean startup.** No new edge-loopback, OSPF or HSRP verification after the 26 October recovery is contained in this capture; the broader operational checks remain those recorded on 16 October. The relationship, if any, to the earlier Phase 10 Layer 2 isolation behaviour has not been established.

**Original first capture:** [26 October startup, VLAN/STP checks and logging — unedited TXT](HQ-Phase-11-26-Oct-Initial-CLI.txt). The later diagnostic and recovery excerpts below were supplied separately from the same session. The snippets retain the console text, including rejected commands, as provided.

## Subsequent CLI — SVI configuration and STP

<details>
<summary>Show SVI and VLAN199 STP checks</summary>

```text
hq-a1#show running-config interface Vlan199
Building configuration...

Current configuration : 83 bytes
!
interface Vlan199
 ip address 10.10.99.4 255.255.255.192
 no ip route-cache
end

hq-a1#show startup-config | section ^interface Vlan199
interface Vlan199
 ip address 10.10.99.4 255.255.255.192
 no ip route-cache
hq-a1#show ip interface Vlan199
Vlan199 is down, line protocol is down
  Internet address is 10.10.99.4/26
  Broadcast address is 255.255.255.255
  Address determined by configuration file
  MTU is 1500 bytes
  Helper address is not set
  Directed broadcast forwarding is disabled
  Outgoing access list is not set
  Inbound  access list is not set
  Proxy ARP is enabled
  Local Proxy ARP is disabled
  Security level is default
  Split horizon is enabled
  ICMP redirects are always sent
  ICMP unreachables are always sent
  ICMP mask replies are never sent
  IP fast switching is disabled
  IP Flow switching is disabled
  IP CEF switching is disabled
  IP Null turbo vector
  IP Null turbo vector
  IP multicast fast switching is disabled
  IP multicast distributed fast switching is disabled
          
hq-a1#how spanning-tree vlan 199 detail
       ^
% Invalid input detected at '^' marker.

hq-a1#show spanning-tree vlan 199 detail

 VLAN0199 is executing the rstp compatible Spanning Tree protocol
  Bridge Identifier has priority 32768, sysid 199, address 5254.0001.189a
  Configured hello time 2, max age 20, forward delay 15, transmit hold-count 6
  Current root has priority 24775, address 5254.00ed.4166
  Root port is 66 (Port-channel20), cost of root path is 3
  Topology change flag not set, detected flag not set
  Number of topology changes 2 last change occurred 00:08:52 ago
          from Port-channel20
  Times:  hold 1, topology change 35, notification 2
          hello 2, max age 20, forward delay 15 
  Timers: hello 0, topology change 0, notification 0, aging 300

 Port 16 (GigabitEthernet3/3) of VLAN0199 is designated forwarding 
   Port path cost 4, Port priority 128, Port Identifier 128.16.
   Designated root has priority 24775, address 5254.00ed.4166
   Designated bridge has priority 32967, address 5254.0001.189a
   Designated port id is 128.16, designated path cost 3
   Timers: message age 0, forward delay 0, hold 0
   Number of transitions to forwarding state: 5
   The port is in the portfast edge mode
   Link type is point-to-point by default
   Bpdu guard is enabled
   BPDU: sent 269, received 0
          
 Port 65 (Port-channel10) of VLAN0199 is alternate blocking 
   Port path cost 3, Port priority 128, Port Identifier 128.65.
   Designated root has priority 24775, address 5254.00ed.4166
   Designated bridge has priority 28871, address 5254.0017.2f24
   Designated port id is 128.65, designated path cost 3
   Timers: message age 16, forward delay 0, hold 0
   Number of transitions to forwarding state: 1
   Link type is point-to-point by default
   BPDU: sent 13, received 250

 Port 66 (Port-channel20) of VLAN0199 is root forwarding 
   Port path cost 3, Port priority 128, Port Identifier 128.66.
   Designated root has priority 24775, address 5254.00ed.4166
   Designated bridge has priority 24775, address 5254.00ed.4166
   Designated port id is 128.65, designated path cost 0
   Timers: message age 16, forward delay 0, hold 0
   Number of transitions to forwarding state: 1
   Link type is point-to-point by default
   BPDU: sent 4, received 253

hq-a1#
```

</details>

## Subsequent CLI — interface status

<details>
<summary>Show physical access port and Po20 status</summary>

```text
hq-a1# show interfaces GigabitEthernet3/3
GigabitEthernet3/3 is down, line protocol is down (notconnect) 
  Hardware is iGbE, address is 5254.00b7.817a (bia 5254.00b7.817a)
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Auto Duplex, Auto Speed, link type is auto, media type is RJ45
  output flow-control is unsupported, input flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input never, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/0 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     0 packets input, 0 bytes, 0 no buffer
     Received 0 broadcasts (0 multicasts)
     0 runts, 0 giants, 0 throttles 
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 0 multicast, 0 pause input
     0 packets output, 0 bytes, 0 underruns
          
hq-a1#show interfaces Port-channel20
Port-channel20 is up, line protocol is up (connected) 
  Hardware is EtherChannel, address is 5254.00f9.fee6 (bia 5254.00f9.fee6)
  MTU 1500 bytes, BW 2000000 Kbit/sec, DLY 10 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:00, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/2000/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 5000 bits/sec, 10 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     6172 packets input, 409148 bytes, 0 no buffer
     Received 0 broadcasts (0 multicasts)
     0 runts, 0 giants, 0 throttles 
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 input packets with dribble condition detected
     181 packets output, 24818 bytes, 0 underruns
     0 output errors, 0 collisions, 0 interface resets
     0 unknown protocol drops
     0 babbles, 0 late collision, 0 deferred
     0 lost carrier, 0 no carrier
     0 output buffer failures, 0 output buffers swapped out
hq-a1#
```

</details>

## Subsequent CLI — recovery

<details>
<summary>Show failed no-shutdown attempt and successful SVI reset</summary>

```text
hq-a1#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#interface Vlan199
hq-a1(config-if)# no shutdown
hq-a1(config-if)#end
hq-a1#show ip interface brief | include Vlan199
Vlan199                10.10.99.4      YES TFTP   down                  down    
hq-a1#ping 10.10.99.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)
hq-a1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
hq-a1(config)#int vlan199
hq-a1(config-if)#shutdown
hq-a1(config-if)#notshutdown
                   ^
% Invalid input detected at '^' marker.

hq-a1(config-if)#no shutdown
hq-a1(config-if)#end              
hq-a1#show ip interface brief | include Vlan199
Vlan199                10.10.99.4      YES TFTP   up                    up      
hq-a1#ping 10.10.99.1                          
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.99.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 4/204/1006 ms
hq-a1#
```

</details>

---

[← Phase 11 evidence index](README.md) · [Phase 11 engineering close-out](../../../docs/implementation/hq/phase-11-final-acceptance.md#overall-assessment)
