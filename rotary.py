from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Running")
flag=False
counter=0
false_flag_tick=0
while True:
	sleep(0.001)
	new_flag=(GPIO.input(21)==1)
	if flag != new_flag:
		counter += 1
		flag=new_flag
	if not flag:
		false_flag_tick += 1
	else:
		false_flag_tick = 0

	if false_flag_tick > 100 and counter >= 2:
		print(counter/2 - 1)
		false_flag_tick = 0
		counter = 0
