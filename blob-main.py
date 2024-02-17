import cv2
import numpy as np
import dlib
import time
from picamera import PiCamera

from time import sleep
from picamera.array import PiRGBArray
from gpiozero import LED
import math
import RPi.GPIO as GPIO


#time.sleep(20)

#led = LED(17)
#for _ in range(5):
#	led.on()
#	time.sleep(0.5)
#	led.off()
#	time.sleep(0.5)

#setup the motor 
motor_pin_1A = 13
motor_pin_1B = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin_1A, GPIO.OUT)
GPIO.setup(motor_pin_1B, GPIO.OUT)

#initialize the PWM
motor_pwm_1A = GPIO.PWM(motor_pin_1A, 50)
motor_pwm_1B = GPIO.PWM(motor_pin_1B, 50)
motor_pwm_1A.start(0)
motor_pwm_1B.start(0)

#camera setup
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

#camera.start_preview(alpha=192)
#sleep(1)
#camera.capture("/home/pi/Desktop/pic.jpg")
#camera.stop_preview()

#not encoder.wait(self.CAPTURE_TIMEOUT):
    
    #File "/usr/lib/python3/dist-packages/picamera/encoders.py", line 395, in wait
    #self.stop()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/selindursun/Downloads/shape_predictor_68_face_landmarks.dat")


def move_motor(speed_1A, speed_1B):
    motor_pwm_1A.ChangeDutyCycle(speed_1A)
    motor_pwm_1B.ChangeDutyCycle(speed_1B)
    
def stop_motor():
    motor_pwm_1A.ChangeDutyCycle(0)
    motor_pwm_1B.ChangeDutyCycle(0)
    

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)
    

def ifFacing(landmarks, flex):
    '''
    This is function to detect if the user has turned their head by culculate
    the width of their left and right face.
    If any of their left/right face width is less than 1/5 of their whole face width,
    we would assume they have turned their face.
    
    *Param: landmarks: face landmarks given by opencv
            flex: a number in between [0.2,0.7], the higher it is, the more sensitive it
            will be to the head truning motion
    *Return: (bool) True if they are facing the camera
                    False if they turn their head
    '''
    nose_point = (landmarks.part(33).x, landmarks.part(33).y) #nose
    left_edge = (landmarks.part(2).x, landmarks.part(2).y) #the left edge point of the face
    right_edge = (landmarks.part(14).x, landmarks.part(14).y) #right edge
    
    face_width = abs(right_edge[0]-left_edge[0]) 
    left_face_width = abs(nose_point[0]-left_edge[0])
    right_face_width = abs(right_edge[0]-nose_point[0])
    
    if right_face_width < flex * face_width or left_face_width < flex * face_width:
        return False
    return True
    
    
motor_running = False


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try:
        frame = frame.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        # # #try this maybe:
        # for face in faces:
            # #check if the user is facing the camera, see the above function
            # landmark = predictor(gray,face)
            # facetheCamera = ifFacing (landmark,0.2)
        
        # #if facing, turn on the motor
        # if facetheCamera:
            # if not motor_running:
                # move_motor(50,0)
                # move_running = True
        # #else turn off
        # else:
            # if motor_runing:
                # stop_motor()
                # motor_running = False
        
        if faces:
        #if face is detected, start the motors
            if not motor_running:
                move_motor(50, 0)
                motor_running = True
            
        else:
            #no face detected, so, stop the motors!
            if motor_running:
                stop_motor()
                motor_running = False
        

        
        for face in faces:
            landmarks = predictor(gray, face)
            left_point = (landmarks.part(36).x, landmarks.part(36).y)
            right_point = (landmarks.part(39).x, landmarks.part(39).y)
            center_top = midpoint(landmarks.part(37), landmarks.part(38))
            center_bottom = midpoint(landmarks.part(41), landmarks.part(30))
        
            hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
            ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)
        
    
        # MATTE: disable this during autorun   
        # cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

        rawCapture.truncate(0)
    
    except Exception as e:
        print("Encoder issue:", str(e))



cv2.destroyAllWindows()
        
#Clean up GPIO

motor_pwm_1A.stop()
motor_pwm_1B.stop()
GPIO.cleanup()
