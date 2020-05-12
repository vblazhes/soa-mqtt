import sys
import traceback
import logging
import paho.mqtt.client as mqtt  # import the client
import time
from uuid import getnode as get_mac
import random


# on_message callback function
# in order to display the message
# def on_message(client, userdata, message):
#     print("message received ", str(message.payload.decode("utf-8")))
#     print("message topic=", message.topic)
#     print("message qos=", message.qos)
#     print("message retain flag=", message.retain)
#

# on_connect callback function
# used to assure that the connection attempt was successful
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK Returned code=", rc)
        # client.subscribe(topic)
    else:
        print("Bad connection Returned code= ", rc)
        client.bad_connection_flag = True


# on_log callback function
# To help troubleshoot your applications
def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_disconnect(client, userdata, rc):
    logging.info("disconnecting reason  " + str(rc))
    client.connected_flag = False
    client.disconnect_flag = True
    my_client.loop_stop()  # Stop loop


def on_publish(client, userdata, result):  # create function for callback
    print("Data published \n")
    pass


# Configuration variables
mqttclient_log = True
#broker_address = "broker.hivemq.com"  # URL of online broker (we use hivemq broker / ip address shoud provide if local)
broker_address = "host.docker.internal"
mac_addr = get_mac()  # getting the mac address of the device as a UID for the client
topic = "server/cpu/test03"
topic_lwt = "server/lwt01"


def Initialise_clients(cname):
    # callback assignment
    client = mqtt.Client(cname, False)  # don't use clean session
    if mqttclient_log:  # enable mqqt client logging
        client.on_log = on_log
    client.on_connect = on_connect  # attach function to on_connect callback
    # client.on_disconnect = on_disconnect  # attach function to on_disconnect callback
    #   client.on_message = on_message  # attach function to callback
    #    client.on_subscribe = on_subscribe
    # flags set
    client.username_pw_set(username="user_01", password="passwd01")
    client.topic_ack = []
    client.run_flag = False
    client.running_loop = False
    client.subscribe_flag = False
    client.bad_connection_flag = False
    client.connected_flag = False  # this flag is used to control the connection - more sophisticated approach
    client.disconnect_flag = False
    return client


#  getting instance of the mqtt client
my_client = Initialise_clients('publisher00-' + str(mac_addr))
my_client.will_set(topic_lwt, "Publisher died :(")

# time.sleep(120)
# my_client.loop_start()

# Connect mqtt client to a broker
print("Connecting to broker ", broker_address)
try:
    my_client.connect(broker_address)  # connecting to a broker (hivemq online broker)
except:
    print("connection failed")
    traceback.print_stack()
    exit(1)  # Should quit or raise flag to quit or retry

my_client.loop_start()

while not my_client.connected_flag and not my_client.bad_connection_flag:  # wait in loop
    print("In wait loop")
    time.sleep(1)
if my_client.bad_connection_flag:
    my_client.loop_stop()  # Stop loop
    sys.exit()

while 1:
    time.sleep(10)
    usage = 50
    variation = random.randrange(-20, 20)
    print(str(usage + variation))
    my_client.publish(topic=topic, payload=str(usage + variation) + "% CPU Usage", qos=2)

# my_client.disconnect()  # disconnect
