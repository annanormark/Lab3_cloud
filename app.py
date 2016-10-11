#!flask/bin/python

from celery import Celery
from celery import group
from tasks import parseTweets
from flask import Flask, jsonify
import subprocess
import sys
import os
import swiftclient.client
import json
import time
import urllib2
from collections import Counter

app = Flask(__name__)
#app = Celery('tasks', backend='amqp', broker='amqp://an:no@130.238.29.13:5672/anno')



#@app.route('/test', methods=['GET'])
#def print_hello():
#	return 'Tjo Valle! Allt bra? :)', 200
#@app.task()
@app.route('/Labb3/messaging', methods=['GET'])
def cow_say():
	req = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets")
	response = urllib2.urlopen(req)
	tweetsObject = response.read().split()


	job = group(parseTweets(i) for i in tweetsObject)
	tweetTask = job.apply_async()
	#tweetTask.save()

	print "Celery is working..."
	counter = 0
	while (tweetTask.ready() == False):
		#print "... %i s" %(counter)
		counter += 5
		time.sleep(5)
	print "The task is done!"

	toReturn = tweetTask.get()

	c = Counter()
	for d in toReturn:
		c.update(d)
	
	display = dict(c)
	return jsonify(display), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)