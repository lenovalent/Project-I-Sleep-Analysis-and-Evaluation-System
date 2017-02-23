import requests
import simplejson as json
import json
import datetime
import time
import csv
import sys
import numpy as np
import os

print "\n========================================="
print "Wolksense data extraction script started"
print "=========================================="
#print 'Argument List:', str(sys.argv[1]) ,str(sys.argv[2])
#g = (datetime.datetime(2017,2,21,0,tzinfo=ICT) - datetime.datetime.utcfromtimestamp(0))
#print '{:.0f}'.format(g.total_seconds()*1000)
t_start = time.time()
true_start = t_start
file_head = "time,mstime,gy_x,gy_y,gy_z"
file_head_act = "time,mstime,act_x,act_y,act_z,act_m"

write_file=[]
write_file.append(file_head)

write_file_act=[]
write_file_act.append(file_head_act)
#sign-in to get access
url = 'https://api.wolksense.com/api/signIn'
data = {'email': 'cpoommitol@gmail.com', 'password': 'hr3kde0e'}
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)
recv = json.loads(json.dumps(r.json()))
end = time.time() - t_start

print "Wolksense API key recieved time: ", end

t_start = time.time()
#use token to get data
accessToken = recv['accessToken']

#set date to extract data
#from_date = '1487642400000' #21 feb 0900
from_date = '1487782800000' #23 feb 0000
#from_date = '1487523600000' #20 feb

#from_date = '1487610000000'  #21 feb
to_date = '1487869200000' #24 feb 0000
#to_date ='1487803670722' #23 feb 0548
#to_date = '1487782800000' #23 feb
#to_date = '1487696400000'  #22 feb
#to_date = '1487610000000' #21 feb
#to_date = '1487534340000'
#to_date ='1487678400000'  #21 feb 1900
#to_date ='1487700000000' #22 feb 0100
#to_date = '1487534220000'
feedId = '77173'

extract_uri = 'https://api.wolksense.com/api/v2/feeds/'+feedId+'/readings?from='+ from_date + '&to=' + to_date + '&aggregationLevel=ONE_MINUTE'
extract_headers = {'Content-type': 'application/json',
                   'Authorization': str(accessToken)}
r = requests.get(extract_uri,headers=extract_headers)
recv = json.loads(json.dumps(r.json()))
end = time.time() - t_start

print "Wolksense Data recieved time: ", end

t_start = time.time()

gy_all_latch = []
gy_all_dict = []
gy_x_latch = []
gy_y_latch = []
gy_z_latch = []

first = 0

time_latch = 0
time_c = 0
for epoch in recv:
    timec = int(epoch["t"])
    times = datetime.datetime.fromtimestamp(int(epoch["t"])/1000).strftime('%Y-%m-%d %H:%M:%S')   
    if time_latch != timec:        
        if first == 0:
        	first+=1
        else:
            gy_all_latch.append(gy_x_latch)
            gy_all_latch.append(gy_y_latch)
            gy_all_latch.append(gy_z_latch)
            dicta = {time_latch:gy_all_latch}
            gy_all_dict.append(dicta)
            gy_all_latch = []
            gy_y_latch = []
            gy_x_latch = []
            gy_z_latch = []
        time_latch = timec
    
    gy_x, gy_y, gy_z = epoch["a"].split(',')
    if abs(float(gy_x)) > 256:
        gy_x = 0
    if abs(float(gy_y)) > 256:
        gy_y = 0
    if abs(float(gy_z)) > 256:
        gy_z = 0
        
    gy_x_latch.append(float(gy_x))
    gy_y_latch.append(float(gy_y))
    gy_z_latch.append(float(gy_z))
    wrt = str(times) + "," + str(int(epoch["t"])) + ',' + str(gy_x) + ',' + str(gy_y) + ',' + str(gy_z)
    write_file.append(wrt)
#dicta = {recv[len(recv)-1]["t"]:gy_x_latch}
gy_all_latch.append(gy_x_latch)
gy_all_latch.append(gy_y_latch)
gy_all_latch.append(gy_z_latch)
gy_y_latch = []
gy_x_latch = []
gy_z_latch = []
'''
gy_y_min = []
gy_x_min = []
gy_z_min = []
'''

dicta = {time_latch:gy_all_latch}
gy_all_dict.append(dicta)

for epoch_dict in gy_all_dict:
    act_x = 0
    act_y = 0
    act_z = 0
    for key,value in epoch_dict.iteritems():
        v = value[0][0:len(value[0])/2]
        x = np.array(v)
        x = np.absolute(x)
        act_x = sum(x)
        v = value[1][0:len(value[1])/2]
        x = np.array(v)
        x = np.absolute(x)
        act_y = sum(x)
        v = value[2][0:len(value[2])/2]
        x = np.array(v)
        x = np.absolute(x)
        act_z = sum(x)
        time_act = datetime.datetime.fromtimestamp(key/1000).strftime('%Y-%m-%d %H:%M:%S')              
        wrt2 = str(time_act) + "," + str(key) + ',' + str(act_x) + ',' + str(act_y) + ',' + str(act_z) + ',' + str((act_x+act_y+act_z)/3)  
        write_file_act.append(wrt2) 
        v = value[0][len(value[0])/2:]
        x = np.array(v)
        x = np.absolute(x)
        act_x = sum(x)
        v = value[1][len(value[1])/2:]
        x = np.array(v)
        x = np.absolute(x)
        act_y = sum(x)
        v = value[2][len(value[2])/2:]
        x = np.array(v)
        x = np.absolute(x)
        act_z = sum(x)
        time_act = datetime.datetime.fromtimestamp((key+30000)/1000).strftime('%Y-%m-%d %H:%M:%S')
        wrt2 = str(time_act) + "," + str(key+30000) + ',' + str(act_x) + ',' + str(act_y) + ',' + str(act_z) + ',' + str((act_x+act_y+act_z)/3)  
        write_file_act.append(wrt2)

    	


file_name = time.strftime('wolksense_cloud/act/%Y-%m-%d/wolksense_act_%Y-%m-%d_%H:%M:%S') + '.csv'
if not os.path.exists(os.path.dirname(file_name)):
    try:
        os.makedirs(os.path.dirname(file_name))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(file_name, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(write_file_act)
csvwrite.close()
print "Act file written dir: "
print os.getcwd() + file_name
file_name = time.strftime('wolksense_cloud/gyro/%Y-%m-%d/wolksense_gyro_%H:%M:%S') + '.csv'
if not os.path.exists(os.path.dirname(file_name)):
    try:
        os.makedirs(os.path.dirname(file_name))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

with open(file_name, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(write_file)
csvwrite.close()
end = time.time() - t_start
print "Gyro file written dir: "
print os.getcwd() + file_name
print "File written time: ", end
true_end = time.time() - true_start
print "Total time: ", true_end
print ""
