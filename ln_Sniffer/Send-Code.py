#!/usr/local/bin/python3.6

from __future__ import print_function
import argparse
import os
import shelve
import time
import warnings

try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
except RuntimeError:
    # Catch here so that we can actually test on non-pi targets
    warnings.warn('This can only be executed on Raspberry Pi', RuntimeWarning)


codes = {}
# Radiocomando 6 Tasti per relè 220V bianco con top azzurrino CMD-001
codes["CMD_601"] = {
                "Key_1":  13636867,
                "Key_2":  13636876,
                "Key_3":  13636869,
                "Key_4":  13636912,
                "Key_5":  13636881,
                "Key_6":  13636884,

                "Key_12":  13636879,
                "Key_13":  13636879,
                "Key_14":  13636915,
                "Key_15":  13636915,
                "Key_16":  13636927,

                "Key_23":  13636879,
                "Key_24":  13636924,
                "Key_25":  13636927,
                "Key_26":  13636924,

                "Key_34":  13636927,
                "Key_35":  13636927,
                "Key_36":  13636924,

                "Key_45":  13636915,
                "Key_46":  13636924,

                "Key_56":  13636927,


                }

# Radiocomando 6 Tasti per relè 220V bianco con top azzurrino (Relè di Silvia)
codes["CMD_602"] = {
                "Key_1":   3163395,
                "Key_2":   3163404,
                "Key_3":   3163407,
                "Key_4":   3163440,
                "Key_5":   3163443,
                "Key_6":   3163452,
                }

# Radiocomando 4 Tasti per relè 220V nero con top azzurrino e coperchio scorrevole
codes["CMD_401"] = {
                "key_A":   15679457,
                "key_B":   15679458,
                "key_C":   15679460,
                "key_D":   15679464,
                }

# Radiocomando 4 Tasti per relè 220V nero con top azzurrino e coperchio scorrevole
codes["CMD_402"] = {
                "key_A":   12461025,
                "key_B":   12461026,
                "key_C":   12461028,
                "key_D":   12461032,
                }



# Radiocomando 4 Tasti antifurto di casetta
codes["CMD_403"] = {
                "Key_unlock" : 4942578,
                "Key_lock"   : 4942580,
                "Key_Sirena" : 4942577,
                "Key_Alarm"  : 4942584,
                }

'''
Radiocomando prese 220 vecchie Technic
    Key-A   1394001
    Key-B   -
    Key-C   -
    Key-D   -
    Key-D   -

Radiocomando 12 Tasti per modulo relè 220V bianco con top nero (Relè tutti in una scatola)
    Key-01   non itercettati
    Key-02   non itercettati
    Key-03   non itercettati
    Key-04   non itercettati
    Key-05   non itercettati
    Key-06   non itercettati
    Key-07   non itercettati
    Key-08   non itercettati
    Key-09   non itercettati
    Key-10   non itercettati
    Key-11   non itercettati
    Key-12   non itercettati
    Key-13   non itercettati

'''
def play(txpin):
    GPIO.setup(txpin, GPIO.OUT, initial=GPIO.LOW)
    for button in args.button:
        for i, (timing, level) in enumerate(buttonsdb[button]):
            if i is not 0:
                # Busy-sleep (gives a better time granularity than
                # sleep() but at the cost of busy looping)
                now = time.time()
                while now + timing > time.time():
                    pass

            GPIO.output(args.txpin, level)


def read_timings(rx_pin):
    capture = []
    while True:
        start = time.time()
        if GPIO.wait_for_edge(rx_pin, GPIO.BOTH, timeout=1000):
            capture.append((time.time() - start, GPIO.input(rx_pin)))

        elif len(capture) < 5:  # Any pattern is likely larger than 5 bits
            capture = []
        else:
            return capture

def record(rxpin):
    # GPIO.setup(rxpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(rxpin, GPIO.IN)

    print('Press xxx')
    sample = read_timings(rxpin)
    print('Recorded', len(sample), 'bit transitions')
    # buttons[args.button] = sample


'''
def record_(args, buttons):
    GPIO.setup(args.rxpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print('Press', args.button)
    sample = read_timings(args.rxpin)
    print('Recorded', len(sample), 'bit transitions')
    buttons[args.button] = sample
'''

from datetime import datetime
# import matplotlib.pyplot as pyplot
# import RPi.GPIO as GPIO


def exPLOT(RECEIVE_PIN):
    RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
    MAX_DURATION = 5
    # RECEIVE_PIN = 23
    # GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    cumulative_time = 0
    beginning_time = datetime.now()
    print( '**Started recording**')
    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - beginning_time
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds
    print( '**Ended recording**')
    print( len(RECEIVED_SIGNAL[0]), 'samples recorded')
    GPIO.cleanup()

    print( '**Processing results**')
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0
        print (RECEIVED_SIGNAL[0])

    '''
    print( '**Plotting results**')
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([0, MAX_DURATION, -1, 2])
    pyplot.show()
    '''
https://github.com/milaq/rpi-rf
https://github.com/milaq/rpi-rf/blob/master/scripts/rpi-rf_receive
# "gpio readall" to see pin layout
def main():
    """ by Loreto:  wiring pi pin wPi
     BCM | wPi |   Name  | Mode | V | Physical
      27 |   2 | GPIO. 2 |   IN | 0 | 13
      17 |   0 | GPIO. 0 |  OUT | 0 | 11
    """
    tx_pin = 11
    # rx_pin = 2
    rx_pin = 13
    # record(rx_pin)
    exPLOT(rx_pin)

import os
if __name__ == '__main__':
    main()
    '''
    os.system('/home/pi/GIT-REPO/Ln_433/433Utils/RPi_utils/codesend 13636915')
    time.sleep(5)
    os.system('/home/pi/GIT-REPO/Ln_433/433Utils/RPi_utils/codesend 13636915')
    '''
