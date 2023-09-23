# PythonScripts
Python scripts developed for logs/threat feeds integration or for automating stuff

**I. libtaxiiV1.py:**

    A python script to poll the ctix/taxii version 1 feeds using libtaxii module.

    This script discovers the "COLLECTION_MANAGEMENT" url and "POLL" url.
    With discovered "COLLECTION_MANAGEMENT" url, the script polls feeds from all the available collection/subscription.

    Input the url, credentials and other details at the beginning and run the script.

    _Dependencies:_
    1. libtaxii
    2. xml.etree.ElementTree
    3. os
    4. re
    5. datetime
    6. time
    7. json
    8. datetime

**II. taxii2client.v20.py:**

    A python script to poll the ctix/taxii version 2 feeds using taxii2client.v20 module.

    The script polls the feeds from all the available collections/subscriptions.
  
    Input the url, credentials and other details at the beginning and run the script.
  
    _Dependencies:_
    1. taxii2client.v20
    2. os
    3. datetime
    4. requests
    5. json
    6. datetime
