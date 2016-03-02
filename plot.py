#!/usr/bin/env python2

""" Plot TGraphs from measurement before and after integrating. """

from SCurve import SCurve


if __name__ == '__main__':
    PRE1 = SCurve('../MAPSA_Software/plots01_nominal/backup_preCalibration__MPA2.root')
    PRE1.set_graphs([1,2,3])
    PRE1.set_directory('.')
    PRE1.set_rootfile('output.root')
    PRE1.set_name('output')
    PRE1.make_s_curve()
