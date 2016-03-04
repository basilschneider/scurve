#!/usr/bin/env python2

""" Plot TGraphs from measurement before and after integrating. """

from SCurve import SCurve


if __name__ == '__main__':

    for mpa in range(0, 6):
        for prefix in ['pre', 'post']:

            print 'Processing MPA {} {}'.format(mpa, prefix)

            path = '../MAPSA_Software/plots01_nominal/'
            scurve = SCurve('{}/backup_{}Calibration__MPA{}.root'
                            .format(path, prefix, mpa))
            scurve.set_graphs(range(0, 48))
            output = 'output01_implementation'
            name = '{}_{}'.format(mpa, prefix)

            scurve.set_directory('{}/{}'.format(output, name))
            scurve.set_rootfile('{}/{}.root'.format(output, name))

            scurve.make_s_curve()
