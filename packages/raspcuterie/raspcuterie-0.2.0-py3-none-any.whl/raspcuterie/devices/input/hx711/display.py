"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

######################################################################
README:

This version runs in python 3.x. It will first prompt the user to
empty the scale. Then prompt user to place an item with a known weight
on the scale and input weight as INT.

The offset and scale will be adjusted accordingly and displayed for
convenience.

The user can choose to [0] exit, [1] recalibrate, or [2] display the
current offset and scale values and weigh a new item to test the accuracy
of the offset and scale values!
#######################################################################
"""
import statistics

import RPi.GPIO as GPIO
import time
import sys

"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify

it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import RPi.GPIO as GPIO
import time
import sys


class HX711:

    def __init__(self, dout, pd_sck, gain=128):
        """
        Set GPIO Mode, and pin for communication with HX711
        :param dout: Serial Data Output pin
        :param pd_sck: Power Down and Serial Clock Input pin
        :param gain: set gain 128, 64, 32
        """
        self.GAIN = 0
        self.OFFSET = 8444931.8125  # 8445225.5
        self.SCALE = 413.9508982035928  # 412.79281437125746

        # Setup the gpio pin numbering system
        GPIO.setmode(GPIO.BCM)

        # Set the pin numbers
        self.PD_SCK = pd_sck
        self.DOUT = dout

        # Setup the GPIO Pin as output
        GPIO.setup(self.PD_SCK, GPIO.OUT)

        # Setup the GPIO Pin as input
        GPIO.setup(self.DOUT, GPIO.IN)

        # Power up the chip
        self.power_up()
        self.set_gain(gain)

    def set_gain(self, gain=128):

        try:
            if gain is 128:
                self.GAIN = 3
            elif gain is 64:
                self.GAIN = 2
            elif gain is 32:
                self.GAIN = 1
        except:
            self.GAIN = 3  # Sets default GAIN at 128

        GPIO.output(self.PD_SCK, False)
        self.read()

    def set_scale(self, scale):
        """
        Set scale
        :param scale, scale
        """
        self.SCALE = scale

    def set_offset(self, offset):
        """
        Set the offset
        :param offset: offset
        """
        self.OFFSET = offset

    def get_scale(self):
        """
        Returns value of scale
        """
        return self.SCALE

    def get_offset(self):
        """
        Returns value of offset
        """
        return self.OFFSET

    def read(self):
        """
        Read data from the HX711 chip
        :param void
        :return reading from the HX711
        """

        # Control if the chip is ready
        while not (GPIO.input(self.DOUT) == 0):
            # Uncommenting the print below results in noisy output
            # print("No input from HX711.")
            pass

        # Original C source code ported to Python as described in datasheet
        # https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf
        # Output from python matched the output of
        # different HX711 Arduino library example
        # Lastly, behaviour matches while applying pressure
        # Please see page 8 of the PDF document

        count = 0

        for i in range(24):
            GPIO.output(self.PD_SCK, True)
            count = count << 1
            GPIO.output(self.PD_SCK, False)
            if (GPIO.input(self.DOUT)):
                count += 1

        GPIO.output(self.PD_SCK, True)
        count = count ^ 0x800000
        GPIO.output(self.PD_SCK, False)

        # set channel and gain factor for next reading
        for i in range(self.GAIN):
            GPIO.output(self.PD_SCK, True)
            GPIO.output(self.PD_SCK, False)

        return count

    def read_average(self, times=16):
        """
        Calculate average value from
        :param times: measure x amount of time to get average
        """
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def get_grams(self, times=16):
        """
        :param times: Set value to calculate average,
        be aware that high number of times will have a
        slower runtime speed.
        :return float weight in grams
        """
        value = (self.read_average(times) - self.OFFSET)
        grams = (value / self.SCALE)
        return grams

    def tare(self, times=16):
        """
        Tare functionality fpr calibration
        :param times: set value to calculate average
        """
        sum = self.read_average(times)
        self.set_offset(sum)

    def power_down(self):
        """
        Power the chip down
        """
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)

    def power_up(self):
        """
        Power the chip up
        """
        GPIO.output(self.PD_SCK, False)


# Force Python 3 ###########################################################


if sys.version_info[0] != 3:
    raise Exception("Python 3 is required.")

############################################################################

# Make sure you correct these to the correct pins for DOUT and SCK.
# gain is set to 128 as default, change as needed.
hx = HX711(12, 16, gain=128)


def cleanAndExit():
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def setup():
    """
    code run once
    """
    print("Initializing.\n Please ensure that the scale is empty.")
    scale_ready = False
    while not scale_ready:
        if (GPIO.input(hx.DOUT) == 0):
            scale_ready = False
        if (GPIO.input(hx.DOUT) == 1):
            print("Initialization complete!")
            scale_ready = True


def loop():
    """
    code run continuously
    """

    history = []

    try:
        prompt_handled = False
        while not prompt_handled:
            val = hx.get_grams(40)
            hx.power_down()
            time.sleep(.001)
            hx.power_up()
            print(round(val, 2))

            history.append(val)
            if len(history) > 1:
                mean = statistics.mean(history)

                print("mean={} len={}".format(mean, len(history)))

                stdev = statistics.stdev(history)

                print(stdev)

                lower = mean - stdev * 2
                upper = mean + stdev * 2

                clean_history = [x for x in history if lower < x < upper]
                if len(clean_history) > 1:
                    print("mean={} len={}".format(statistics.mean(clean_history), len(clean_history)))

            choice = "2"

            if choice == "2":
                # print("\nOffset: {}\nScale: {}".format(hx.get_offset(), hx.get_scale()))
                time.sleep(1)
            elif choice == "0":
                prompt_handled = True
                cleanAndExit()
            else:
                print("Invalid selection.\n")
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


##################################

if __name__ == "__main__":

    setup()
    while True:
        loop()


