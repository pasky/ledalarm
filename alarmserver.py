#!/usr/bin/env python

from __future__ import print_function, division

import datetime
import RPi.GPIO as GPIO
import random
import sched
import serial
import time


GPIO.setmode(GPIO.BOARD)


class Panel:
    def __init__(self, btntrigger, ledplus=11, ledminus=13, btnplus=7):
        self.ledplus = ledplus
        GPIO.setup(self.ledplus, GPIO.OUT)
        GPIO.output(self.ledplus, 0)

        self.ledminus = ledminus
        GPIO.setup(self.ledminus, GPIO.OUT)
        GPIO.output(self.ledminus, 0)

        self.btnplus = btnplus
        GPIO.setup(self.btnplus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.btnplus, GPIO.FALLING, callback=btntrigger, bouncetime=200)

    def blink(self, delay=0.5, repeats=1):
        for i in range(repeats):
            GPIO.output(self.ledplus, 1)
            time.sleep(delay)
            GPIO.output(self.ledplus, 0)
            time.sleep(delay)


class LED:
    def __init__(self, tty='/dev/ttyUSB0'):
        self.ser = serial.Serial(tty, 9600)
        self.wakeup = None

        self.ser.write("0\n")
        time.sleep(1)
        self.ser.write("1\n")
        time.sleep(2)
        self.ser.write("0\n")

    def intensity(self, value):
        print('int: %d' % (value,))
        self.ser.write("%d\n" % (value,))

    def run_wakeup(self, delay=4):
        self.wakeup = True
        for i in range(1, 10):
            self.intensity(i)
            time.sleep(delay * 4)
            if not self.wakeup:
                return
        for i in range(11, 30):
            self.intensity(i)
            time.sleep(delay * 3)
            if not self.wakeup:
                return
        for i in range(31, 70):
            self.intensity(i)
            time.sleep(delay * 2)
            if not self.wakeup:
                return
        for i in range(71, 192):
            self.intensity(i)
            time.sleep(delay)
            if not self.wakeup:
                return
        time.sleep(900)
        for i in range(3600):
            time.sleep(0.6 + random.random()-0.5)
            self.intensity(192)
            time.sleep(0.4 + (random.random()-0.5)/2)
            self.intensity(0)
            if not self.wakeup:
                return
        self.wakeup = False


def snooze(_):
    if led.wakeup:
        print('SNOOZE')
        panel.blink(delay=0.1, repeats=2)
    else:
        print('SNOOZE nop')
        led.intensity(1)
        panel.blink(repeats=2)
        led.intensity(0)
    led.wakeup = False
    led.intensity(0)


# hour in GMT (-1h), and subtract ~12min. for early weak intensities
def alarmtime(hour=6, minute=48):
    day_ofs = hour * 3600 + minute * 60
    t = time.time()
    day_start = (t // 86400) * 86400
    if t - day_start < day_ofs:
        return day_start + day_ofs
    else:
        return day_start + 86400 + day_ofs


if __name__ == "__main__":
    panel = Panel(btntrigger=snooze)
    led = LED()

    s = sched.scheduler(time.time, time.sleep)

    while True:
        t = alarmtime()
        print('setting time %d (now %d)' % (t, time.time()))
        s.enterabs(t, 0, led.run_wakeup, ())
        print('zzz...')
        s.run()
