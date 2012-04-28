#!/usr/bin/env python

'''
Created on Feb 2, 2012
'''

from __future__ import division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyue@mit.edu"
__date__ = "Feb 2, 2012"

import unittest
import os

from pymatgen.core.structure import Composition

from pymatgen.app.battery.conversion_battery import ConversionElectrode
from pymatgen.entries.computed_entries import computed_entries_from_json

module_dir = os.path.dirname(os.path.abspath(__file__))

class ConversionElectrodeTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        formulas = ['LiCoO2', "FeF3"]
        expected_properties = {}
        expected_properties['LiCoO2'] = {'average_voltage' : 2.26940307125,
                                         'capacity_grav': 903.19752911225669,
                                         'capacity_vol': 2903.35804724,
                                         'specific_energy': 2049.7192465127678,
                                         'energy_density': 6588.8896693479574}
        expected_properties['FeF3'] = {'average_voltage' : 3.06179925889,
                                         'capacity_grav': 601.54508701578118,
                                         'capacity_vol': 2132.2069115142394,
                                         'specific_energy': 1841.8103016131706,
                                         'energy_density': 6528.38954147}
        for f in formulas:

            with open(os.path.join(module_dir, f + ".json"), 'r') as fid:
                entries = computed_entries_from_json(fid.read())

            c = ConversionElectrode.from_composition_and_entries(Composition.from_formula(f), entries)
            self.assertEqual(len(c.sub_electrodes(True)), c.num_steps)
            self.assertEqual(len(c.sub_electrodes(False)), sum(xrange(1, c.num_steps + 1)))

            p = expected_properties[f]

            for k, v in p.items():
                self.assertAlmostEqual(getattr(c, "get_" + k).__call__(), v)


if __name__ == "__main__":
    unittest.main()

