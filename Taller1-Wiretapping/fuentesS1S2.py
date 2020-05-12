#!/usr/bin/python

from math import *
from scapy.all import *

S1 = {}
S2 = {}

def mostrar_fuente(S):
	N = sum(S.values())
	print "\ncant frames: %d" % (N)
	simbolos = sorted(S.iteritems(), key=lambda x: -x[1])
	entropia = 0
	for d,k in simbolos:
		prob = k/N # k/N es la prob de ese simbolo
		info = - math.log(prob,2) # info de ese simbolo
		entropia += prob*info # acumulo para la entropia
		print "\n %s : %.5f --- %s %.5f" % (d,prob,"Info: ",info)
	print "\n %s : %.5f" % ("Entropia: ",entropia)
	print "\n -----------"

def callback(pkt):
	# para S1
	if pkt.haslayer(Ether):
		dire = "BROADCAST" if pkt[Ether].dst=="ff:ff:ff:ff:ff:ff" else "UNICAST"
		proto = pkt[Ether].type # El campo type del frame tiene el protocolo
		s_i = (dire, proto) # Aca se define el simbolo de la fuente
		if s_i not in S1: S1[s_i] = 0.0
		S1[s_i] += 1.0
	# para S2
	if pkt.haslayer(ARP):
		src = pkt[ARP].psrc # Origen
		dst = pkt[ARP].pdst # Destino
		r_i = (src,dst)
		if r_i not in S2: S2[r_i] = 0.0
		S2[r_i] += 1.0


	mostrar_fuente(S1)
	mostrar_fuente(S2)

sniff(prn=callback)
