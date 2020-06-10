import sys
import os

# exportar la salida de port_scanner_tcp_udp y pasar ese archivito como argumento aca (path relativo)

path = os.getcwd()
filename = sys.argv[1]
filepath = os.path.join(path,filename) 

respuestas = {} # {puerto: {protocolo: respuesta}}

tipos_resp_UDP = {} # {respuesta UDP: lista de puertos con esa respuesta}
tipos_resp_TCP = {} # {respuesta TCP: lista de puertos con esa respuesta}
comp_resp_UDP_TCP = {} # {(respuesta UDP,respuesta TCP): lista de puertos con esas respuestas}

with open(filepath) as fp:

	for line in fp:
		if "Pruebas TCP" in line:
			protocolo = "TCP"
			tipos = tipos_resp_TCP

		elif "Pruebas UDP" in line:
			protocolo = "UDP"
			tipos = tipos_resp_UDP

		else:
			k = int(line.partition(' ')[0])
			v = line.partition(' ')[2]
			if k not in respuestas:
				respuestas[k] = {}
			respuestas[k][protocolo] = v

			if v not in tipos:
				tipos[v] = []
			tipos[v].append(k)

print "Respuestas TCP:"
for t in tipos_resp_TCP:
	print t,len(tipos_resp_TCP[t]) # respuesta TCP y cantidad de puertos con esa respuesta
print "\nRespuestas UDP:"
for t in tipos_resp_UDP:
	print t, len(tipos_resp_UDP[t]) # respuesta UDP y cantidad de puertos con esa respuesta

print "\nTodas las respuestas:"
for k in sorted(respuestas):
	print k,'-',respuestas[k] # puerto - {protocolo: respuesta}
	par_resp = (respuestas[k]['UDP'],respuestas[k]['TCP'])
	if par_resp not in comp_resp_UDP_TCP:
		comp_resp_UDP_TCP[par_resp] = []
	comp_resp_UDP_TCP[par_resp].append(k)

print "\nAgrupados por resp UDP y resp TCP"
for p in comp_resp_UDP_TCP:
	print p,len(comp_resp_UDP_TCP[p])
