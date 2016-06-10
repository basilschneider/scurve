#!/usr/bin/env python2

"""
Author: Basil Schneider <basil.schneider@cern.ch>
Data class to store Gaussian fit values.
"""

from Logger import LGR

class ToolboxFit(object):

    """ Data class to store Gaussian fit values. """

    def __init__(self, fit=None, numbering=None):

        """ Initialize class variables. """

        # Overloaded constructor, both fit and numbering need to be given,
        # or neither of them
        if fit is not None and numbering is not None:
            self._numbering = numbering
            self._constant = fit.GetParameter(0)
            self._constant_error = fit.GetParError(0)
            self._mu = fit.GetParameter(1)
            self._mu_error = fit.GetParError(1)
            self._sigma = fit.GetParameter(2)
            self._sigma_error = fit.GetParError(2)
            self._chi2 = fit.GetChisquare()
            self._ndf = fit.GetNDF()
        elif fit is None and numbering is None:
            self._numbering = -1
            self._constant = 0.
            self._constant_error = 0.
            self._mu = 0.
            self._mu_error = 0.
            self._sigma = 0.
            self._sigma_error = 0.
            self._chi2 = 0.
            self._ndf = 0.
        else:
            raise RuntimeError('An instance of ToolboxFit was created without '
                               'either defining both numbering and fit or '
                               'defining neither of them.')

    def get_numbering(self):

        """ Return numbering of fit, which can be used to locate it e.g. in a
        2d map. """

        return self._numbering

    def get_c(self):

        """ Return constant. """

        return self._constant

    def get_c_err(self):

        """ Return error on constant. """

        return self._constant_error

    def get_mu(self):

        """ Return mu. """

        return self._mu

    def get_mu_err(self):

        """ Return error on mu. """

        return self._mu_error

    def get_sigma(self):

        """ Return sigma. """

        return self._sigma

    def get_sigma_err(self):

        """ Return error on sigma. """

        return self._sigma_error

    def get_chi2(self):

        """ Return chi square. """

        return self._chi2

    def get_ndf(self):

        """ Return number of degrees of freedom for chi square fit. """

        return self._ndf
