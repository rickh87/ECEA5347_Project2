import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

# Code copied from Project 1
import time
from psuedoSensor import PseudoSensor
ps = PseudoSensor()
alarmOn = False
storeStruct = []

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
        print ('message received:  %s' % message)
        # Test for which message is recieved
        if (message == "alarmOn"):
            onClicked()
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
            on_close()
        else:
            print('unknown command recieved')
 
    def on_close(self):
        print ('connection closed')
 
    def check_origin(self, origin):
        return True

# When the Alarms On/Off radio button is clicked in the client this codes checks to see
# the alarm on/off, toggles the flag and sends the flag to the client

    def onClicked():
        global alarmOn
        if alarmOn:
            alarmOn = False
            WSHandler.write_message('Alarm Off')
        else:           
            alarmOn = True
            WSHandler.write_message('Alarm On')



    def read10():
        ts = time.gmtime()
        h,t = ps.generate_values()
        displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                     + " deg  Single Read"
        WSHandler.write_message(displayStr)

    def avgMinMax():
        ts = time.gmtime()
        h,t = ps.generate_values()
        displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                     + " deg  Single Read"
        WSHandler.write_message(displayStr)
        
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
 
