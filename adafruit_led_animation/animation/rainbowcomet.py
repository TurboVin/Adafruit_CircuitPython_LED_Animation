# The MIT License (MIT)
#
# Copyright (c) 2019-2020 Roy Hooper
# Copyright (c) 2020 Kattni Rembor for Adafruit Industries
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
`adafruit_led_animation.animation.rainbowcomet`
================================================================================

TODO

* Author(s): Roy Hooper, Kattni Rembor

"""

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import colorwheel, BLACK


class RainbowComet(Comet):
    """
    A rainbow comet animation.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param int tail_length: The length of the comet. Defaults to 10. Cannot exceed the number of
                            pixels present in the pixel object, e.g. if the strip is 30 pixels
                            long, the ``tail_length`` cannot exceed 30 pixels.
    :param bool reverse: Animates the comet in the reverse order. Defaults to ``False``.
    :param bool bounce: Comet will bounce back and forth. Defaults to ``True``.
    :param int colorwheel_offset: Offset from start of colorwheel (0-255).
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        tail_length=10,
        reverse=False,
        bounce=False,
        colorwheel_offset=0,
        name=None,
    ):
        self._colorwheel_is_tuple = isinstance(colorwheel(0), tuple)
        self._colorwheel_offset = colorwheel_offset

        super().__init__(pixel_object, speed, 0, tail_length, reverse, bounce, name)

    def _calc_brightness(self, n, color):
        brightness = (n * self._color_step) + self._color_offset
        if not self._colorwheel_is_tuple:
            color = (color & 0xFF, ((color & 0xFF00) >> 8), (color >> 16))
        return [int(i * brightness) for i in color]

    def __recompute_color(self, color):
        factor = int(256 / self._tail_length)
        self._comet_colors = [BLACK] + [
            self._calc_brightness(
                n,
                colorwheel(
                    int((n * factor) + self._color_offset + self._colorwheel_offset)
                    % 256
                ),
            )
            for n in range(self._tail_length - 1)
        ]
        self._reverse_comet_colors = list(reversed(self._comet_colors))
        self._computed_color = color
