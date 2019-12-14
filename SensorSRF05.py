#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

class SensorSRF05:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)


    def trigger(self):
        """Give a short pulse (10uS) on the trigger pin"""
        GPIO.output(self.trigger_pin, 1)
        time.sleep(10/1000000)
        GPIO.output(self.trigger_pin, 0)

    
    def get_distance(self):
        """Get the distance measured in cm"""

        # Activate trigger
        self.trigger()

        # Detect rising edge of echo pin
        channel = GPIO.wait_for_edge(self.echo_pin, GPIO.RISING, timeout=2)
        if channel is None:
            # Timeout on wait of rising interrupt
            return None
        else:
            # Rising edge detected, save pulse start
            pulse_start = time.time()


        # Detect falling edge of echo pin
        channel = GPIO.wait_for_edge(self.echo_pin, GPIO.FALLING, timeout=2)
        if channel is None:
            # Timeout on wait of falling interrupt")
            return None
        else:
            # Falling edge detected, save pulse end
            pulse_end = time.time()

        # Calculated pulse width in microseconds (x1mln)
        pulse_width = (pulse_end - pulse_start)*1000000

        # Return distance in cm
        return pulse_width / 58
        
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    trigger_pin = int(input("Trigger pin (BCM): "))
    echo_pin = int(input("Echo pin (BCM): "))
    
    srf = SensorSRF05(trigger_pin, echo_pin)

    while True:
        print("Measuring distance: ", end='')
        distance = srf.get_distance()
        print(distance)
        time.sleep(1)

    

    