import csv
import numpy as np
import time
import sys
show=[]
show1=[]
get = ""
activity=[]
state=[]
times=[]
sumact=0
count=21
runtime=0
Max=0
five_mean=0
ten_epoch=[]
fivecount=0

#name_file = "C:\\Users\\chananan\\Desktop\\hchs-sol-sueno-00238589.csv" 
#name_file = "C:\\Users\\chananan\\Desktop\\hchs-sol-sueno-00163225.csv"
#name_file = "C:\\Users\\chananan\\Desktop\\hchs-sol-sueno-00258857.csv"
#name_file = "C:\\Users\\chananan\\Desktop\\hchs-sol-sueno-00306064.csv"
name_file = "C:\\Users\\chananan\\Desktop\\hchs-sol-sueno-00311734.csv"
name_new_file ="C:\\Users\\chananan\\Desktop\\"+time.strftime("hchs-sol-sueno-00306064_%H-%M-%S")+".csv"
with open(name_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    
    for row in readCSV:
        if row[0]!="pid": 
                if (int(row[2])>0 and int(row[2])<=10000):
                    if(row[4]== ''):
                        activity.append(0)
                        print("xxxxxxxxxxxxx")
                        continue
                    activity.append(int(row[4]))
                    state.append(row[10])
                    times.append(row[16])
                    #print(row[2])    
                #print(activity[start]+"---")
                #print(x)
                #x=x+1
                #wake.append(row[10])
                #time.append(row[16])
                    
    mean=np.mean(np.array(activity))
    fivetime_meanact=mean*5
    
    #print(np.mean(fivetime_meanact))
    get = "sumact,max,stdev,fivecount,log,state"        
    show.append(get) #keep in array not write to new file           
    while runtime < 10000 :
        if (runtime>=20 and runtime <=9950):
            check_actzero = activity[runtime]
            if (check_actzero == 0) :
                check_actzero = 1
            Nlog = np.log(check_actzero)+1
            Max = activity[runtime-count+10]
            while count>10:
                ten_epoch.append(activity[runtime-count+10])
                sumact=sumact+activity[runtime-count+10]
                #print(sumact)
                if(activity[runtime-count+10]> Max):
                    Max = activity[runtime-count+10]
                if(activity[runtime-count+10]>fivetime_meanact):
                    fivecount+=1
                count=count-1
                
            while count<=10 and count>0:
                ten_epoch.append(activity[runtime+count])
                sumact=sumact+activity[runtime+count]
                if(activity[runtime+count]> Max):
                    Max = activity[runtime+count]
                if(activity[runtime+count]>fivetime_meanact):
                    fivecount+=1
                #print(activity[runtime-count]+"----"+str(count)+"---"+str(runtime-count))
                count=count-1
            count=21
            
            #print(str(ten_epoch)+"____"+str(np.std(ten_epoch,ddof=1)))
            #get = str(activity[runtime])+","+state[runtime]+","+time[runtime]+","+str(sumact)+","+str(Max)+","+str(np.std(ten_epoch,ddof=1))+","+str(fivecount)+","+str(Nlog)
            #print(state[runtime]);
            if state[runtime] == '':
                slpstate = "wake"
            elif int(state[runtime]) == 1:
                slpstate = "wake"    
            else:slpstate = "sleep"
            get = str(sumact)+","+str(Max)+","+str(np.std(ten_epoch,ddof=1))+","+str(fivecount)+","+str(Nlog)+","+slpstate        
            show.append(get) #keep in array not write to new file
            sumact=0
            fivecount=0
            ten_epoch=[]
        runtime=runtime+1

        
 
csvfile.close()

with open(name_new_file, 'w') as csvwrite:
    writer = csv.writer(csvwrite, delimiter='\n' ,dialect='excel-tab')
    writer.writerow(show)
csvwrite.close()

