import time, os, sys
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "m1.small"
private_net = "g2015034-net_2"

#config = {'username':os.environ['OS_USERNAME'], 
 #         'api_key':os.environ['OS_PASSWORD'],
  #        'project_id':os.environ['OS_TENANT_NAME'],
   #       'auth_url':os.environ['OS_AUTH_URL'],
    #       }

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_domain_name=env['OS_PROJECT_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print "user authorization completed."
# Create instanovae
import time 
image = nova.images.find(name="Ubuntu-16.04")
flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.networks.find(label=private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")
    

ud = open('userdata.yml', 'r')
secgroup = nova.security_groups.find(name="default")
secgroups = [secgroup.id]

#floating_ip = nova.floating_ips.create(nova.floating_ip_pools.list()[0].name)
#floating_ip_pool_name = nova.floating_ip_pools.list()[0].name

#if floating_ip_pool_name != None: 
#floating_ip = nova.floating_ips.create("130.238.29.31")#floating_ip_pool_name)
#else: 
 #   sys.exit("public ip pool name not defined.")


keypair = nova.keypairs.find(name="anno7997")

print "Creating instance ... "
instance = nova.servers.create(name="anno_lab3", image=image, flavor=flavor, userdata=ud, nics=nics,security_groups=secgroups, key_name = keypair.name)
inst_status = instance.status
print "waiting for 10 seconds.. "
time.sleep(10)

while inst_status == 'BUILD':
    print "Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more..."
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print "Instance: "+ instance.name +" is in " + inst_status + "state"

#if floating_ip.ip != None: 
#    instance.add_floating_ip("130.238.29.31")
#    print "Instance booted! Name: " + instance.name + " Status: " +instance.status+ ", floating IP attached " + floating_ip.ip
#else:
#    print "Instance booted! Name: " + instance.name + " Status: " +instance.status+ ", floating IP missing"
floating_ip = "130.238.29.31"
print 'attaching ip: ' 
print floating_ip
instance.add_floating_ip(floating_ip)






