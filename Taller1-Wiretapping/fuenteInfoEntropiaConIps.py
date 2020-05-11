#!/usr/bin/python

from math import *
from scapy.all import *

frames = 0
S1 = {}

def mostrar_fuente(S):
	global frames
	frames += 1
	N = sum(S.values())
	simbolos = sorted(S.iteritems(), key=lambda x: -x[1])
	entropia = 0
	for d,k in simbolos:
		prob = k/N # k/N es la prob de ese simbolo
		info = - math.log(prob,2) # info de ese simbolo
		entropia += prob*info # acumulo para la entropia
		print "\n %s : %.5f --- %s %.5f" % (d,prob,"Info: ",info)
	print "\n %s : %.5f" % ("Entropia: ",entropia)
	print "\n%d frames" % (frames)
	print "\n -----------"

def callback(pkt):
	if pkt.haslayer(Ether):
		proto = "0%x" % pkt[Ether].type # El campo type del frame tiene el protocolo
		src = pkt[Ether].src # Origen
		dst = pkt[Ether].dst # Destino
		s_i = (src, dst, proto) # Aca se define el simbolo de la fuente
		if s_i not in S1: S1[s_i] = 0.0
		S1[s_i] += 1.0

	mostrar_fuente(S1)

sniff(prn=callback)
