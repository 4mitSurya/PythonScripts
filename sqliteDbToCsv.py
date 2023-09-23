import sqlite3, csv, os, datetime
from datetime import timedelta

dbfile_dir ="/path/of/db/files/"
csvfile_dir="/path/to/store/csv/files"

#provide database selecct query to read from database file
query = "<select query>"

n=0
m=0
l=0
t=0
p=0

for filename in os.listdir(dbfile_dir):

	t=t+1

	dbfile=os.path.join(dbfile_dir, filename)
	#print(dbfile)

	conn = sqlite3.connect(dbfile)

	conn.text_factory = str

	c = conn.cursor()

	try:

		c.execute(query)

	except (sqlite3.OperationalError, sqlite3.DatabaseError) as z:
	
		if 'no such table:' in str(z):
			l=l+1
			#print l
			continue
		elif 'file is encrypted or is not a database' in str(z):
			p=p+1
			#print l
			continue

	try:

		csvfile=csvfile_dir+filename[:-2]+'csv'
		#print(csvfile)

		with open(csvfile, 'wb') as f:

			writer = csv.writer(f)

			writer.writerows(c)

	except sqlite3.OperationalError:
		m=m+1
		#print m
		continue

	n=n+1
	#print n

print "Total DB Files                        : %05d"%t
print "DB Files processed successfully       : %05d"%n
print "DB Files with corrupt data            : %05d"%m
print "DB Files with wrong DB Schema         : %05d"%l
print "DB Files encrypted or not a database  : %05d"%p
