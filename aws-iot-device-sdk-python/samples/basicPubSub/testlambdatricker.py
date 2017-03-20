from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt


print('Loading function')

def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

useWebsocket = False
host = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""

    
logger = None
if sys.version_info[0] == 3:
	logger = logging.getLogger("core")  # Python 3
else:
	logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

myAWSIoTMQTTClient = None
if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
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


myAWSIoTMQTTClient.connect()

myAWSIoTMQTTClient.publish("lambda",'{"Id": "finish","key2": "finish2","key1": "book"}', 1)



#print("Received event: " + json.dumps(event, indent=2))
#print("value1 = " + event["key1"])

#return event["key2"] # Echo back the first key value
#raise Exception('Something went wrong')
