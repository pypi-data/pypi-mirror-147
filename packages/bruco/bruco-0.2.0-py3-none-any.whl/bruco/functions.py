# Brute force coherence (Gabriele Vajente, 2022-02-08)
# Auxiliary functions

import numpy
import scipy.signal
import fnmatch
import os
from gwpy.timeseries import TimeSeries

from .ligodata import *

def computeFFTs(x, npoints, noverlap, fs):
    """
    Compute the windowed FFTs of the channel x, each with npoints and overlapped by noverlap.

    Parameters
    ----------
    x: numpy.array
        channel time series
    npoints: int
        number of points used for each FFT
    noverlap: int
        number of points of overlap between FFTs
    fs: int
        channel sampling frequency

    Returns
    -------
    segs: numpy.array
        array of FFTs, normalized to gte PSD units when squared
    """

    # compute the starting indexes of all segments
    npoints = int(npoints)
    noverlap = int(noverlap)
    step = npoints - noverlap
    ind = numpy.arange(0, len(x) - npoints + 1, step, dtype=int)
    nsegs = len(ind)

    # pre-compute window
    wind = numpy.hanning(npoints)

    # pre-allocate output data
    segs = numpy.zeros((int(npoints/2+1), nsegs), dtype=numpy.cfloat)

    # compute all FFTs
    for i in range(nsegs):
        segs[:,i] = numpy.fft.rfft( scipy.signal.detrend(x[ind[i]:ind[i]+npoints], type='linear') * wind)

    # normalization to get PSD with |fft|^2
    segs = segs * numpy.sqrt(2.0/fs / numpy.sum(wind**2))

    # that's all
    return segs

def cohe_color(c):
    """
    Return an hex color code depending continuosly on input: 1 = red, 0 = white

    Parameters
    ----------
    c: float
        the input value between 0 and 1

    Returns
    -------
    color: str
        a hex color code varying between white and red
    """

    if c == 0:
        return '#ffffff'
    else:
        if c == 1:
            return '#ff0000'
        else:
            s = hex(int((1.0 - c) * 256)).split('x')[1]
            if len(s) == 1:
                s = '0' + s
            return '#ff' + s + s

def newline_name(s):
    """
    Split a channel name in multiple lines if it's too long.

    Parameters
    ----------
    s: str
        the channel name
    
    Returns
    -------
    s: str
        the same name, with inserted new lines
    """

    if len(s) > 10:
        N = int(len(s)/10)
        idx = []
        for i in range(N):
            try:
                idx.append(s.index('_', 10*(i+1)))
            except:
                pass
        if len(idx) !=0:
            idx  = numpy.unique(idx)
            newstr = ''
            for i in range(len(idx)):
                if i == 0:
                    newstr = s[0:idx[0]]
                else:
                    newstr = newstr + "<br>" + s[idx[i-1]:idx[i]]
            newstr = newstr + '<br>' + s[idx[-1]:]
            return newstr
        else:
            return s
    else:
        return s

def enc(x):
    """
    Some newer versions of matplotlib throw an error when labels have a '_'. So here I replace them with a blank.
    """
    return x.replace('_', ' ')

def select_channels(opt, channels, sample_rates):
    """
    Select only channels with high enough sampling rate and not in the exclusion list.

    Parameters
    ----------
    opt: dict
        parsed command line options
    channels: numpy.array of str
        list of all channels
    sample_rates: numpy.array of int
        list of corresponding sampling rates

    Returns
    -------
    channels: numpy.array of str
        the list of good channels
    sample_rates: numpy.array of int
        the list of corresponding sampling rates
    """

    # remove channels with low sampling rate
    idx = numpy.where(sample_rates >= opt['minfs'])[0]
    channels = channels[idx]
    sample_rates = sample_rates[idx]

    if opt['excluded'] != '':
        # load exclusion list from file
        with open(opt['excluded'], 'r') as f:
            L = f.readlines()
            excluded = []
            for c in L:
                c = c.split()
                if len(c):
                    excluded.append(c[0])
        opt['excluded'] = excluded
    
        # delete excluded channels, allowing for unix-shell-like wildcards
        idx = numpy.ones(channels.shape, dtype='bool')
        for i,c in enumerate(channels):
            if c == opt['ifo'] + ':' + opt['channel']:
                # remove the main channel
                idx[i] = False
            for e in excluded:
                if fnmatch.fnmatch(c, opt['ifo'] + ':' + e):
                    idx[i] = False

        channels = channels[idx]
        sample_rates = sample_rates[idx]

    # keep only channels that match the wildcards selection, if provided
    if opt['select'] != '':
        opt['select'] = opt['ifo'] + ':' + opt['select']
        print('Selecting only channels matching ' + opt['select'])
        idx = numpy.zeros(channels.shape, dtype='bool')
        for i,c in enumerate(channels):
            if fnmatch.fnmatch(c, opt['select']):
                idx[i] = True
        channels = channels[idx]
        sample_rates = sample_rates[idx]

    # remove repeated channels
    channels = numpy.unique(channels)

    # save the channel list to a file in the output directory
    os.makedirs(opt['dir'], exist_ok=True)
    with open(opt['dir'] + '/channels.txt', 'w') as fid:
        for c in channels:
            fid.write('%s\n' % c)
    opt['nch'] = channels.shape[0]

    print('Found %d auxiliary channels\n' % opt['nch'])

    return channels

def read_target_data(opt):
    """
    Read the target channel data.

    Parameters
    ----------
    opt: dict
        parsed command line arguments

    Returns
    -------
    ch1: numpy.array
        an array containing the channel data
    fs1: int
        channel sampling frequency
    """

    ## Read main channel data
    if opt['file'] == '':
        # read the main channel from frame data
        if opt['target_source'] == 'getTargetData':
            # no source specified, let gwpy find the data
            print('Reading target channel %s with gwpy' % (opt['ifo'] + ':' + opt['channel']))
            ch1, fs1 = getTargetData(opt['ifo'] + ':' + opt['channel'], opt['gpsb'], opt['gpse'])
        else:
            # read from the provided file list
            print('Reading target channel %s from files:' % (opt['ifo'] + ':' + opt['channel']))
            print('\n'.join(['    ' + t for t in opt['target_source']]))
            data = TimeSeries.read(opt['target_source'], opt['ifo'] + ':' + opt['channel'], 
                                   start=opt['gpsb'], end=opt['gpse'])
            ch1 = data.value
            fs1 = int(data.sample_rate.value)
    else:
        # the user provided a filename, read data from there
        print('Reading target channel %s from %s' % (opt['ifo'] + ':' + opt['channel'], opt['file']))
        extension = opt['file'].split('.')[-1]
        if extension == 'txt':
            ch1 = numpy.loadtxt(opt.file)
            fs1 = int(len(ch1)/(gpse-gpsb))
        elif extension == "gwf":
            x = TimeSeries.read(opt['file'], opt['ifo'] + ':' + opt['channel'], start=opt['gpsb'], end=opt['gpse'])
            ch1 = x.value
            fs1 = int(x.sample_rate.value)
        elif extension == 'pickle':
            import pickle
            x = pickle.load(open(opt['file'], 'rb'))
            ch1 = x[opt.channel]
            fs1 = int(len(ch1)/(gpse-gpsb))
        else:
            print('Error: file format not recognized for ' + opt['file'] +'. Must be txt, gwf or pickle')
            exit()
        print("    Read %d samples > sampling rate is %d" % (len(ch1), fs1))

    return ch1, fs1

def ifo_prefix(channels, ifo):
    """
    Make sure that the channels in the list start with the IFO prefix

    Parameters
    ----------
    channels: list of str
        list of channel names
    ifo: str
        IFO prefix ('H1' or 'L1')

    Returns
    -------
    channels: list of str
        list of channel names, all starting with the IFO prefix
    """
    new_channels = []
    for c in channels:
        if c[0:2] == ifo:
            new_channels.append(c)
        else:
            new_channels.append(ifo + ':' + c)
    return new_channels

