#!/usr/bin/python

import sys
from scapy.all import*

ports = [19, 20, 21, 22, 23, 53, 80]
ip = sys.argv[1]

for i in ports:
	p = IP(dst=ip)/TCP(dport=i, flags='S')
	print i,

	resp = sr1(p, verbose=False, timeout=0.2)
	if resp is None:
		print "filtrado"
	elif resp.haslayer(TCP):
		tcp_layer = resp.getlayer(TCP)
		if tcp_layer.flags == 0x12:
			print "abierto", tcp_layer.flags
			sr1(IP(dst=ip)/TCP(dport=ports, flags='AR'), verbose=False, timeout=1)
		elif tcp_layer.flags == 0x14:
			print "cerrado", tcp_layer.flags