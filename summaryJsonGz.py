import json, gzip, os
from collections import Counter

LogFolderPath = input("Enter 'json.gz' ABSOLUTE Log Folder Path below with ending (back|forward)slash\n: ")

action = input("\nWhich of the followint action you would like to take?\n1. Find top field VALUE\n2. Find top unique field VALUE COUNT and PERCENTAGE\nPlease enter the corresponding number: ")

field = input("\nOn what field you want to perform this action? [CASE SENSETIVE]: ")

top = int(input("\nWhat top value you want to see? [e.g., top 5, top 10]\nEnter a number: "))

print("\nYou have chosen to view top " + str(top) + " values in " + field + "\n")

list = []

for file in os.listdir(LogFolderPath):
    filename = os.fsdecode(file)

    if filename.endswith("json.gz"):
        print("Processing File: %s" %(filename))

        with gzip.open(LogFolderPath+filename, "rb") as f:
            records = json.loads(f.read())

            for record in records["Records"]:
                list.append(record[field])

print("\n=====RESULT=====\n")

if action == "1":

    print("VALUE: COUNT")
    for key, count in Counter(list).most_common(top):
        print("%s: %d" %(key, count))

elif action == "2":

    print("VALUE|  COUNT|  PERCENTAGE")
    for key, count in Counter(list).most_common(top):
        print("%s|  %d|  %f" %(key, count, count/len(list)*100))
