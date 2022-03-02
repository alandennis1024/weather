#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install speedtest-cli


# In[2]:


filename = "speeds.csv"


# In[3]:


import os
import speedtest 


# In[4]:


import socket
import requests
import json


# In[5]:


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


# In[6]:


import datetime
import time


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


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




