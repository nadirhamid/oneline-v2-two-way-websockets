

import onelinev2
import time

class two_way(object):
  ## start should always be called
  ## before anything setup any information
  def start(self,*args,**kwargs):
     self.messages=[]
     self.last_time=time.time()
     self.state="STOPPED"
     return "Started two way module"
  def end(self,*args,**kwargs):
     return "Ended two way module"
  ## Listener will run in an event loop
  ## we need to make this function one use
  ## per call
  ##
  def listener(self,message):
     print "Calling listener"
     if self.state != "STOPPED":
         #config = onelinev2.parse_config(self)
         
         #message = onelinev2.parse(message)
         time_now = time.time()
         messages =self.find_messages( time_now )
         return onelinev2.pack({"status": "OK", "data":  messages.as_list()} )
     return onelinev2.pack({"status": "EMPTY"})
  ## we wont do anything particular here
  def receiver(self,message):
     print "Calling receiver"
     message=onelinev2.parse(message)
     if message['type']=="STARTED" or message['type'] == "STOPPED":
        self.state=message['type']      
        return onelinev2.pack({"status": "OK", "type": message['type']}) 
     if message['type']=="MESSAGE": 
        message={
            "time": time.time(),
            "from": "",
            "to": message['to'],
            "message": message['message'] }
        self.messages.push( message )
        return onelinev2.pack({"status": "OK", "data": message})
     return onelinev2.pack({"status": "EMPTY"})   

  # helper function to receive our messages
  def find_messages(self, time):
     messages=[]
     for i in self.messages:
        if (i.time>= self.last_time) and (i.time<=time):
           messages.append( i )
     return messages
     
     



