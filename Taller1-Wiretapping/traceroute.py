#!/usr/bin/python
import sys
from scapy.all import *
from time import *

def main():
	responses = {}
	runs = 30

	for i in range(runs):
		print "\nCorrida %d" % i
		for ttl in range(1,40):
			probe = IP(dst=sys.argv[1], ttl=ttl) / ICMP()
			t_i = time()
			ans = sr1(probe, verbose=False, timeout=0.8)
			t_f = time()
			rtt = (t_f - t_i)*1000
			if ans is not None:
				if ttl not in responses: responses[ttl] = []
				responses[ttl].append((ans.src, rtt))
			if ttl in responses:
				print ".",  # print ttl, responses[ttl]
			else:
				print "*",

	print "" 	# fin de linea
	averages = {}

	for ttl in responses:
		print ttl, responses[ttl];
		ip = mode(responses[ttl])
		avg = average_by_ip(responses[ttl], ip)
		averages[ttl] = [ip, avg]

	for ttl in averages:
		print ttl, averages[ttl]

	print "\nHops:"
	previous_average = 0
	previous_ttl = ""
	first = True
	for ttl in averages:
		current_ip = averages[ttl][0]
		current_average = averages[ttl][1]
		if not first:
			diff = current_average - previous_average
			print "%s a %s: %f" % (previous_ttl, current_ip, diff)
		previous_average = current_average
		previous_ttl = current_ip

		first = False


def mode(tests):
	ips = {}
	maxvalue = 0
	maxkey = ""
	for test in tests:
		ip = test[0]
		if test[0] in ips:
			ips[ip] = ips[ip]+1
		else:
			ips[ip] = 1
		if ips[ip] > maxvalue:
			maxvalue = ips[ip]
			maxkey = ip

	return maxkey

def average_by_ip(tests, ip):
	total = 0
	quantity = 0
	for test in tests:
		if test[0] == ip:
			quantity = quantity+1
			total = total + test[1]

	return total/quantity

if __name__ == "__main__":
    main()

