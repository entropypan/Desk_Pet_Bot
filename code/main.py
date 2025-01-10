import time
import smbus
import json
import datetime
import os
import requests
import sys
import mediapipe as mp
import cv2
import math
import threading
import requests
from pytz import timezone
from pydub import AudioSegment
from pydub.playback import play
from multiprocessing import Process

### weather ###
API_KEY = '' # !!! 
url = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization='+API_KEY+'&downloadType=WEB&format=JSON'
wdata = requests.get(url)
wdata_json = wdata.json()
loc= wdata_json['cwaopendata']['dataset']['location']

maxt8 = 50
mint8 = 0
pop8 = 300

for i in loc:
    city = i['locationName']
    if city == '桃園市':
        maxt8 = i['weatherElement'][1]['time'][0]['parameter']['parameterName']  # 最高溫
        mint8 = i['weatherElement'][2]['time'][0]['parameter']['parameterName']  # 最低溫
        ci8 = i['weatherElement'][3]['time'][0]['parameter']['parameterName']    # 舒適度
        pop8 = i['weatherElement'][4]['time'][0]['parameter']['parameterName']   # 降雨機率

### 2x16 LCD ###

LCD_WIDTH = 16 
I2C_ADDR  = 0x27
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0 
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4
LCD_BACKLIGHT  = 0x08
ENABLE = 0b00000100

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)

def lcd_init():
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)
  time.sleep(E_DELAY)
  
def lcd_byte(bits, mode):
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
    
lcd_init()


### Hand Tracking ###
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

def hand_pos(finger_angle, flag):
    global mFlag
    global cnt
    global cf
    global rf
    global cn
    global pMusic
    global pBell
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1<50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        
        return 'good'
    elif f1>=50 and f2>=50 and f3<50 and f4>=50 and f5>=50:
        bgw.clear()
        if flag == 0:
            lcd_init()
        lcd_string("  STOP PLAYING  ",LCD_LINE_1)
        lcd_string("< LITTLE STAR > ",LCD_LINE_2)
        if mFlag == 1:
            
            pMusic.terminate()
            mFlag = 0
        return 'no!!!'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5<50:
        
        return 'ROCK!'
    elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        
        return '0'
    elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        bgw.clear()
        if flag == 0:
            lcd_init()
        lcd_string("  START PLAYING ",LCD_LINE_1)
        lcd_string(" < LITTLE STAR >",LCD_LINE_2)
        if mFlag == 0:
            mFlag = 1
            pMusic = Process(target=play, args=(some_audio,))
            pMusic.start()
        return 'pink'
    elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        bgw.clear()
        if flag == 0:
            lcd_init()
        weather1 = "Temp: "+ str(mint8)+  " - " + str(maxt8)
        weather2 = "Rain%: " + str(pop8) + "%"
        lcd_string(weather1,LCD_LINE_1)
        lcd_string(weather2,LCD_LINE_2)
        
        return '1'
    elif f1>=50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        
        
        return '2'
    elif f1>=50 and f2>=50 and f3<50 and f4<50 and f5<50:
        if cf == 1 & rf == 1:
            cf = 0
            rf = 0
            pBell.terminate()
            bgw.clear()
            if flag == 0:
                lcd_init()
            lcd_string("  STOP TIMER    ",LCD_LINE_1)
            lcd_string("ENJOY YOUR FOOD!",LCD_LINE_2)
        return 'ok'
    elif f1<50 and f2>=50 and f3<50 and f4<50 and f5<50:
        if cf == 1 & rf == 1:
            cf = 0
            rf = 0
            pBell.terminate()
            cn.terminate()
            bgw.clear()
            if flag == 0:
                lcd_init()
            lcd_string("  STOP TIMER    ",LCD_LINE_1)
            lcd_string("ENJOY YOUR FOOD!",LCD_LINE_2)
        return 'ok'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
        if cf == 0 & rf == 0:
            cf = 1
            rf = 0
            cn = Process(target = cupmen)
            cn.start()
            bgw.clear()
            if flag == 0:
                lcd_init()
            lcd_string("  START TIMER   ",LCD_LINE_1)     
            lcd_string(str(cnt)+" sec left ",LCD_LINE_2)
            
        elif rf == 0:
            bgw.clear()
            if flag == 0:
                lcd_init()
            lcd_string("   YOUR TIMER   ",LCD_LINE_1)
            lcd_string(str(cnt)+" sec left ",LCD_LINE_2)
            
            
        return '3'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5<50:
        
        return '4'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
        bgw.clear()
        localtime = time.localtime()
        if flag == 0:
            lcd_init()
        result1 = time.strftime("%Y-%m-%d", localtime)
        result2 = time.strftime("%I:%M:%S %p", localtime)
        lcd_string(result1,LCD_LINE_1)
        lcd_string(result2,LCD_LINE_2)
        return '5'
    elif f1<50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        
        return '6'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        
        return '7'
    elif f1<50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        
        return '8'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5>=50:
        
        return '9'
    else:
        bgw.set()
        return ''
    
### emotions & music & timer ###

def background():
    while True:
        lcd_string("     0     0    ",LCD_LINE_1)
        lcd_string("        .       ",LCD_LINE_2)
        time.sleep(1)
        bgw.wait()
        lcd_string("     -     -    ",LCD_LINE_1)
        lcd_string("        .       ",LCD_LINE_2)
        time.sleep(1)
        bgw.wait()
        
def cupmen():
    global cnt
    global rf
    global cf
    global cn
    global pBell
    cf = 1
    rf = 0
    cnt = 180
    cntt = cnt
    for i in range(cntt):
        time.sleep(1)
        cnt -= 1
    rf = 1
    while cf == 1:
        pBell = Process(target=play, args=(ring,))
        pBell.start()
        for i in range(17):
            if cf == 0:
                break
            time.sleep(1)
        
        

bgw = threading.Event()
bg = threading.Thread(target = background)
bgw.set()
bg.start()

cn = Process(target = cupmen)

some_audio = AudioSegment.from_file('sound/Mozart1.mp3')
pMusic = Process(target=play, args=(some_audio,))
ring = AudioSegment.from_file('sound/clock_bell.mp3')

cap = cv2.VideoCapture(-2, cv2.CAP_V4L)
fontFace = cv2.FONT_HERSHEY_SIMPLEX 
lineType = cv2.LINE_AA               
ttext = ''
flag = 0

mFlag = 0
cf = 0
rf = 0
cnt = 180

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    w, h = 540, 310     
    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (w,h))    
        img = cv2.rotate(img, cv2.ROTATE_180)
    
        if not ret:
            print("Cannot receive frame")
            break
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img2)     
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = []         
                for i in hand_landmarks.landmark:
                    x = i.x*w
                    y = i.y*h
                    finger_points.append((x,y))
                if finger_points:
                    finger_angle = hand_angle(finger_points) 
                    text = hand_pos(finger_angle, flag)   
                    flag = 1
                    if text != ttext:
                        bgw.set()
                        lcd_init()
                        flag = 0
                    ttext = text
                    cv2.putText(img, text, (30,120), fontFace, 5, (255,255,255), 10, lineType)
                else :
                    bgw.set()
                    print('else')
                    
        cv2.imshow('oxxostudio', img)
        if cv2.waitKey(5) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()