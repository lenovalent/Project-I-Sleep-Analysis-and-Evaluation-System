import requests
import simplejson as json
import json
import datetime
import time
import csv
import numpy as np

print "start script"
t_start = time.time()
file_head = "time,mstime,gy_x,gy_y,gy_z"
file_head_act = "time,mstime,act_x,act_y,act_z"

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
print "api key recv time"
end = time.time() - t_start
print end
t_start = time.time()
#use token to get data
accessToken = recv['accessToken']

#set date to extract data
from_date = '1487523600000' #20 feb

#from_date = '1487610000000'  #21 feb
#to_date = '1487782800000' #23 feb
#to_date = '1487696400000'  #22 feb
#to_date = '1487610000000' #21 feb
to_date = '1487534340000'
#to_date = '1487534220000'
feedId = '77173'

extract_uri = 'https://api.wolksense.com/api/v2/feeds/'+feedId+'/readings?from='+ from_date + '&to=' + to_date + '&aggregationLevel=ONE_MINUTE'
extract_headers = {'Content-type': 'application/json',
                   'Authorization': str(accessToken)}
r = requests.get(extract_uri,headers=extract_headers)
recv = json.loads(json.dumps(r.json()))
print "data recv time"
end = time.time() - t_start
print end
t_start = time.time()
gy_x_min = []
gy_x_latch = []
gy_x_dict = []


gy_y_min = []
gy_y_latch = []
gy_y_dict = []


gy_z_min = []
gy_z_latch = []
gy_z_dict = []


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
        	gy_x_min.append(gy_x_latch)
        	dicta = {time_latch:gy_x_latch}
        	gy_x_dict.append(dicta)
        	gy_x_latch = []

        	#gy_x_latch.append(int(epoch["t"]))
        
        	gy_y_min.append(gy_y_latch)
        	dicta = {time_latch:gy_y_latch}
        	gy_y_dict.append(dicta)
        	gy_y_latch = []
        	#gy_y_latch.append(int(epoch["t"]))
        
        
        	gy_z_min.append(gy_z_latch)
        	dicta = {time_latch:gy_z_latch}
        	gy_z_dict.append(dicta)
        	gy_z_latch = []
        	#gy_x_latch.append(int(epoch["t"]))
        time_latch = timec
    
    gy_x, gy_y, gy_z = epoch["a"].split(',')
    gy_x_latch.append(float(gy_x))
    gy_y_latch.append(float(gy_y))
    gy_z_latch.append(float(gy_z))
    
    wrt = str(times) + "," + str(int(epoch["t"])) + ',' + str(gy_x) + ',' + str(gy_y) + ',' + str(gy_z)
    write_file.append(wrt)
#dicta = {recv[len(recv)-1]["t"]:gy_x_latch}
gy_x_min.append(gy_x_latch)
dicta = {time_latch:gy_x_latch}
gy_x_dict.append(dicta)
gy_x_latch = []

        	#gy_x_latch.append(int(epoch["t"]))
        
gy_y_min.append(gy_y_latch)
dicta = {time_latch:gy_y_latch}
gy_y_dict.append(dicta)
gy_y_latch = []
        	#gy_y_latch.append(int(epoch["t"]))
        
gy_z_min.append(gy_z_latch)
dicta = {time_latch:gy_z_latch}
gy_z_dict.append(dicta)
gy_z_latch = []

for i in range(0,len(gy_x_dict)):
	act_x = 0
	
	for key, value in gy_x_dict[i].iteritems():
		v = value[0:len(value)/2]
		x = np.array(v)
		x = np.absolute(x)
    	act_x = sum(x)
    	time_act = datetime.datetime.fromtimestamp(key/1000).strftime('%Y-%m-%d %H:%M:%S')      		
    	wrt2 = str(time_act) + "," + str(int(epoch["t"])) + ',' + str(act_x) 
    	write_file_act.append(wrt2)
    	v = value[len(value)/2:]
    	x = np.array(v)
    	x = np.absolute(x)
    	act_x = sum(x)
    	time_act = datetime.datetime.fromtimestamp((key+30000)/1000).strftime('%Y-%m-%d %H:%M:%S')
    	wrt2 = str(time_act) + "," + str(int(epoch["t"])) + ',' + str(act_x)
    	write_file_act.append(wrt2)
    	
		


#print len(gy_x_dict[0][0])
#print gy_x_min

file_name = time.strftime('wolksense_act_%Y-%m-%d_%H:%M:%S') + '.csv'
with open(file_name, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(write_file_act)
csvwrite.close()

file_name = time.strftime('wolksense_gyro_%Y-%m-%d_%H:%M:%S') + '.csv'
with open(file_name, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(write_file)
csvwrite.close()
print "file write time"
end = time.time() - t_start
print end
