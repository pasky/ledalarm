#!/usr/bin/env python

from __future__ import print_function, division

import datetime
import RPi.GPIO as GPIO
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
        self.ser.write("%d\n" % (value,))

    def wakeup(self, delay=4):
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
        while self.wakeup:
            time.sleep(0.6)
            self.intensity(192)
            time.sleep(0.6)
            self.intensity(0)


def snooze():
    led.wakeup = False
    led.intensity(0)


def alarmtime(hour=8, minute=0):
    day_ofs = hour * 3600 + minute * 60
    t = time.time()
    day_start = t // 86400
    if t - day_start < day_ofs:
        return day_start + day_ofs
    else:
        return day_start + 86400 + day_ofs


if __name__ == "__main__":
    panel = Panel(btntrigger=snooze)
    led = LED()

    s = sched.scheduler(time.time, time.sleep)

    while True:
        print('setting time')
        s.enterabs(alarmtime(), 0, led.wakeup)
        print('zzz...')
        s.run()
