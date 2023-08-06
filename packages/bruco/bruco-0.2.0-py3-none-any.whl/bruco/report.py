# Brute force coherence (Gabriele Vajente, 2022-02-08)

import numpy
import os
import pickle
import gpstime
import sys
import time

from . import __version__, __date__
from .functions import *
from .html import markup

def collect_results(results, opt):
    """
    Collect all the results in single tables.

    Parameters
    ----------
    results: list
        list of results as returned by the multiprocessing computations
    opt: dict
        parsed command line arguments

    Returns
    -------
    cohtab: numpy.array
        table of all coherences, for all processes
    idxtab: numpy.array
        and table of corresponding channel indexes
    modstab: n umpy.array
        and table of corresponding modulation channel indexes
    """

    # first step, concatenate the tables
    x = list(zip(*results))
    cohtab = numpy.concatenate(x[0], axis=1)
    idxtab = numpy.concatenate(x[1], axis=1)
    modtab = numpy.concatenate(x[2], axis=1)

    # save timing info
    timing = x[4]
    with open(opt['dir'] + '/timing.pickle', 'wb') as timingfile:
        pickle.dump(timing, timingfile)

    # list of channels with errors
    errchannellist = numpy.concatenate(x[5],axis=0)
    numpy.savetxt(opt['dir']+'/channels_error.txt', errchannellist, fmt='%s')

    # then sort in order of descending coherence for each bin
    for j in numpy.arange(cohtab.shape[0]):
        ccoh = cohtab[j,:]
        iidx = idxtab[j,:]
        mmod = modtab[j,:]
        ii = ccoh.argsort()
        cohtab[j, :] = cohtab[j, ii]
        idxtab[j, :] = idxtab[j, ii]
        modtab[j, :] = modtab[j, ii] 
    # Finally, keep only the top values, which are the last columns
    cohtab = cohtab[:,-opt['ntop']:]
    idxtab = idxtab[:,-opt['ntop']:]
    modtab = modtab[:,-opt['ntop']:]
    # save the coherence tables to files
    numpy.savetxt(opt['dir'] + '/cohtab.txt', cohtab)
    numpy.savetxt(opt['dir'] + '/idxtab.txt', idxtab)
    numpy.savetxt(opt['dir'] + '/modtab.txt', modtab)

    return cohtab, idxtab, modtab

def generate_report(opt, cohtab, idxtab, modtab, channels, modulations):
    """
    Generate the HTML report page.

    Parameters
    ----------
    opt: dict
        parsed command line arguments
    cohtab: numpy.array
        table of all coherences, for all processes
    idxtab: numpy.array
        and table of corresponding channel indexes
    modtab: numpy.array
        and table of corresponding modulation indexes
    channels: list of str
        list of all channels
    modulations: list of str
        list of modulation names
    """

    dt = {'report': -time.time(), 'data': 0, 'decim':0, 'fft':0, 'plot':0, 'tot':0}

    print(">>>>> Generating report....")

    # get list of files, since they corresponds to the list of plots that have been created
    files = [f.split('.')[0] for f in os.listdir(opt['dir'])]

    # open web page
    page = markup.page( )
    page.init( title="Brute force Coherences",
               footer="(2022) <a href=mailto:vajente@caltech.edu>vajente@caltech.edu</a>" )
    page.h1('Top %d coherences of %s with auxiliary channels' % (opt['wtop'], opt['channel']))
    page.h2('GPS %d + %d s [%s]' % (opt['gpsb'], opt['dt'],
                  gpstime.tconvert(opt['gpsb'], form='%Y-%m-%d %H:%M:%S %Z')))

    # first section, top channels per frequency bin
    nf,nt = cohtab.shape
    freq  = numpy.linspace(0,opt['outfs']/2,nf)

    ## Write the main coherence table
    page.table(border=1, style='font-size:12px')
    page.tr()
    page.td(bgcolor="#5dadf1")
    page.h3('Frequency [Hz]')
    page.td.close()
    page.td(colspan=opt['ntop'], bgcolor="#5dadf1")
    page.h3('Top channels')
    page.td.close()
    page.tr.close()

    # here we create a huge table that contains, for each frequency bin, the list of most 
    # coherent channels, in descending order. The cell background color is coded from white 
    # (no coherence) to red (coherence 1)
    for i in range(nf):
        page.tr()
        page.td(bgcolor="#5dadf1")
        page.add("%.2f" % freq[i])
        page.td.close()
        for j in range(opt['wtop']):
            # write the channel only if the coherence in above the significance level
            if cohtab[i,-(j+1)] > opt['s']:
                page.td(bgcolor=cohe_color(cohtab[i,-(j+1)]))
                ch = (channels[int(idxtab[i,-(j+1)])]).split(':')[1]
                if modulations[int(modtab[i,-(j+1)])] != 'No modulation':
                    chm = ch  + ' * ' + modulations[int(modtab[i,-(j+1)])]
                else:
                    chm = ch
                if opt['plotformat'] != "none":
                    page.add("<a target=_blank href=%s.%s>%s</a><br>(%.2f)"
                             % (ch, opt['plotformat'], newline_name(chm), cohtab[i,-(j+1)]))
                else:
                    page.add("%s<br>(%.2f)" % (newline_name(chm), cohtab[i,-(j+1)]))
            else:
                page.td(bgcolor=cohe_color(0))
            page.td.close()
        page.tr.close()
    page.table.close()

    ## second section, links to all coherence plots
    if len(files)>0:
        page.h1('Coherence with all channels ')
        page.h2('GPS %d [%s] + %d s' % (opt['gpsb'],
                   gpstime.tconvert(opt['gpsb'], form='%Y-%m-%d %H:%M:%S %Z'), opt['dt']))

        N = len(files)
        m = 6     # number of channels per row
        M = int(N / m + 1)

        page.table(border=1)
        for i in range(M):
            page.tr()
            for j in range(m):
                if i*m+j < N:
                    page.td()
                    page.add('<a target=_blank href=%s.%s>%s</a>' % \
                                  (files[i*m+j], opt['plotformat'], files[i*m+j]))
                    page.td.close()
                else:
                    page.td()
                    page.td.close()
            page.tr.close()
        page.table.close()
        page.br()

    page.h2('Excluded channels:')
    page.code('  '.join(opt['excluded']))

    # Command call for reference
    page.h2('BruCo call string')
    page.code(' '.join(sys.argv))
    page.p()

    # That's the end, save the HTML page
    with open(opt['dir']  + '/index.html', 'w') as fileid:
        print(page, file=fileid)

    # timing info
    dt['report'] = dt['report'] + time.time()
    timing = pickle.load(open(opt['dir'] + '/timing.pickle', 'rb'))
    for t in timing:
        for k in t.keys():
            dt[k] += t[k]
    label = {'data':'Read data','decim':'Resampling','fft':'FFT','plot':'Plotting','tot':'Total', 'report':'Write report'}
    print()
    print('Task           Time  Time/nproc  Percent')
    print('----------------------------------------')
    for k in dt.keys():
        if k == 'report':
            print('%-12s          %6d' % (label[k], dt[k] ))
        elif k != 'tot':
            print('%-12s %6d   %6d      %3d' % (label[k], dt[k], dt[k]/opt['ncpu'], 100*dt[k]/dt['tot']))
    print('%-12s %6d   %6d' % (label['tot'], dt['tot'], dt['tot']/opt['ncpu']))

