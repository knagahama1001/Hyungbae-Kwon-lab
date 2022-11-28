# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:25:55 2020

@author: chuljung kwak
"""

import cv2
import numpy as np
from scipy import ndimage
import sys
import time
import RPi.GPIO as GPIO


def run(file_name):
    
    GPIO.setmode(GPIO.BCM)
    
    ttl_out = 10
    
    GPIO.setup (ttl_out, GPIO.OUT, initial = GPIO.LOW)
    
    cap = cv2.VideoCapture(0)
    
    fps = cap.get(cv2.CAP_PROP_FPS) 
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    out = cv2.VideoWriter(file_name + '.avi', fourcc, fps, (640,360))
    
    output = sys.stdout       
    
    time_stamp = []
    
    x_stamp = []
    
    y_stamp = []
    
    ttl_stamp = []
    
    miss_stamp = []
    
    f = 0
    
    ttl_on = 0
    
    previous_x = 0
    previous_y = 0
    
    target_size = 120
    
    
            
    x_start = 140
    y_start = 10
    
    
    while True:
        
        ret, frame = cap.read() 
        
        if ret == True:
            
            f += 1
            
            time_stamp.append(time.time())
            
            frame = cv2.resize(frame, (640,360), interpolation = cv2.INTER_AREA)
            
            
            out.write(frame)
            
            frame_ = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            frame_[frame_ > 50] = 255
            
            frame_[0:100,0:218] = 255
            
            frame_[0:100,387:] = 255
            
            x_shift = 30
            
            frame_ = frame_[2:340,x_shift:500]
            
            frame_ = cv2.bitwise_not(frame_)
            
            com=ndimage.measurements.center_of_mass(frame_)
            
            
            x_target = [x_start , x_start + target_size]
            y_target = [y_start , y_start + target_size]
            
            if  5000 > np.count_nonzero(frame_>200) > 100:
                
                previous_x, previous_y = int(com[0]), int(com[1] + x_shift)
                
                cv2.circle(frame, (int(com[1])+x_shift, int(com[0])), 10, (0, 0, 255), -1)
                cv2.rectangle(frame, (x_target[0], y_target[0]), (x_target[1], y_target[1]), (255,255,255), 2)
                cv2.rectangle(frame, (x_start + 335  - target_size, y_target[0]), (x_start + 335, y_target[1]), (255,255,255), 2)
                
                
                x_stamp.append(int(com[1])+x_shift)
                y_stamp.append(int(com[0]))
                miss_stamp.append(0)
                
            else:
                
                cv2.circle(frame, (previous_y+x_shift, previous_x), 10, (255, 0, 0), -1)
                
                x_stamp.append(previous_y+x_shift)
                y_stamp.append(previous_x)
                miss_stamp.append(1)
                
                print ('can not find animal!!')
                
            if x_target[0] - x_shift< int(com[1]) < -x_shift + x_target[1] and y_target[0] < int(com[0]) < y_target[1]:
                
                if ttl_on == 0:
                    
                    GPIO.output(ttl_out, GPIO.HIGH)
                    
                    ttl_on = 1
                
            else:
                
                if ttl_on == 1:
                    
                    GPIO.output(ttl_out, GPIO.LOW)
                    
                    ttl_on = 0
                
            output.flush()
            
            cv2.imshow('frame', frame)
            
            
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                
                 break
        
        else: 
            
            break
        
    cap.release() 
  
    cv2.destroyAllWindows()
    
    GPIO.cleanup()
    
    return time_stamp, x_stamp, y_stamp, miss_stamp
    
if __name__ == '__main__':
    
    file_name = raw_input('file name: ')
    
    run(file_name)
    


        
        
                    
        

        
        
        

    