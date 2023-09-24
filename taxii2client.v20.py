#create following directories
#1. Checkpoint
#2. Scripts
#3. IOCs

from taxii2client.v20 import Server, as_pages
import os, datetime, requests, json
from datetime import timezone

#provide path where all the directories are stored
path= "/path/of/directories/"

#provide base taxii2 url
baseUrl = "https://....."

#provide collection url without ending slash [/]
baseCollectionUrl = "https://....."

#provie credentials
user = "user"
password = "password"

#provide basic auth credential string
basicAuthCreds=""

# Instantiate server and get API Root
server = Server(baseUrl,user=user,password=password)
api_root = server.api_roots[0]

while True:
	if os.path.exists(path+"Checkpoint/lastPollTime.txt"):
		p = open(path+"Checkpoint/lastPollTime.txt",'r')
		added_after = p.read()

	else:
		added_after = datetime.datetime.strftime((datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=12)),'%Y-%m-%dT%H:%M:%S.%sZ')
		#added_after = "2022-08-19T14:00:00.0000000000Z"

	poll_time = datetime.datetime.strftime(datetime.datetime.now(timezone.utc),'%Y-%m-%dT%H:%M:%S.%sZ')

	# Print name and ID of all available collections
	for collection in api_root.collections:

		print("Polling IOCs for collection - %s from %s" %(collection.title,added_after))

		url=baseCollectionUrl+"/"+collection.id+"/objects/?added_after="+added_after
    
		headers = {
		'Accept': 'application/vnd.oasis.stix+json; version=2.0',
		'Range' : '0-20',
		'Authorization': basicAuthCreds
		}

		response = requests.get(url, headers=headers)

		IOCs = []

		if "Content-Range" in response.headers:
			total_IOCs=int(str(response.headers["Content-Range"])[str(response.headers["Content-Range"]).find('/')+1:len(str(response.headers["Content-Range"]))])
			print("Total IOCs found for %s: %s" %(collection.title,total_IOCs))

			lastValueOfRange = total_IOCs-1

			IOCs = response.json()

			n=21
			while n < lastValueOfRange:
				r1=n
				if n+21>=lastValueOfRange:
					r2=lastValueOfRange
				else:
					r2=n+20

				headers['Range'] = '%i-%i' %(r1,r2)

				response =  requests.get(url, headers=headers)

				IOCs['id'] = IOCs['id']+","+response.json()['id']
				IOCs['objects'].extend(response.json()['objects'])

				n = n+21

			with open(path+'IOCs/'+collection.title+'_'+poll_time[0:19].replace(":","")+'.json', 'w') as f:
				json.dump(IOCs, f)
			f.close()

			print("Dumped %s IOCs for %s to %s at 'path'" %(len(IOCs['objects']),collection.title,'IOCs/'+collection.title+'_'+poll_time[0:19].replace(":","")+'.json'))

		else:
			print("NO IOCs from %s upto now" %(added_after))

	with open(path+"Checkpoint/lastPollTime.txt", 'w') as f1:
		f1.write(poll_time)
	f1.close()

	print("Updated next poll_time to %s and dumped to %s at 'path'" %(poll_time,"Checkpoint/"+"lastPollTime.txt"))

	break
