#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install SenseHat


# In[2]:


# pip install speedtest-cli


# In[3]:


filename = "speeds.csv"


# In[4]:


import os
import speedtest 


# In[5]:


import datetime
import time


# In[6]:


import socket
import requests
import json


# In[7]:


import platform
import socket
import uuid


# In[8]:


def GetISPInfo():
    ipUrl = "http://ip-api.com/json"
    response= json.loads(requests.get(ipUrl).content)
    print(response)
    print(response["query"])
    return response


# In[9]:


def test():
    s = speedtest.Speedtest()
    
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    print(res)
    return res["download"], res["upload"], res["ping"]


# In[10]:


hostname = socket.gethostname()
print(hostname)


# In[11]:


def ProcessSpeedTest(linesToWrite):
    newId = uuid.uuid4()
    now = datetime.datetime.utcnow()
    datepart = now.strftime("%Y_%m_%d")
    filename = "data/speed." + datepart +".csv"
    print(filename)
    try:
        ip = socket.gethostbyname(socket.gethostname())
        ispInfo = GetISPInfo()
        externalIp = ispInfo["query"]
        print("running test")
        d, u, p = test()
        print("Download was ", round(d/1024/1024,1))
        print(d,u,p,ip,ispInfo)
    except  Exception as e:
        print("exception ",e)
        d = -1
        u = -1
        p = -1
        ip = socket.gethostbyname(socket.gethostname())
    try:
        url = "https://alddataapi.azurewebsites.net/api/Speeds"
        # url = "https://localhost:44323/api/Speeds"
        print(url)

        d = {
            "id": str(newId),  "utc": now.isoformat() ,  "pingMs": int(p),  "downloadSpeed":int(d),  "uploadSpeed": int(u),  
            "publicIp": externalIp,  "isp": "string",  "lat": ispInfo["lat"],  "lon": ispInfo["lon"],  "data": str(json.dumps(ispInfo))
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        stringData = json.dumps(d)
        print(stringData)
        r = requests.post(url, data=json.dumps(d), headers=headers,verify=False)
        print(r)
    except Exception as e:
        print("Unable to put",e)    
    
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
            print("wrote lines")
            linesToWrite = []
            
        except:
            print("Unable to write line")
            for line in linesToWrite:
                print (line)
            print("----")
    return linesToWrite


# In[ ]:


print("ready to start work")
linesToWrite = []
while (True):    
    try:
        linesToWrite = ProcessSpeedTest(linesToWrite)
    except Exception as e:
        print("Exception ",e)
    print('sleeping')
    time.sleep(600) # 60*10 - 10 minutes 


# In[ ]:





# In[ ]:




