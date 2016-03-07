#!/usr/bin/env python2

"""
Author: Basil Schneider <basil.schneider@cern.ch>
Take calibration measurement and integrate, to get S-curves.
"""

from os import system
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

    def retrieve_graphs(self):

        """ Retrieve TGraphs. """

        LGR.info('Retrieve TGraphs from ROOT file.')
        # Open ROOT file
        f_in = TFile(self._path, 'READ')

        # Get TGraphs from ROOT file and fill list in ToolboxTGraph object
        graphs = []
        for s_graph in self._s_graphs:
            graph = f_in.Get(str(s_graph))
            check_if_object(graph, TGraph)
            graphs.append(graph)

        self._toolbox_graph.fill_graphs(graphs)

        LGR.info('Create plot with original TGraphs.')
        self._draw_save('Gaussian', ['measurements'])

    def make_gaussian_fit(self):

        """ Fit a Gaussian distribution over the TGraph. """

        LGR.info('Fit Gaussian on TGraph.')
        self._toolbox_graph.fit('gaus', ['measurements'])
        self._draw_save('Gaussian_fit', ['measurements'])

    def make_s_curve(self):

        """ Call a sequence of functions to get the S-curves. """

        LGR.info('Integrate TGraphs to get S-curves.')
        self._toolbox_graph.integrate_graphs(['measurements'])
        self._draw_save('S-curve_unnormalized', ['scurves'])
        LGR.info('Normalize S-curves.')
        self._toolbox_graph.normalize()
        self._draw_save('S-curve', ['scurves'])

    def _draw_save(self, name, s_graphs):

        """ Draw and save TGraphs. """

        self._toolbox_graph.set_axis_title('THDAC', s_graphs)
        self._toolbox_graph.set_title(name, s_graphs)
        self._toolbox_graph.draw_graphs(s_graphs)
        self.set_name(name)
        self._toolbox_graph.save(s_graphs)

    def get_graphs(self):

        """ Get list of graphs to be drawn. """

        return self._s_graphs

    def set_graphs(self, graphs):

        """ Set list of graphs to be drawn. This can be any combination of
        numbers between 0 and 47. """

        # Make sure that graphs is a list
        check_if_object(graphs, list)

        # Filter out all numbers outside 0 and 47
        self._s_graphs = filter(lambda y: y in range(0, 48), graphs)

    def get_directory(self):

        """ Get directory where plots and ROOT files are stored in. """

        return self._toolbox_graph.directory

    def set_directory(self, s_dir):

        """ Set directory where plots and ROOT files are stored in. """

        self._toolbox_graph.directory = s_dir.rstrip('/')

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
