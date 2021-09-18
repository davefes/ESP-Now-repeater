# ESP-Now-repeater
ESP-Now repeater or link

ESP-Now water tank level monitoring system


This project is an example of using ESP-Now in a situation where a repeater or link is required.

As the path to my house supply water tank is obstructed by trees, as well as being about 300 mtrs from the house, I needed a system that uses a repeater or link to ensure that a solid signal gets back to the house.

Three ESP32-WROOM32U (Generic) are being used with the latest Micropython port of ESP-Now found at:

https://github.com/glenn20/micropython-espnow-images

The system consists of a remote (with a float level switch), a repeater and a local (with an LED to indicate remote state or a siren).

The remote is solar powered, so it uses lightsleep() to conserve battery power.  Once a minute it wakes up and sends the sensor state to the repeater.  There is an option of running machine.WDT() to help keep this unit running.   This unit is connected to a small patch antenna pointed at the repeater.

The repeater relays the sensor state to the local unit.  This unit is connected to a "WiFi" whip (uni-directional) antenna.

The local unit is wired to another "WiFi" whip antenna.

If using a watchdog timer ensure that the timeout period is longer than CYCLE_TIME, 70 seconds for a CYCLE_TIME of 60 seconds.

Notes:

- for initial setup the lines #mac = w0.config('mac') and
  #print(mac) need to be uncommented so that the MAC address
  of the device can be determined
- the wdt_feed(), if used, needs to go in the for loop on the
  repeater and the local

Best place to get help would be on the Micropython forum:
https://forum.micropython.org/viewtopic.php?f=18&t=9177

  
Credits to:

glenn20 for the "iterating over the ESPNow singleton" example at
https://forum.micropython.org/viewtopic.php?f=18&t=9177&start=110
