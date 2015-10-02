QRadar-CTI-Manager
	+ Automated QRadar CTI Reference Dataset Manager 
		- Current
			* Requires python requests library
			* Creates the following reference sets:
				. CTI_IPs_Zeus
				. CTI_IPs_TOR
				. CTI_IPs_MPP
			* Pulls IP addresses from the following sources:
				. Zeus Tracker  https://zeustracker.abuse.ch/blocklist.php
				. TOR Exit Nodes http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv
				. MiscreantsPlusPlus https://punchplusplus.miscreantpunchers.net/feeds.php?feed=iprep.txt
					_ MiscreantsPlusPlus requires API key. Send request to Nathan[at]packetmail[dot]net
				. PacketMail https://www.packetmail.net/iprep.txt
			* Does not support time filtering (IE: Only previous 24 hours)
		- Future
			* Supporting other IOC types: Hashes, Domain Names
			* Supporting other Thread Feeds: Soltra Edge, AlienVault OTX, CriticalStack, iSight Partners
			* Allow auto creation of CTI Rules.
	+ Setup Instructions
		- 1 Install Python Requests if you haven't 
			* Install using: pip install requests
			* If pip is not installed, download from: https://github.com/kennethreitz/requests
		- 2 Navigate to QRadar Console > Admin Tab > Authorized Services
		- 3 Create an authorized token that the tool will use.
			* You will be prompted for this during script execution.
		- 4 Execute the script (You will be prompted for required information.)
	+ Notes
		- I've included comments you can uncomment to permanently store: Console IP; QRadar Token; MPP Key;
	

			
	

	