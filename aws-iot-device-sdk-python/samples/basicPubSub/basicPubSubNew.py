from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import numpy as np
import csv

name_file = str(sys.argv[1])
maximum = []
stdev = []
fivecount = []
log = []
state = []
with open(name_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    feature = np.array(list(readCSV))
    raw_data = feature[1:,:5].astype("float")
    print(raw_data)
#X = []
# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
        #x= message.payload

#raw_data=[[1,2,3,4]]



# Read in command-line parameters
useWebsocket = False
host = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""


# Configure logging
logger = None
logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient

host = "a25a68oquogzqy.iot.ap-southeast-1.amazonaws.com"	
myAWSIoTMQTTClient = AWSIoTMQTTClient("Mqttpy")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("D:\\Study\\year4\\project\\awscertificate\\3-Public-Primary-Certification-Authority-G5.pem", "D:\\Study\\year4\\project\\awscertificate\\5724cc25ea-private.pem.key", "D:\\Study\\year4\\project\\awscertificate\\5724cc25ea-certificate.pem.crt")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
print(host)
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("lambda",1,customCallback)
print("ccccccccc")
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
        
        start_time = time.time()
        #text ='{"Id": "mixmix'+time.strftime("%Y-%m-%d %H:%M:%S")+'","sumact":"'+str(test_array)+'","max":"'+str(test_array)+'","stdev":"'+str(test_array)+'","fivecount":"'+str(test_array)+'","log":"'+str(test_array)+'","state": "book'+str(test_array)+'"}'
        text ='{"Id": "Name'+time.strftime("%Y-%m-%d %H:%M:%S")+'","sumact":"'+str(raw_data)+'"}'  
        #myAWSIoTMQTTClient.publish("$aws/things/Mqttpy/shadow/update", "New Message " + str(loopCount), 1)
        myAWSIoTMQTTClient.publish("$aws/things/Mqttpy/shadow/update",text, 1)
	#myAWSIoTMQTTClient.publish("$aws/things/Mqttpy/shadow/update",'{"Id": "mixmix'+str(loopCount)+'"}', 1)
        loopCount += 1
        print("done------------------------------")
        time.sleep(10)
       
