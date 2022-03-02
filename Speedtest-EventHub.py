#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install azure-eventhub


# In[2]:


eventHubConnectString = 'Endpoint=sb://alanweather.servicebus.windows.net/;SharedAccessKeyName=send;SharedAccessKey=79nvrOv7sOpJeZ24urbpIKLY9Bp3ZiHFhllHZ8BFWrc='
eventhub_name = 'weather'


# In[3]:


# pip install speedtest-cli


# In[4]:


filename = "speeds.csv"


# In[5]:


import os
import speedtest 


# In[6]:


import socket
import requests
import json


# In[7]:


def test():
    s = speedtest.Speedtest()
    ip = socket.gethostbyname(socket.gethostname())
    ipUrl = "https://api.ipify.org/?format=json"
    response= json.loads(requests.get(ipUrl).text)
    print(response)
    print(response["ip"])
    externalIp = response["ip"]
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    return res["download"], res["upload"], res["ping"],externalIp


# In[8]:


import datetime
import time


# In[9]:


from azure.eventhub import EventHubProducerClient, EventData

def SendToEventHub(data):
    try:
        print("enter SendToEventHub", data)
        client = EventHubProducerClient.from_connection_string(eventHubConnectString, eventhub_name=eventhub_name)
        event_data_batch = client.create_batch()
        event_data_batch.add(EventData(data))
        with client:
            client.send_batch(event_data_batch)
        print("Sent data")
    except Exception as e:
        print("Unable to send data to event hub",e)


# In[ ]:


print("ready to start work")
linesToWrite = []
while (True):    
    now = datetime.datetime.utcnow()
    datepart = now.strftime("%Y_%m_%d")
    filename = "data/speed." + datepart +".csv"
    print(filename)
    try:
        d, u, p,ip = test()
        print(d,u,p,ip)
    except:
        print("exception")
        d = -1
        u = -1
        p = -1
        ip = socket.gethostbyname(socket.gethostname())
    eventData = json.dumps( {"utc":d,"ip":ip,"download":d,"upload":u,"ping":p})
    SendToEventHub(eventData)
    print("sent to event hub")
    if os.path.isfile(filename):
        print(filename + ' exists')
    else:
        with open(filename, 'w') as f:
            f.write('utc,ip,download,upload,ping\n') 
    with open(filename, 'a') as f:
        line = '{},{},{},{},{}\n'.format(datetime.datetime.utcnow(),ip,d, u, p)
        linesToWrite.append(line)
        print(line)
        try:
            for line in linesToWrite:
                print("Writing line",line)
                f.write(line)
            linesToWrite = []
        except:
            print("Unable to write line")
            for line in linesToWrite:
                print (line)
            print("----")
    print('sleeping')
    time.sleep(600) # 60*10 - 10 minutes 


# In[ ]:




