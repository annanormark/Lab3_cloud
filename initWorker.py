from random import randrange
import swiftclient.client
import time, os, sys, inspect
from os import environ as env

import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL'],
           }
from novaclient client
from novaclient.client import Client
nova = Client('2',**config)

# Create instanovae
def initWrk(worker_number):
	worker_name = "anna_wrk_%i" %worker_number
	import time 
	print 1
	image = nova.images.find(name="Ubuntu-16.04")
	print 2
	flavor = nova.flavors.find(name="m1.small")
	print 3
	network = nova.networks.find(label="g2015034-net_2")
	keypair = nova.keypairs.find(name="anno7997")	
	ud = open('userdata2.yml', 'r')
	nova.keypairs.list()
	#f = open('cloud.key.pub','r')
	#publickey = f.readline()[:-1]
	#keypair = nova.keypairs.create('mathieukeypair',publickey)
	#f.close()
	instance = nova.servers.create(name = worker_name ,image = image.id,flavor = flavor.id,network = network.id,
	 key_name = keypair.name, userdata = ud)
	time.sleep(5)
	#try:
	#	if nova.floating_ips.list():
	#		floating_ip = nova.floating_ips.list()[0]
	#		print "*** uses old ip: %s ***" %(floating_ip.ip)
	#	else:
	#		floating_ip = nova.floating_ips.create(nova['floating_ip_pool'])
	#		print "*** no ip available, creating new ip: %s ***" %(floating_ip.ip)
	#	server.add_floating_ip(floating_ip)
	#except Exception as e:
	#	raise ProviderException("Failed to attach a floating IP to the controller.\n{0}".format(e))

	#floating_ip = nova.floating_ips.create(nova.floating_ip_pools.list()[0].name)
	#server.add_floating_ip(floating_ip)
	#print floating_ip.ip

	floating_ip_information_list = nova.floating_ips.list()
	floating_ip_list = []
	#print floating_ip_information_list
	for floating_ip_information in floating_ip_information_list:
		if getattr(floating_ip_information, 'fixed_ip') == None:
			floating_ip_list.append(getattr(floating_ip_information, 'ip'))

	if len(floating_ip_list) == 0:
		new_ip = nova.floating_ips.create(getattr(nova.floating_ip_pools.list()[0],'name'))
		print new_ip
		floating_ip_list.append(getattr(new_ip, 'ip'))

	floating_ip = floating_ip_list[0]

	#iplist = nova.floating_ips.list()
  	#if (len(iplist) < 1):
  	#	print "No IP:s available!"
   
  	#random_index = randrange(0,len(iplist))
  	#ip_obj = iplist[random_index] # Pick random address
  	#floating_ip = getattr(ip_obj, 'ip')
   
  	print "Attaching IP:"
  	print floating_ip
  	server.add_floating_ip(floating_ip)

#def main():
#	for i in range(6,8):
#		init(i)

if __name__ == "__main__":
	initWrk(1)

