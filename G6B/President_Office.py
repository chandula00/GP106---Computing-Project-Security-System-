#import libraries
from pyfirmata import Arduino, util, INPUT, OUTPUT
import time
from numpy import log
import turtle

#setup board
board = Arduino('COM7')
iterator = util.Iterator(board)
iterator.start()

#setup pins
thermister = board.analog[0]                #thermister pin
Fire_alert_LED = board.digital[5]           #red LED pin
Fire_alert_buzzer = board.digital[7]        #buzzer pin
Fire_alert_off = board.digital[6]           #push button 1
knocking_button1 = board.digital[12]        #push button 4
knocking_button2 = board.digital[8]         #push button 3
Threat_alert_LED = board.digital[5]         #red LED pin
Giving_Access_LED = board.digital[2]        #green LED pin
Threat_buzzer = board.digital[7]            #buzzer pin
Threat_alert_off = board.digital[6]         #push button 1
Emergency_lockdown = board.digital[3]
panic_button = board.digital[10]            #push button 2
panic_off_button = board.digital[6]         #push button 1

#set pin modes
thermister.mode = INPUT
Fire_alert_LED.mode = OUTPUT
Fire_alert_buzzer.mode = OUTPUT
Fire_alert_off.mode = INPUT
knocking_button1.mode = INPUT
knocking_button2.mode = INPUT
Threat_alert_LED.mode = OUTPUT
Threat_buzzer.mode = OUTPUT
Threat_alert_off.mode = INPUT
Emergency_lockdown.mode = OUTPUT
panic_button.mode = INPUT
panic_off_button.mode = INPUT
Giving_Access_LED.mode = OUTPUT

    
#setup display with turtle graphics
wn = turtle.Screen()
wn.title('President Office')
wn.bgcolor('LightSkyBlue4')
wn.setup(width = 800, height = 800)
wn.tracer(0)

#create pen for display with turtle graphics
pen = turtle.Turtle()
pen.speed(0)
pen.shape('square')
pen.color('white')

#set invalid count to zero
invalid_count = 0
#Set temperature value to zero
temp = 0

def display_text(pen,x,y,text,align):
    '''A function to display a text with given alignment'''
    
    pen.penup()
    pen.goto(x,y)
    pen.hideturtle()
    pen.write(text, align = align, font = ('Courier', 24, 'bold'))



def read_temperature(thermister):
    '''A function to read thermister value and return temperature'''
    global temp
    sum = 0
    for i in range(10):
        value = thermister.read()
        sum += value
    
    temp = round(1/((1/273)-(1/1948)*(log((sum/10)/0.34))) - 273.15, ndigits = 3)
    display_text(pen, 0, 360,'Temperature', 'center')
    display_text(pen, 0, 300,temp, 'center')
    time.sleep(1)
    return temp


# defining a function for allowing access to the President Office
def secret_door():
    '''A fuction for allowing access to the President Office'''
    
    global invalid_count
    global knock_code
    global pass_code
    global Threat_alert_State
    
    #alocating a space for knock code
    knock_code =[]
    
    pass_code = [1,1,1,0,0,1,0]

    #gets knock code from user
    print('Enter Knock Knock')
    time.sleep(0.5)
    for i in range(1,8):
        time.sleep(0.5)

        #displays instructions
        pen.clear()
        display_text(pen, 0, 360,'Knock Your Pattern', 'center')
        wn.bgcolor('blue')
        display_text(pen, 0, 250,i, 'center')
        print('knok',i)

        time.sleep(1)
        x = knocking_button1.read()
        y = knocking_button2.read()
        if x == True:
            knock_code.append(1)
        elif y == True:
             knock_code.append(0)
        
        #displays the entered code
        display_text(pen, 0, 150,knock_code, 'center')
    
    #when knock code is correct
    if knock_code == pass_code:
        pen.clear()
        display_text(pen, 0, 0,'Welcome to the president office', 'center')
        wn.bgcolor('green')
        print('Access given to the president office')
        Giving_Access_LED.write(1)
        Threat_buzzer.write(1)
        time.sleep(0.2)
        Threat_buzzer.write(0)
        time.sleep(1)
        Giving_Access_LED.write(0)
        
    #when knock code is invalid
    else:
       pen.clear()
       display_text(pen, 0, 260,'Invalid Knock Code', 'center')    #displays code is invalid
       wn.bgcolor('red')
       print('invalid knock code')

       #gives alert
       Threat_alert_LED.write(1)
       Threat_buzzer.write(1)
       time.sleep(1)
       Threat_alert_LED.write(0)
       Threat_buzzer.write(0)
       
       invalid_count += 1
       print(invalid_count)
       if invalid_count > 2:
           #displays the alert
           display_text(pen, 0, 0,'ALERT : An unauthorised entry attempt', 'center')
           display_text(pen, 0, -60,'Emergency LOCKDOWN', 'center')
           print('Threat Alert')
           print('emergency lockdown')
           
           invalid_count = 2
           Threat_alert_State = 'Yes'
           Threat_alert()
           

#panic button for the office
def panic_button_fn():
    '''A function for panic button'''
    
    global panic_off
    panic = panic_button.read()
    if panic == True:
       global Threat_alert_State
       Threat_alert_State = 'Yes'
       
       
       #displays threat alert
       pen.clear()
       display_text(pen, 0, 100,'Threat ALERT', 'center')
       display_text(pen, 0, -100,'Emergency LOCKDOWN', 'center')
       wn.bgcolor('red')
       print('Threat Alert')
       print('emergency lockdown')
       
    else:
        #when wants to turn off alerts
        panic_off = panic_off_button.read()
        if panic_off == True:
            Threat_alert_State = 'No'
            Emergency_lockdown.write(0)
            pen.clear()
            display_text(pen, 0, 0,'NOW SAFE', 'center')
            wn.bgcolor('green')
            print('Threat Alert and emergency lockdown off')
            time.sleep(1)
    
    
#how threat alert works
def Threat_alert():
    '''A function to difine how threat alert works'''

    while Threat_alert_State == 'Yes':
        Threat_alert_LED.write(1)
        Threat_buzzer.write(1)
        time.sleep(0.3)
        Threat_alert_LED.write(0)
        Threat_buzzer.write(0)
        time.sleep(0.3)
        panic_off = panic_off_button.read()
        
        if panic_off == True:
            panic_button_fn()
            break
           

def TemperatureAlert():
    '''A function to check whether temperature is above critical temperature or not'''

    global Threat_alert_State
    temperature = read_temperature(thermister)
    if temperature > 40:
        pen.clear()
        display_text(pen, 0, 0,'Fire ALERT', 'center')
        wn.bgcolor('red')
        print('fire alert')
        Threat_alert_State = 'Yes'


#Continues_main_loop
while True:
    
    
    #introducing the program to user
    pen.clear()
    display_text(pen, 0, 0,'President Office | SECURITY SYSTEM', 'center')
    wn.bgcolor('LightSkyBlue4')

    S_d = knocking_button1.read()
    if S_d == True:
        secret_door()
    
    Threat_alert_State = 'No'

    TemperatureAlert()
    panic_button_fn()
    Threat_alert()
    

    # to exit from the system
    exit_p = knocking_button2.read()
    if exit_p == True:
        exit()

