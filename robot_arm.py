#!/usr/bin/env python3
from ev3dev.ev3 import *
import ibmiotf.device
from time import time
import os, sys, json

# 재고 수(옮긴 박스 수) 변수
countplus = 0

# 센서 변수 할당
touch = TouchSensor('in1')
gripper = Motor('outD') 
base_motor = Motor('outB')
elbow_motor = Motor('outC')

# 대기 함수
def wait(second):
    current_time = time()
    while time() - current_time < second:
        pass

# IBM Cloud 로 JSON 데이터 발행
def publish_to_IBM(color, boxnum):
    while True:
        try:
            client.publishEvent("boxes", "json", {"color" : color, "boxnum":boxnum}, qos=2)
            print("send!!")
            Sound.beep()
            wait(2)
            break
        except IOError:
            print("Error")
# 손 열기
def gripper_open():
    gripper.run_forever(speed_sp=-65)
    wait(1.5)
    gripper.stop(stop_action='hold')

# 손 닫기
def gripper_close(): 
    gripper.run_forever(speed_sp=60)
    wait(2)
    gripper.stop(stop_action='hold')

# 팔 올리기
def elbow_up():
    elbow_motor.position=0
    elbow_motor.run_forever(speed_sp = -110)
    while elbow_motor.position >= -450:
        pass
    elbow_motor.stop(stop_action = "hold")  
    wait(3)

# 제자리로 돌아가기
def go_to_original():
    base_motor.run_forever(speed_sp = 300)
    while base_motor.position <=0:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)

# 새 박스 가져다 놓기
def new_box(position_angle):
    initialize()
    # 새 박스까지 가기
    base_motor.run_forever(speed_sp = 300)
    while base_motor.position <= 100:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    # 새 박스 위치에서 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 새 박스 잡기
    gripper_close()
    # 새 박스 들기
    elbow_motor.run_forever(speed_sp = -100)
    while elbow_motor.position >= -450:
        pass
    elbow_motor.stop(stop_action = "hold")
    wait(3)
    # 새 박스 내려놓을 위치로 이동
    base_motor.run_forever(speed_sp = -300)
    while base_motor.position >= position_angle:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    # 터치 센서 닿으면 
    if touch.value()==True:
        base_motor.stop(stop_action = 'hold')
    # 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    gripper_open()
    elbow_up()

# 동작 전 초기화
def initialize():
    gripper_close()
    elbow_up()
    gripper_open()

# 동작 함수
def green_box():
    initialize()
    # 박스 위치로 이동
    base_motor.position=0
    base_motor.run_forever(speed_sp = -300)
    while base_motor.position >= -380:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    # 박스 위치에서 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 박스 잡기
    gripper_close()
    # 박스 들기
    elbow_motor.run_forever(speed_sp = -110)
    while elbow_motor.position >= -450:
        pass
    elbow_motor.stop(stop_action = "hold")
    wait(3)
    # 박스내려놓을 위치 이동
    base_motor.run_forever(speed_sp = -300)
    while base_motor.position >= -650:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    if touch.value()==True:
        base_motor.stop(stop_action = 'hold')
    # 박스 위치까지 팔 내리기
    elbow_motor.run_forever(speed_sp = 100)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 박스 놓기
    gripper_open()
    # 팔 올리기
    elbow_up()
    # 다시 돌아가기
    go_to_original()
    # 박스 위치까지 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")

    publish_to_IBM(countcolor, countplus)

    new_box(-400)
    go_to_original()
    # 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")

def yellow_box():
    initialize()
    # 박스 위치로 이동
    base_motor.position=0
    base_motor.run_forever(speed_sp = -300)
    while base_motor.position >= -290:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    # 박스 위치에서 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 박스 잡기
    gripper_close()
    # 박스 들기
    elbow_motor.run_forever(speed_sp = -100)
    while elbow_motor.position >= -450:
        pass
    elbow_motor.stop(stop_action = "hold")
    wait(3)
    # 박스 내려놓을 위치로 이동
    base_motor.run_forever(speed_sp = -300)
    while base_motor.position >= -610:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    # 터치센서 닿으면 
    if touch.value()==True:
        base_motor.stop(stop_action = 'hold')
    # 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 박스 놓기
    gripper.run_forever(speed_sp=-50)
    wait(2)
    gripper.stop(stop_action = 'hold')
    # 팔 올리기
    elbow_up()
    # 다시 돌아가기
    go_to_original()
    # 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 컬러소터에게 JSON 데이터 발행
    publish_to_IBM(countcolor, countplus)
    # 새 박스 갖다놓기
    new_box(-310)
    # 다시 돌아가기
    go_to_original()
    # 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")

def red_box():
    initialize()
    # 동작 시작
    base_motor.position=0
    base_motor.run_forever(speed_sp =  -320)
    while base_motor.position >= -205:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    # 박스 위치에서 팔 내리기
    elbow_motor.run_forever(speed_sp = 100)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 박스 잡기
    gripper_close()
    # 박스 들기
    elbow_motor.run_forever(speed_sp = -100)
    while elbow_motor.position >= -450:
        pass
    elbow_motor.stop(stop_action = "hold")
    wait(3)
    # 박스 내려놓을 위치까지 이동
    base_motor.run_forever(speed_sp = -300)
    while base_motor.position >= -530:
        pass
    base_motor.stop(stop_action = "hold")
    wait(0.5)
    if touch.value()==True:
        base_motor.stop(stop_action = 'hold')
    # 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    # 박스 놓기
    gripper.run_forever(speed_sp=-50)
    wait(2)
    gripper.stop(stop_action = 'hold')
    # 팔 올리기
    elbow_up()
    # 다시 돌아가기
    go_to_original()
    # 팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
    publish_to_IBM(countcolor, countplus)
    new_box(-225)
    #다시 돌아가기
    go_to_original()
    #팔 내리기
    elbow_motor.run_forever(speed_sp = 110)
    while elbow_motor.position <= 0:
        pass
    elbow_motor.stop(stop_action = "hold")
countplus = 0

# IBM Cloud 에서 구독한 데이터에 따라 실행할 함수 결정
def CommandCallback(event):
    global countcolor
    global countplus
    print(event.data)
    if event.command == "color_number":
        Sound.beep()
        data = event.data
        if int(data["green"])>=3:
            color = data["green"]
            countcolor = "green"
            print("green")
            countplus += 1
            green_box()
        if int(data["yellow"])>=3:
            color = data["yellow"]
            countcolor = "yellow"
            print("yellow")
            countplus += 1
            yellow_box()
        if int(data["red"])>=3:
            color = data["red"]
            countcolor = "red"
            print("red")
            countplus += 1
            red_box()

# IBM Cloud 에 등록된 Robot_Arm 정보
options = {
    "org": "b5ixrk",
    "type": "Ev3",
    "id": "Robot_Arm",
    "auth-method": "token",
    "auth-token": "g@1UPpSxftL(nrKNl&",
    "clean-session": True}

# IBM Cloud 로부터 구독 실행
try:
    client = ibmiotf.device.Client(options)
    client.connect()
    client.commandCallback = CommandCallback
except ibmiotf.ConnectionException as e:
    print(e)
while True:
    pass

elbow_motor.run_forever(speed_sp = -110)
while elbow_motor.position >= -450:
    pass
elbow_motor.stop(stop_action = "hold")
wait(3)

#박스위치까지 팔 내리기
elbow_motor.run_forever(speed_sp = 110)
while elbow_motor.position <= 0:
    pass
elbow_motor.stop(stop_action = "hold")
