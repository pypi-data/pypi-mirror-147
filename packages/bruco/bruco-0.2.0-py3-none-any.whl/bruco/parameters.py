# Brute force coherence (Gabriele Vajente, 2022-02-08)

import argparse
import os
 
from bruco import __version__

def parse_arguments():
    """
    Parse the command line arguments and return the values.

    Returns
    -------
    opt: class
        container for all the parsed parameters
    """

    helpstring = """
    Brute force coherence (Gabriele Vajente, 2022-02-03)
    
    Example:
    python -m bruco --ifo=H1 --channel=CAL-DELTAL_EXTERNAL_DQ 
               --calib=share/lho_cal_deltal_calibration.txt 
               --gpsb=1111224016 --length=600 --outfs=4096 --naver=100  
               --dir=./bruco_1111224016 --top=100 --webtop=20 --xlim=1:2048  
               --ylim=1e-21:1e-14 --excluded=share/lho_excluded_channels_O3.txt
    """
    
    ##### Define and get command line options ################################################
    parser = argparse.ArgumentParser(description=helpstring, 
                                     epilog="bruco version %s" % __version__, 
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument("--channel", dest="channel",
                      default='', type=str, required=True,
                      help="name of the target channel")
    parser.add_argument("--file", dest="file",
                      default='', type=str,
                      help="specify an ASCII file containing the data to be " +\
                           "used as the main channel. " +\
                           "The --channel option will be ignored. ")
    parser.add_argument("--target_source", dest="target_source",
                      default="", type=str,
                      help="point to a file with a list of GWF files from where the target signal can be read")
    parser.add_argument("--aux_source", dest="aux_source",
                      default="", type=str,
                      help="point to a file with a list of GWF files from where the auxiliary signals can be read")
    parser.add_argument("--aux_num_read", dest="aux_num_read",
                      default=20, type=int,
                      help="maximum number of auxiliary channels to read simultaneously")
    parser.add_argument("--ifo", dest="ifo",
                      default="", type=str,
                      help="interferometer prefix [H1, L1]")
    parser.add_argument("--gpsb", dest="gpsb", required=True,
                      default=0, type=int,
                      help="start GPS time")
    parser.add_argument("--length", dest="dt",
                      default=0, type=int, required=True,
                      help="amount of data to use (in seconds)")
    parser.add_argument("--outfs", dest="outfs",
                      default=8192, type=int,
                      help="sampling frequency of the output results " + \
                           "(coherence will be computed up to outfs/2 " +\
                           "if possible)")
    parser.add_argument("--naver", dest="nav",
                      default=100, type=int,
                      help="number of FFTs to average")
    parser.add_argument("--fres", dest="fres",
                      default=0, type=float,
                      help="desired frequency resolution, overwrite the --naver parameter")
    parser.add_argument("--dir", dest="dir", type=str,
                      default='bruco_report',
                      help="output directory")
    parser.add_argument("--top", dest="ntop",
                      default=100, type=int,
                      help="number of top coherences saved (for each frequency) " +\
                           "in the datafiles idxtab.txt and cohtab.txt")
    parser.add_argument("--webtop", dest="wtop",
                      default=20, type=int,
                      help="number of top coherences written to the web page, for each frequency bin")
    parser.add_argument("--minfs", dest="minfs",
                      default=32, type=int,
                      help="minimum sampling frequency of aux channels, skip those with lower sampling rate")
    parser.add_argument("--plot", dest="plotformat",
                      default='png', type=str,
                      help="plot format (png, pdf or html)")
    parser.add_argument("--nproc", dest="ncpu",
                      default=-1, type=int,
                      help="number of processes to launch (if not specified, use all available cores)")
    parser.add_argument("--calib", dest="calib",
                      default='', type=str,
                      help="name of a text file containing the calibration "+\
                           "transfer function to be applied to the target "+\
                           "channel spectrum, in a two column format  " +\
                           "(frequency, absolute value)")
    parser.add_argument("--xlim", dest="xlim",
                      default='', type=str,
                      help="frequency axis limit, in the format fmin:fmax")
    parser.add_argument("--ylim", dest="ylim",
                      default='', type=str,
                      help="PSD y axis limits, in the format ymin:ymax")
    parser.add_argument("--excluded", dest="excluded",
                      default='', type=str,
                      help="point to a text file with a list of channels excluded from the coherence computation")
    parser.add_argument("--modulations", dest="modulations",
                      default='', type=str,
                      help="name of a file that containes the list of modulation channels")
    parser.add_argument("--select", dest="select",
                      default='', type=str,
                      help="wildcard used to select only a subset of auxiliary channels")

    opt = vars(parser.parse_args())

    # see if the user specified custom plot limits
    if opt['xlim'] != '':
        opt['xlim'] = [float(x) for x in opt['xlim'].split(':')]
    else:
        opt['xlim'] = [-1, -1]
    opt['xmin'], opt['xmax'] = opt['xlim']
    if opt['ylim'] != '':
        opt['ylim'] = [float(x) for x in opt['ylim'].split(':')]
    else:
        opt['ylim'] = [-1, -1]
    opt['ymin'], opt['ymax'] = opt['ylim']

    # extract the IFO identifier if not specified
    if opt['ifo'] == '':
        if opt['channel'][0:2] == 'H1' or opt['channel'][0:2] == 'L1':
            opt['ifo'] = opt['channel'][0:2]
            opt['channel'] = opt['channel'][3:]
        else:
            print('Error: IFO identifier not specified, and cannot detect from target channel name')
            exit()
    
    # tweak some parameters as needed
    opt['gpse'] = opt['gpsb'] + opt['dt']
    opt['dir'] = os.path.expanduser(opt['dir'])

    return opt
