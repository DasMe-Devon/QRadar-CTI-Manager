#!/usr/bin/python

"""
	Twitter: @DasMe_Devon
	Email: SlyDGotcha[at]gmail[dot]com
	
	Automated QRadar CTI Reference Dataset Manager 
		* Requires python requests library
		* RATT requires API key request from Nathan Fowler Nathan[at]packetmail[dot]net
		* Currently only pulls IP addresses
"""

try:
	import requests
except:
	print ("Python Requests is missing.\n\t - Install using: pip install requests.\n\t - If pip is not installed, download from: https://github.com/kennethreitz/requests")
	exit()

# Setup Required Header Information (Prompt for Key)
server = raw_input("Enter the IP address of your QRadar Console: ")
addInfo = {'SEC':raw_input("Enter token: ")}
 
#If you prefer to hard code your token and run as a scheduled task/cron job, uncomment this line and comment the line above.
#addInfo = {'SEC':'REPLACE WITH YOUR TOKEN'}	

def main():
	checkDataSets()
	"""
		Fetches information from https://zeustracker.abuse.ch/blocklist.php
		Uncomment the function below to enable.
	"""
	fetchZeusTrackerList()
	"""
		Fetches information from http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv
		Uncomment the function below to enable.
	"""
	fetchTorNodeList()
	"""
		MiscreantsPlusPlus requires API key request from nathan fowler [Nathan.Fowler@zionsbancorp.com]
		Uncomment the line and functions below to enable.
	"""
	#If you wish to hardcode your key, uncomment the line below and comment the one after it.
	#mppKey = 'Your MiscreantsPlusPlus Key Here'
	mppKey = raw_input("Enter your MiscreantsPlusPlus Key: ")
	fetchRATTPubList()
	fetchRATTPrivList(mppKey)

def checkDataSets():
	datasetNames = ['CTI_IPs_TOR','CTI_IPs_MPP','CTI_IPs_Zeus']
	for name in datasetNames:
		dataz = {'name':name,'element_type':'IP','timeout_type':'LAST_SEEN'}
		req = requests.post('https://'+server+'/api/reference_data/sets', verify=False, data=dataz, headers=addInfo)
		if(req.status_code == 201):
			print("Successfully created %s\n" % name)
		elif(req.status_code == 409):
			print("%s already exists!\n" % name)
		else:
			print("Author done goofed! Encountered an issue with %s. Please post on github for assistance.\nReturn Code: %i" % (name,req.status_code))

def addDataToSet(datasetName,IP,Source):
	paramz = {'value':IP,'source':Source}
	req = requests.post('https://'+server+'/api/reference_data/sets/'+datasetName, verify=False, headers=addInfo, params=paramz)
	req.close()

def fetchZeusTrackerList():
	hInfo = {'user-agent':'QRadar-CTI-Manager'}
	paramz = {'download':'ipblocklist'}
	req = requests.get('https://zeustracker.abuse.ch/blocklist.php',params=paramz, headers=hInfo)
	IPs = req.text.split('\n')[6:-1]
	for IP in IPs:
		addDataToSet('CTI_IPs_Zeus',IP,'ZeusTracker')
	
	print "Successfully added %d IPs from ZeusTrackerList" % len(IPs)
	req.close()
	
def fetchTorNodeList():
	hInfo = {'user-agent':'QRadar-CTI-Manager'}
	req = requests.get('http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv', headers = hInfo)
	IPs = req.text.split('\n')
	for IP in IPs:
		addDataToSet('CTI_IPs_TOR',IP,'TorTracker')
		
	print "Successfully added %d IPs from TorNodeList." % len(IPs)
	req.close()

def fetchRATTPubList():
	hInfo = {'user-agent':'QRadar-CTI-Manager'}
	req = requests.get('https://www.packetmail.net/iprep.txt')
	intel = req.text.split('\n')[31:]
	for item in intel:
		IP = str(item.split(';')[0])
		addDataToSet('CTI_IPs_MPP',IP,'MPP')
	
	print "Successfully added %d IPs from MiscreantsPlusPlus (Public)." % len(intel)
	req.close()

def fetchRATTPrivList(mppKey):
	hInfo = {'user-agent':'QRadar-CTI-Manager'}
	req = requests.get('https://punchplusplus.miscreantpunchers.net/feeds.php?feed=iprep.txt&apikey='+mppKey)
	intel = req.text.split('\n')[19:]
	for item in intel:
		IP = str(item.split(';')[0])
		addDataToSet('CTI_IPs_MPP',IP,'RATT')
	print "Successfully added %d IPs from MiscreantsPlusPlus (Private)." % len(intel)
	req.close()

if(__name__ == "__main__"):
	main()