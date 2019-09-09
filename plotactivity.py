### Simple script that reads the json file and displays the number of hrs/mins/secs spent on each app
from matplotlib import pyplot as plt
import sys
import json
from datetime import datetime

def readjson(actifile):
	with open(actifile, "r") as f:
		data=json.load(f)
	
	return data

data=readjson(sys.argv[1])
print("Below is your time count for apps:")
for d in data['activity']:
	
	h=0
	m=0
	s=0

	for t in d['time']:
		h=h+int(t['hours'])
		m=m+int(t['min'])
		s=s+int(t['sec'])
		if(s > 60):
			m=m+int(s/60)
			s=s%60
		if(m>60):
			h=h+int(m/60)
			m=m%60

	print("App: " + d['name'] + "\t\t\tTime spent: " + str(h) +':' + str(m) +':' + str(s))