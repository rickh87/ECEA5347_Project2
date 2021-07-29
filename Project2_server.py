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
humid = 80.0
temp = 80.0

'''
The web socket handler is derived from the HelloWorld example from the Tornado
Websockets website at https://os.mbed.com/cookbook/Websockets-Server 
'''
# Create a web socket handler
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
      
    def on_message(self, message):
        global alarmOn
        global humid
        global temp
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
            # read 1 time stamp, humidity and temperature
            ts = time.gmtime()
            h,t = ps.generate_values()
            print(h, humid, t, temp)
            # if the alarm is set, test to see if humidity and temperature
            # are exceeded. If so, add text to indicate alarm
            if alarmOn:
                if ((h >= humid) and (t < temp)):
                    displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                      + " deg  Single Read   Humidity Alarm"
                elif ((h < humid) and (t >= temp)):
                    displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                      + " deg  Single Read Temperature Alarm"
                elif ((h >= humid) and (t >= temp)):
                    displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                      + " deg  Single Read Humid/Temp Alarm"
                else:
                    displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                      + " deg  Single Read"
            else:
                displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                  + " deg  Single Read"
            self.write_message(displayStr)
        elif (message == "Read10"):
            # read 10 time stamps, humidities and temperatures            
            for i in range(1,11):
                ts = time.gmtime()
                h,t = ps.generate_values()
                # if the alarm is set, test to see if humidity and temperature
               # are exceeded. If so, add text to indicate alarm
                if alarmOn:
                    if ((h >= humid) and (t < temp)):
                        displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                          + " deg " + str(i) + " Humidity Alarm"
                    elif ((h < humid) and (t >= temp)):
                        displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                          + " deg " + str(i) + " Temperature Alarm"
                    elif ((h >= humid) and (t >= temp)):
                        displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                          + " deg " + str(i) + " Humid/Temp Alarm"
                    else:
                        displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                          + " deg " + str(i)
                else:
                    displayStr = time.strftime("%Y-%m-%d %H:%M:%S   ",ts) + str(round(h,1)) + "%  " + str(round(t,1)) \
                      + " deg " + str(i)
                self.write_message(displayStr)
                # sleep for 1 second      
                time.sleep(1)
        elif (message == "AvgMinMax"):
            #Calculate the average, the minimum and maximum of 10 readings
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
            #Close the connection
            print ('connection closed')
            self.close()

        elif(message[:6] == "Humd ="):
            #Set the humidty alarm.
            #First test to see if a valid number was entered
            try:
               #round the number to one decimal place 
               t_humid = round(float(message[6:]),1)
               #test to see if the humidity entered is within valid range
               if ((t_humid >= 0.0) and (t_humid <= 100.0)):
                  humid = t_humid
                  print (f"Humidity Alarm Set to {humid}")
                  self.write_message(f"Humidity alarm set to {humid}")
               else:
                  print ("Humidity entered is out of range")
                  self.write_message("Humidity entered is out of range")
            except:                 
               print ("Humidity entry is not a valid number")
               self.write_message("Humidity entry is not a valid number")
        elif(message[:6] == "Temp ="):
            #test to see if the temperature entered is a valid number
            try:
               #rond off to one decimal place 
               t_temp = round(float(message[6:]),1)
               #test to see if temperature entered is within range
               if ((t_temp >= -20.0) and (t_temp <= 100.0)):
                  temp = t_temp
                  print (f"Temperature Alarm Set to {temp}")
                  self.write_message(f"Temperature alarm set to {temp}")
               else:
                  print ("Temperature entered is out of range")
                  self.write_message("Temperature entered is out of range")
            except:                 
               print ("Temperature entry is not a valid number")
               self.write_message("Temperature entry is not a valid number")
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
 
