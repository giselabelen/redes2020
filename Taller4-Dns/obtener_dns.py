from scapy.all import *

dns = DNS(rd=1,qd=DNSQR(qname="dc.uba.ar",qtype="MX")) # ahora es una query MX
udp = UDP(sport=RandShort(), dport=53)
ips = [IP(dst="199.9.14.201")] # ahora es una lista de ips
ns_to_ar = {} # diccionario {name server : ip} (auxiliar)
dom_ns_ip = {} # diccionario {dominio: {name server : ip}}

for ip in ips:
	
	print "\n\n",ip.dst,"\n"

	answer = sr1( ip / udp / dns , verbose=0, timeout=10)
	
	if answer == None: 
		print "No responde"
		continue

	if answer.haslayer(DNS) and answer[DNS].qd.qtype == 15:

		print "AUTHORITY" # armo el dic ns_to_ar
		for i in range( answer[DNS].arcount):
			ar_name = answer[DNS].ar[i].rrname
			ar_data = answer[DNS].ar[i].rdata
			if not ar_name in ns_to_ar: # lo agrego si es nuevo
				ns_to_ar[ar_name] = ar_data
			print ar_name, ar_data

		print "NAME SERVERS" # armo el dic dom_ns_ip
		for i in range( answer[DNS].nscount):
			ns_name = answer[DNS].ns[i].rrname
			ns_data = answer[DNS].ns[i].rdata
			if not ns_name in dom_ns_ip:
				dom_ns_ip[ns_name] = {}
			if (ns_data in ns_to_ar) and (ns_data not in dom_ns_ip[ns_name]): # lo agrego si es nuevo
				dom_ns_ip[ns_name][ns_data] = ns_to_ar[ns_data]
				ips.append(IP(dst=ns_to_ar[ns_data])) # me guardo esa ip nueva para iterar
			print ns_name, ns_data

		print "ANSWER" 
		for i in range( answer[DNS].ancount):
			print answer[DNS].an[i].rrname, answer[DNS].an[i].exchange


print "\n\nNIVELES VISTOS"
for dom in dom_ns_ip:
	print dom
	for ns in dom_ns_ip[dom]:
		print "\t",ns,dom_ns_ip[dom][ns]


# TODO: creo que deberiamos preguntar a todos los root servers y handlear en caso de recibir SOA