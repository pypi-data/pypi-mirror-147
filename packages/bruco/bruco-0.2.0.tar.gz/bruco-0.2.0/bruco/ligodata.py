# Brute force coherence (Gabriele Vajente, 2022-02-08)
# LIGO data access functions

import os
from urllib.parse import urlparse
import gwdatafind
from gwpy.timeseries import TimeSeries, TimeSeriesDict
import numpy

def find_data_path(observatory, gpsb, gpse):
    """
    Return the local disk path of the GWF files containing the RAW data.

    Parameters
    ----------
    observatory: str
        either 'H1' or 'L1'
    gpsb, gpse: int, int
        start and end GPS times of the desired RAW data

    Returns
    -------
    files: list of str
        list of filenames
    """

    obs = observatory[0]
    urls = gwdatafind.find_urls(
        obs,
        "{}1_R".format(obs),
        int(gpsb),
        int(gpse),
        urltype='file',
    )
    return [str(urlparse(x).path) for x in urls]

def get_channel_list(files):
    """
    Get the list of all channels that are available in the first file.

    Parameters
    ----------
    files: list of str
        list of filenames

    Returns
    -------
    channels: array of str
        channel names
    sample_rate: array of int
        corresponding sampling rates
    """

    print('Getting list of all channels from ' + files[0])

    # call external command to get the list of channels written to a file
    os.system('/usr/bin/FrChannels ' + files[0] + ' > bruco.channels')
    with open('bruco.channels', 'r') as f:
        lines = f.readlines()
    # parse all lines in the file
    channels = []
    sample_rate = []
    for l in lines:
        ll = l.split()
        if ll[0][1] != '0':
            # don't add L0/H0 channels, only L1 / H1 channels
            channels.append(ll[0])
            sample_rate.append(int(ll[1]))
    # convert to numpy arrays
    channels = numpy.array(channels)
    sample_rate = numpy.array(sample_rate)
    # remove temporary channel list file
    os.system('rm bruco.channels')

    return channels, sample_rate

def getRawData(channels, gpsb, gpse, files):
    """
    Read data from RAW files using gwpy

    Parameters
    ----------
    channels: list of str
        list of channel names
    gpsb, gpse: int, int
        start and end GPS times of desired data
    files: list of str
        list of GWF files where the data is available

    Returns
    -------
    data: dict
        dictionary containing the data, keys are channel names
    sampling_rate: dict
        dictionary containing the sampling rates, keys are channel names    

    """
    # read all channels using gwpy
    d = TimeSeriesDict.read(files, channels, start=gpsb, end=gpse)

    # extract data and sampling rate
    data = {}
    sampling_rate = {}

    for k in d.keys():
        data[k] = d[k].value
        sampling_rate[k] = int(d[k].sample_rate.value)

    return data, sampling_rate

def getTargetData(channel, gpsb, gpse):
    """
    Read target data using gwpy get() function

    Parameters
    ----------
    channel: str
        channel name
    gpsb, gpse: int, int
        start and end GPS times of desired data

    Returns
    -------
    data: numpy.array 
        array containing the data
    sampling_rate: int
        channel sampling rate    

    """
    # read channel using gwpy
    d = TimeSeries.get(channel, start=gpsb, end=gpse)

    # extract data and sampling rate
    data = d.value
    sampling_rate = int(d.sample_rate.value)

    return data, sampling_rate

