#!/usr/bin/python

import sys
from scapy.all import*

ports = range(1025)
#ip = sys.argv[1]
ip = socket.gethostbyname(sys.argv[1])
#print ip

print "Pruebas TCP"
for i in ports:
	p = IP(dst=ip)/TCP(dport=i, flags='S')
	print i,

	resp = sr1(p, verbose=False, timeout=8)
	if resp is None:
		print "filtrado"
	elif resp.haslayer(TCP):
		tcp_layer = resp.getlayer(TCP)
		if tcp_layer.flags == 0x12:
			print "abierto", tcp_layer.flags
			sr1(IP(dst=ip)/TCP(dport=ports, flags='AR'), verbose=False, timeout=1)
		elif tcp_layer.flags == 0x14:
			print "cerrado", tcp_layer.flags
		else:
			print "TCP ",tcp_layer.flags # esto es por si vienen otros flags (no creo)
	else:
		print resp.summary() # esto es por si pasa algo distinto, muestra todo



print "Pruebas UDP"
for i in ports:
	q = IP(dst=ip)/UDP(dport=i)
	print i,

	resp = sr1(q, verbose=False, timeout=8)
	if resp is None: 
	 	print "abierto o filtrado"
	elif resp.haslayer(UDP):
		print "abierto"
	elif resp.haslayer(ICMP):
		icmp_layer = resp.getlayer(ICMP)
		if icmp_layer.type == 0x03 and icmp_layer.code == 0x03:
			print "cerrado", icmp_layer.flags
		elif icmp_layer.type == 0x03 and icmp_layer.code in [0x09,0x0A,0x0D]:
			print "filtrado"
		else:
			print "ICMP ",icmp_layer.code # esto es por si me viene un codigo distinto
	else:
		print resp.summary() # esto es por si pasa algo distinto, muestra todo