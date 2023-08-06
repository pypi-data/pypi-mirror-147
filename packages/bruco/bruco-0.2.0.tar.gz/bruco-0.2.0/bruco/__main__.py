# Brute force coherence (Gabriele Vajente, 2022-02-08)

import numpy
import os
import multiprocessing
import pickle

from scipy.signal import resample_poly, resample, detrend
import scipy.stats

from . import __version__, __date__
from .functions import *
from .html import markup
from .parameters import *
from .ligodata import *
from .coherence import *
from .report import *


def bruco():
    """
    Main function, that is called when the module is execued from the command line
    """

    ## parse command line arguments
    opt = parse_arguments()

    print("********************************************************************************")
    print("****                    BruCo version %s (%s)                    ****" % (__version__, __date__))
    print("********************************************************************************")
    print()
    print("Analyzing data from gps %d to %d (%d s)." % (opt['gpsb'], opt['gpse'], opt['dt']))
    print()
 
    ## Find target data source ####################################################################
    if opt['target_source'] != '':
        # get list of files from file
        with open(opt['target_source'], 'r') as fid:
            opt['target_source'] = fid.read().splitlines()
    else:
        # by default we read the target channel with a custom function
        # that is able to identify the correct frame type
        opt['target_source'] = 'getTargetData'

    ## Find auxiliary data source  ################################################################
    if opt['aux_source'] != '':
        # get list of files from file
        with open(opt['aux_source'], 'r') as fid:
            opt['aux_source'] = fid.read().splitlines()
    else:
        # call a function to find raw data on disk
        opt['aux_source'] = find_data_path(opt['ifo'], opt['gpsb'], opt['gpse'])

    ## Read list of channels and keep only relevant channels ######################################
    channels, sample_rates = get_channel_list(opt['aux_source'])
    channels = select_channels(opt, channels, sample_rates)

    ## Read main channel data #####################################################################
    ch1, fs1 = read_target_data(opt)

    # check if the main channel is flat
    if ch1.min() == ch1.max():
        print("Error: main channel %s is flat!" % opt['channel'])
        exit()

    ## Resample to the output sampling frequency
    if opt['outfs'] == -1:
        # use the target channel sampling rate as analysis rate
        opt['outfs'] = fs1
    if fs1 > opt['outfs']:
        if fs1 % opt['outfs'] == 0:
            # the channel sampling rate is a multiple of the analysis rate
            ch1 = resample_poly(ch1, up=1, down=int(numpy.round(fs1) / opt['outfs']))
        else:
            # use a resample function that allows non integer ratios
            ch1 = resample(ch1, opt['outfs'], int(numpy.round(fs1)))
        fs1 = opt['outfs']

    ## Compute main channel FFT ###################################################################

    ## Decide the number of points for each FFT, setting it to the closer power of two
    if opt['fres'] != 0:
        # if the user specified a frequency resolution, try to match it
        npoints = opt['outfs']/opt['fres']
        opt['npoints'] = pow(2, int(numpy.log(npoints)/numpy.log(2)))
    else:
        opt['npoints'] = pow(2, int(numpy.log(2*(opt['gpse'] - opt['gpsb']) * \
                                     opt['outfs'] / opt['nav']) / numpy.log(2)))

    print("\nNumber of points            = %d" % opt['npoints'])
    dtime = opt['npoints']/opt['outfs']
    opt['naver'] = int(2*opt['dt']//dtime - 1)
    opt['fres'] = float(opt['outfs']) / float(opt['npoints'])
    print("Frequency resolution of FFT = %f Hz" % opt['fres'])
    print("Number of averages          = %d\n" % opt['naver'])

    ## Compute the main channels FFTs and PSD. Here I save the single segments FFTS,
    # to reuse them later on in the CSD computation. In this way, the main channel FFTs are
    # computed only once, instead of every iteration. This function returns the FFTs already
    # scaled is such a way that PSD = sum |FFT|^2, in units of 1/sqrt(Hz)
    ch1_ffts = computeFFTs(ch1, opt['npoints'], opt['npoints']//2, fs1)
    # compute the average to get the PSD
    psd1 = numpy.mean(numpy.abs(ch1_ffts)**2,1)
    # and compute the frequency bins
    f1 = numpy.linspace(0, fs1/2, int(opt['npoints']//2+1))

    ## Read the calibration transfer function, if specified
    if opt['calib'] != '':
        # load from file
        cdata = numpy.loadtxt(opt.calib)
        # interpolate to the right frequency bins
        opt['calib'] = numpy.interp(f1, cdata[:,0], cdata[:,1])
    else:
        # no calibration specified, use unity
        opt['calib'] = numpy.ones_like(f1)

    ## Compute the coherence confidence level based on the number of averages used in the PSD
    opt['s'] = scipy.stats.f.ppf(0.95, 2, 2*opt['nav'])
    opt['s'] = opt['s']/(opt['nav'] - 1 + opt['s'])

    ## Read modulation channels if any ############################################################

    if opt['modulations']:
        # read list of modulation channels
        modulations = open(opt['modulations'], 'r').read().splitlines()
        modulations = ifo_prefix(modulations, opt['ifo'])
        print('Reading modulation channels:\n    ' + '\n    '.join(modulations))
        # read data
        mod_data, mod_fs = getRawData(modulations, opt['gpsb'], opt['gpse'], opt['aux_source'])
        # create array of resampled data
        mod_channels = numpy.zeros((len(modulations)+1, (opt['gpse']-opt['gpsb'])*opt['outfs']))
        mod_channels[0,:] = 1   # including constant
        for i,m in enumerate(modulations):
            if mod_fs[m] < opt['outfs']:
                mod_channels[i+1,:] = resample_poly(mod_data[m], up=opt['outfs']//mod_fs[m], down=1)
            elif fs[m] > opt['outfs']:
                mod_channels[i+1,:] = resample_poly(mod_data[m], up=1, down=mod_fs[m]//opt['outfs'])
            else:
                mod_channels[i+1,:] = mod_data[m]
        mod_channels[i,:] = detrend(mod_channels[i,:])
        # add empty string to list of modulation channels, to represent unmodulated channel
        modulations = ['No modulation'] + modulations
    else:
        # there are no modulations
        modulations = ['No modulation']
        mod_channels = numpy.ones((1,(opt['gpse']-opt['gpsb'])*opt['outfs']))

    ## Start the multiprocess coherence computations ##############################################
        
    # split the list of channels in as many sublist as there are CPUs
    if opt['ncpu'] == -1:
        opt['ncpu'] = multiprocessing.cpu_count()

    # try the most even possible distribution of channels among the processes
    nchannels = len(channels)
    n = int(nchannels / opt['ncpu'])
    N1 = int( (nchannels / float(opt['ncpu']) - n) * opt['ncpu'])
    ch2 = []
    chidx = []
    for i in range(N1):
        ch2.append(channels[i*(n+1):(i+1)*(n+1)])
        chidx.append(i*(n+1))
    for i in range(opt['ncpu']-N1):
        ch2.append(channels[N1*(n+1)+i*n:N1*(n+1)+(i+1)*n])
        chidx.append(N1*(n+1)+i*n)

    # start a multiprocessing pool
    print(">>>>> Starting %d parallel processes..." % opt['ncpu'])
    if opt['ncpu'] > 1:
        pool = multiprocessing.Pool(opt['ncpu'])

    # Build the list of arguments
    args = []
    for i,c in enumerate(ch2):
        args.append([opt, ch1_ffts, f1, psd1, c, i, chidx[i], mod_channels, modulations])

    # Start all the processes
    if opt['ncpu'] > 1:
        results = pool.map(parallelized_coherence, args)
    else:
        results = [parallelized_coherence(args[0])]

    # when we get here, all the computations are concluded
    print(">>>>> Parallel processes finished...")

    ## Put all the results together ###############################################################

    cohtab, idxtab, modtab = collect_results(results, opt)

    ## Write the HTML report ######################################################################

    generate_report(opt, cohtab, idxtab, modtab, channels, modulations)


if __name__ == '__main__':
    # execute the main function when called from command line
    bruco()
