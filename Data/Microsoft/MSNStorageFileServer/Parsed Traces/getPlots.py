import os
import sys
import collections
import random
import gc
import bisect

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

files = os.listdir()

def seconds_timeScale(dataframe,fname):
    data = dataframe
    # columns = Index(['Disk Operation', 'TimeStamp', 'Process Name ( PID)', 'ThreadID',
    #   'IrpPtr', 'ByteOffset', 'IOSize', 'ElapsedTime', 'DiskNum', 'IrpFlags',
    #   'DiskSvcTime', 'I/O Pri', 'FileObject', 'FileName'],
    #  dtype='object')
    
    # we care about TimeStamp and Process Name only for now
    
    startTime = min(dataframe['TimeStamp'])
    maxCount = (max((data['TimeStamp']))-min((data['TimeStamp'])))//(10**6)

    # 1s = 10**6 us
    # all numbers are in us scale
    
    bins = [startTime+i*10**6 for i in range(maxCount)]
    
    assert bins[-1] <= max(dataframe['TimeStamp'])
    
    bins_dict = collections.defaultdict(int)
    
    for i,v in data['TimeStamp'].iteritems():
        index = bisect.bisect(bins,v)
        bins_dict[index] += 1

    
    plt.figure(figsize = (60,30))
    plt.title('Processes counts by minute')
    plt.bar(range(len(list(bins_dict.values()))),
        list(bins_dict.values()))
    plt.xticks(list(bins_dict.keys()), rotation= 90)
    #plt.show()
    plt.savefig('..'+os.sep+'plots'+os.sep+'seconds_plotter'+fname+'.png')
    plt.close()
    gc.collect()
    return 0

def frequency_plotter(dataframe,fname):

    if 'Process Name ( PID)' in dataframe.columns:
        vc = dataframe['Process Name ( PID)'].value_counts()
        counts_dict = vc.to_dict()
        x = [i for i in range(len(counts_dict))]
        plt.figure(figsize = (8,8))
        plt.title('Process ID vs Counts')
        plt.xticks(x, list(counts_dict.values()))
        plt.xticks(range(len(counts_dict)), list(counts_dict.keys()), rotation=45) #writes strings with 45 degree angle
        plt.plot(x,list(counts_dict.values()),'r*')
        plt.savefig('..'+os.sep+'plots'+os.sep+'frequency_plotter'+fname+'.png')
        plt.close()
        gc.collect()
    else:
        raise ValueError('Process Name ( PID) column not found!' )
    
    del vc
    return 0

def main(fname = None):
    if fname == None:
        raise ValueError('Unkown file')
    
    data = pd.read_csv(fname)
    print("\nTotal duration: {} seconds".format((max((data['TimeStamp']))-min((data['TimeStamp'])))//(10**6)))
    seconds_timeScale(data,fname)
    frequency_plotter(data,fname)

for i in files:
    if os.path.splitext(i)[1] == '.csv':
        main(i)
        gc.collect()
    else:
        print('skipping {}'.format(i))