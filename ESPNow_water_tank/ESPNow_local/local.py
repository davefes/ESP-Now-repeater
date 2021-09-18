# local.py for ESPNow repeater link.

# The MIT License (MIT)
#
# Copyright (c) 2021 David Festing
# Copyright (c) 2021 Glenn Moloney, https://github.com/glenn20/micropython-espnow-images
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
import watchdog_timer as wdt
#from machine import WDT


CYCLE_TIME = 60             # seconds
REBOOT_DELAY = 5            # seconds
LED_PIN = 27
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

    led_pin = Pin(LED_PIN, Pin.OUT) #  LED drive pin
    wdt.init(timeout = CYCLE_TIME + 10)
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
    print ('waiting for initial msg from the repeater')

    w0.active(True)

    for mac, msg in e0:
#        wdt.feed()
        if mac == repeater_mac:
            msg = msg.decode('utf-8')
            print (msg)

         #  alarm off if 'level OK', anything else is an alarm
            led_pin.value(0 if msg == 'level OK' else 1)
        elif mac == None:
            pass #  timed out waiting for message
        else:
            print ('Recv from {}: "{}"'.format(mac, msg))
except KeyboardInterrupt as err:
    raise err #  use Ctrl-C to exit to micropython repl
except Exception as err:
 #  all other exceptions cause a reboot
    print ('Error during execution:', err)
    reboot()
