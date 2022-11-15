from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    

def find_silver_token():
    
	markers=R.see()
    
	dist=100
	for token in markers:
		if token.dist <dist and token.info.marker_type is MARKER_TOKEN_SILVER:
			dist = token.dist
			rot_y = token.rot_y
			code=token.info.code
	
	if dist==100:
		return -1, -1 ,-1
	else:
		return dist, rot_y ,code

def find_golden_token():
   
	markers=R.see()
	dist=100
    
			    
	for token in markers:
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
			dist=token.dist
			rot_y=token.rot_y
			code=token.info.code   
	
	
	if dist==100:
		return -1, -1 ,-1
	else:
		return dist, rot_y , code
  		
def nearest_silver_token(x):
	
	while 1:
	    
		dist, rot_y ,code= find_silver_token()
	    
		if silver_code:
			for i in range(len(silver_code)):
				if silver_code[i]==code: 
					dist,rot_y,code=-1,-1,-1   #if token has already been taken, ignore it
				
		if dist==-1: # if no token is detected, we make the robot turn 
			print("I don't see any token!!")
			turn(+10, 1)
		elif dist < d_th: # if we are close to the token, we try grab it.
			print("Found it!")
			R.grab()      
			silver_code.append(code)  # keep track of silver tokens already taken
			
			print("Gotcha!")
			nearest_golden_token(x) #call function to find a golden token
	          
	          
			exit()
		
		
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			print("Ah, that'll do.")
			-drive(30, 0.5)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+2, 0.5)
def nearest_golden_token(x):
	
	
	while 1:
		
		dist, rot_y ,code= find_golden_token()
	    
		if gold_code:
			for i in range(len(gold_code)):
				if gold_code[i]==code:
					dist,rot_y,code=-1,-1,-1 #if token has already been taken, ignore it
					
		if dist==-1: # if no token is detected, we make the robot turn 
			print("I don't see any token!!")
			
			turn(+10, 1)
		elif dist < 1.6*d_th: # if we are close to the token, we try grab it.
			print("Found it!")
			R.release()
			drive(20,0.1)
			gold_code.append(code) # keep track of golden tokens already taken
			
			x-=1   #when robot releases the silver token, counter is decremented 
			
			if x==0:   #the robot brought all silver tokens
				exit()   #end of program 
	
			nearest_silver_token(x) #call function to find a silver token
	        
			
		
		
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			print("Ah, that'll do.")
			drive(30, 0.5)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+2, 0.5)

x=6      #set counter = number of golden token
silver_code=list()  #list of silver token's codes
gold_code=list()  #list of golden token's codes
nearest_silver_token(x)  #the robot starts looking for a silver token

