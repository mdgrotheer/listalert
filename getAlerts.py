import csv
from newrelic import getConfig, nrcomm
import argparse
import logging
import json
import datetime
from sys import *
import os

parser = argparse.ArgumentParser(description='Reset host not reporting globally')
parser.add_argument('-config_name', help='Config file example.conf')
parser.add_argument('-apikey_file', help='list of API Keys')
parser.add_argument('-start_date', help='Example 2018-10-26T19:43:00+00:00 in none will start from beginning')
args = parser.parse_args()
alertURL = ""

if args.config_name is None:
    print('Missing config_name')
    exit(1)
if args.apikey_file is None:
    print('Missing apikey_file')
    exit(1)

# Get Configuration

config = {}
config = getConfig.parseConfig(args.config_name)
logging.basicConfig(filename='nrproc.log', level=logging.INFO)
systemLog = logging.getLogger("__NR___")
logging.info("Start")


# Read apikey file

with open(args.apikey_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:

        print(row[0])
        nextpage=True
        pagecount = 0

        filename = row[0].replace(" ", "_") + '.csv'
        with open(filename, mode='w') as api_file:
            api_writer = csv.writer(api_file, delimiter=',', quotechar='"')
            fieldnames = ["id", "label", "policy_name", "condition_name", "priority", "opened_at", "eproduct", "etype",
                          "eid", "ename"]
            api_writer.writerow(fieldnames)

            while(nextpage):

                pagecount = pagecount + 1
                print("Processing Page: " + str(pagecount))

                if args.start_date is None:

                    alertURL = config['apiurl'] + '?page=' + str(pagecount)

                else:

                    alertURL = config['apiurl'] + '?page=' + str(pagecount) + "&start_date=" + args.start_date

                if args.start_date is None:
                    print('No Optional Start Date')
                else:
                    alertURL = alertURL + '&start_date=' + args.start_date

                response = nrcomm.nrGet(alertURL, row[1], logging)
                resultJson = json.loads(response)
                resultlen = len(resultJson["violations"])
                #print(resultJson)
                if resultlen > 0:
                    for apiresult in resultJson["violations"]:

                        id = apiresult["id"]
                        label = apiresult["label"]
                        duration = apiresult["duration"]
                        policy_name = apiresult["policy_name"]
                        condition_name = apiresult["condition_name"]
                        priority = apiresult["priority"]
                        opened_at = datetime.datetime.fromtimestamp(apiresult["opened_at"]/1000.0)
                        #closed_at = datetime.datetime.fromtimestamp(apiresult["closed_at"]/1000.0)
                        eproduct = apiresult["entity"]["product"]
                        etype = apiresult["entity"]["type"]
                        #eid = apiesult["entity"]["id"]
                        eid="99999"
                        ename = apiresult["entity"]["name"]

                        myrow = [id,label,policy_name,condition_name,priority,opened_at,eproduct,etype,eid,ename]

                        api_writer.writerow(myrow)

                else:
                    nextpage=False

        api_file.close()
