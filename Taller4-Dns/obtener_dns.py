import sys
from scapy.all import *

qname = sys.argv[1]
dns = DNS(rd=1,qd=DNSQR(qname=qname,qtype="MX")) # ahora es una query MX
udp = UDP(sport=RandShort(), dport=53)
ips = [	IP(dst="198.41.0.4"),\
		IP(dst="199.9.14.201"),\
		IP(dst="192.33.4.12"),\
		IP(dst="199.7.91.13"),\
		IP(dst="192.203.230.10"),\
		IP(dst="192.5.5.241"),\
		IP(dst="192.112.36.4"),\
		IP(dst="198.97.190.53"),\
		IP(dst="192.36.148.17"),\
		IP(dst="192.58.128.30"),\
		IP(dst="193.0.14.129"),\
		IP(dst="199.7.83.42"),\
		IP(dst="202.12.27.33")] # ahora es una lista de ips
								# empieza con todos los root servers, no se si es necesario
ns_to_ar = {} # diccionario {name server : ip} (auxiliar)
dom_ns_ip = {} # diccionario {dominio: {name server : ip}}
mx_ip = {} # diccionario {mail server: ip}

for ip in ips:
	
	print "\n\n",ip.dst,"\n"
	answer = sr1( ip / udp / dns , verbose=0, timeout=10)
	
	if answer == None: 
		print "No responde"
		continue

	if answer.haslayer(DNS) and answer[DNS].qd.qtype == 15: # MX

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
				an_name = answer[DNS].an[i].rrname
				an_exchange = answer[DNS].an[i].exchange
				if (not an_exchange in mx_ip) and (an_exchange in ns_to_ar):
					mx_ip[an_exchange] = ns_to_ar[an_exchange] # lo agrego si es nuevo
				print an_name, an_exchange


print "\n\nNIVELES VISTOS"
for dom in dom_ns_ip:
	print dom
	for ns in dom_ns_ip[dom]:
		print "\t",ns,dom_ns_ip[dom][ns]

print "\n\nMAIL SERVERS"
for mx in mx_ip:
	print mx, mx_ip[mx]

# PENSAR: hay que hacer algo con SOA?