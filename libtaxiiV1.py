import libtaxii as t
import libtaxii.clients as tc
import libtaxii.messages_11 as tm11
from libtaxii.constants import *
import xml.etree.ElementTree as ET
from datetime import timezone, timedelta
import json, datetime, time, re, os

# Create directories - Checkpoint, Details, IOCs, and Scripts
# Place this script in Scripts

# Path where script and other details are stored 
path = ""

# Is the url https?
is_https  = True

# Domain name in URL without https:// OR http://
taxiiDomain = 'example.com'

# Discovery URL path ri.e URL without without https://<taxiiDomain> OR http://<taxiiDomain> 
taxiiDiscoveryUrl='/url/path/to/discovery/service/'

# Cerdentials received from CERT-IN
username = 'user'
password = 'pass'

# Number of days past feeds you want to pull
days = 30

# Interval in seconds to wait before next run
interval = 21600

while True:
    # Create the TAXII HTTPS Client
    client = tc.HttpClient()

    # Uncomment to use HTTPS
    client.set_use_https(is_https)

    # Uncomment to use basic authentication
    client.set_auth_type(tc.HttpClient.AUTH_BASIC)
    client.set_auth_credentials({'username': username, 'password': password})

    # Uncomment to use certificate-based authentication
    #client.set_auth_type(tc.HttpClient.AUTH_CERT)
    #client.set_auth_credentials({'key_file': 'keyfile', 'cert_file': 'certfile'})

    # Uncomment to set a proxy
    #client.set_proxy(tc.HttpClient.PROXY_HTTP, 'http://proxy.company.com:80')
    
    # Discover collection url
    discovery_request = tm11.DiscoveryRequest(tm11.generate_message_id())

    http_resp = client.call_taxii_service2(taxiiDomain,taxiiDiscoveryUrl, VID_TAXII_XML_11, discovery_request.to_xml())
    discovery_taxii_message = t.get_message_from_http_response(http_resp, discovery_request.message_id)
    discovery=discovery_taxii_message.to_xml().decode()

    # Store discovery details in a file
    discoveryfile=path+"/Details/Discovery.xml"
    DFO=open(discoveryfile, "w")
    DFO.write(discovery)
    DFO.close()

    # Parse xml discovery details
    tree = ET.parse(discoveryfile)
    discovery_root = tree.getroot()
    
    for child in discovery_root:
        JO=json.loads(str(child.attrib).replace("'",'"'))
        if JO['service_type'] == 'COLLECTION_MANAGEMENT':
            i=0
            while True:
                try:
                    if re.match('.*?Address',child[i].tag):
                        m = re.search('(https://[^/]{0,}|http://[^/]{0,}).*?',child[i].text)
                        taxiiCollectionUrl = child[i].text[len(m.group()):]
                except IndexError:
                    break;
                i=i+1
                
    for child in discovery_root:
        JO=json.loads(str(child.attrib).replace("'",'"'))
        if JO['service_type'] == 'POLL':
            i=0
            while True:
                try:
                    if re.match('.*?Address',child[i].tag):
                        m = re.search('(https://[^/]{0,}|http://[^/]{0,}).*?',child[i].text)
                        taxiiPollUrl = child[i].text[len(m.group()):]
                except IndexError:
                    break;
                i=i+1

    # Query collection details
    collection_info = tm11.CollectionInformationRequest(tm11.generate_message_id())

    http_resp = client.call_taxii_service2(taxiiDomain,taxiiCollectionUrl, VID_TAXII_XML_11, collection_info.to_xml())
    collection_taxii_message = t.get_message_from_http_response(http_resp, collection_info.message_id)
    collections=collection_taxii_message.to_xml().decode()

    # Store collection details in a file
    collectionsfile=path+"/Details/Collections.xml"
    CFO=open(collectionsfile, "w")
    CFO.write(collections)
    CFO.close()

    # Parse xml collection details
    tree = ET.parse(collectionsfile)
    collections_root = tree.getroot()

    for child in collections_root:
        JO=json.loads(str(child.attrib).replace("'",'"'))
        CN=JO["collection_name"]
        
        checkpointfile=path+"/Checkpoint/" + CN + ".txt"
        
        if os.path.exists(checkpointfile):
            ChFO = open(checkpointfile,'r')
            checkpoint = ChFO.read()
            ChFO.close()
        else:
            checkpoint=(datetime.datetime.strftime(datetime.datetime.now() - timedelta(days=days),'%Y-%m-%dT%H:%M:%S'))

        collectionTime=(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%dT%H:%M:%S'))

        # Create the poll request
        poll_request = tm11.PollRequest(message_id=tm11.generate_message_id(), collection_name=CN,poll_parameters=tm11.PollParameters(),exclusive_begin_timestamp_label=checkpoint+'+05:30')

        # Call without a proxy
        http_response = client.call_taxii_service2(taxiiDomain,taxiiPollUrl, VID_TAXII_XML_11, poll_request.to_xml(),443)

        taxii_message = t.get_message_from_http_response(http_response,poll_request.message_id)
        output=taxii_message.to_xml().decode()

        ChFO=open(checkpointfile, "w")
        ChFO.write(collectionTime)
        ChFO.close()

        outputfile=open((path+"/IOCs/"+ CN + "_" + collectionTime.replace(":","") + ".xml"), "w")
        outputfile.write(output)

    print("Waiting "+str(interval)+" seconds before next run")
    time.sleep(interval)

