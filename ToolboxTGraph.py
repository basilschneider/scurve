#!/usr/bin/env python2

""" Toolbox classes for various operations on ROOT TGraphs. """

from os import makedirs, chdir, getcwd, path
from array import array
from ROOT import TFile, TGraph, TCanvas, TLegend  # pylint: disable=import-error
from ROOT import Double, gStyle, gROOT
from Logger import LGR
from ToolboxFit import ToolboxFit
from ToolboxHelper import check_if_object, safe_divide

gROOT.SetBatch(True)

class ToolboxTGraph(object):

    """ Toolbox class for various operations on ROOT TGraphs. """

    def __init__(self, graphs=None, numbering=None):

        """ Initialize object variables. """

        self.s_rootfile = ''
        self.directory = ''
        self.name = ''

        # Define list of TGraphs; if constructor is called with list of
        # TGraphs, fill them into the list
        self._measurements = []
        if graphs is not None:
            fill_graphs(graphs)
        self._numbering = []
        if numbering is not None:
            fill_numbering(numbering)
        self._scurves = []
        self._fits = []
        self._clear()

    def _clear(self):

        """ Initializes/clears ROOT objects. """

        self._canvas = TCanvas()
        self._legend = TLegend(0.9, 0.2, 1.00, 0.9)

    def create_graph(self, name, title, coordinate_x):

        """ Create TGraph with sensible binning. """

        pass

    def fill_graphs(self, graphs):

        """ Fill list of TGraphs with graphs. """

        # Check all objects before filling the list
        check_if_object(graphs, list)
        for graph in graphs:
            check_if_object(graph, TGraph)
            self._measurements.append(graph)

    def fill_numbering(self, numbering):

        """ Fill list with numbering of TGraphs. """

        check_if_object(numbering, list)
        self._numbering = numbering

    def draw_graphs(self, s_graphs):

        """ Draw all TGraphs. """

        graphs = self._get_graphs(s_graphs)

        self._canvas.cd()
        same = ''
        for idx, graph in enumerate(graphs):
            #graph.Draw('AC* {0}'.format(same))
            graph.Draw(same)
            same = 'SAME'

    def integrate_graphs(self, s_graphs):

        """ Integrate TGraphs to get S-curves. """

        graphs = self._get_graphs(s_graphs)

        for graph in graphs:

            integral = 0

            # Need arrays for TGraph constructor
            a_pts = array('d', range(0, graph.GetN()))
            a_int = array('d', [])

            for point in a_pts:

                # Calculate the integral, this is done for every point, and the
                # calculation is mostly the same; if performance becomes an
                # issue, one can consider only calculating the new piece of the
                # integral instead of the whole thing
                integral = self._integral(graph, 0, point)
                a_int.append(integral)

            self._scurves.append(TGraph(len(a_pts), a_pts, a_int))

    def _integral(self, graph, x_lo, x_hi):

        """ Return integral of TGraph from x_lo to x_hi. This is done by using
        triangles. Note that TGraph::Integral() does not return the integral of
        the TGraph, but the area of the polygon spanned by the TGraph. """

        integral = 0.

        for point in range(0, graph.GetN()):
            # Check if we are in the range requested by the user
            if point < x_lo:
                continue
            if point >= x_hi:
                break

            # Use ROOT::Double() for x_n, y_n and x_n+1, y_n+1
            x_n1 = Double()
            y_n1 = Double()
            x_n2 = Double()
            y_n2 = Double()
            graph.GetPoint(int(point), x_n1, y_n1)
            graph.GetPoint(int(point)+1, x_n2, y_n2)

            # Calculate new integral segment and add it to old one
            integral += 1./2*(y_n2+y_n1)*(x_n2-x_n1)

        return integral

    def normalize(self):

        """ Normalize S-curves.
        First point is at y=1., last point is at y=0.  """

        # List to store normalize graps
        graphs_normalized = []

        for graph in self._scurves:

            # Last point of TGraph needed for normalization
            x_N = Double()
            y_N = Double()
            graph.GetPoint(graph.GetN()-1, x_N, y_N)

            # Need arrays for TGraph constructor
            a_pts = array('d', range(0, graph.GetN()))
            a_nrm = array('d', [])

            for point in a_pts:

                # Use ROOT::Double() for x_n, y_n
                x_n1 = Double()
                y_n1 = Double()
                graph.GetPoint(int(point), x_n1, y_n1)

                # Normalize to 1 and invert
                a_nrm.append(-safe_divide(y_n1, y_N))


            graphs_normalized.append(TGraph(len(a_pts), a_pts, a_nrm))

        # Overwrite class member list
        self._scurves = graphs_normalized

    def fit(self, distribution, s_graphs):

        """ Fit Gaussian distribution over TGraphs. """

        graphs = self._get_graphs(s_graphs)

        for idx, graph in enumerate(graphs):
            try:
                numbering = self._numbering[idx]
            except IndexError:
                numbering = -1
            graph.Fit(distribution, 'Q')
            graph.GetFunction(distribution).SetLineColor(4)
            self._fits.append(ToolboxFit(graph.GetFunction(distribution),
                              numbering))

        # If there is only one fit, show stats
        if len(graphs) == 1:
            gStyle.SetOptFit(1111111)
        else:
            gStyle.SetOptFit(0000000)

    def set_title(self, title, s_graphs):

        """ Set title of TGraph. """

        graphs = self._get_graphs(s_graphs)

        # Only change first TGraph in list, since this one defines axes
        graphs[0].SetTitle(title)

    def set_axis_title(self, axis_x, s_graphs):

        """ Set axis title of TGraph. """

        graphs = self._get_graphs(s_graphs)

        # Only change first TGraph in list, since this one defines axes
        graphs[0].GetXaxis().SetTitle(axis_x)

    def _add_legend(self):

        """ Add TLegend. """

        pass

    def _get_graphs(self, s_graphs):

        """ Get list of TGraphs according to the values passed. """

        check_if_object(s_graphs, list)

        # Find out what list of graphs are requested
        graphs = []
        for s_graph in s_graphs:
            if s_graph == 'measurements':
                graphs += self._measurements
            if s_graph == 'scurves':
                graphs += self._scurves

        # If list is not empty, return list, otherwise throw error
        if graphs:
            return graphs
        else:
            raise ValueError('Don\'t know what list of TGraphs to use.')

    def get_fits(self):

        """ Get list with ToolboxFits. """

        return self._fits

    def save(self, s_graphs):

        """ Save TGraph in TFile and as *.pdf. """

        graphs = self._get_graphs(s_graphs)

        # Open TFile
        rootfile = TFile(self.s_rootfile, 'UPDATE')

        # Go into directory if it is defined
        if self.directory:
            cwd = getcwd()

            # Change directory in rootfile
            if not rootfile.GetDirectory(self.directory):
                rootfile.mkdir(self.directory)
            rootfile.cd(self.directory)

            # Change directory on filesystem
            if not path.exists(self.directory):
                makedirs(self.directory)
            chdir(self.directory)

        self._canvas.SaveAs('{0}.pdf'.format(self.name))
        for graph in graphs:
            graph.Write()

        # Go back to original working directories
        if self.directory:
            rootfile.cd()
            chdir(cwd)

        # Close TFile
        rootfile.Close()

        self._clear()

    def reset(self):

        """ Reset all TGraphs. """

        self._measurements = []
        self._numbering = []
        self._scurves = []
        self._fits = []
