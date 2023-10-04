import paho.mqtt.subscribe as subscribe
import json

def get_next_uplink(username, apikey,host="eu1.cloud.thethings.industries",timeout=10):
      """
      This function waits maximum [timeout] s to intercept an uplink message from a device connected to TTN.
      The data are returned as a json dict.
      """
      m = subscribe.simple(topics=['#'], 
                         hostname=host, 
                         port=1883, 
                         auth={'username':username,
                               'password':apikey}, 
                         msg_count=1,
                         keepalive=timeout)
      return json.loads(m)
