#!/usr/bin/env python2

"""
Author: Basil Schneider <basil.schneider@cern.ch>
Take calibration measurement and integrate, to get S-curves.
"""

from ROOT import TFile, TGraph  # pylint: disable=import-error
from Logger import LGR
from ToolboxTGraph import ToolboxTGraph
from ToolboxHelper import check_if_object

class SCurve(object):

    """ Take calibration measurement and integrate, to get S-curve. """

    def __init__(self, path):
        # Path to ROOT file
        self._path = path

        # List of names of TGraphs to be drawn
        # This can be any combination of numbers between 0 and 47
        self._s_graphs = range(0, 48)

        # List with all ToolboxTGraph objects
        self._toolbox_graph = ToolboxTGraph()

    def make_s_curve(self):

        """ Call a sequence of functions to get the S-curves. """

        LGR.info('Retrieve TGraphs from ROOT file.')
        self._get_graphs()
        LGR.info('Create plot with original TGraphs.')
        self._toolbox_graph.draw_graphs()
        self._toolbox_graph.save()

    def _get_graphs(self):

        """ Read data from ROOT file given in path. """

        # Open ROOT file
        f_in = TFile(self._path, 'READ')

        # Get TGraphs from ROOT file and fill list in ToolboxTGraph object
        graphs = []
        for s_graph in self._s_graphs:
            graph = f_in.Get(str(s_graph))
            check_if_object(graph, TGraph)
            graphs.append(graph)

        self._toolbox_graph.fill_graphs(graphs)

    def get_graphs(self):

        """ Get list of graphs to be drawn. """

        return self._s_graphs

    def set_graphs(self, graphs):

        """ Set list of graphs to be drawn. This can be any combination of
        numbers between 0 and 47. """

        # Make sure that graphs is a list
        check_if_object(graphs, list)

        self._s_graphs = graphs

    def get_directory(self):

        """ Get directory where plots and ROOT files are stored in. """

        return self._toolbox_graph.directory

    def set_directory(self, s_dir):

        """ Set directory where plots and ROOT files are stored in. """

        self._toolbox_graph.directory = s_dir

    def get_name(self):

        """ Get name of output files. """

        return self._toolbox_graph.name

    def set_name(self, s_name):

        """ Set name of output files. """

        self._toolbox_graph.name = s_name

    def get_rootfile(self):

        """ Get name of output ROOT file. """

        return self._toolbox_graph.s_rootfile

    def set_rootfile(self, s_rootfile):

        """ Set name of output ROOT file. """

        # If rootfile is located in a subdirectory, create directory first
        if '/' in s_rootfile:
            system('mkdir -p {}'
                   .format('/'.join(s_rootfile.split('/')[:-1])))

        self._toolbox_graph.s_rootfile = s_rootfile


if __name__ == '__main__':
    PRE1 = SCurve('../MAPSA_Software/plots01_nominal/backup_preCalibration__MPA2.root')
    PRE1.set_graphs([1,2,3])
    PRE1.set_directory('.')
    PRE1.set_rootfile('output.root')
    PRE1.set_name('output')
    PRE1.make_s_curve()
