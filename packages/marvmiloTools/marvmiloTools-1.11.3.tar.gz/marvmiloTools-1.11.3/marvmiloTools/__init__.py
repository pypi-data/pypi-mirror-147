"""
# marvmiloTools

Version: 1.11.3

## Dependencies:
- pandas
- dash
- dash-bootstrap-components
- paho-mqtt

## Description:
A tool a wrote for myself to have multiple functions and classes avalibale on diffrent servers and devices.

## Subparts:
- dash
- json
- dictionary

## Available Tools:
- ScriptPrint
- Timer
- get_variable_name
- random_ID
- CloudMQTT
- SQL
- prettyprint
"""

import datetime as dt
import pandas as pd
import time
import random
import string
import paho.mqtt.client as mqtt
import sqlite3
import threading
import datetime
import traceback
import os
import json as j
import sys

#load other scripts
from . import dash_tools as dash_import
from . import json_tools as json_import
from . import dictionary_tools as dictionary_import

__version__ = "1.11.3"

#dash tools
dash = dash_import
"""
# Dash
Tools for Dash Plotly
## Available:
- flex_style
- mobile_optimization
- content_div
- modal_header_close
- random_ID
- browsertime
- nav
- picture
"""

#json tools
json = json_import
"""
# Json
Tools for editing json files.
## Available:
- load
- save
- write
"""

#dictionary tools
dictionary = dictionary_import
"""
# Dictionary
Tools for editing dictionaries.
## Available:
- toObj
- toDict
"""

#print command with Script name in front
class Output:
    """
# Output:
Logging and Output Tool for different Scipts.
## Example 1(Printing):
```
import marvmiloTools as mmt

output = mmt.Output("SCRIPT")
print = output.print

print("hello world")
```
### Output:
```
2022-04-18 23:53:48.015564 - INFO - [SCRIPT]: hello world
``` 
### Example 2(Logging):  
```
import marvmiloTools as mmt

output = mmt.Output("SCRIPT", logfile = "output.log")
#cleanup from last time
output.cleanup_logfile()
output.log("logging output")

print = output.print
print("logging prints")

def main():
    1 / 0

output.log_python_error(main)
```
### output.log:
```
2022-04-18 23:49:41.898101 - INFO - [SCRIPT]: logging output
2022-04-18 23:49:41.898891 - INFO - [SCRIPT]: logging prints
2022-04-18 23:49:41.901410 - ERROR - [SCRIPT]: 
Traceback (most recent call last):
  File "C:Users/user/Projects/marvmiloTools/__init__.py", line 168, in log_python_error
    function()
  File "C:Users/user/Projects/log.py", line 12, in main
    1 / 0
ZeroDivisionError: division by zero
```
    """
    def __init__(self, name, block = False, timestamp = True, logfile = None, log_prints = True):
        self.name = name
        self.block = block
        self.timestamp = timestamp
        self.logfile = logfile
        self.log_prints = log_prints
    
    def __create_msg__(self, msg, loglevel = None):
        msg = f"[{self.name}]: {msg}"
        if loglevel:
            msg = f"{loglevel} - " + msg
        if self.timestamp:
            if loglevel:
                msg = "- " + msg
            msg = f"{datetime.datetime.now()} " + msg
        return msg
        
    def print(self, msg, loglevel = "INFO"):
        if not self.block:
            edited_msg = self.__create_msg__(msg, loglevel)
            print(edited_msg)
            
            #logging
            if self.log_prints and self.logfile:
                self.log(msg)
           
    def log(self, msg, level = "INFO"):
        if not self.block:
            if self.logfile:
                msg = self.__create_msg__(msg, loglevel = level)
                with open(self.logfile, "a") as logfile:
                    logfile.write(msg + "\n")
            else:
                raise ValueError("No logfile given!")
    
    def log_python_error(self, function, exit_script = True):
        try:
            function()
        except:
            tb = traceback.format_exc()
            msg = "\n" + tb
            print(tb)
            self.log(msg , level = "ERROR")
            if exit_script:
                exit()
    
    def cleanup_logfile(self):
        if self.logfile:
            os.remove(self.logfile)
        else:
            raise ValueError("No logfile given!")
            
#Timer for Script runtimes
class Timer:
    """
# Timer:
A build in timer for measuring runtimes.
## Example:
```
import marvmiloTools as mmt
from time import sleep

#start the timer
mmt.timer.start()

sleep(3)

#pause timer
runtime = mmt.timer.pause()
print("Type of runtime: " + str(type(runtime)))
print("Runtime at pause: " + str(runtime))

#reset timer and get runtime function
mmt.timer.reset()
runtime = mmt.timer.get_runtime()
print("Runtime at reset: " + str(runtime))

#set some laps
mmt.timer.start()
for i in range(3):
    sleep(1)
    runtime = mmt.timer.set_lap()
    print("Runtime at lap " + str(i) + ": " + str(runtime))

#get all laps
laps = mmt.timer.get_laps()
print("Laps: " + str(laps))

sleep(2)

#get time of current lap without setting a lap
lap_runtime = mmt.timer.get_lap_runtime()
print("Current Lap Runtime: " + str(lap_runtime))
```
### Output:
```
Type of runtime: <class 'datetime.timedelta'>
Runtime at pause: 0:00:03.003270
Runtime at reset: 0:00:00
Runtime at lap 0: 0:00:01.001151
Runtime at lap 1: 0:00:01.001191
Runtime at lap 2: 0:00:01.001231
Laps: [datetime.timedelta(seconds=1, microseconds=1151), datetime.timedelta(seconds=1, microseconds=1191), datetime.timedelta(seconds=1, microseconds=1231)]
Current Lap Runtime: 0:00:02.002030
```
### Create a new instance of timer:
```
timer = mmt.Timer()
timer.start()
...
```
    """
    def __init__(self):
        self.startpoint = None
        self.lapstartpoint = None
        self.runtime = dt.timedelta(seconds = 0)
        self.lapruntime = dt.timedelta(seconds = 0)
        self.laps = []
    def start(self):
        if not self.startpoint:
            self.startpoint = dt.datetime.now()
            self.lapstartpoint = dt.datetime.now()
        else:
            raise Exception("Timer already running")
    def pause(self):
        if self.startpoint:
            now = dt.datetime.now()
            self.runtime += now - self.startpoint
            self.lapruntime += now - self.lapstartpoint
            self.startpoint = None
            self.lapstartpoint = None
            return self.runtime
        else:
            raise Exception("Timer not running")
    def set_lap(self):
        if self.lapstartpoint:
            now = dt.datetime.now()
            self.laps.append(self.lapruntime + now - self.lapstartpoint)
            self.lapstartpoint = now
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
        else:
            self.laps.append(self.lapruntime)
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
    def get_runtime(self):
        if self.startpoint:
            return self.runtime + dt.datetime.now() - self.startpoint
        else:
            return self.runtime
    def get_laps(self):
        return self.laps
    def get_lap_runtime(self):
        if self.lapstartpoint:
            return self.lapruntime + dt.datetime.now() - self.lapstartpoint
        else:
            return self.lapruntime
    def reset(self):
        self.__init__()
timer = Timer()

#CloudMQTT connector
class CloudMQTT:
    """
# CloudMQTT
CloudMQTT client with multiple functions.
## Example:
```
import marvmiloTools as mmt

#init cloudMQTT client
cloudmqtt = mmt.CloudMQTT(
    client_name = "clientname", 
    channel = "channel", 
    qos = 0
)

#connect to server
cloudmqtt.connect(
    user = "user", 
    pw = "password", 
    addr = "cloudmqtt.com", 
    port = 1234
)

#reconnecting to server if no connection
if not cloudmqtt.check_connection():
    cloudmqtt.reconnect()

#on message function
def on_message(msg, topic):
    print(f"received message: '{msg}', topic: '{topic}'")
    
#binding on_message function to a topic
cloudmqtt.bind(topic = "hello", function = on_message)

#publishing a message
cloudmqtt.publish(topic = "hello", message = "world")

#response function
def on_request(msg, topic):
    resp = "hello world"
    print(f"publishing response: {resp}")
    return(resp)

#binding on_request to request topic
cloudmqtt.bind_response("demo", on_request)

#request data from server
resp = (
    cloudmqtt.request(
        topic = "demo",
        message = ".",
        retry = 5
    )
)
print("got response: " + resp)

#disconnecting form server
cloudmqtt.disconnect()
```
## Output:
```
received message: 'world', topic: 'hello'
publishing response: hello world
got response: hello world
```
    """
    def __init__(self, client_name = "mmt_client", channel = "", qos = 0):
        self.client_name = client_name
        self.channel = channel
        self.qos = qos
        self.client = None
        self.bindings = {}
        self.user = None
        self.pw = None
        self.addr = None
        self.port = None
        
    #for handling messages
    def on_message(self, client, obj, msg):
        for bind in self.bindings:
            if msg.topic.startswith(bind):
                self.bindings[bind](msg.payload.decode("utf-8"), "/".join(msg.topic.split("/")[1:]))
                break
    #for conecting to server
    def connect(self, user, pw, addr, port):
        self.user = user
        self.pw = pw
        self.addr = addr
        self.port = port
        self.client = mqtt.Client(self.client_name)
        self.client.username_pw_set(user, pw)
        self.client.connect(addr, port)
        self.client.on_message = self.on_message
        self.client.subscribe(self.channel + "/#", qos = self.qos)
        self.client.loop_start()
    #for disconnecting
    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
    #for reconnecting
    def reconnect(self):
        self.disconnect()
        self.connect(self.user, self.pw, self.addr, self.port)
    #check connection
    def check_connection(self):
        try: resp = self.client.is_connected()
        except NameError: resp = False
        return resp
    #for publishing on channel
    def publish(self, topic, message):
        self.client.publish("/".join([self.channel, topic]), message, qos = self.qos)
    #for binding function to topic subcription
    def bind(self, topic, function):
        self.bindings["/".join([self.channel, topic])] = function
    #for binding a response function to topic
    def bind_response(self, topic, function):
        def resp_func(msg, topic):
            topic_list = topic.split("/")
            if topic_list[1] == "req":
                topic_list[1] = "resp"
                self.publish("/".join(topic_list), function(msg, topic))
        self.bind(topic + "/req", resp_func)
    #for unbinding functions
    def unbind(self, topic):
        del self.bindings["/".join([self.channel, topic])]
    #for requesting information
    def request(self, topic, message = "request", ID = None, retry = 5):
        if not ID:
            ID = random_ID()
        response = None
        def get_resp(msg, topic):
            nonlocal response
            response = msg
        self.bind("/".join([topic, "resp", str(ID)]), get_resp)
        self.publish("/".join([topic, "req", str(ID)]), message)
        start = time.time()
        while not response:
            if time.time()-start > retry:
                break
        self.unbind("/".join([topic, "resp", str(ID)]))
        return response    
cloudmqtt = CloudMQTT()    

#for getting variable name as string
def get_variable_name(var, namespace):
    """
# get_variable_name
Converting variable in namespace into an string.
## Example:
```
import marvmiloTools as mmt

#declare a variable
variable = "hello world"

#get name as string from variable
variable_name = mmt.get_variable_name(variable, locals())
print(variable_name, type(variable_name))
```
### Output:
```
variable <class 'str'>
```
    """
    if not isinstance(var, pd.DataFrame):
        return [k for k, v in namespace.items() if v == var][0]
    else:
        return [k for k, v in namespace.items() if var.equals(v)][0]

#for generating random ID
def random_ID(len = 20):
    """
# random_ID
Creating a random ID of specific length.
## Example:
```
import marvmiloTools as mmt
print(mmt.random_ID(10))
```
## Output:
```
R1DBXY64KH73BPPF7WFT
```
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

#SQL tools
class SQL:
    """
# SQL
Simple sqlite3 manager.
## Example:
```
import marvmiloTools as mmt

mmt.sql.connect("database.db")
mmt.sql.execute("CREATE TABLE IF NOT EXISTS test (a INTEGER, b INTEGER)")
mmt.sql.execute("INSERT INTO test (a,b) VALUES (0,1)")
mmt.sql.disconnect()

#new sql instance
sql = mmt.SQL()
sql.connect(...
```
    """
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db = None
        self.commands = []
    def __exc_cmds___(self):
        for command in self.commands:
            self.cursor.execute(command)
        self.connection.commit()
        self.commands = []
    def __update__(self):
        while self.connection:
            self.__exc_cmds___()
            time.sleep(1)
    def connect(self, db):
        self.db = db
        self.connection = sqlite3.connect(self.db, check_same_thread = False)
        self.cursor = self.connection.cursor()
        threading.Thread(target = self.__update__).start()
    def disconnect(self):
        self.__exc_cmds___()
        self.connection.close()
        self.__init__()
    def execute(self, command):
        self.commands.append(command)
sql = SQL()

def prettyprint(obj):
    """
# prettyprint
Prettyprint lists, dictionaries, DictObjects etc. in json format.
## Example:
```
import marvmiloTools as mmt

random_list = [1, 2, 3]
random_dict = {"a": "A", "b": "B"}
random_dictobj = mmt.dictionary.toObj(random_dict)

mmt.prettyprint(random_list)
mmt.prettyprint(random_dict)
mmt.prettyprint(random_dictobj)
```
## Output:
```
[
    1,
    2,
    3
]
{
    "a": "A",
    "b": "B"
}
{
    "a": "A",
    "b": "B"
}
```
    """
    if type(obj) == dictionary.DictObject:
        obj = obj.toDict()
    print(j.dumps(obj, indent=4))

threads = dictionary.toObj(dict())
"""
# Thread
For managing Threads
## Example:
```
import time
import marvmiloTools as mmt

def function(string):
    while True:
        print(string)
        time.sleep(1)

thread_id = mmt.thread(function, "hello world")
print(mmt.threads[thread_id].is_alive())

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    for id in mmt.threads:
        mmt.threads[id].stop()
```
## Output:
```
hello world
True
hello world
hello world
KeyboardInterrupt:
```
"""
def thread(function, *args, **kwargs):
    """
# Thread
For managing Threads
## Example:
```
import time
import marvmiloTools as mmt

def function(string):
    while True:
        print(string)
        time.sleep(1)

thread_id = mmt.thread(function, "hello world")
print(mmt.threads[thread_id].is_alive())

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    for id in mmt.threads:
        mmt.threads[id].stop()
```
## Output:
```
hello world
True
hello world
hello world
KeyboardInterrupt:
```
    """
    class Thread(threading.Thread):
        def __init__(self, *args, **keywords):
            threading.Thread.__init__(self, *args, **keywords)
            self.killed = False
        def start(self):
            self.__run_backup = self.run
            self.run = self.__run     
            threading.Thread.start(self)
        def __run(self):
            sys.settrace(self.globaltrace)
            self.__run_backup()
            self.run = self.__run_backup
        def globaltrace(self, frame, why, arg):
            if why == 'call':
                return self.localtrace
            else:
                return None
        def localtrace(self, frame, why, arg):
            if self.killed:
                if why == 'line':
                    raise SystemExit()
            return self.localtrace
        def stop(self):
            self.killed = True
    
    id = random_ID()
    thread_obj = Thread(target = function, args = args, kwargs = kwargs)
    thread_obj.start()
    threads[id] = thread_obj
    return id