# The MIT License (MIT)
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
"""
`adafruit_led_animation.animation.volume`
================================================================================
Volume animation for CircuitPython helper library for LED animations.
* Author(s): Mark Komus
Implementation Notes
--------------------
**Hardware:**
* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

from adafruit_led_animation.animation import Animation

class Volume(Animation):
    """
    Animate the brightness and number of pixels based on volume.
    :param pixel_object: The initialised LED object.
    :param float speed: Animation update speed in seconds, e.g. ``0.1``.
    :param brightest_color: Color at max volume ``(r, g, b)`` tuple, or ``0x000000`` hex format
    :param decoder: a MP3Decoder object that the volume will be taken from
    :param float max_volume: what volume is considered maximum where everything is lit up
    """

    def __init__(self, pixel_object, speed, brightest_color, decoder, max_volume=500, name=None):
        self._decoder = decoder
        self._num_pixels = len(pixel_object)
        self._max_volume = max_volume
        self._brigthest_color = brightest_color
        super().__init__(pixel_object, speed, brightest_color, name=name)

    def _set_color(self, brightest_color):
        self.colors = [brightest_color]

    def map_range(self, x, in_min, in_max, out_min, out_max):
        mapped = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        if out_min <= out_max:
            return max(min(mapped, out_max), out_min)

        return min(max(mapped, out_max), out_min)

    def draw(self):
        red = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._brigthest_color[0]))
        green = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._brigthest_color[1]))
        blue = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._brigthest_color[2]))

        lit_pixels = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._num_pixels))
        if lit_pixels > self._num_pixels:
            lit_pixels = self._num_pixels

        self.pixel_object[0:lit_pixels] = [(red,green,blue)] * lit_pixels
        self.pixel_object[lit_pixels:self._num_pixels] = [(0,0,0)] * (self._num_pixels-lit_pixels)
