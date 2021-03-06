from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

# Usage
usageInfo = """Usage:

Use certificate based mutual authentication:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

Use MQTT over WebSocket:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

Type "python basicPubSub.py -h" for available options.
"""
# Help info
helpInfo = """-e, --endpoint
	Your AWS IoT custom endpoint
-r, --rootCA
	Root CA file path
-c, --cert
	Certificate file path
-k, --key
	Private key file path
-w, --websocket
	Use MQTT over WebSocket
-h, --help
	Help information


"""
test_array=[1,2,3,4]
# Read in command-line parameters
useWebsocket = False
host = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""
try:
	opts, args = getopt.getopt(sys.argv[1:], "hwe:k:c:r:", ["help", "endpoint=", "key=","cert=","rootCA=", "websocket"])
	if len(opts) == 0:
		raise getopt.GetoptError("No input parameters!")
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print(helpInfo)
			exit(0)
		if opt in ("-e", "--endpoint"):
			host = arg
		if opt in ("-r", "--rootCA"):
			rootCAPath = arg
		if opt in ("-c", "--cert"):
			certificatePath = arg
		if opt in ("-k", "--key"):
			privateKeyPath = arg
		if opt in ("-w", "--websocket"):
			useWebsocket = True
except getopt.GetoptError:
	print(usageInfo)
	exit(1)

# Missing configuration notification
missingConfiguration = False
if not host:
	print("Missing '-e' or '--endpoint'")
	missingConfiguration = True
if not rootCAPath:
	print("Missing '-r' or '--rootCA'")
	missingConfiguration = True
if not useWebsocket:
	if not certificatePath:
		print("Missing '-c' or '--cert'")
		missingConfiguration = True
	if not privateKeyPath:
		print("Missing '-k' or '--key'")
		missingConfiguration = True
if missingConfiguration:
	exit(2)

# Configure logging
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

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None

if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	host = "a25a68oquogzqy.iot.us-west-2.amazonaws.com"	
	myAWSIoTMQTTClient = AWSIoTMQTTClient("Mqttpy")
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials("D:\\Study\\year4\\project\\awscertificate_oregon\\VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem", "D:\\Study\\year4\\project\\awscertificate_oregon\\bfe4301105-private.pem.key", "D:\\Study\\year4\\project\\awscertificate_oregon\\bfe4301105-certificate.pem.crt")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
print(host)
myAWSIoTMQTTClient.connect()
print("aaaa")
#myAWSIoTMQTTClient.publish("$aws/things/Mqttpy/shadow/update",'{"Id": "mixmix'+time.strftime("%d-%m-%Y %H:%M:%S")+'","key2": "value2","key1": "book"}', 1)
print("bbbbbbb")
#myAWSIoTMQTTClient.subscribe("$aws/things/Mqttpy/shadow/update",0,customCallback)
myAWSIoTMQTTClient.subscribe("lambda",1,customCallback)
print("ccccccccc")
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
	#myAWSIoTMQTTClient.publish("$aws/things/Mqttpy/shadow/update", "New Message " + str(loopCount), 1)
	myAWSIoTMQTTClient.publish("$aws/things/Mqttpy/shadow/update",'{"Id": "mixmix'+time.strftime("%Y-%m-%d %H:%M:%S")+'","sumact":"'+str(test_array)+'","max":"'+str(test_array)+'","stdev":"'+str(test_array)+'","fivecount":"'+str(test_array)+'","log":"'+str(test_array)+'","state": "book'+str(test_array)+'"}', 1)
	#myAWSIoTMQTTClient.publish("$aws/things/Mqttpy/shadow/update",'{"Id": "mixmix'+str(loopCount)+'"}', 1)

	loopCount += 1
	time.sleep(5)
