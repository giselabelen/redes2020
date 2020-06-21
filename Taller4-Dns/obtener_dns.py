from scapy.all import *

dns = DNS(rd=1,qd=DNSQR(qname="www.dc.uba.ar"))
udp = UDP(sport=RandShort(), dport=53)
ips = [IP(dst="199.9.14.201")] # ahora es una lista de ips
ns_to_ar = {} # diccionario {name server : ip}
nss = [] # lista de name servers
hay_respuesta = False

while not hay_respuesta: # voy a iterar hasta tener an > 0

	for ip in ips: # miro cada ip que tengo para esa iteracion hasta que una me responda
	
		answer = sr1( ip / udp / dns , verbose=0, timeout=10)
		
		if answer == None: continue

		if answer.haslayer(DNS) and answer[DNS].qd.qtype == 1:

			print "AUTHORITY" # armo el dic ns_to_ar
			for i in range( answer[DNS].arcount):
				ns = answer[DNS].ar[i].rrname
				ar = answer[DNS].ar[i].rdata
				if answer[DNS].ar[i].type == 1:
					ns_to_ar[ns] = IP(dst=ar)
				elif ns not in ns_to_ar:
					ns_to_ar[ns] = IPv6(dst=ar)
				print ns, ar

			print "NAME SERVERS" # me guardo los ns
			for i in range( answer[DNS].nscount):
				nss.append(answer[DNS].ns[i].rdata)
				print answer[DNS].ns[i].rrname, answer[DNS].ns[i].rdata
			
			print "ANSWER" 
			for i in range( answer[DNS].ancount):
				hay_respuesta = True
				print answer[DNS].an[i].rrname, answer[DNS].an[i].rdata

		break

	ips = [] # actualizo la lista de ips con las de esta iteracion
	for ns in nss:
		if ns in ns_to_ar: ips.append(ns_to_ar[ns])
	ns_to_ar = {}
	nss = []

	# TODO: VER EL COSO DE MX
	## hasta ahora muestra todas las respuestas
	## hay que llegar a un registro MX