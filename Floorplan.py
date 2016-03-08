#!/usr/bin/env python2

"""
Author: Basil Schneider <basil.schneider@cern.ch>
Make 2d maps of MPA, showing various fit characteristics.
"""

from os import getcwd, path, chdir
from ROOT import TH2F, TFile, TCanvas, gStyle
from Logger import LGR

class Floorplan(object):

    """ Make 2d maps of MPA, showing various fit characteristics. """

    def __init__(self):

        """ Initialize class variables. """

        self._geometry = []
        self._histogram = TH2F()
        self._bins_x = 0
        self._bins_y = 0
        self.directory = '.'
        self.name = ''
        self.s_rootfile = ''
        self._canvas = TCanvas()

    def set_geometry(self, geometry):

        """ Defines geometry, i.e. the following list is interpreted as a
        geometry:

        [[1, 2, 3][4, 5, 6]]

        1 2 3
        4 5 6

        Also creates a TH2F with the corresponding number of bins. """

        # Set geometry
        self._geometry = geometry

        # Get number of bins in x
        self._bins_x = 0
        for subgeometry in geometry:
            self._bins_x = max(self._bins_x, len(subgeometry))

        # Get number of bins in y
        self._bins_y = len(geometry)

        self._histogram = TH2F('name', 'title', self._bins_x, 0, self._bins_x,
                               self._bins_y, 0, self._bins_y)

    def _get_x(self, numbering):

        """ Return x axis coordinate in TH2F for numbering. """

        for subgeometry in self._geometry:
            if numbering in subgeometry:
                return subgeometry.index(numbering) + 0.5

    def _get_y(self, numbering):

        """ Return y axis coordinate in TH2F for numbering. """

        for idx, subgeometry in enumerate(self._geometry):
            if numbering in subgeometry:
                # Subtract idx from number of bins in y, since we start
                # counting from top; subtract 0.5 to hit bin center
                return self._bins_y - idx - 0.5

    def fill_map(self, fits):

        """ Make 2d maps of one MPA. """

        for fit in fits:
            try:
                self._histogram.Fill(self._get_x(fit.get_numbering()),
                                     self._get_y(fit.get_numbering()),
                                     fit.get_mu())
            except TypeError:
                raise TypeError('Couldn\'t fill map for MPA number {}. Maybe '
                                'the geometry is not defined for this MPA?'
                                .format(fit.get_numbering()))

        self._draw()
        self._save()

    def _draw(self):

        """ Draw map on TCanvas. """

        self._canvas = TCanvas()
        gStyle.SetOptStat(0000000)
        self._histogram.Draw('COLZ')

    def _save(self):

        """ Save map in TFile and as *.pdf. """

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

        self._canvas.SaveAs('{}.pdf'.format(self.name))
        self._histogram.Write()

        # Go back to original working directories
        if self.directory:
            rootfile.cd()
            chdir(cwd)

        # Close TFile
        rootfile.Close()
