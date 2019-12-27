#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import time
import sys, os, json
import ibmiotf.application
import ev3dev.fonts as fonts
import paho.mqtt.client as mqtt

def EventCallback(event):
    #print("got event" + json.dumps(event.data))
    #a = json.dumps(event.data)
    global greennum
    global yellownum
    global rednum
    #global switch
    while True:
        try:
            if event.event == 'boxes':
                Sound.speak('boxes')
                data = event.data
                if data["color"]=="green":
                    print("green")
                    greennum -= 3
                    print('total: green',greennum,'yellow', yellownum, 'red', rednum)
                    break
                elif data["color"]=="yellow":
                    print("yellow")
                    yellownum -= 3
                    print('total: green',greennum,'yellow', yellownum, 'red', rednum)
                    break
                elif data["color"]=="red":
                    print("red")
                    rednum -= 3
                    print('total: green',greennum,'yellow', yellownum, 'red', rednum)
                    break
                else:
                    pass
            else:
                pass
        except IOError:
           print("Error")


options = { 
    "org": "b5ixrk", 
    "type": "Ev3", 
    "id": "Color_Sorter", 
    "auth-method": "token", 
    "auth-key":"a-b5ixrk-rcpxl7yhor",
    "auth-token":"pi32JyZ3j5V9HqDbRs", 
    "clean-session": True}

try: 
    client = ibmiotf.application.Client(options)
    client.connect() 
except ibmiotf.ConnectionException as e: 
    print(e)

Sound.beep()

belt_motor = LargeMotor('outA')
feed_motor = MediumMotor('outB')

colors = ColorSensor('in3')
colors.mode = 'COL-COLOR'
touchs = TouchSensor('in2')
button = Button()

#인식 가능한 색상 값
possible_color = [3,4,5]
#lcd = Screen()

def wait(second): 
    current_time= time() 
    while time() - current_time < second: 
        pass

#전체 컬려별 개수 리스트
#all_color_list = []
greennum = 0
yellownum = 0
rednum = 0 

print("start")
while True:
    color_list = []
    while len(color_list) < 8:
        #Sound.speak("start")
        while True:
            pressed = button.enter
            color = colors.value()
            #button.buttons_pressed
            if pressed or (color in possible_color):
                break
        if pressed:
            Sound.beep()
            break
        else:
            Sound.beep()
            color_list.append(color)
            if color == 3:
                greennum +=1
            elif color == 4:
                yellownum +=1
            else:
                rednum +=1
            # color_all_list.append(color)
            # '3'='green'
            # '4' == 'yellow'
            # '5' == 'red'
            print("colornumber=",color," length = ",len(color_list))
            wait(1)

    for color in color_list:
        Sound.beep()
        wait(1)
        #터치센서있는곳까지 오기
        belt_motor.run_forever(speed_sp = -200)
        while not touchs.value():
            pass
        belt_motor.stop(stop_action= "hold")  
        
        if color == 3:
            belt_motor.run_forever(speed_sp=200) 
            wait(0.2)
            belt_motor.stop(stop_action="hold") 
        elif color == 4:
            belt_motor.run_forever(speed_sp=200) 
            wait(1.6)
            belt_motor.stop(stop_action="hold") 
        elif color == 5:
            belt_motor.run_forever(speed_sp=200) 
            wait(2.8)
            belt_motor.stop(stop_action="hold") 

        feed_motor.position = 0
        #레고뱉기
        feed_motor.run_forever(speed_sp = -300)
        while feed_motor.position >= -150:
            pass
        feed_motor.stop(stop_action = "hold")

        feed_motor.run_forever(speed_sp = 300) 
        while feed_motor.position < 0:
            pass
        feed_motor.stop(stop_action = "hold")
        wait(0.5)

    #색상레고 개수 메시지발행
    while True: 
        client.publishCommand("Ev3", "Robot_Arm", 
        "color_number", "json",{'green':greennum,'yellow':yellownum,'red':rednum}) 
        print('total: green',greennum,'yellow', yellownum, 'red', rednum)
        break
    
    
    #event에 따라 수행할 작업
    while True:
        client.deviceEventCallback = EventCallback    
        break
    
    #로봇팔이 가져간 컬러 데이터 받기
    #디바이스 type, id, event
    client.subscribeToDeviceEvents(
        deviceType = "Ev3",
        deviceId = "Robot_Arm",
        event="boxes",
        qos = 2)

    

    



