#!/usr/bin/env python2

"""
Author: Basil Schneider <basil.schneider@cern.ch>
Take calibration measurement and integrate, to get S-curves.
"""

from ROOT import TFile  # pylint: disable=import-error
from Logger import LGR
from ToolboxHelper import check_if_object

class SCurve(object):

    """ Take calibration measurement and integrate, to get S-curve. """

    def __init__(self, path):
        # Path to ROOT file
        self._path = path

        # Graphs to be drawn, can be any combination of numbers 0 to 47
        self._graphs = range(0, 48)

    def make_s_curve(self):

        """ Call a sequence of functions to get the S-curves. """

        LGR.info('Retrieve histogram from ROOT file.')
        histo = self._get_histo()
        LGR.info('Integrate histogram.')
        histo = self._histo_integrate(histo)

    def _get_histo(self):

        """ Read data from ROOT file given in path. """

        f_in = TFile(self._path, 'READ')
        graph = f_in.Get('1')

    def _histo_integrate(self, histo):

        """ Integrate histogram. """

        pass

    def get_graphs(self):

        """ Get list of graphs to be drawn. """

        return self._graphs

    def set_graphs(self, graphs):

        """ Set list of graphs to be drawn. This can be any combination of
        numbers between 0 and 47. """

        # Make sure that graphs is a list
        check_if_object(graphs, list)

        self._graphs = graphs


if __name__ == '__main__':
    PRE1 = SCurve('../MAPSA_Software/plots01_nominal/backup_preCalibration__MPA2.root')
    PRE1.set_graphs([1,2,3])
    PRE1.make_s_curve()
