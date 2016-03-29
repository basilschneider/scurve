#!/usr/bin/env python2

"""
Author: Basil Schneider <basil.schneider@cern.ch>
Make 2d maps of MPA, showing various fit characteristics.
"""

from os import makedirs, getcwd, path, chdir
from ROOT import TH2F, TFile, TCanvas, gStyle, gPad
from Logger import LGR

class Floorplan(object):

    """ Make 2d maps of MPA, showing various fit characteristics. """

    def __init__(self):

        """ Initialize class variables. """

        self._geometry = []
        self._histogram_c = []
        self._histogram_c_err = []
        self._histogram_mu = []
        self._histogram_mu_err = []
        self._histogram_sigma = []
        self._histogram_sigma_err = []
        self._histogram_chi2 = []
        self._histogram_ndf = []
        self._bins_x = 0
        self._bins_y = 0
        self.directory = '.'
        self.name = ''
        self.s_rootfile = ''
        self._canvas = TCanvas()
        self._map_c = [TCanvas(), TCanvas()]
        self._map_c_err = [TCanvas(), TCanvas()]
        self._map_mu = [TCanvas(), TCanvas()]
        self._map_mu_err = [TCanvas(), TCanvas()]
        self._map_sigma = [TCanvas(), TCanvas()]
        self._map_sigma_err = [TCanvas(), TCanvas()]
        self._map_chi2 = [TCanvas(), TCanvas()]
        self._map_ndf = [TCanvas(), TCanvas()]
        for idx in range(0, 2):
            self._map_c[idx].Divide(3, 2)
            self._map_c_err[idx].Divide(3, 2)
            self._map_mu[idx].Divide(3, 2)
            self._map_mu_err[idx].Divide(3, 2)
            self._map_sigma[idx].Divide(3, 2)
            self._map_sigma_err[idx].Divide(3, 2)
            self._map_chi2[idx].Divide(3, 2)
            self._map_ndf[idx].Divide(3, 2)

    def set_geometry(self, geometry, prefix):

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

        # Create histograms
        if prefix == 0:
            prefix_str = 'pre'
        else:
            prefix_str = 'post'

        self._histogram_c.append(TH2F('c', 'Constant ({})'.format(prefix_str),
                                      self._bins_x, 0, self._bins_x,
                                      self._bins_y, 0, self._bins_y))
        self._histogram_c_err.append(TH2F('c_err', 'Error on constant ({})'
                                          .format(prefix_str),
                                          self._bins_x, 0, self._bins_x,
                                          self._bins_y, 0, self._bins_y))
        self._histogram_mu.append(TH2F('mu', 'Mean ({})'.format(prefix_str),
                                       self._bins_x, 0, self._bins_x,
                                       self._bins_y, 0, self._bins_y))
        self._histogram_mu_err.append(TH2F('mu_err', 'Error on mean ({})'
                                           .format(prefix_str),
                                           self._bins_x, 0, self._bins_x,
                                           self._bins_y, 0, self._bins_y))
        self._histogram_sigma.append(TH2F('sigma', '#sigma ({})'
                                          .format(prefix_str),
                                          self._bins_x, 0, self._bins_x,
                                          self._bins_y, 0, self._bins_y))
        self._histogram_sigma_err.append(TH2F('sigma_err',
                                              'Error on #sigma ({})'
                                              .format(prefix_str),
                                              self._bins_x, 0, self._bins_x,
                                              self._bins_y, 0, self._bins_y))
        self._histogram_chi2.append(TH2F('chi2', '#chi^{{2}} ({})'
                                         .format(prefix_str),
                                         self._bins_x, 0, self._bins_x,
                                         self._bins_y, 0, self._bins_y))
        self._histogram_ndf.append(TH2F('ndf', 'NDF ({})'.format(prefix_str),
                                        self._bins_x, 0, self._bins_x,
                                        self._bins_y, 0, self._bins_y))

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

    def fill_maps(self, fits, coordinate, prefix):

        """ Make 2d maps of one MPA. """

        for fit in fits:
            try:
                numbering = fit.get_numbering()
            except TypeError:
                raise TypeError('Couldn\'t fill map for MPA number {}. Maybe '
                                'the geometry is not defined for this MPA?'
                                .format(fit.get_numbering()))

            self._histogram_c[-1].Fill(self._get_x(numbering),
                                   self._get_y(numbering), fit.get_c())
            self._histogram_c_err[-1].Fill(self._get_x(numbering),
                                       self._get_y(numbering), fit.get_c_err())
            self._histogram_mu[-1].Fill(self._get_x(numbering),
                                    self._get_y(numbering), fit.get_mu())
            self._histogram_mu_err[-1].Fill(self._get_x(numbering),
                                        self._get_y(numbering), fit.get_mu_err())
            self._histogram_sigma[-1].Fill(self._get_x(numbering),
                                       self._get_y(numbering), fit.get_sigma())
            self._histogram_sigma_err[-1].Fill(self._get_x(numbering),
                                           self._get_y(numbering),
                                           fit.get_sigma_err())
            self._histogram_chi2[-1].Fill(self._get_x(numbering),
                                      self._get_y(numbering), fit.get_chi2())
            self._histogram_ndf[-1].Fill(self._get_x(numbering),
                                     self._get_y(numbering), fit.get_ndf())

        self._draw_save(coordinate, prefix)

    def _chdir(self, directory, rootfile):

        """ Change directory on file system and in ROOT file. """

        # Change directory in rootfile
        if not rootfile.GetDirectory(directory):
            rootfile.mkdir(directory)
        rootfile.cd(directory)

        # Change directory on filesystem
        if not path.exists(directory):
            makedirs(directory)
        chdir(directory)

    def _draw_save(self, coordinate, prefix):

        """ Draw and save map in TFile and as *.pdf. """

        self._canvas = TCanvas()
        gStyle.SetOptStat(0000000)

        # Open TFile
        rootfile = TFile(self.s_rootfile, 'UPDATE')

        cwd = getcwd()

        # Go into directory if it is defined
        if self.directory:
            self._chdir(self.directory, rootfile)

        self._cosmetics()

        self._canvas.cd()
        #self._histogram_c[-1].GetZaxis().SetRangeUser(6000, 10000)
        self._histogram_c[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_c.pdf'.format(self.name))
        self._histogram_c[-1].Write()
        self._map_c[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_c[-1].Draw('COLZ')

        self._canvas.cd()
        #self._histogram_c_err[-1].GetZaxis().SetRangeUser(0, 300)
        self._histogram_c_err[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_c_err.pdf'.format(self.name))
        self._histogram_c_err[-1].Write()
        self._map_c_err[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_c_err[-1].Draw('COLZ')

        self._canvas.cd()
        self._histogram_mu[-1].GetZaxis().SetRangeUser(30, 170)
        self._histogram_mu[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_mu.pdf'.format(self.name))
        self._histogram_mu[-1].Write()
        self._map_mu[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_mu[-1].Draw('COLZ')

        self._canvas.cd()
        self._histogram_mu_err[-1].GetZaxis().SetRangeUser(0, 0.1)
        self._histogram_mu_err[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_mu_err.pdf'.format(self.name))
        self._histogram_mu_err[-1].Write()
        self._map_mu_err[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_mu_err[-1].Draw('COLZ')

        self._canvas.cd()
        self._histogram_sigma[-1].GetZaxis().SetRangeUser(1, 7)
        self._histogram_sigma[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_sigma.pdf'.format(self.name))
        self._histogram_sigma[-1].Write()
        self._map_sigma[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_sigma[-1].Draw('COLZ')

        self._canvas.cd()
        self._histogram_sigma_err[-1].GetZaxis().SetRangeUser(0, 0.1)
        self._histogram_sigma_err[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_sigma_err.pdf'.format(self.name))
        self._histogram_sigma_err[-1].Write()
        self._map_sigma_err[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_sigma_err[-1].Draw('COLZ')

        self._canvas.cd()
        self._histogram_chi2[-1].GetZaxis().SetRangeUser(0e6, 50e6)
        self._histogram_chi2[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_chi2.pdf'.format(self.name))
        self._histogram_chi2[-1].Write()
        self._map_chi2[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_chi2[-1].Draw('COLZ')

        self._canvas.cd()
        self._histogram_ndf[-1].Draw('COLZ')
        self._canvas.SaveAs('{}_ndf.pdf'.format(self.name))
        self._histogram_ndf[-1].Write()
        self._map_ndf[prefix].cd(self._get_mpa_coordinate(coordinate))
        self._histogram_ndf[-1].Draw('COLZ')

        # Go back to original working directories
        if self.directory:
            rootfile.cd()
            chdir(cwd)

        # Save complete map when coordinate is 5;
        # this is not completely sane, but good enough
        if coordinate == 5:
            self._chdir('{}/all'
                        .format('/'.join(self.directory.split('/')[:-1])),
                        rootfile)
            for idx in range(0, 2):
                if idx == 0:
                    prefix = 'pre'
                else:
                    prefix = 'post'
                self._map_c[idx].Write()
                self._map_c[idx].SaveAs('{}_all_{}_c.pdf'
                                        .format(self.name, prefix))
                self._map_c_err[idx].Write()
                self._map_c_err[idx].SaveAs('{}_all_{}_c_err.pdf'
                                            .format(self.name, prefix))
                self._map_mu[idx].Write()
                self._map_mu[idx].SaveAs('{}_all_{}_mu.pdf'
                                         .format(self.name, prefix))
                self._map_mu_err[idx].Write()
                self._map_mu_err[idx].SaveAs('{}_all_{}_mu_err.pdf'
                                             .format(self.name, prefix))
                self._map_sigma[idx].Write()
                self._map_sigma[idx].SaveAs('{}_all_{}_sigma.pdf'
                                            .format(self.name, prefix))
                self._map_sigma_err[idx].Write()
                self._map_sigma_err[idx].SaveAs('{}_all_{}_sigma_err.pdf'
                                                .format(self.name, prefix))
                self._map_chi2[idx].Write()
                self._map_chi2[idx].SaveAs('{}_all_{}_chi2.pdf'
                                           .format(self.name, prefix))
                self._map_ndf[idx].Write()
                self._map_ndf[idx].SaveAs('{}_all_{}_ndf.pdf'
                                          .format(self.name, prefix))

            # Go back to original working directories
            if self.directory:
                rootfile.cd()
                chdir(cwd)

        # Close TFile
        rootfile.Close()

    def _get_mpa_coordinate(self, coordinate):

        """ Return physical coordinate of MPA on MaPSA assembly. """

        if coordinate == 0:
            return 1
        if coordinate == 1:
            return 2
        if coordinate == 2:
            return 3
        if coordinate == 3:
            return 6
        if coordinate == 4:
            return 5
        if coordinate == 5:
            return 4
        else:
            return -1

    def _cosmetics(self):

        """ Do cosmetics on 2d maps. """

        # Set 16 ticks on x axis and 3 ticks on y axis
        self._histogram_c[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_c[-1].GetYaxis().SetNdivisions(3, 0, 0)
        self._histogram_c_err[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_c_err[-1].GetYaxis().SetNdivisions(3, 0, 0)
        self._histogram_mu[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_mu[-1].GetYaxis().SetNdivisions(3, 0, 0)
        self._histogram_mu_err[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_mu_err[-1].GetYaxis().SetNdivisions(3, 0, 0)
        self._histogram_sigma[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_sigma[-1].GetYaxis().SetNdivisions(3, 0, 0)
        self._histogram_sigma_err[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_sigma_err[-1].GetYaxis().SetNdivisions(3, 0, 0)
        self._histogram_chi2[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_chi2[-1].GetYaxis().SetNdivisions(3, 0, 0)
        self._histogram_ndf[-1].GetXaxis().SetNdivisions(16, 0, 0)
        self._histogram_ndf[-1].GetYaxis().SetNdivisions(3, 0, 0)

        # Make ticks cross whole grid
        #self._histogram_sigma[-1].GetXaxis().SetTickLength(1.)
        #self._histogram_sigma[-1].GetYaxis().SetTickLength(1.)

