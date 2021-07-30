import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)

GPIO.setup(18, GPIO.OUT)

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressed = False
hold = False

while True:
   if GPIO.input(10):
      time.sleep(3)
      if GPIO.input(10) == GPIO.LOW:
         pressed = not pressed
         if pressed is True:
            print("Recording")
            GPIO.output(18, GPIO.HIGH)
            os.system('python interfaces/pixels_recording.py &')
            os.system('python recording_examples/record_one_channel.py')
            print("Finished Recording")
            time.sleep(1)
            print("Button was pushed!")
            GPIO.output(18, GPIO.LOW)
            time.sleep(0.5)
         else:
            GPIO.output(11, GPIO.HIGH)
            os.system('python interfaces/pixels_stop.py &')
            time.sleep(1)
            os.system('bash stopRecording.sh')
            print("Kill Recording Scripts")
            time.sleep(3)
            print("Button was pushed!")
            GPIO.output(11, GPIO.LOW)
            time.sleep(0.5)
      if GPIO.input(10) == GPIO.HIGH:
         os.system('python3 picture.py')
         GPIO.output(11, GPIO.HIGH)
         print("Picture Was Taken!")
         time.sleep(2)
         print("Button was hold!")
         GPIO.output(11, GPIO.LOW)
         time.sleep(0.5)

