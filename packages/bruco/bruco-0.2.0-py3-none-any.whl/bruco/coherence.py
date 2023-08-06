# Brute force coherence (Gabriele Vajente, 2022-02-08)

import numpy
import scipy.signal
import pylab
import matplotlib
import time
matplotlib.use("Agg")

from scipy.signal import resample_poly, resample, detrend

from .functions import *

def parallelized_coherence(args):
    """
    Compute the coherence of a subset of auxiliary channels with the target channel,
    and produce the coherence plots.

    Parameters
    ----------
    args: list
        a list of arguments, containing:
        opt: dict
            dictionary of command line arguments
        ch1_ffts: numpy.array
            precomputed FFTs of the target channel (ch1)
        f1: numpy.array
            corresponding frequency bins
        psd1: numpy.array
            averaged PSD of the target channel
        c: list of str
            list of channel names
        id: int
            process id number
        chidx: int
            channel index corresponding to the first in the list
        mod_channels: numpy.array
            resampled modulation channels
        modulations: list of str
            and corresponding channel names  
 
    Returns
    -------
    cohtab: numpy.array
        table of coherence values
    idxtab: numpy.array
        table of channel index values
    modtab: numpy.array
        table of modulation index values
    id: int
        process id number
    dt: dict
        timing information
    errchannels: list of str
        list fo the channels that had errors
    """

    # parse input arguments
    opt, ch1_ffts, f1, psd1, channels, id, chidx, mod_channels, modulations = args
    print("Called parallelized_coherence(), process %d" % id)

    # import locally the plotly library if needed and possible
    if opt['plotformat'] == 'html':
        try:
            from plotly.subplots import make_subplots
            import plotly.express as px
            import plotly.graph_objects as go
        except:
            try:
                import plotly
                print("WARNING: Your plotly version (" + plotly.__version__ + ") is too old, you need version 5.2.1 or later.")
            except:
                print("WARNING: You need the plotly library version 5.2.1 or later.")
            print("         Interactive plots disabled, saving plots in PNG format.")
            opt.plotformat = 'png'

    # dictionary to store timing information
    dt = {'data': 0, 'decim': 0, 'fft': 0, 'plot': 0, 'tot': 0}
    dt['tot'] = -time.time()

    # init tables
    cohtab = numpy.zeros((int(opt['npoints']/2+1), opt['ntop']))
    idxtab = numpy.zeros((int(opt['npoints']/2+1), opt['ntop']), dtype=int)
    modtab = numpy.zeros((int(opt['npoints']/2+1), opt['ntop']), dtype=int)
    # initialize empty list for the channels with errors
    errchannels = []

    # we might need multiple sampling frequencies for the modulation channels, so
    # we store them in a dictiornary once we need to compute them
    mod_channels = {opt['outfs']: mod_channels}

    # initialize figure and plot
    dt['plot'] = dt['plot'] - time.time()
    if opt['plotformat'] != 'none' and opt['plotformat'] != 'html':
        fig, ax = pylab.subplots(2, 1, sharex=True, figsize=(10,10))
        firstplot = True
    if opt['plotformat'] != 'none':
        # calibrated PSD of target channel, for plotting
        psd_plot = numpy.sqrt(psd1) * opt['calib']
    dt['plot'] = dt['plot'] + time.time()

    # analyze every channel in the list, reading them in batches to speed-up data IO
    nchannels = len(channels)
    channels_id = numpy.arange(nchannels)
    # divide in batches
    channels    = [channels[i:i+opt['aux_num_read']] for i in range(0, nchannels, opt['aux_num_read'])]
    channels_id = [channels_id[i:i+opt['aux_num_read']] for i in range(0, nchannels, opt['aux_num_read'])]
    # count progress
    count = 0

    for channels_subset, channels_id_subset in zip(channels, channels_id):
        # read all channels in this subset
        dt['data'] = dt['data'] - time.time()
        print("  Process %d: reading\n        %s" % (id, '\n        '.join(channels_subset)))
        data, sampling_rates = getRawData(channels_subset, opt['gpsb'], opt['gpse'], opt['aux_source'])
        dt['data'] = dt['data'] + time.time()

        # loop over all the channels we just got
        for i,channel2 in zip(channels_id_subset, channels_subset):
            count = count + 1
            print("  Process %d: channel %d of %d: %s" % \
                     (id, count, nchannels, channel2))
            ch2 = data[channel2]
            fs2 = sampling_rates[channel2]
            # check if the channel is flat, and skip it if so
            if ch2.min() == ch2.max():
                print("  Process %d: %s is flat, skipping" % (id, channel2))
                continue

            # resample to outfs if needed
            dt['decim'] = dt['decim'] - time.time()
            if fs2 > opt['outfs']:
                if fs2 % opt['outfs'] == 0:
                    ch2 = resample_poly(ch2, up=1, down=int(numpy.round(fs2) / opt['outfs']))
                else:
                    ch2 = resample(ch2, opt['outfs'], numpy.round(fs2))
                fs2 = opt['outfs']
            elif fs2 < opt['outfs']:
                # when the sampling frequency of the channel is smaller than outfs
                # we need to resample the modulation channels
                if fs2 not in list(mod_channels.keys()):
                    mod_channels[fs2] = resample_poly(mod_channels[opt['outfs']], axis=1, 
                                              up=1, down=int(opt['outfs']//fs2))
            dt['decim'] = dt['decim'] + time.time()

            ch2 = detrend(ch2)

            ## loop over all modulations, and keep all computed coherences
            C = []
            for k,modul in enumerate(modulations):
                # compute coherence
                dt['fft'] = dt['fft'] - time.time()
                # compute all the FFTs of the aux channel (those FFTs are returned already 
                # normalized so that the PSD is just sum |FFT|^2)
                # we use a number of points so that the frequency binning is the same as the
                # target channel FFTs
                ch2_ffts = computeFFTs(ch2*mod_channels[fs2][k,:], int(opt['npoints']*fs2/opt['outfs']), 
                                        int(opt['npoints']*fs2/opt['outfs']/2), fs2)
                # average to get PSDs and CSDs, create frequency vector
                psd2 = numpy.mean(abs(ch2_ffts)**2, axis=1)
                f = numpy.linspace(0, int(fs2/2), int(opt['npoints']*fs2/opt['outfs']/2+1))
                csd12 = numpy.mean(numpy.conjugate(ch2_ffts)*\
                               ch1_ffts[0:int(opt['npoints']*fs2/opt['outfs']/2+1),:], axis=1)
                # we use the full sampling PSD of the main channel, using only the bins 
                # corresponding to channel2 frequency bins
                c = numpy.abs(csd12)**2/(psd2 * psd1[0:len(psd2)])
                # mask frequencies above Nyquist
                c[f > fs2/2] = 0
                # save coherecne to list
                C.append(c)
                dt['fft'] = dt['fft'] + time.time()

                # save coherence in summary table. Basically, cohtab has a row for each frequency 
                # bin and a number of columns which is determined by the option --top. For each 
                # frequency bin, the new coherence value is added only if it's larger than the 
                # minimum already present. Then idxtab contains again a row for each frequency
                # bin: but in this case each entry is an unique index that determines the channel 
                # that gave that coherence. Finally modtab contains the corresponding modulation
                # channel index, if modulations are present. Modulation index 0 means no modulation.
                # So for example cohtab[100,0] gives the highest coherence for the 100th frequency 
                # bin; idxtab[100,0] contains an integer id that corresponds to the channel. This 
                # id is saved in channels.txt. modtab[100,0] contains the corresponging modulation
                # channel index.
                for j,cx in enumerate(c):
                    top = cohtab[j, :]
                    idx = idxtab[j, :]
                    mod = modtab[j, :]
                    # if the coherence of this channel at this frequency is higher than the smaller
                    # on record, then we add it and keep only the highest values and channels
                    if cx > top.min():
                        ttop = numpy.concatenate((top, [cx]))         # new coherence value
                        iidx = numpy.concatenate((idx, [chidx + i]))  # and corresponding new channel
                        mmod = numpy.concatenate((mod, [k]))          # and modulation channel
                        ii = ttop.argsort()
                        ii = ii[1:]
                        cohtab[j, :] = ttop[ii]
                        idxtab[j, :] = iidx[ii]
                        modtab[j, :] = mmod[ii]

            # create the output plot, if desired, and with the desired format
            dt['plot'] = dt['plot'] - time.time()
            if opt['plotformat'] != "none" and opt['plotformat'] != 'html':
                ## Use matplotlib for png or pdf static plot

                mask = numpy.ones_like(f)
                mask[c < opt['s']] = numpy.nan
                # faster plotting, create all the figure and axis stuff once for all,
                # at the beginning, the just upadte the traces and texts
                if firstplot:
                    pltitle = ax[0].set_title('Coherence %s vs %s - GPS %d' % \
                                        (enc(opt['channel']), enc(channel2), opt['gpsb']), \
                                         fontsize='smaller')
                    # make a list of non-repeating colors and line styles
                    colors = list(matplotlib.colors.TABLEAU_COLORS) + list(matplotlib.colors.BASE_COLORS)[:-2]
                    line_styles = ['-']*len(colors) + [':']*len(colors)
                    line_colors = colors + colors
                    line1 = {}
                    line4 = {}
                    line3, = ax[1].loglog(f1, psd_plot[0:len(f1)], color='k', alpha=1, label='Target')
                    for k,m in enumerate(modulations):
                        if len(modulations) > 1:
                            line1[k], = ax[0].loglog(f, C[k], label=m, alpha=1, linestyle=line_styles[k], color=line_colors[k])
                        else:
                            line1[k], = ax[0].loglog(f, C[k], label='Coherence', alpha=1, linestyle=line_styles[k], color=line_colors[k])
                        mask = numpy.ones_like(f)
                        mask[C[k]<opt['s']] = numpy.nan
                        if len(modulations) > 1:
                            line4[k], = ax[1].loglog(f, psd_plot[0:len(psd2)] * numpy.sqrt(C[k]) * mask, label=m, alpha=1,
                                                                         linestyle=line_styles[k], color=line_colors[k])
                        else:
                            line4[k], = ax[1].loglog(f, psd_plot[0:len(psd2)] * numpy.sqrt(C[k]) * mask, label='Projection', alpha=1,
                                                                         linestyle=line_styles[k], color=line_colors[k])
                    line2, = ax[0].loglog(f, numpy.ones_like(f)*opt['s'], 'r--', linewidth=1)
                    if opt['xmin'] != -1:
                        ax[0].axis(xmin=opt['xmin'], xmax=opt['xmax'])
                        ax[1].axis(xmin=opt['xmin'], xmax=opt['xmax'])
                    else:
                        ax[0].axis(xmax=opt['outfs']/2)
                    ax[0].axis(ymin=opt['s']/2, ymax=1)
                    ax[0].grid(True, alpha=0.5, linestyle=':')
                    ax[0].set_ylabel('Coherence')

                    if opt['ymin'] != -1:
                        ax[1].axis(ymin=opt['ymin'], ymax=opt['ymax'])
                    ax[1].set_xlabel('Frequency [Hz]')
                    ax[1].set_ylabel('Spectrum')
                    ax[1].legend(('Target channel', 'Noise projection'))
                    ax[1].grid(True, alpha=0.5, linestyle=':')
                    pylab.subplots_adjust(bottom=0.1, left=0.05, right=0.75, top=0.85, hspace=0.15)
                    firstplot = False
                else:
                    # if not the first plot, just update the traces and title
                    pltitle.set_text('Coherence %s vs %s - GPS %d' % (enc(opt['channel']), enc(channel2), opt['gpsb']))
                    for k,m in enumerate(modulations):
                        line1[k].set_data(f, C[k])
                        mask = numpy.ones_like(f)
                        mask[C[k]<opt['s']] = numpy.nan
                        line4[k].set_data(f, psd_plot[0:len(psd2)] * numpy.sqrt(C[k]) * mask)
                # add legends
                if len(modulations) > 1:
                    ax[0].legend(fontsize=8, title='Modulation', bbox_to_anchor=(1.05, 1.0), loc='upper left')
                    ax[1].legend(fontsize=8, title='Modulation', bbox_to_anchor=(1.05, 1.0), loc='upper left')
                else:
                    ax[1].legend(fontsize=8, bbox_to_anchor=(1.05, 1.0), loc='upper left')
                pylab.tight_layout()

                # save figure to file
                fig.savefig(opt['dir'] + '/%s.%s' % (channel2.split(':')[1], opt['plotformat']), format=opt['plotformat'])
            elif opt['plotformat'] == 'html':
                ## use plotly for interactive HTML plot

                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

                for k,m in enumerate(modulations):
                    if len(modulations) > 1:
                        fig.add_trace(go.Scatter(x=f, y=C[k], mode="lines", name=m,
                                             line_color=px.colors.qualitative.Alphabet[k],
                                             legendgroup=m, hovertemplate='freq: %{x:.2f}<br>coher: %{y:.4f}'), row=1, col=1)
                    else:
                        fig.add_trace(go.Scatter(x=f, y=C[k], mode="lines", name='Coherence',
                                             line_color=px.colors.qualitative.Alphabet[k], 
                                             legendgroup=m, hovertemplate='freq: %{x:.2f}<br>coher: %{y:.4f}'), row=1, col=1)
                    mask = numpy.ones_like(f)
                    mask[C[k]<opt['s']] = numpy.nan
                    if len(modulations) > 1:
                        fig.add_trace(go.Scatter(x=f, y=psd_plot[0:len(psd2)] * numpy.sqrt(C[k]) * mask, mode="lines",
                                                  line_color=px.colors.qualitative.Alphabet[k], name=m,
                                                  legendgroup=m, showlegend=False,
                                                  hovertemplate='freq: %{x:.2f} Hz<br>ASD: %{y:.4f}'), row=2, col=1)
                    else:
                        fig.add_trace(go.Scatter(x=f, y=psd_plot[0:len(psd2)] * numpy.sqrt(C[k]) * mask, mode="lines",
                                                  line_color=px.colors.qualitative.Alphabet[k], name='Projection',
                                                  legendgroup=m, showlegend=False,
                                                  hovertemplate='freq: %{x:.2f} Hz<br>ASD: %{y:.4f}'), row=2, col=1)
                fig.add_trace(go.Scatter(x=f, y=numpy.ones_like(f)*opt['s'], mode="lines", name='Threshold', line_color='red',
                                                       legendgroup='1', line={'dash':'dot'},
                                                  hovertemplate='freq: %{x:.2f} Hz<br>coher: %{y:.4f}'), row=1, col=1)
                fig.add_trace(go.Scatter(x=f, y=psd_plot[0:len(f1)], mode="lines", name='Target signal',
                                                       legendgroup='2', line_color='black',
                                                  hovertemplate='freq: %{x:.2f} Hz<br>ASD: %{y:.4f}'), row=2, col=1)

                fig.update_xaxes(type="log")
                fig.update_yaxes(type="log", exponentformat='power')
                fig.update_layout(title='Coherence %s vs %s - GPS %d' % (enc(opt['channel']), enc(channel2), opt['gpsb']))
                fig.update_layout(legend_tracegroupgap=5, template='plotly')
                fig.update_xaxes(title_text='Frequency [Hz]', row=2, col=1)
                fig.update_yaxes(title_text='Coherence', row=1, col=1)
                fig.update_yaxes(title_text='Spectrum', row=2, col=1)
                fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=10))

                if opt['xmin'] != -1:
                    fig.update_xaxes(range=[numpy.log10(opt['xmin']),numpy.log10(opt['xmax'])])
                else:
                    fig.update_xaxes(range=[-1,numpy.log10(opt['outfs']/2)])
                fig.update_yaxes(range=[numpy.log10(opt['s']/2),0], row=1, col=1)
                if opt['ymin'] != -1:
                    fig.update_yaxes(range=[numpy.log10(opt['ymin']),numpy.log10(opt['ymax'])], row=2, col=1)

                fig.write_html(opt['dir'] + '/%s.%s' % (channel2.split(':')[1], opt['plotformat']), include_plotlyjs='cdn')

            dt['plot'] = dt['plot'] + time.time()
            # do some cleanup of memory
            del ch2, c, f
    # close figure, clean-up
    del fig

    print("  Process %s concluded" % id)
    dt['tot'] = dt['tot'] + time.time()
    return cohtab, idxtab, modtab, id, dt, errchannels


