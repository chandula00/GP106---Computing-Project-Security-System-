#2022/02/18
#COM PROJECT
#GROUP 6A
#Group A: Classified Document Room

# import libraries
try:
    from pyfirmata import Arduino,util,  INPUT, OUTPUT
    import paho.mqtt.client as mqtt
except:
    import pip
    pip.main(['install','pyfirmata','paho-mqtt'])
    from pyfirmata import Arduino,util, INPUT, OUTPUT

import pyfirmata as pf
import time
import math

#Setup for mqtt
group = "G6A"
topic = "G6A/CDR/DATA"
mqttBroker = "vpn.ce.pdn.ac.lk"
mqttPort = 8883

# setting up

board = pf.Arduino("COM8")

key_pin1 = 2 #digital pin for password
key_pin2 = 3 #digital pin for password
therm_pin = 4 #analog pin for thermister
ldr_pin = 5   #analog pin for LDR
press_pin =4  #digital pin for pressure sensor

#digital pins for LEDs
led1_pin=5
led2_pin=6
led3_pin=7
led4_pin=8
led5_pin=9
led6_pin=10
led7_pin=12 #woeking LED

buz_pin = 11 #digital pin for buzzer
press_off= 13 #digital pin for reset button


board.analog[therm_pin].mode = pf.INPUT
board.digital[buz_pin].mode = pf.OUTPUT
board.digital[press_off].mode=pf.INPUT
board.digital[press_pin].mode = pf.INPUT
board.analog[ldr_pin].mode = pf.INPUT
board.digital[key_pin1].mode=pf.INPUT
board.digital[key_pin2].mode=pf.INPUT

board.digital[led1_pin].mode = pf.OUTPUT
board.digital[led2_pin].mode = pf.OUTPUT
board.digital[led3_pin].mode = pf.OUTPUT
board.digital[led4_pin].mode = pf.OUTPUT
board.digital[led5_pin].mode = pf.OUTPUT
board.digital[led6_pin].mode = pf.OUTPUT
board.digital[led7_pin].mode = pf.OUTPUT

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    "print(msg.topic+" "+str(msg.payload))"


client = mqtt.Client(group)

try:
    client.connect(mqttBroker, mqttPort)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()

except:
    print("Connection to MQTT broker failed!")
    exit(1)


# UTILIZATION
itr = pf.util.Iterator(board)
itr.start()
#################################################################################
#Working LED
#indicate code is running

def blink():
    run=time.time_ns()
    run=round((run/1e8))% 5
    board.digital[led7_pin].write(run==0)

#################################################################################
#TEMPERATURE CODE

board.analog[therm_pin].enable_reporting()

def Read_Temp():
    global Temp_c
    value = board.analog[therm_pin].read()

#convert thermister value to the celcius value
    if value==None:
        pass
    else:
        Resistor = float((1023.0*10000)/(value*1023)-10000)
        Temp_c = round(float((3435.0/(math.log(Resistor/10000)+(3435.0/(273.15+25))))-(273.15)-20),ndigits=1)
        #print(Temp_c)
    #print(value)
    
    if value == None:
        pass    
    
    elif Temp_c>70:
        board.digital[buz_pin].write(1)
        board.digital[led4_pin].write(1)
        global Fire
        Fire = "Fire Alert"
        

       
    else :
        Fire = "Safe"
        #The buzzer is running until the temperature become limited value
        
        pass
    return Temp_c
        

       
##################################################################################       
        
#PRESSURE CODE

def check_pressure(board,press_pin):
    global p
    press_1 = board.digital[press_pin].read()

    
    
    if press_1 == 1 :
        p = "Pressed"
        print('PRESSURE SENSOR TRIGGERED')
        board.digital[buz_pin].write(1)
        board.digital[led5_pin].write(1)
        data_list = [Temp_c, p, brightness, Door_Status, Fire, light]

        data = ",".join([str(i) for i in data_list])

        client.publish(topic, data)
        time.sleep(0.5)
    else:
        p = "Unpressed"

    return p
 #If pressure is triggered for a time the buzzer and LED will turn on until it is switched off using reset button.      
        

##############################################################################
#LDR CODE

def Read_light():
    global brightness,light
    brightness = round((board.analog[ldr_pin].read())*10,ndigits=1)
    if brightness == None:
        pass
    else:
        if brightness <= 0.5 or brightness >= 8:
            board.digital[buz_pin].write(1)
            board.digital[led3_pin].write(1)
            light = "Attention Required"
            print("CHANGED BRIGHTNESS")
        else:
            light = "Safe"
    return brightness,light
  
     #If brightness is changed for a time the buzzer and LED will turn on until it is switched off using reset button.
    #print(brightness)


##################################################################################

#SECRET ROOM
Door_Status = "Locked"
            
#Confidential room password for staff members
code_low1=['long','long','short','long','short']
code_low2=['long','short','short','long','long']

#Secret room password for staff members
code_secret1=['long','short','long','short','short']
code_secret2=['short','long','short','long','short']

#Top Secret room password for staff members
top_secret1=['long','long','long','short','long']
top_secret2=['short','short','long','short','short']

#variables
code1=[]
code2=[]

key1=[]
key2=[]

isPressed1=False
currentPressed1=False
isPressed2=False
currentPressed2=False

longTime=3

lock1=0
lock2=0

lckst1=1
lckst2=1

entering_password1=False
entering_password2=False


#Code for 1st Staff member
#If it is a long press the switch should be press at least more than a second and if it is a short press the switch should be press for a little time

def secret_code1():

    global code_low1,code1,key1,isPressed1,currentPressed1,lckst1,lock1,entering_password1,Door_Status

    if len(code1)>=5 and entering_password1==True:
        Door_Status = "Entering Passcode"
        data_list = [Temp_c, p, brightness, Door_Status, Fire, light]

        data = ",".join([str(i) for i in data_list])

        client.publish(topic, data)

        #Checking typed password match for confidantial room password one
        if code1==code_low1:
            if lckst1==1:
                lock1='unlock'

                print('Confidential room 1st key Unlockd')
                Door_Status = "confidantial room Unlocked"

                
        #Checking typed password match for Secret room password one
        elif code1==code_secret1:
            if lckst1==1:
                lock1='secret_room_unlock'

                print('Secret room 1st key Unlocked')
                Door_Status = "Secret room 1st key Unlocked"

                
        #Checking typed password match for Top Secret room password one
        elif code1==top_secret1:
            if lckst1==1:
                lock1='top_secret_unlock'

                print('Top secret room 1st key Unlocked')
                Door_Status = "Top secret room 1st key Unlocked"
                
                
        else:
            print("Invalid Password !... Try Again..")
            lock1=0
            Door_Status = "Locked"
            
        entering_password1=False
        
                
    else:
        press_5 = board.digital[key_pin1].read()

        #check whether it has started typing code ,button has been already pressed or not.
        if press_5==1:
            entering_password1=True
            isPressed1=True
            currentPressed1=True
                
            press_5 = board.digital[key_pin1].read()
            
          #depending on the time that button is pressed,values are appending to the list.
            if press_5==1:
                key1.append(1)


        if isPressed1 ==True and press_5==False:
            isPressed1=False
            
        if isPressed1==False and currentPressed1==True:

            
            
            if len(key1)>=longTime:
                print('long')
                code1.append('long')
                
            elif len(key1)==0:
                pass
            
            else:
                print('short')
                code1.append('short')
               
            currentPressed1=False
            
            key1=[]
        return Door_Status
            
        


#code for 2nd staff member

def secret_code2():

    global code_low2,code2,key2,isPressed2,currentPressed2,lckst2,lock2,entering_password2,Door_Status
    
    if len(code2)>=5 and entering_password2==True:

        #Checking typed password match for confidantial room password two
        if code2==code_low2:
            if lckst2==1:
                lock2='unlock'

                print('Confidential room 2nd key Unlock')
                Door_Status = "Confidential room 2nd key Unlock"

                
        #Checking typed password match for Secret room password two
        elif code2==code_secret2:
            if lckst2==1:
                lock2='secret_room_unlock'

                print('Secret room 2nd key Unlocked')
                Door_Status = "Secret room 2nd key Unlocked"

                
        #Checking typed password match for Top Secret room password two
        elif code2==top_secret2:
            if lckst1==1:
                lock2='top_secret_unlock'

                print('Top secret room 2nd key Unlocked')
                Door_Status = "Top secret room 2nd key Unlocked"


        else:
            print("Invalid Password !... Try Again..")
            Door_Status = "Locked"

            lock2=0
            
        
        entering_password2=False

        
               
    else:
        press_6 = board.digital[key_pin2].read()
        if press_6==1:
            entering_password2=True
            isPressed2=True
            currentPressed2=True
               
            press_6 = board.digital[key_pin2].read()


            
            if press_6==1:
                key2.append(1)


        if isPressed2 ==True and press_6==False:
            isPressed2=False
            
        if isPressed2==False and currentPressed2==True:

            #depending on the number of values in the list, it decides whether it is long press or short press
            #If the press is a long one it append values as "long" and if the press is a short one it append values as "short" to the list

            if len(key2)>=longTime:
                print('long')
                code2.append('long')
            elif len(key2)==0:
                pass
            else:
                print('short')
                code2.append('short')
                #count=count+1
            currentPressed2=False
            
            key2=[]

    return Door_Status



#TESTING

#Inform programme is going to start
for i in range (2):
    '''board.digital[buz_pin].write(1)
    time.sleep(0.2)
    board.digital[buz_pin].write(0)
    time.sleep(0.15)
    board.digital[buz_pin].write(1)
    time.sleep(0.5)
    board.digital[buz_pin].write(0)'''
    
    time.sleep(0.5)


#Test buttons, LEDs and buzzzers are working properly
for i in range(3):
   
    print('*'*80)
print('#'*33+'INITIALIZATION'+'#'*33)
for i in range(3):
     print('*'*80)
print("LOADING.......")
test=50
for i in range(2):
    board.digital[led1_pin].write(1)
    time.sleep(0.3)
    board.digital[led1_pin].write(0)
    board.digital[led2_pin].write(1)
    time.sleep(0.3)
    board.digital[led2_pin].write(0)
    board.digital[led3_pin].write(1)
    time.sleep(0.3)
    board.digital[led3_pin].write(0)
    board.digital[led4_pin].write(1)
    time.sleep(0.3)
    board.digital[led4_pin].write(0)
    board.digital[led5_pin].write(1)
    time.sleep(0.3)
    board.digital[led5_pin].write(0)
    board.digital[led6_pin].write(1)
    time.sleep(0.3)
    board.digital[led6_pin].write(0)
    print(test,"% LOADING COMPLITED...")
    test=test+25
board.digital[buz_pin].write(1)
print("*"*25+'LOADING COMPLITED'+"*"*25)
time.sleep(0.5)
board.digital[buz_pin].write(0)


#LOOP

#call the functions    
while True:

    #Call Temperature function
    Read_Temp()
    
    #Call Pressure function
    check_pressure(board,press_pin)
    
    #Call LDR function
    Read_light()

    #Working LED
    blink()

    #Checking secret codes
    secret_code1()
    secret_code2()

    #check password contain relevant number of buttons
    if entering_password1==False and entering_password2==False:
        if len(code1)>=5  and len(code2)>=5:


    #depending on the password it decides which door to unlock
            # If password is correct green light would be blink with two beeps
            # If password is wrong red light would blink with a beep
            if lock1=='unlock' and lock2=='unlock':
                print("***CONFIDENTIAL DOOR UNLOCKED***")
                Door_Status = "***CONFIDENTIAL DOOR UNLOCKED***"
                for i in range(2):
                    board.digital[led6_pin].write(1)
                    board.digital[buz_pin].write(1)
                    time.sleep(0.2)
                    board.digital[led6_pin].write(0)
                    board.digital[buz_pin].write(0)
                    time.sleep(0.1)

                    
            elif lock1=='secret_room_unlock' and lock2=='secret_room_unlock':
                print("***SECRET ROOM DOOR UNLOCKED***")
                Door_Status = "***SECRET ROOM DOOR UNLOCKED***"
                for i in range(2):
                    board.digital[led6_pin].write(1)
                    board.digital[buz_pin].write(1)
                    time.sleep(0.2)
                    board.digital[led6_pin].write(0)
                    board.digital[buz_pin].write(0)
                    time.sleep(0.1)


            elif lock1== 'top_secret_unlock' and lock2=='top_secret_unlock':
                print("***TOP SECRET ROOM DOOR UNLOCKED***")
                Door_Status = "***TOP SECRET ROOM DOOR UNLOCKED***"
                for i in range(2):
                    board.digital[led6_pin].write(1)
                    board.digital[buz_pin].write(1)
                    time.sleep(0.2)
                    board.digital[led6_pin].write(0)
                    board.digital[buz_pin].write(0)
                    time.sleep(0.1)


            else:
                print('WRONG PASSWORD..... TRY AGAIN !')
                board.digital[led2_pin].write(1)
                board.digital[buz_pin].write(1)
                time.sleep(0.4)
                board.digital[led2_pin].write(0)
                board.digital[buz_pin].write(0)

                
            code1.clear()
            code2.clear()
            
        

#If one person's password get wrong he cant type correct password until other person finish typing his password whether correctly or incorrectly.
    
    time.sleep(0.2)
    switch_off=board.digital[press_off].read()
    if switch_off==1:
            board.digital[buz_pin].write(0)
            board.digital[led4_pin].write(0)
            board.digital[led5_pin].write(0)
            board.digital[led3_pin].write(0)
            time.sleep(0.2)
            for i in range(2):
                board.digital[led1_pin].write(1)
                board.digital[buz_pin].write(1)
                time.sleep(0.2)
                board.digital[led1_pin].write(0)
                board.digital[buz_pin].write(0)
                time.sleep(0.1)
                
    else:
        pass

    data_list = [Temp_c,p,brightness, Door_Status, Fire,light]

    data = ",".join([str(i) for i in data_list])


    client.publish(topic, data)  # publish the data to MQTT broker using the topic
    # print('Sent from Arduino ',data)
    time.sleep(0.05)





