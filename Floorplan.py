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
        self._histogram_c = TH2F()
        self._histogram_c_err = TH2F()
        self._histogram_mu = TH2F()
        self._histogram_mu_err = TH2F()
        self._histogram_sigma = TH2F()
        self._histogram_sigma_err = TH2F()
        self._histogram_chi2 = TH2F()
        self._histogram_ndf = TH2F()
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

        self._histogram_c = TH2F('c', 'Constant', self._bins_x, 0, self._bins_x,
                                 self._bins_y, 0, self._bins_y)
        self._histogram_c_err = TH2F('c_err', 'Error on constant', self._bins_x, 0, self._bins_x,
                                     self._bins_y, 0, self._bins_y)
        self._histogram_mu = TH2F('mu', 'Mean', self._bins_x, 0, self._bins_x,
                                  self._bins_y, 0, self._bins_y)
        self._histogram_mu_err = TH2F('mu_err', 'Error on mean', self._bins_x, 0, self._bins_x,
                                      self._bins_y, 0, self._bins_y)
        self._histogram_sigma = TH2F('sigma', '#sigma', self._bins_x, 0, self._bins_x,
                                     self._bins_y, 0, self._bins_y)
        self._histogram_sigma_err = TH2F('sigma_err', 'Error on #sigma', self._bins_x, 0, self._bins_x,
                                         self._bins_y, 0, self._bins_y)
        self._histogram_chi2 = TH2F('chi2', '#chi^{2}', self._bins_x, 0, self._bins_x,
                                    self._bins_y, 0, self._bins_y)
        self._histogram_ndf = TH2F('ndf', 'NDF', self._bins_x, 0, self._bins_x,
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

    def fill_maps(self, fits):

        """ Make 2d maps of one MPA. """

        for fit in fits:
            try:
                numbering = fit.get_numbering()
            except TypeError:
                raise TypeError('Couldn\'t fill map for MPA number {}. Maybe '
                                'the geometry is not defined for this MPA?'
                                .format(fit.get_numbering()))

            self._histogram_c.Fill(self._get_x(numbering),
                                   self._get_y(numbering), fit.get_c())
            self._histogram_c_err.Fill(self._get_x(numbering),
                                       self._get_y(numbering), fit.get_c_err())
            self._histogram_mu.Fill(self._get_x(numbering),
                                    self._get_y(numbering), fit.get_mu())
            self._histogram_mu_err.Fill(self._get_x(numbering),
                                        self._get_y(numbering), fit.get_mu_err())
            self._histogram_sigma.Fill(self._get_x(numbering),
                                       self._get_y(numbering), fit.get_sigma())
            self._histogram_sigma_err.Fill(self._get_x(numbering),
                                           self._get_y(numbering),
                                           fit.get_sigma_err())
            self._histogram_chi2.Fill(self._get_x(numbering),
                                      self._get_y(numbering), fit.get_chi2())
            self._histogram_ndf.Fill(self._get_x(numbering),
                                     self._get_y(numbering), fit.get_ndf())

        self._draw_save()

    def _draw_save(self):

        """ Draw and save map in TFile and as *.pdf. """

        self._canvas = TCanvas()
        gStyle.SetOptStat(0000000)

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

        self._histogram_c.Draw('COLZ')
        self._canvas.SaveAs('{}_c.pdf'.format(self.name))
        self._histogram_c.Write()

        self._histogram_c_err.Draw('COLZ')
        self._canvas.SaveAs('{}_c_err.pdf'.format(self.name))
        self._histogram_c_err.Write()

        self._histogram_mu.Draw('COLZ')
        self._canvas.SaveAs('{}_mu.pdf'.format(self.name))
        self._histogram_mu.Write()

        self._histogram_mu_err.Draw('COLZ')
        self._canvas.SaveAs('{}_mu_err.pdf'.format(self.name))
        self._histogram_mu_err.Write()

        self._histogram_sigma.Draw('COLZ')
        self._canvas.SaveAs('{}_sigma.pdf'.format(self.name))
        self._histogram_sigma.Write()

        self._histogram_sigma_err.Draw('COLZ')
        self._canvas.SaveAs('{}_sigma_err.pdf'.format(self.name))
        self._histogram_sigma_err.Write()

        self._histogram_chi2.Draw('COLZ')
        self._canvas.SaveAs('{}_chi2.pdf'.format(self.name))
        self._histogram_chi2.Write()

        self._histogram_ndf.Draw('COLZ')
        self._canvas.SaveAs('{}_ndf.pdf'.format(self.name))
        self._histogram_ndf.Write()

        # Go back to original working directories
        if self.directory:
            rootfile.cd()
            chdir(cwd)

        # Close TFile
        rootfile.Close()
