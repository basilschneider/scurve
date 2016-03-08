#!/usr/bin/env python2

""" Plot TGraphs from measurement before and after integrating. """

from SCurve import SCurve


if __name__ == '__main__':

    for mpa in range(0, 1):
        for prefix in ['pre']:
        #for prefix in ['pre', 'post']:

            print 'Processing MPA {} {}'.format(mpa, prefix)

            path = '../MAPSA_Software/plots01_nominal/'
            scurve = SCurve('{}/backup_{}Calibration__MPA{}.root'
                            .format(path, prefix, mpa))
            output = 'output03_maps'
            name = '{}_{}'.format(mpa, prefix)

            scurve.set_directory('{}/{}'.format(output, name))
            scurve.set_rootfile('{}/{}.root'.format(output, name))

            pixels = 4
            # All individual pixels
            for pixel in range(0, pixels):
                scurve.set_graphs([pixel])
                scurve.retrieve_graphs()
                scurve.make_s_curve()
                scurve.fit_gaussian()

            # All pixels together
            scurve.set_graphs(range(0, pixels))
            scurve.retrieve_graphs()
            scurve.make_s_curve()
            scurve.fit_gaussian()
            scurve.make_maps()
