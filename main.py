"""PyNetcal, super-simple IP subnet calculator (IPv4/IPv6)

Usage:
  pynetcal subnetter flsm <network-address> <hosts> <subnets> [--priority=(hosts|subnets)] [--limit=<subnet-limit>]
  pynetcal subnetter vlsm <network-address> <subnet-size>...
  pynetcal ip <ip-address> [--dec-to-bin| --dec-to-hex| --bin-to-dec| --bin-to-hex| --hex-to-dec| --hex-to-bin| --check]
  pynetcal version

"""

from ipaddress import IPv4Network, IPv4Address, IPv6Network, IPv6Address
from docopt import docopt
import json
import sys


from pynetcal.ipv6pynetcal import PyNIPv6Address, PyNIPv6Network
from pynetcal.ipv4pynetcal import PyNIPv4Address, PyNIPv4Network
import pynetcal.helpers as helpers
import pynetcal.validator as validator


# retrieve arguments from CLI
arguments = docopt(__doc__,version=None)


# perform an action based on the commands
# and options passed from the CLI.


if(arguments["version"]):
	# show the app version.
	helpers.show_version()


elif(arguments['subnetter']):
	# do subnetting.
	if(arguments['flsm']):
		# do FLSM subnetting


		# retrieve arguments passed
		network = arguments['<network-address>']
		hosts = arguments['<hosts>']
		subnets = arguments['<subnets>']
		subnet_limit = arguments['--limit']
		
		if(subnet_limit is None):
			pass
		else:
			try:
				subnet_limit = int(subnet_limit)
			except:
				helpers.show_error("--limit argument must be an integer.")


		# do some validation first
		if(not validator.ipv4network(network) and not validator.ipv6network(network)):
			helpers.show_error("IPv4/IPv6 network address you supplied is invalid.")
			sys.exit()
		elif(not validator.integer(hosts)):
			helpers.show_error("number of <hosts> specified must be an integer.")
			sys.exit()
		elif(not validator.integer(subnets)):
			helpers.show_error("number of <subnets> specified must be an integer.")
			sys.exit()

		is_ipv4 = validator.ipv4network(network)
		is_ipv6 = validator.ipv6network(network)
		
		# all good continue with code.
		if(arguments['--priority']=='hosts'):
			priorityHosts = True
		elif(arguments['--priority']=='subnets'):
			priorityHosts = False
		elif(arguments['--priority']==None):
			priorityHosts = True
		else:
			priorityHosts = True
		
		subnetList = list()
		try:
			if(is_ipv4):
				subnetList = PyNIPv4Network(network).subnets_flsm(
				int(hosts),
				int(subnets),
				priorityHosts)
				num_of_subnets = PyNIPv4Network(network).num_of_subnets(int(hosts), int(subnets), priorityHosts)
				if(num_of_subnets > 50 and subnet_limit is None):
					helpers.show_warning("%d subnets to be shown. Output could get very long."%(num_of_subnets))
					userOption = input("Are you sure (y/n)? ")
					selection = list(userOption)
					if(selection[0] == 'y' or selection[0] == 'Y'):
						helpers.show_ipv4_subnet_table(network, hosts, subnets, subnetList, num_of_subnets, subnet_limit)
					else:
						exit(0)
				elif(num_of_subnets > 50 and subnet_limit is not None):
					helpers.show_ipv4_subnet_table(network, hosts, subnets, subnetList, num_of_subnets, subnet_limit)
				else:
					helpers.show_ipv4_subnet_table(network, hosts, subnets, subnetList, num_of_subnets, subnet_limit)
			if(is_ipv6):
				subnetList = PyNIPv6Network(network).subnets_flsm(
				int(hosts),
				int(subnets),
				priorityHosts)
				num_of_subnets = PyNIPv6Network(network).num_of_subnets(int(hosts), int(subnets), priorityHosts)
				if(num_of_subnets > 50 and subnet_limit is None):
					helpers.show_warning("%d subnets to be shown. Output could get very long."%(num_of_subnets))
					userOption = input("Are you sure you want to continue (y/n)? ")
					selection = list(userOption)
					if(selection[0] == 'y' or selection[0] == 'Y'):
						helpers.show_ipv6_subnet_table(network, hosts, subnets, subnetList, num_of_subnets, subnet_limit)
					else:
						exit(0)
				elif(num_of_subnets > 50 and subnet_limit is not None):
					helpers.show_ipv6_subnet_table(network, hosts, subnets, subnetList, num_of_subnets, subnet_limit)
				else:
					helpers.show_ipv6_subnet_table(network, hosts, subnets, subnetList, num_of_subnets, subnet_limit)

		except TypeError:
			helpers.show_error("Invalid IPv4/IPv6 network address passed")
			sys.exit()
		except KeyboardInterrupt:
			sys.exit()
		except Exception:
			helpers.show_error("Unknown error occured")
			sys.exit()


	elif(arguments['vlsm']):
		# do VLSM subnetting
		
		# retrieve the arguments passed
		network = arguments['<network-address>']
		hosts = arguments['<subnet-size>']
		
		
		# do some validation on the arguments
		if(not validator.ipv4network(network) and not validator.ipv6network(network)):
			helpers.show_error("IPv4/IPv6 network address you supplied is invalid.")
			sys.exit()

		for host in hosts:
			if(not validator.integer(host)):
				helpers.show_error("All <hosts> numbers must all be integers")
				sys.exit()

		is_ipv4 = validator.ipv4network(network)
		is_ipv6 = validator.ipv6network(network)


		# Now, get to work on VLSM.
		hosts = list(map(lambda i: int(i), hosts))
		try:
			if(is_ipv4):
				subnetList = PyNIPv4Network(network).subnets_vlsm(hosts)
				helpers.show_ipv4_subnet_table(network, hosts, len(hosts), subnetList, len(hosts))
			elif(is_ipv6):
				subnetList = PyNIPv6Network(network).subnets_vlsm(hosts)
				helpers.show_ipv6_subnet_table(network, hosts, len(hosts), subnetList, len(hosts))

		except ValueError:
			helpers.show_error("Specified number of hosts or \
				subnets cannot be accommodated")
			sys.exit()
				





elif(arguments['ip']):
	# do ipv4 manipulation tasks.
	# # validation, and determine if ipv6 or ipv4
	

	if(arguments["--dec-to-bin"]):
		address = arguments['<ip-address>']
		#do some validation on the arguments
		is_ipv4, is_ipv6 = False, False
		try:
			PyNIPv6Address(address)
			is_ipv6 = True
		except:
			is_ipv6 = False
		try:
			PyNIPv4Address(address)
			is_ipv4 = True
		except:
			is_ipv4 = False
		# go ahead for either ipv4 or ipv6
		if(is_ipv4):
			print(PyNIPv4Address(address).pn_binary)
		elif(is_ipv6):
			print(PyNIPv6Address(address).binary)
		else:
			helpers.show_error("IP address entered is not a valid IPv6 or IPv4 address")
			sys.exit()


	elif(arguments["--dec-to-hex"]):
		address = arguments['<ip-address>']
		#do some validation on the arguments
		is_ipv4, is_ipv6 = False, False
		try:
			PyNIPv6Address(address)
			is_ipv6 = True
		except:
			is_ipv6 = False
		try:
			PyNIPv4Address(address)
			is_ipv4 = True
		except:
			is_ipv4 = False
		# go ahead for either ipv4 or ipv6
		if(is_ipv4):
			print(PyNIPv4Address(address).pn_hexadecimal)
		elif(is_ipv6):
			print(PyNIPv6Address(address).hexadecimal)
		else:
			helpers.show_error("IP address entered is not a valid IPv6 or IPv4 address")
			sys.exit()


	elif(arguments["--bin-to-dec"]):
		address = arguments['<ip-address>']
		#do some validation on the arguments
		is_ipv4, is_ipv6 = False, False
		try:
			PyNIPv6Address(address)
			is_ipv6 = True
		except:
			is_ipv6 = False
		try:
			PyNIPv4Address(address)
			is_ipv4 = True
		except:
			is_ipv4 = False
		# go ahead for either ipv4 or ipv6
		if(is_ipv4):
			print(PyNIPv4Address(address).pn_decimal)
		elif(is_ipv6):
			print(PyNIPv6Address(address).decimal)
		else:
			helpers.show_error("IP address entered is not a valid IPv6 or IPv4 address")
			sys.exit()


	elif(arguments["--bin-to-hex"]):
		address = arguments['<ip-address>']
		#do some validation on the arguments
		is_ipv4, is_ipv6 = False, False
		try:
			PyNIPv6Address(address)
			is_ipv6 = True
		except:
			is_ipv6 = False
		try:
			PyNIPv4Address(address)
			is_ipv4 = True
		except:
			is_ipv4 = False
		# go ahead for either ipv4 or ipv6
		if(is_ipv4):
			print(PyNIPv4Address(address).pn_hexadecimal)
		elif(is_ipv6):
			print(PyNIPv6Address(address).hexadecimal)
		else:
			helpers.show_error("IP address entered is not a valid IPv6 or IPv4 address")
			sys.exit()


	elif(arguments["--hex-to-dec"]):
		address = arguments['<ip-address>']
		#do some validation on the arguments
		is_ipv4, is_ipv6 = False, False
		try:
			PyNIPv6Address(address)
			is_ipv6 = True
		except:
			is_ipv6 = False
		try:
			PyNIPv4Address(address)
			is_ipv4 = True
		except:
			is_ipv4 = False
		# go ahead for either ipv4 or ipv6
		if(is_ipv4):
			print(PyNIPv4Address(address).pn_decimal)
		elif(is_ipv6):
			print(PyNIPv6Address(address).decimal)
		else:
			helpers.show_error("IP address entered is not a valid IPv6 or IPv4 address")
			sys.exit()


	elif(arguments["--hex-to-bin"]):
		address = arguments['<ip-address>']
		#do some validation on the arguments
		is_ipv4, is_ipv6 = False, False
		try:
			PyNIPv6Address(address)
			is_ipv6 = True
		except:
			is_ipv6 = False
		try:
			PyNIPv4Address(address)
			is_ipv4 = True
		except:
			is_ipv4 = False
		# go ahead for either ipv4 or ipv6
		if(is_ipv4):
			print(PyNIPv4Address(address).pn_binary)
		elif(is_ipv6):
			print(PyNIPv6Address(address).binary)
		else:
			helpers.show_error("IP address entered is not a valid IPv6 or IPv4 address")
			sys.exit()


	elif(arguments["--check"]):
		# check that an ip address is a valid ipv4 address

		# fetch arguments to be used here.
		address = arguments['<ip-address>']
		
		# validation of arguments
		if(not validator.ipv4address(address) and
			not validator.ipv6address(address) and
			not validator.ipv4network(address) and
			not validator.ipv6network(address)):
			helpers.show_error("IP address or network not recognized.")
		elif(validator.ipv4address(address)):
			print("{} is a valid IPv4 address".format(address))
		elif(validator.ipv6address(address)):
			print("{} is a valid IPv6 address".format(address))
		elif(validator.ipv4network(address)):
			print("{} is a valid IPv4 network".format(address))
		elif(validator.ipv6network(address)):
			print("{} is a valid IPv6 network".format(address))
			

	else:
		# show IP address stats

		# fetch arguments to be used here.
		address = arguments['<ip-address>']
		
		# do some validation on the arguments
		if(not validator.ipv4address(address) and
			not validator.ipv6address(address) and
			not validator.ipv4network(address) and
			not validator.ipv6network(address)):
			helpers.show_error("IPv4/IPv6 address entered is invalid.")
			sys.exit()

		# identify whether it is an ipv4 or ipv6
		is_ipv4 = validator.ipv4address(address)
		is_ipv6 = validator.ipv6address(address)
		is_ipv4_net = validator.ipv4network(address)
		is_ipv6_net = validator.ipv6network(address)

		# show the IP address stats accordingly
		if(is_ipv4):
			addr = PyNIPv4Address(address)
			helpers.show_ipv4_address_stats(addr)
		elif(is_ipv6):
			addr = PyNIPv6Address(address)
			helpers.show_ipv6_address_stats(addr)
		elif(is_ipv4_net):
			addr = PyNIPv4Network(address)
			helpers.show_ipv4_network_stats(addr)
		elif(is_ipv6_net):
			addr = PyNIPv6Network(address)
			helpers.show_ipv6_network_stats(addr)