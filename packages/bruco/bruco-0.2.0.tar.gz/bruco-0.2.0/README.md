# BruCo: Brute-force coherence noise analsysis

BruCo is a python package that systematically computes the coherence of a target channel with *all* available auxiliary channels, including in presence of known modulation by slow channels.

```
$ python -m bruco --help
usage: __main__.py [-h] --channel CHANNEL [--file FILE] [--target_source TARGET_SOURCE] [--aux_source AUX_SOURCE] [--aux_num_read AUX_NUM_READ]
                   [--ifo IFO] --gpsb GPSB --length DT [--outfs OUTFS] [--naver NAV] [--fres FRES] [--dir DIR] [--top NTOP] [--webtop WTOP]
                   [--minfs MINFS] [--plot PLOTFORMAT] [--nproc NCPU] [--calib CALIB] [--xlim XLIM] [--ylim YLIM] [--excluded EXCLUDED]
                   [--modulations MODULATIONS] [--select SELECT]

    Brute force coherence (Gabriele Vajente, 2022-02-03)
    
    Example:
    python -m bruco --ifo=H1 --channel=CAL-DELTAL_EXTERNAL_DQ 
               --calib=share/lho_cal_deltal_calibration.txt 
               --gpsb=1111224016 --length=600 --outfs=4096 --naver=100  
               --dir=./bruco_1111224016 --top=100 --webtop=20 --xlim=1:2048  
               --ylim=1e-21:1e-14 --excluded=share/lho_excluded_channels_O3.txt
    

optional arguments:
  -h, --help            show this help message and exit
  --channel CHANNEL     name of the target channel
  --file FILE           specify an ASCII file containing the data to be used as the main channel. The --channel option will be ignored.
  --target_source TARGET_SOURCE
                        point to a file with a list of GWF files from where the target signal can be read
  --aux_source AUX_SOURCE
                        point to a file with a list of GWF files from where the auxiliary signals can be read
  --aux_num_read AUX_NUM_READ
                        maximum number of auxiliary channels to read simultaneously
  --ifo IFO             interferometer prefix [H1, L1]
  --gpsb GPSB           start GPS time
  --length DT           amount of data to use (in seconds)
  --outfs OUTFS         sampling frequency of the output results (coherence will be computed up to outfs/2 if possible)
  --naver NAV           number of FFTs to average
  --fres FRES           desired frequency resolution, overwrite the --naver parameter
  --dir DIR             output directory
  --top NTOP            number of top coherences saved (for each frequency) in the datafiles idxtab.txt and cohtab.txt
  --webtop WTOP         number of top coherences written to the web page, for each frequency bin
  --minfs MINFS         minimum sampling frequency of aux channels, skip those with lower sampling rate
  --plot PLOTFORMAT     plot format (png, pdf or html)
  --nproc NCPU          number of processes to launch (if not specified, use all available cores)
  --calib CALIB         name of a text file containing the calibration transfer function to be applied to the target channel spectrum, in a two column
                        format (frequency, absolute value)
  --xlim XLIM           frequency axis limit, in the format fmin:fmax
  --ylim YLIM           PSD y axis limits, in the format ymin:ymax
  --excluded EXCLUDED   point to a text file with a list of channels excluded from the coherence computation
  --modulations MODULATIONS
                        name of a file that containes the list of modulation channels
  --select SELECT       wildcard used to select only a subset of auxiliary channels

bruco version 0.2.0
```

## Explanation of parameters 

| Parameter | Explanation |
| ------ | ------ |
| `channel` | name of the target channel: BruCo with compute the coherence of this channels with all other available channels |
| `file`    | instead of specifying the channel with the argument above, you can provide the name of a ASCII or pickle file where the data can be read. If you use this option, the channel name specified with `--channel` is ignored, and the sampling frequency is inferred from the number of datapoints in the file and the GPS times |
| `target_source` | name of a text file containing a list of GWF files from where the target channel data is read. If not give, data is read with `gwpy` |
| `aux_source` | name of a text file containing a list of GWF files from where the auxiliary channels will be read. If not specified, `gw_data_find` is used to look for raw frame file |
| `ifo` | prefix determining the IFO, either 'H1' or 'L1' |
| `gpsb` | start GPS time of the data to analyze |
| `length` | duration of the data to be analyzed, in seconds |
| `outfs` | sampling frequency for all computations, meaning that coherence will be computed up to `outfs/2` |
| `naver` | number of desired averages for the periodogram-based computation of coherence. BruCo will approximate this number of averages by choosing a power-of-two FFT length that closely matches the desired number of averages |
| `fres` | an alternative way to specify the length of the FFTs, by giving the desired frequency resolution in Hz. BruCo will approximate this resolution by choosing a power-of-two FFT length |
| `dir` | all results and plots will be saved in this directory |
| `excluded` | name of a text file containing, in each row, the name of auxiliary channels to be excluded from the coherence computation, becuase they are known to have coherence with the target. Each row can be a unix-style wildcard |
| `minfs` | minimum sampling frequency of the auxiliary channels: all channels sampled at a lower frequency are excluded |
| `select` | a single unix-style wildcard to specify a subset of auxiliary channels to be analyzed |
| `modulations` | name of a text file where each row is the full name of a channel that will be used as a modulation witness. If specified, BruCo will compute the coherence of the target channel with each auxiliary channel, and with the product of each auxiliary channel with each of the modulation channels |
| `plot` | plot format. This can be `png` or `pdf` to produce static plots of the corresponding format, or `html` to produce interactive plots based on the `plotly` library |
| `calib` | name of a text file containing the calibration transfer function to be applied to the target channel spectrum, in a two column format (frequency, absolute value) |
| `aux_num_read` | maximum number of auxiliary channels to read simultaneously |
| `top` | save this many top-coherence channels for each frequency bin |
| `webtop` | include this many top-coherence channels in the final report |
| `xlim` | specify custom limits for the horizontal frequency axis |
| `ylim` | specify custom limits for the vertical amplitude spectral density axis |
| `nproc` | number of parallel processes to use. If not specified, use all available cores |
