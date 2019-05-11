import numpy as np
import cv2
import time
import RPi.GPIO as GPIO
import time
import sys
import PIC32Interface


def MotorMotion( servo_number, direction ):
 if( servo_number == 1 ):
  if( direction == 'stop' ):
   PIC32Interface.EnablePWM1(0,1)
   #print 'duty cycle: ', 0, "freq: ", 50, "pulse width:", 0
  elif( direction == 'clockwise' ):
   PIC32Interface.EnablePWM1(146,1)
   #print 'duty cycle: ', 6.103, "freq: ", 46.948, "pulse width:", 1.47
  elif( direction == 'counter_clockwise' ):
   PIC32Interface.EnablePWM1(154,1)
   #print 'duty cycle: ', 7.407, "freq: ", 46.296, "pulse width:", 1.55
 elif( servo_number == 2 ):
  if( direction == 'stop' ):
   PIC32Interface.EnablePWM2(0,1)
   #print 'duty cycle: ', 0, "freq: ", 50, "pulse width:", 0
  elif( direction == 'clockwise' ):
   PIC32Interface.EnablePWM2(146,1)
   #print 'duty cycle: ', 6.103, "freq: ", 46.948, "pulse width:", 1.4
  elif( direction == 'counter_clockwise' ):
   PIC32Interface.EnablePWM2(154,1)
   #print 'duty cycle: ', 7.407, "freq: ", 46.296, "pulse width:", 1.55

def control( direction, sleep_time ):
	if ( direction == 'left' ):
		MotorMotion(  1, 'clockwise' )
		MotorMotion(  2, 'clockwise' )
		#time.sleep( 0.1 )
		#MotorMotion( pwm,pwm2, 1, 'stop' )
		#MotorMotion( pwm,pwm2, 2, 'stop' )
	elif ( direction == 'right' ):
		MotorMotion( 1, 'counter_clockwise' )
		MotorMotion( 2, 'counter_clockwise' )
		#time.sleep( 0.1 )
		#MotorMotion( pwm,pwm2, 1, 'stop' )
		#MotorMotion( pwm,pwm2, 2, 'stop' )
	elif ( direction == 'center' ):
		MotorMotion( 1, 'stop' )
		MotorMotion( 2, 'stop' )


def master( run_flag, qr1_receive_queue, qr2_receive_queue, qr3_receive_queue, p_start_turn, p_end_turn, frame_queue ):
	# start video capture
	cap = cv2.VideoCapture(0)
	
	# set up GPIO PINs
	#GPIO.setmode(GPIO.BCM)
	#GPIO.setup(5, GPIO.OUT)
	#GPIO.setup(19, GPIO.OUT)
	
	
	# create PWM instances
	#pwm = GPIO.PWM( 5, freq )
	#pwm.start( dc)
	#pwm2 = GPIO.PWM( 19, freq )
	#pwm2.start( dc )
	print ( 'master' )
	PIC32Interface.SetPWMPeriod(22, 3)
	control( 'center',0 )
	
	# start timer
	start = time.time()
	time_interval = 0
	
	# results
	directions = []
	previous = "center"
	miss_count=0
	
	
	while ( run_flag.value ) :
		try:
			if cap.isOpened() :
				time_interval = time.time() - start 
				if time_interval > 0.03 and frame_queue.qsize() < 5:
					tmp = p_start_turn
					ref, frame = cap.read()
					frame_queue.put( frame, True )
					start = time.time()
					time_interval = 0
				if not qr1_receive_queue.empty():
					qr1 = qr1_receive_queue.get()
					if ( len(directions) < 10 ):
						directions.append( qr1 ) 
				if not qr2_receive_queue.empty():
					qr2 = qr2_receive_queue.get()
					if ( len(directions) < 10 ):
						directions.append( qr2 ) 
				if not qr3_receive_queue.empty():
					qr3 = qr3_receive_queue.get()
					if ( len(directions) < 10 ):
						directions.append( qr3 ) 
				if ( len(directions) > 0 ):
					curr_dir = directions.pop(0)
					if(curr_dir[0]=="miss" and previous=="miss"):
						miss_count+=1
					else:
						miss_count=0
					if curr_dir[0] != 'center' and curr_dir[0] != 'miss' and curr_dir[0] != previous:
						control( curr_dir[0], abs( curr_dir[1] - 320.0 ) / 1000.0 )
						print ( curr_dir[1] )
					#elif curr_dir[0] != previous:
					#	control( pwm,pwm2,curr_dir[0], 0 )
					#	pass
					elif miss_count==10 or curr_dir[0] == 'center':
						control( "center", 0 )
					print ( curr_dir[0] )
					
					previous = curr_dir[0]
			else:
				print "run into problem here"
				run_flag.value = 0
		except KeyboardInterrupt:
			run_flag.value = 0
			print "cleaned up!!!"
			PIC32Interface.EnablePWM1(0,1)
			PIC32Interface.EnablePWM2(0,1)
			cap.release()
