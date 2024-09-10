# Read redis, take averages of observations, output them to a json file for uploading

import redis
import sys
import time
import numpy as np
import json

REDIS_STREAM = str(sys.argv[1])
NUM_KEY_VALUE_PAIRS = int(sys.argv[2])
INTERVAL_SECONDS = int(sys.argv[3])  #If INTERVAL_SECONDS=1, than not averaging 
MQTT_TOPIC = str(sys.argv[4])

# the while loop below will read output from the following redis query:
#
#	redis-cli XRANGE bme680 [unix time start] [unix time end]
#
# to see sample output for all points in the redis database execute the following query:
#
#	redis-cli XRANGE bme680 - +
#

# calculate query interval start and end time
# to do this get the current time and mod by 60
# then subtract the remainder from the current time
# to get end of last whole minute

# Python returns utime as decimal, round down and remove decimal
epoch = int(np.floor(time.time()))
secs = epoch % 60

# determine start and end times for redis query
# REDIS keys are in millis
# "000" needs to be appended to start
# "999" needs to be appended to end to get a full minute

if INTERVAL_SECONDS == 0:
    average = False

else:
    average = True

epoch_end = epoch - secs
epoch_start = epoch_end - INTERVAL_SECONDS
epoch_end = epoch_end - 1
epoch_start_key = str(epoch_start) + "000" # typecasting best way to append miliseconds
epoch_start_key = int(epoch_start_key)   # convert back to integer
epoch_end_key = str(epoch_end) + '999' # same as above, append milliseconds
epoch_end_key = int(epoch_end_key)  # same as above, typecast back to integer

# Create empty arrays to hold stats parameters for each key value
avgs = np.zeros(NUM_KEY_VALUE_PAIRS -1)
sdevs = np.zeros(NUM_KEY_VALUE_PAIRS -1)

r = redis.Redis(host='localhost', port=6379, db=0) # Open redis

if average == True:
    msg = r.xrange(REDIS_STREAM,epoch_start_key,epoch_end_key) # retrieve obs from 

else:
    msg = r.xrevrange(REDIS_STREAM,'+','-',count=1)

# create array to hold message values
vals = np.zeros((len(msg),NUM_KEY_VALUE_PAIRS))
key_names = []

# Loop to parse message by message
i = 0
while i<len(msg):
        x_msg = ''
        x_msg = str(msg[i]) # Create temporary string to store 1 message
        x_msg = x_msg.split("'") # Split message
        
        j = 1
        while j <= NUM_KEY_VALUE_PAIRS: 
            vals[i,j-1] = x_msg[1+j*4] # Values stored in 2D array, column=keypairs, row=msg#
            j = j+1
            
        msg_count = i
        i = i+1

k = 3
l = 0
while l<NUM_KEY_VALUE_PAIRS:
    key_names.append(x_msg[k])
    k = k+4
    l = l+1        

    
if average == True:
    avg = vals.mean(0)
    avg = avg.round(decimals=2)
    sdev = vals.std(0)
    sdev = sdev.round(decimals=2)

m = 0
data_file = '{ "epoch": ' + str(epoch) + ', "start_epoch": ' + str(epoch_start) + ', "end_epoch": ' + str(epoch_end) + ', "count": ' + str(msg_count) + ', "topic": ' + '"' + str(MQTT_TOPIC) + '"'

if average == True:
    while m<NUM_KEY_VALUE_PAIRS:
        data_file = data_file + ', "' + key_names[m] + '": { "average": ' + str(avg[m]) + ', "sdev": ' + str(sdev[m]) + " }"
        m = m+1

else:
        while m<NUM_KEY_VALUE_PAIRS:
            data_file = data_file + ', "' + key_names[m] + '": ' + str(vals[0,m]) 
            m = m+1  
    
data_file = data_file + " }"

print(data_file)
#data_file_json = json.loads(data_file)
#print(data_file_json)

#json_file = str(REDIS_STREAM) + "_msg.json"
#with open(json_file, 'w') as file:
#    json.dump(data_file, file)


#for i in range(len(x_msg)):
#    print(x_msg[i])
#    print(i)


# Next output json
# Format
# temp {average:x, sdev:x} or something like that
    
    