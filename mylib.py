import RPi.GPIO as GPIO
import time
# ---- CONSTANTS ----
MAX_DAC_VOLTAGE = 3.3
MAX_DAC_NUMBER = 255

dac = [26, 19, 13, 6, 5, 11, 9, 10]   # DAC pins (BCM)
comp = 4                              # Comparator pin (BCM)
troyka = 17                           # Troyka power pin (BCM)
leds = [21, 20, 16, 12, 7, 8, 25, 24] # Led pins (BCM)
aux = [22, 23, 27, 18, 15, 14, 3, 2]  # AUX pins (BCM)

# ---- FUNCTIONS ----
def dec2bin(value):
    """ Return a list of size 8 containing binary representation of passed integer. """
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    """ Return a decimal number proportional to voltage on S pin on troyka. """
    L, R = 0, MAX_DAC_NUMBER
    while L < R:
        x = L + (R - L) // 2
        GPIO.output(dac, dec2bin(x))  # Show how algo works on dac leds
        time.sleep(0.005)
        comp_res = GPIO.input(comp)
        if comp_res == 0:
            R = x
        else:
            L = x + 1
    return L