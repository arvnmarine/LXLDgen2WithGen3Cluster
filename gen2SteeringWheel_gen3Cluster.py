import RPi.GPIO as GPIO
import can
import time
import os
import queue
from threading import Thread

led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

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
print('Ready')

# test connection
try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	GPIO.output(led,False)
	exit()
	
	
try:
	while True:
		message = bus.recv()	# Wait until a message is received.
		if message.arbitration_id != GEN2_PID_STEERINGWHEEL:
			continue
			
		if message.data == MSG_GEN2_UP_ARROW_STEERINGWHEEL_LEFT:
		   message.data = MSG_GEN3_UP_ARROW_STEERINGWHEEL_LEFT
		elif message.data == MSG_GEN2_DOWN_ARROW_STEERINGWHEEL_LEFT:
		   message.data = MSG_GEN3_DOWN_ARROW_STEERINGWHEEL_LEFT
		elif message.data == MSG_GEN2_LEFT_ARROW_STEERINGWHEEL_LEFT:
		   message.data = MSG_GEN3_LEFT_ARROW_STEERINGWHEEL_LEFT
		elif message.data == MSG_GEN2_RIGHT_ARROW_STEERINGWHEEL_LEFT:
		   message.data = MSG_GEN3_RIGHT_ARROW_STEERINGWHEEL_LEFT
		elif message.data == MSG_GEN2_VR_BUTTON_STEERINGWHEEL_LEFT:
		   message.data = MSG_GEN3_OK_BUTTON_STEERINGWHEEL_LEFT
		elif message.data == MSG_GEN2_RELEASEBUTTON_STEERINGWHEEL_LEFT:
		   message.data = MSG_GEN3_RELEASEBUTTON_STEERINGWHEEL_LEFT
		else:
			print "Unknown message"
			continue
	
		message.arbitration_id = GEN3_PID_STEERINGWHEEL
		bus.send(message)
	
except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False) 
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')