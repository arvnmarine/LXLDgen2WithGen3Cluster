#! /usr/bin/python

import RPi.GPIO as GPIO
import can
import time
import os
import queue
from threading import Thread



GEN2_PID_STEERINGWHEEL = 0x318;
MSG_GEN2_UP_ARROW_STEERINGWHEEL_LEFT = [0x00,0x00,0x00, 0x00, 0x10, 0x0C,0xFF, 0x00]
MSG_GEN2_DOWN_ARROW_STEERINGWHEEL_LEFT = [0x00,0x00,0x00, 0x00, 0x04, 0x0C,0xFF, 0x00]
MSG_GEN2_LEFT_ARROW_STEERINGWHEEL_LEFT = [0x00,0x00,0x00, 0x00, 0x01, 0x0C,0xFF, 0x00]
MSG_GEN2_RIGHT_ARROW_STEERINGWHEEL_LEFT = [0x00,0x00,0x00, 0x00, 0x40, 0x0C,0xFF, 0x00]
MSG_GEN2_VR_BUTTON_STEERINGWHEEL_LEFT = [0x00,0x00,0x00, 0x00, 0x00, 0x0E,0xFF, 0x00]
MSG_GEN2_RELEASEBUTTON_STEERINGWHEEL_LEFT = [0x00,0x00,0x00, 0x00, 0x00, 0x0C,0xFF, 0x00]


GEN3_PID_STEERINGWHEEL = 0x22D;
MSG_GEN3_UP_ARROW_STEERINGWHEEL_LEFT = [0xFF,0x00,0x00, 0x00, 0x00, 0x04,0x00, 0x00]
MSG_GEN3_DOWN_ARROW_STEERINGWHEEL_LEFT = [0xFF,0x00,0x00, 0x00, 0x40, 0x00,0x00, 0x00]
MSG_GEN3_LEFT_ARROW_STEERINGWHEEL_LEFT = [0xFF,0x00,0x00, 0x00, 0x10, 0x00,0x00, 0x00]
MSG_GEN3_RIGHT_ARROW_STEERINGWHEEL_LEFT = [0xFF,0x00,0x00, 0x00, 0x00, 0x01,0x00, 0x00]
MSG_GEN3_OK_BUTTON_STEERINGWHEEL_LEFT = [0xFF,0x00,0x00, 0x00, 0x00, 0x10,0x00, 0x00]
MSG_GEN3_RELEASEBUTTON_STEERINGWHEEL_LEFT = [0xFF,0x00,0x00, 0x00, 0x00, 0x00,0x00, 0x00]

print('\n\rCAN Rx test')
print('Bring up CAN0....')

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)	
print("Ready")

# test connection
try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print("Cannot find PiCAN board.")
	
	exit()
	
	
def compareData (data, buttonGen2):
	for i in range(8):
		if data[i] != buttonGen2[i]:
			return False
	return True
	
	
try:
	while True:
		message = bus.recv()	# Wait until a message is received.
		#print ("Received Message id ", message.arbitration_id)
		
			
			
		if message.arbitration_id != 0x318:
			continue
			
		
			
		
			
		
		if compareData(message.data, MSG_GEN2_UP_ARROW_STEERINGWHEEL_LEFT):
			print ("UP pressed ")
			for i in range(message.dlc ):
				message.data[i] = MSG_GEN3_UP_ARROW_STEERINGWHEEL_LEFT[i]
		elif compareData(message.data , MSG_GEN2_DOWN_ARROW_STEERINGWHEEL_LEFT):
			print ("DOWN pressed ")
			for i in range(message.dlc ):
				message.data[i] = MSG_GEN3_DOWN_ARROW_STEERINGWHEEL_LEFT[i]
		elif compareData(message.data , MSG_GEN2_LEFT_ARROW_STEERINGWHEEL_LEFT):
			print ("LEFT pressed ")
			for i in range(message.dlc ):
				message.data[i] = MSG_GEN3_LEFT_ARROW_STEERINGWHEEL_LEFT[i]
		elif compareData(message.data , MSG_GEN2_RIGHT_ARROW_STEERINGWHEEL_LEFT):
			print ("RIGHT pressed ")
			for i in range(message.dlc ):
				message.data[i] = MSG_GEN3_RIGHT_ARROW_STEERINGWHEEL_LEFT[i]
		elif compareData(message.data , MSG_GEN2_VR_BUTTON_STEERINGWHEEL_LEFT):
			print ("VR pressed ")
			for i in range(message.dlc ):
				message.data[i] = MSG_GEN3_OK_BUTTON_STEERINGWHEEL_LEFT[i]
		elif compareData(message.data , MSG_GEN2_RELEASEBUTTON_STEERINGWHEEL_LEFT):
			# print ("Released button")
			for i in range(message.dlc ):
				message.data[i] = MSG_GEN3_RELEASEBUTTON_STEERINGWHEEL_LEFT[i]
		else:
			#print ("Unknown message")
			continue
	
		message.arbitration_id = GEN3_PID_STEERINGWHEEL
		
		bus.send(message)
		time.sleep(0.01)
		
	
except KeyboardInterrupt:
	#Catch keyboard interrupt
	 
	os.system("sudo /sbin/ip link set can0 down")
	print("\n\rKeyboard interrtupt")