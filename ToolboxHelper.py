#!/usr/bin/env python2

""" Toolbox helper functions. """

from os.path import isfile
from inspect import getsourcelines
from collections import defaultdict
from ROOT import TFile  # pylint: disable=import-error
from Logger import LGR


def check_if_list(lst, length_min=-1, length_max=-1):

    """ Check if user passed a list and if meets the requirements of
    minimum and maximum lengths. """

    # Check if it is a list
    check_if_object(lst, list)
    # Check for the minimum length of the list
    if length_min > -1 and len(lst) < length_min:
        raise TypeError('The argument {} does not meet the minimum length '
                        'requirement of {}.'.format(lst, length_min))
    # Check for the maximum length of the list
    if length_max > -1 and len(lst) > length_max:
        raise TypeError('The argument {} does not meet the maximum length '
                        'requirement of {}.'.format(lst, length_max))
    return True


def check_if_file_exists(path_file):

    """ Check if file exists on file system or on eos. """

    # if path_file starts with root://, we have to look on eos
    if path_file.startswith('root://'):
        LGR.info('File seems to reside on eos. I will not check its '
                 'presence. Further errors might be due to non-'
                 'existing file.')
    elif not isfile(path_file):
        raise IOError('The file {} does not exist.'.format(path_file))
    return True


def check_if_tree_exists(path_file, path_tree):

    """ Check if TTree exists in TFile. """

    file_in = TFile(path_file)
    # pyROOT does not allow try/except, so make it in a non pythonic way
    if not file_in.Get(path_tree):
        raise ValueError('TTree {} does not exist in {}.'
                         .format(path_tree, path_file))
    del file_in


def check_if_object(obj, obj_type):

    """ Check if obj is of type obj_type. """

    if not isinstance(obj, obj_type):
        raise TypeError('The object {} is not of type {}.'
                        .format(obj, obj_type.__name__))
    return True


def get_lst_entry_default(lst, entry, default=0):

    """ Returns lst[entry] if it exists, otherwise default value. """

    try:
        return lst[entry]
    except IndexError:
        return default

def inspect_function(fnctn):

    """ Returns definition of function. Good for inspection. """

    for line in getsourcelines(fnctn)[0]:
        print line.rstrip()

def safe_divide(num, den, default=0):

    """ Divide num by den; if den = 0, return default. """

    try:
        return num/den
    except ZeroDivisionError:
        return default

def tree():

    """ Get tree data structure, i.e. a dictionary with default value being
    again a dictionary. Every node is either another defaultdict or a
    value. Example:
    t = tree_inf()
    t[0] = 3  # OK
    t[1][2] = 4  # OK
    t[0][1] = 5  # Error, t[0] is already defined as value

    If you need a fixed depth, use something like
    defaultdict(lambda : defaultdict(dict))

    See also
    http://stackoverflow.com/a/12260480/1945981
    http://stackoverflow.com/a/652226/1945981
    """

    return defaultdict(tree)

def get_lo_edge(axis):

    """ Return lower edge of TAxis. """

    return axis.GetBinLowEdge(axis.GetFirst())

def get_hi_edge(axis):

    """ Return higher edge of TAxis. """

    return axis.GetBinUpEdge(axis.GetLast())

def get_dir_name(string, delimiter='/'):

    """ Removes substring from string after last occurence of delimiter, e.g.
    /path/to/file --> /path/to """

    return delimiter.join(string.split(delimiter)[:-1])
