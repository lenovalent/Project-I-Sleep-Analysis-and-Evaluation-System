import requests
import simplejson as json
import json
import datetime
import time
import csv
import numpy as np

file_head = "time,mstime,acc_x,acc_y,acc_z"
write_file=[]
write_file.append(file_head)
#sign-in to get access
url = 'https://api.wolksense.com/api/signIn'
data = {'email': 'cpoommitol@gmail.com', 'password': 'hr3kde0e'}
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)
recv = json.loads(json.dumps(r.json()))

#use token to get data
accessToken = recv['accessToken']

#set date to extract data
from_date = '1487523600000'
to_date = '1487610000000'
#to_date = '1487534340000'
#to_date = '1487534220000'
feedId = '77172'

extract_uri = 'https://api.wolksense.com/api/v2/feeds/'+feedId+'/readings?from='+ from_date + '&to=' + to_date + '&aggregationLevel=ONE_MINUTE'
extract_headers = {'Content-type': 'application/json',
                   'Authorization': str(accessToken)}
r = requests.get(extract_uri,headers=extract_headers)
recv = json.loads(json.dumps(r.json()))


time_latch = 0
time_c = 0
for epoch in recv:
    times = datetime.datetime.fromtimestamp(int(epoch["t"])/1000).strftime('%Y-%m-%d %H:%M:%S')   
    acc_x, acc_y, acc_z = epoch["a"].split(',')
    wrt = str(times) + "," + str(int(epoch["t"])) + ',' + str(acc_x) + ',' + str(acc_y) + ',' + str(acc_z)
    write_file.append(wrt)

file_name = time.strftime('wolksense_acc_%Y-%m-%d_%H:%M:%S') + '.csv'
with open(file_name, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(write_file)
csvwrite.close()
