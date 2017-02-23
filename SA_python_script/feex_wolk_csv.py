import requests
import simplejson as json
import csv
import sys
import numpy as np
import time
import os

print "\n============================================"
print "Wolksense feature extraction script started"
print "============================================"

activity=[]
count=21
five_mean=0
fivecount=0
get = "sumact,max,stdev,fivecount,log,state"   
get1 = "act,slpstate,time"
Max=0
runtime=21
show=[]
show.append(get) #keep in array not write to new file
show1=[]
show1.append(get1) #keep in array not write to new file
state=[]
sumact=0
times=[]
ten_epoch=[]


#allfile =["hchs-sol-sueno-00238589.csv","hchs-sol-sueno-00163225.csv",
#          "hchs-sol-sueno-00258857.csv","hchs-sol-sueno-00306064.csv",
#          "hchs-sol-sueno-00311734.csv","hchs-sol-sueno-00329320.csv",
#          "hchs-sol-sueno-00349159.csv","hchs-sol-sueno-00358110.csv",
#          "hchs-sol-sueno-00496432.csv","hchs-sol-sueno-00504839.csv"]
t_start = time.time()
true_start = t_start
name_file = str(sys.argv[1])
with open(name_file) as csvfile:
    readCSV = list(csv.reader(csvfile, delimiter=','))
    total_row = len(readCSV)#sum(1 for row in readCSV)
    skip_1_row = 0;
    for row in readCSV:
        if skip_1_row == 0 :
            skip_1_row +=1
        else :
            activity.append(float(row[5]))
            times.append(row[0])
    #print activity[9]
    mean=np.mean(np.array(activity))
    fivetime_meanact=mean*5
    #print mean
    
csvfile.close()
end = time.time() - t_start

print "Wolksense activity data extracted time: ", end

t_start = time.time()
while runtime < (total_row - 20) :
        check_actzero = activity[runtime]
        if (check_actzero == 0) :
            check_actzero = 1
        Nlog = np.log(check_actzero)+1
        Max = 0
        while count>10:
            ten_epoch.append(activity[runtime-count+10])
            sumact=sumact+activity[runtime-count+10]
            #print(sumact)
            if(activity[runtime-count+10]> Max):
                Max = activity[runtime-count+10]
            if(activity[runtime-count+10]>fivetime_meanact):
                fivecount+=1
            count=count-1
            
        while count<=10 and count>0 :
            ten_epoch.append(activity[runtime+count])
            sumact=sumact+activity[runtime+count]
            if(activity[runtime+count]> Max):
                Max = activity[runtime+count]
            if(activity[runtime+count]>fivetime_meanact):
                fivecount+=1
            #print(activity[runtime-count]+"----"+str(count)+"---"+str(runtime-count))
            count=count-1
        count=21
        slpstate = '-1'
        #print(str(ten_epoch)+"____"+str(np.std(ten_epoch,ddof=1)))
        #get = str(activity[runtime])+","+state[runtime]+","+times[runtime]+","+str(sumact)+","+str(Max)+","+str(np.std(ten_epoch,ddof=1))+","+str(fivecount)+","+str(Nlog)
        get = str(sumact)+","+str(Max)+","+str(np.std(ten_epoch,ddof=1))+","+str(fivecount)+","+str(Nlog)+","+slpstate        
        #get1 = str(activity[runtime])+","+state[runtime]+","+times[runtime]
        show.append(get) #keep in array not write to new file
        #show1.append(get1)
        sumact=0
        fivecount=0
        ten_epoch=[]
        runtime=runtime+1

end = time.time() - t_start

print "Wolksense feature extract time: ", end

t_start = time.time()
name_new_file  = time.strftime("feature/%Y-%m-%d/feature_wolksense_%H-%M-%S")+".csv"
#name_new_file1 = time.strftime("act-date-state_%H-%M-%S")+".csv"
if not os.path.exists(os.path.dirname(name_new_file)):
    try:
        os.makedirs(os.path.dirname(name_new_file))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
with open(name_new_file, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(show)
csvwrite.close()
print "feature file written dir: "
print os.getcwd() + name_new_file

end = time.time() - t_start
print "File written time: ", end
true_end = time.time() - true_start
print "Total time: ", true_end
print ""
'''
with open(name_new_file1, 'w+') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(show1)
csvwrite.close()
'''