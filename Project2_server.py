import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

# Code copied from Project 1
import time
from psuedoSensor import PseudoSensor
ps = PseudoSensor()
storeStruct = []
alarmOn = False

'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
      
    def on_message(self, message):
        global alarmOn
        print ('message received:  %s' % message)
        # Test for which message is recieved
        if (message == "alarmOn"):
            if alarmOn == False:
                alarmOn = True
                self.write_message("Alarms On")
            else:
                alarmOn = False
                self.write_message("Alarms Off")
        elif (message == "Read1"):
            ts = time.gmtime()
            h,t = ps.generate_values()
            displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
              + " deg  Single Read"
            self.write_message(displayStr)
        elif (message == "Read10"):
            for i in range(1,11):
                ts = time.gmtime()
                h,t = ps.generate_values()
                displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                    + " deg " + str(i)
                self.write_message(displayStr)
                # sleep for 1 second      
                time.sleep(1)
        elif (message == "AvgMinMax"):
            hSum = 0
            hMin = 101.0
            hMax = -.1
            tSum = 0
            tMin = 101.0
            tMax = -21.0
            for ii in range(1,10):
                tss = time.gmtime()
                hh,tt = ps.generate_values()
            
                # Calulate the sum of the 10 readings
                hSum = hh + hSum
                tSum = tt + tSum
            
                # Test to see if the current reading is greater than the current maximum. If so, set the
                # maximum to the current maximum. Do likewise for the minimum.
                if tt > tMax:
                    tMax = tt
                if hh > hMax:
                    hMax = hh
                if hh < hMin:
                    hMin = hh
                if tt < tMin:
                    tMin = tt
                
                # sleep for 1 second      
                time.sleep(1)
            
            #calculate the average of the ten readings
            hAvg = hSum/10
            tAvg = tSum/10

            #Display the average humidity and temperature
            displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",tss) + str(round(hAvg,1)) + \
                     "%  Avg  " + str(round(tAvg,1)) + " deg  Avg"
            self.write_message(displayStr)
        
            #Display the minimum humidity and temperature
            displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",tss) + str(round(hMin,1)) + \
                     "%  Min  " + str(round(tMin,1)) + " deg  Min"
            self.write_message(displayStr)
            
            #Display the minimum humidity and temperature
            displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",tss) + str(round(hMax,1)) + \
                     "%  Max  " + str(round(tMax,1)) + " deg  Max"
            self.write_message(displayStr)

        elif (message == "Close"):
            print ('connection closed')

        elif(message[:6] == "Humd ="):
            print ("Humidity Alarm Set to")
            self.write_message("Humidity alarm set to ")
            
        elif(message[:6] == "Temp ="):
            print ("Temp alarm set to ")
            self.write_message("Temperature alarm set to ")
            
        else:
            print('unknown command recieved')
 
    def check_origin(self, origin):
        return True
        
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
 
