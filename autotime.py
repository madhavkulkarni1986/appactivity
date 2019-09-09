from win32gui import GetForegroundWindow
from win32gui import GetClassName
from time import sleep
from datetime import datetime
from win32process import GetWindowThreadProcessId
from psutil import Process
import sys
import os
import json

'''
Sample JSON entry:-
{
	"activity" : [
			{
				"name": "chrome",
				"time": [
					{
						start: "09:25:16",
						end: "09:27:11",
						hours: "0" ,
						min: "1",
						sec: "55",
					}
					{
						start: "10:01:05",
						end: "10:13:45",
						hours: "0",
						min: "12",
						sec: "40",
					}
				]
			},
	]
}
'''

def get_activity(app):
	''' Return true if the activity is already present in the dictionary '''
	if(len(activitydata) == 0):
		return False
	for entry in activitydata['activity']:
		if(entry['name'] == app):
			return True
	return False

def add_activity(app, stime, etime, diff_time, appexists):
	''' Add activty(app, start time, end time, hourse, mins, secs) to the dictionary'''
	global activitydata
	h,m,s=str(diff_time).split(":")
	timejson={
		"start":stime,
		"end":etime,
		"hours":h,
		"min":m,
		"sec":s
	}
	if(appexists):
		for entry in activitydata['activity']:
			if(entry['name'] == app):
				entry['time'].append(timejson)
	else:
		activityjson={
			"name":app,
			"time":[
				timejson
			]
		}
		if (len(activitydata) == 0):
			activitydata={
				"activity":[
					activityjson
				]
			}
		else:
			activitydata['activity'].append(activityjson)

def readactivityfile(activityfile):
	''' Read the activity file into the dictionary '''
	with open(activityfile, "r") as f:
		data=json.load(f)
	return data

def writeactivityfile(activityfile, data):
	''' Write the activity dictionary to activity file '''
	with open(activityfile, "w+") as f:
		json.dump(data, f, indent=3, sort_keys=True)


## Main ##
## Get the current process name
curWin=((Process(GetWindowThreadProcessId(GetForegroundWindow())[-1]).name()).split('.')[0]).lower()
# Set the start time
stime=datetime.now().time().strftime('%H:%M:%S')

# Initialize dictionary and the json output file
activitydata=dict()
activityfile=os.path.dirname(os.path.realpath(__file__)) + '\\activity.json'

# Check if json file exists. If yes, load the file into dictionary
if(os.path.exists(activityfile)):
	activitydata=readactivityfile(activityfile)

# Continuously run the app
while(True):
	try:
		# Get the name of curent active window
		window=((Process(GetWindowThreadProcessId(GetForegroundWindow())[-1]).name()).split('.')[0]).lower()
		# If it is not same as curWin, process the data and make an entry into dictionary
		if(window != curWin):
			etime=datetime.now().time().strftime('%H:%M:%S')
			diff_time=datetime.strptime(etime, '%H:%M:%S') - datetime.strptime(stime, '%H:%M:%S')
			app=curWin
			appexists=get_activity(app)
			add_activity(app, stime, etime, diff_time, appexists)
			writeactivityfile(activityfile, activitydata)
			print("App: " + app + "\tStime: "+ str(stime) + "\tEtime: " + str(etime) +"\tTdiff: " + str(diff_time))			
			stime=datetime.now().time().strftime('%H:%M:%S')
			curWin=window
		sleep(3)
	except KeyboardInterrupt:
		print("\nStopping...")
		sys.exit()