# remote.py for ESPNow repeater link.

# The MIT License (MIT)
#
# Copyright (c) 2021 David Festing
# Copyright (c) 2021 Glenn Moloney https://github.com/glenn20/micropython-espnow-images
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# V1 18 Sept 2021


import network
from esp import espnow
import utime
import machine
from machine import Pin
#from machine import WDT


CYCLE_TIME = 60             #  seconds
REBOOT_DELAY = 5            #  seconds
WATER_LEVEL_PIN = 27
repeater_mac = b'\x08:\xf2\xab^\x04'
#wdt = WDT(timeout = (CYCLE_TIME + 10) * 1000)  # enable it with a timeout
#wdt.feed()


def reboot(delay = REBOOT_DELAY):
 #  print a message and give time for user to pre-empt reboot
 #  in case we are in a (battery consuming) boot loop
    print (f'Rebooting device in {delay} seconds (Ctrl-C to escape).')
 #  or just machine.deepsleep(delay) or lightsleep()
    utime.sleep(delay)
    machine.reset()


try:
    print ('you have 5 seconds to do Ctrl-C if you want to edit the program')
    utime.sleep(5)

    pin = Pin(WATER_LEVEL_PIN, Pin.IN, Pin.PULL_UP) #  water level sensor

    w0 = network.WLAN(network.STA_IF)
#    print (w0.config('mac'))
    e0 = espnow.ESPNow()
#    print (e0)

 #  these functions generate exceptions on error - always return None
    e0.init()

 #  so that we wake up and reset the wdt before it times out
    e0.config(timeout = CYCLE_TIME * 1000)

    e0.add_peer(repeater_mac)
except KeyboardInterrupt as err:
    raise err #  use Ctrl-C to exit to micropython repl
except Exception as err:
    print ('Error initialising espnow:', err)
    reboot()


try:
    while True:
#        wdt.feed()

        water_status = 'level OK' if pin.value() == 1 else 'level alarm'
        print (water_status)

        w0.active(True) #  turn on radio only when needed
     #  if you want to save more battery, set sync=False
     #  at cost of not knowing if message was received.
        retval = e0.send(repeater_mac, water_status, True)
        w0.active(False)

     # for testing from remote end
#       if (retval != True):
#            print ('send did NOT work')
#            reboot()

        machine.lightsleep(CYCLE_TIME * 1000)
except KeyboardInterrupt as err:
    raise err #  use Ctrl-C to exit to micropython repl
except Exception as err:
    print ('Error during execution:', err)
    reboot()
