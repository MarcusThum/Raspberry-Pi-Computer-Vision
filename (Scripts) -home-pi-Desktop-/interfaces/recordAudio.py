# Import LED Library Feedback

import apa102
import time
import threading
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from alexa_led_pattern import AlexaLedPattern

# Import Recording Libraries

import pyaudio
import wave
import numpy as np

# Import GPIO
import RPi.GPIO as GPIO
import time
import os

#install numpy to use GoogleHomeLedPattern
#from google_home_led_pattern import GoogleHomeLedPattern

## LED Setup

class Pixels:
    PIXELS_N = 12

    def __init__(self, pattern=AlexaLedPattern):
        self.pattern = pattern(show=self.show)

        self.dev = apa102.APA102(num_led=self.PIXELS_N)

        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()


## GPIO Setup

GPIO.setmode(GPIO.BOARD)

GPIO.setup(18, GPIO.OUT)

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressed = False
hold = False

# Recording Setup

RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 2  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output_one_channel"
RESPEAKER_RATE = 16000


#if __name__ == '__main__':
while True:

          if GPIO.input(10):
             time.sleep(3)
             if GPIO.input(10) == GPIO.LOW:
                   p = pyaudio.PyAudio()

                   stream = p.open(
                      rate=RESPEAKER_RATE,
                      format=p.get_format_from_width(RESPEAKER_WIDTH),
                      channels=RESPEAKER_CHANNELS,
                      input=True,
                      input_device_index=RESPEAKER_INDEX,)

                   frames = []

                   ## Pixels Listen
                   pixels.wakeup()
                   pixels.speak()

                   print("Audio Recording Started")
                   time.sleep(1)
                   print("Button was pushed!")
                   GPIO.output(18, GPIO.HIGH)
                   time.sleep(0.5)

                   while True:
                      ## Start Recording
                      data = stream.read(CHUNK)
                      # extract channel 0 data from 2 channels, if you want to extract channel 1, please change to [1::2]
                      a = np.fromstring(data,dtype=np.int16)[0::2]
                      frames.append(a.tostring())

                      if GPIO.input(10):
                         time.sleep(3)
                         if GPIO.input(10) == GPIO.LOW:

                            ## Stop Recording
                            stream.stop_stream()
                            stream.close()
                            p.terminate()

                            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                            wf.setnchannels(1)
                            wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
                            wf.setframerate(RESPEAKER_RATE)
                            wf.writeframes(b''.join(frames))
                            wf.close()

                            # Pixels Off
                            pixels.off()

                            print("Stopped Audio Recording")
                            time.sleep(1)
                            print("Button was pushed!")
                            GPIO.output(18, GPIO.LOW)
                            time.sleep(0.5)
                            break



        #try:
        #    pixels.wakeup()
        #    time.sleep(3)
        #    pixels.think()
        #    time.sleep(3)
        #    pixels.speak()
        #    time.sleep(6)
        #    pixels.off()
        #    time.sleep(3)
        #except KeyboardInterrupt:
        #    break


