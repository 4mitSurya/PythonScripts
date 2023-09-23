# PythonScripts
Python scripts developed to collect, analyse, summarise logs/feeds or for automating stuff.

**I. libtaxiiV1.py:**

  A python script to poll the ctix/taxii version 1 feeds using libtaxii module.

  This script discovers the "COLLECTION_MANAGEMENT" url and "POLL" url.
  With discovered "COLLECTION_MANAGEMENT" url, the script polls feeds from all the available collection/subscription.

  Input the url, credentials and other details at the beginning and run the script.

  Dependencies:
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
  
  Dependencies:
  1. taxii2client.v20
  2. os
  3. datetime
  4. requests
  5. json
  6. datetime

**III. summaryJsonGz.py:**

  A python script to read json data from json files and summarize them based on fields.

  If your logs do not have .gz extention, replace gzip.open on line #22 with open.
  
  Dependencies:
  1. json
  2. gzip
  3. os
  4. collections

**IV. sqliteDbToCsv.py:**

  A python script to export data from sqlite db files to csv files.

  The script reads rows from .db sqlite files without authentication.
