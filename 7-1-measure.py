#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
from mylib import dec2bin
from matplotlib import pyplot as plt

# ---- SETUP ----
GPIO.setmode(GPIO.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

MAX_DAC_VOLTAGE = 3.3
MAX_DAC_NUMBER = 255

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

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

# ---- MAIN ----
time0 = time.time()  # Capacitor has started to charge
capacitor_sig_init = adc()
print(f'Charging... Initial voltage on capacitor = {capacitor_sig_init}')
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
# GPIO.output(troyka, GPIO.HIGH)

try:
    capacitor_vals = []
    x = []
    i = 0
    has_charged = False
    while True:
        capacitor_sig = adc()                      # Read current voltage on capacitor
        voltage = capacitor_sig * MAX_DAC_VOLTAGE / MAX_DAC_NUMBER
        print(f'Current voltage level = {voltage:.2f}V, {capacitor_sig}')
        capacitor_vals.append(voltage)             # Save read data
        x.append(i)
        i = i + 1
        GPIO.output(leds, dec2bin(capacitor_sig))  # Indicate if capacitor is charging or discharging

        if (capacitor_sig >= 83):                  # Begin discharging
            has_charged = True
            GPIO.output(troyka, GPIO.LOW)          
            print("Discharging...")
        if ((capacitor_sig < 5 and (has_charged is True)) or capacitor_sig == 0):
            break
    
    time1 = time.time()                            # Stop measurements
    duration = time1 - time0

    plt.ylabel('Напряжение, В')
    plt.title('Зависимость напряжения от номера измерения')
    plt.xlabel('Номер измерения')
    plt.grid('--')
    plt.scatter(x, capacitor_vals, c=[0,0,0], marker='+')
    plt.show()

    capacitor_vals = [str(item) for item in capacitor_vals]
    with open('data.txt', 'w') as dataf:
        dataf.write('\n'.join(capacitor_vals))

    sample_freq = 25
    quant_step = float(max(capacitor_vals)) / 80
    with open('settings.txt', 'w') as settingsf:
        settingsf.write(f'{sample_freq}\n{quant_step}')
    print(f'Sampling frequency: {sample_freq}, quantization step:{quant_step}, measuremnts duration: {duration}, period of single measuremnt: {sample_freq ** -1}')
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()
