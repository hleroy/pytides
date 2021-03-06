#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A very basic test case for pytides

Based on "How to use the NOAA's published Harmonic Constituents"
https://github.com/sam-cox/pytides/wiki/How-to-use-the-NOAA's-published-Harmonic-Constituents-in-Python-with-Pytides
"""

from datetime import datetime
from pytides.tide import Tide
import pytides.constituent as cons
import numpy as np
import unittest


class TestPytides(unittest.TestCase):

    def test_kings_point(self):
        # Check that Pytides prediction in King's Point for 0000 and 0600 GMT
        # on January 1 2013 are [-0.086250887498591222 2.207534179351927].
        # Results have been updated to take into account commit #7d5e3c7

        # These are the NOAA constituents, in the order presented on their website.
        constituents = [c for c in cons.noaa if c != cons._Z0]

        # Phases and amplitudes (relative to GMT and in degrees and metres)
        published_phases = [115.7, 140.7, 92.6, 192, 145.5, 220.6, 159.9, 202.8, 152.3, 117.2, 92, 0, 0, 69.7, 224.5, 141.7, 121.9,
                            228.4, 252.1, 0, 60.1, 135.5, 0, 0, 204.5, 212.2, 112.3, 141.8, 249.1, 211.1, 75.1, 181.4, 140.4, 202.4, 141.8, 155, 160.9]

        published_amplitudes = [1.142, 0.189, 0.241, 0.1, 0.036, 0.066, 0.08, 0.01, 0.004, 0.022, 0.052, 0, 0, 0.03, 0.007, 0.025, 0.009,
                                0.005, 0.008, 0, 0.024, 0.065, 0, 0, 0.004, 0.017, 0.015, 0.002, 0.002, 0.032, 0.003, 0.007, 0.07, 0.009, 0.053, 0.007, 0.008]

        # We can add a constant offset (e.g. for a different datum, we will use relative to MLLW):
        MTL = 5.113
        MLLW = 3.928
        offset = MTL - MLLW
        constituents.append(cons._Z0)
        published_phases.append(0)
        published_amplitudes.append(offset)

        # Build the model.
        assert(len(constituents) == len(published_phases) == len(published_amplitudes))
        model = np.zeros(len(constituents), dtype=Tide.dtype)
        model['constituent'] = constituents
        model['amplitude'] = published_amplitudes
        model['phase'] = published_phases

        tide = Tide(model=model, radians=False)

        heights = tide.at([datetime(2013, 1, 1, 0, 0, 0), datetime(2013, 1, 1, 6, 0, 0)])

        self.assertEqual(heights[0], -0.086250887498591222)
        self.assertEqual(heights[1], 2.207534179351927)


if __name__ == '__main__':
    unittest.main()
