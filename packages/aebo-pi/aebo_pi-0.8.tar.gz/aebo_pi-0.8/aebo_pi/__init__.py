from picamera import PiCamera
from time import sleep
import mediapipe
import cv2
from tkinter import *
from turtle import *
import RPi.GPIO as GPIO
from time import sleep
import pyttsx3
import pyaudio
import wave
import speech_recognition as sr
import random

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44000
# Change this to change the recording time
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "/home/pi/output.wav"

engine = pyttsx3.init()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

motor1 = GPIO.PWM(19, 500)
motor2 = GPIO.PWM(21,500)

def Forward(speed):
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(20,GPIO.HIGH)
    motor1.start(speed) #to increase the seed increase this value 0-100
    motor2.start(speed)

def Backward(speed):
    GPIO.output(16,GPIO.LOW)
    GPIO.output(20,GPIO.LOW)
    motor1.start(speed) #to increase the seed increase this value 0-100
    motor2.start(speed)
    
def Left(speed):
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(20,GPIO.LOW)
    motor1.start(speed) #to increase the seed increase this value 0-100
    motor2.start(speed)
    
def Right(speed):
    GPIO.output(16,GPIO.LOW)
    GPIO.output(20,GPIO.HIGH)
    motor1.start(speed) #to increase the seed increase this value 0-100
    motor2.start(speed)
    
def Stop():
    motor1.stop()
    motor2.stop()

def Speak(text):
    engine.say(text)
    engine.runAndWait()

def RecogniseText():
    print("Hello. Please say something")
    
    ## Program to record the input from mic
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("*"*80)
    
    
    
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("*"*80)
    print("Stop speaking")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    ##Playing the recorded sound
    r = sr.Recognizer()
    audio = sr.AudioFile('/home/pi/output.wav')
    with audio as source:
        a = r.record(source)
        return r.recognize_google(a)

def takePhoto(filename):
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/Desktop/'+filename+'.jpg')
    camera.stop_preview()
    camera.close()

def showPreview(time):
    camera = PiCamera()
    camera.start_preview()
    sleep(time)
    camera.stop_preview()
    camera.close()
    

    
def recogniseHand():
    #Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands

    #Use CV2 Functionality to create a Video stream and add some values
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
         while True:
               ret, frame = cap.read()
           #Unedit the below line if your live feed is produced upsidedown
               #flipped = cv2.flip(frame, flipCode = -1)
           
           #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
               frame1 = cv2.resize(frame, (640, 480))
           
           #Produces the hand framework overlay ontop of the hand, you can choose the colour here too)
               results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
           
           #In case the system sees multiple hands this if statment deals with that and produces another hand overlay
               if results.multi_hand_landmarks != None:
                  for handType,handLms in zip(results.multi_handedness,results.multi_hand_landmarks):
                      handy =  (handType.classification[0].label)
                      if handy=='Left':
                          handy='Right'
                      elif handy=='Right':
                          handy='Left'
                  for handLandmarks in results.multi_hand_landmarks:
                      drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
               else:
                  handy =  None  
                  
                              
           #Below shows the current frame to the desktop 
               cv2.imshow("Frame", frame1);
               key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
               if key == ord("q"):
                   Stop()
                   #break
                   exit()
               return handy
               #cv2.destroyAllWindows()

    

def stop():
    key = cv2.waitKey(1)&0xFF
    if key == ord('q'):
        exit()

def countFingers():
    #Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands

    #Use CV2 Functionality to create a Video stream and add some values
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

#Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
#image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
#More hands can be tracked at the same time if desired but will slow down the system
    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
         while True:
               ret, frame = cap.read()
           #Unedit the below line if your live feed is produced upsidedown
           #flipped = cv2.flip(frame, flipCode = -1)
           
           #Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
               frame1 = cv2.resize(frame, (640, 480))
           
           #Produces the hand framework overlay ontop of the hand, you can choose the colour here too)
               results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
               count=0
           
           #In case the system sees multiple hands this if statment deals with that and produces another hand overlay
               if results.multi_hand_landmarks != None:
                  for handType,handLms in zip(results.multi_handedness,results.multi_hand_landmarks):
                      handy =  (handType.classification[0].label)
                      if handy=='Left':
                          handy='Right'
                      elif handy=='Right':
                          handy='Left'
                  for handLandmarks in results.multi_hand_landmarks:
                      drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                      #print (handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP].y)
                      #print (handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_PIP].y)
                      if handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_TIP].y<handLandmarks.landmark[handsModule.HandLandmark.INDEX_FINGER_PIP].y:
                          count=count+1
                      if handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_TIP].y<handLandmarks.landmark[handsModule.HandLandmark.MIDDLE_FINGER_PIP].y:
                          count=count+1
                      if handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_TIP].y<handLandmarks.landmark[handsModule.HandLandmark.RING_FINGER_PIP].y:
                          count=count+1
                      if handLandmarks.landmark[handsModule.HandLandmark.PINKY_TIP].y<handLandmarks.landmark[handsModule.HandLandmark.PINKY_PIP].y:
                          count=count+1
                      if handy=='Left'and (handLandmarks.landmark[handsModule.HandLandmark.THUMB_TIP].x<handLandmarks.landmark[handsModule.HandLandmark.THUMB_IP].x):
                          count=count+1
                      if handy=='Right'and (handLandmarks.landmark[handsModule.HandLandmark.THUMB_TIP].x>handLandmarks.landmark[handsModule.HandLandmark.THUMB_IP].x):
                          count=count+1
               else:
                  handy =  None  
                  
                              
           #Below shows the current frame to the desktop 
               cv2.imshow("Frame2", frame1);
               key = cv2.waitKey(1) & 0xFF
           
           #Below states that if the |q| is press on the keyboard it will stop the system
               if key == ord("q"):
                   Stop()
                   #break
                   exit()
               return count
               #cv2.destroyAllWindows()
