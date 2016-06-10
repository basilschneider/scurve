#!/usr/bin/env python2

""" Plot TGraphs from measurement before and after integrating. """

from SCurve import SCurve
from ROOT import gROOT


if __name__ == '__main__':

    gROOT.SetBatch(True)

    for mpa in range(0, 6):
        for idx, prefix in enumerate(['pre', 'post']):

            print 'Processing MPA {} {}'.format(mpa, prefix)

            path = '../MAPSA_Software/plots19_cable_rutgers'
            scurve = SCurve('{}/backup_{}Calibration__MPA{}.root'
                            .format(path, prefix, mpa))
            output = 'output27_cable_rutgers_03'
            name = '{}_{}'.format(mpa, prefix)

            scurve.set_directory('{}/{}'.format(output, name))
            scurve.set_rootfile('{}/out.root'.format(output, name))

            pixels = 48
            # All individual pixels
            for pixel in range(0, pixels):
                scurve.set_graphs([pixel])
                scurve.retrieve_graphs()
                scurve.make_s_curve()
                scurve.fit_gaussian()

            # All pixels together
            #l = range(1, 15)
            #l.extend(range(17, 31))
            #l.extend(range(33, 47))
            l = range(0, pixels)
            scurve.set_graphs(l)
            scurve.retrieve_graphs()
            scurve.make_s_curve()
            scurve.fit_gaussian()
            scurve.make_maps(mpa, idx)
