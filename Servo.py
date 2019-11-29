#!/usr/bin/env python
import asyncio
import time
import RPi.GPIO as GPIO
from helper_functions import *

class Servo:
    # PWM frequency: 50Hz
    #  0 degrees:  .5ms (2.5%)
    # 90 degress: 1.5ms (12.5%)

    def __init__(self, signal_pin, pwm_frequency=50):
        # Store signal_pin and pwm_frequency (bypass setter)
        self._signal_pin = signal_pin
        self._pwm_frequency = pwm_frequency
        self._duty_cycle = 0

        # Set signal pin to output mode
        GPIO.setup(self._signal_pin, GPIO.OUT)

        # Set signal pint to PWM with 
        self.pwm = GPIO.PWM(self._signal_pin,self._pwm_frequency) # Set PWM frequency to 50Hz / 3000 cycles per minute
        self.pwm.start(0)

        # Default values for duty cycle 
        self._start = 2.5
        self._end = 12.5

    
    def calibrate(self, start=2.5, end=12.5):
        """Sets the servo duty cycle range"""
        self._start = start
        self._end = end

    def set(self, x):
        """Sets the servo position with a valye between -1 (left) and 1 (right)"""
        self.duty_cycle = map_range(x,-1,1,self._start, self._end)

    def get_normalized_position(self, min=-1, max=1):
        """Return the normalized position of the serve based on the dut4y cycle"""
        return map_range(self.duty_cycle,self._start, self._end, -1, 1)

    @property
    def duty_cycle(self):
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, duty_cycle):
        """Sets the duty cycle of the servo"""
        self._duty_cycle = duty_cycle
        self.pwm.ChangeDutyCycle(duty_cycle)
        

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    s = Servo(4,50)

    try:
        while True:
            x = float(input("Set position (-1 - 1): "))
            s.set(x)
            print(f" - Duty cycle: {s.duty_cycle}")
            print(f" - Normalized position: {s.get_normalized_position()}")
    except KeyboardInterrupt:
        s.pwm.stop()
        GPIO.cleanup
    except ValueError:
        s.pwm.stop()
        GPIO.cleanup
