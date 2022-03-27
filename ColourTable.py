#!/usr/bin/env python3
import colorsys
import itertools
from fractions import Fraction
from typing import Iterable, Tuple

# Based on solutions from here
# https://stackoverflow.com/questions/309149/generate-distinctly-different-rgb-colors-in-graphs


def _get_series():
    # this will generate a faction of powers 1/2 1/4 1/8 etc
    for v in itertools.count():
        yield Fraction(1, 2**v)


def _get_fraction():
    yield Fraction(0)
    for v in _get_series():
        denom = v.denominator
        for j in range(1, denom, 2):
            yield Fraction(j, denom)


def _hue_to_tones(h: Fraction):
    for s in [Fraction(6, 10)]:  # optionally use range
        for v in [Fraction(8, 10), Fraction(5, 10)]:  # could use range too
            yield (h, s, v)  # use bias for v here if you use range


class ColourTable:
    fraction = _get_fraction()

    def __init__(self):
        pass

    @classmethod
    def get_rgb_float(cls):
        fraction = next(cls.fraction)
        values = next(_hue_to_tones(fraction))
        return colorsys.hsv_to_rgb(*map(float, values))

    @classmethod
    def get_rgb(cls):
        values = cls.get_rgb_float()
        return [*map(lambda v: int(v * 255), values)]


if __name__ == "__main__":
    for i in range(0, 10):
        print(ColourTable.get_rgb())
        print(ColourTable.get_rgb_float())
