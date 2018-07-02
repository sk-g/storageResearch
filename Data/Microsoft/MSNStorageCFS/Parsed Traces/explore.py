import os
import sys
import collections
import random
import gc
import bisect
import time
from math import sqrt

import pandas as pd
import numpy as np

from multiprocessing import Process, Pool
def loader(fname):
    data = pd.read_csv(fname,
                            index_col = False,
                            usecols = [ 'TimeStamp',
                                'Disk Operation',
                                'Process Name ( PID)'])
    return data

def drawProgressBar(percent, barLen = 50):
	sys.stdout.write("\r")
	progress = ""
	for i in range(barLen):
		if i<int(barLen * percent):
			progress += "="
		else:
			progress += " "
	sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
	sys.stdout.flush()

def change_process(dataframe):
    l = len(dataframe)
    for i,row in dataframe.iterrows():
        #drawProgressBar(i/l)
        name = dataframe.at[i,'Process Name ( PID)']
        name = list(name)
        name = collections.deque(name)
        for _ in range(len(name)-1,-1,-1):
            x = name.pop()
            if x == '(':
                break;
        name = ''.join([_ for _ in name])
        
        dataframe.at[i,'Process Name ( PID)'] = name
    #print(dataframe.head(15))
    return dataframe


        
def main():
    paths = "M:\Course stuff\SSRC\Data\Microsoft\MSNStorageFileServer\Parsed Traces"
    files = ['parsed.MSNFS.2008-03-10.01-01.trace.csv', 'parsed.MSNFS.2008-03-10.01-11.trace.csv', 'parsed.MSNFS.2008-03-10.01-21.trace.csv', 'parsed.MSNFS.2008-03-10.01-31.trace.csv', 'parsed.MSNFS.2008-03-10.01-42.trace.csv', 'parsed.MSNFS.2008-03-10.01-52.trace.csv', 'parsed.MSNFS.2008-03-10.02-02.trace.csv', 'parsed.MSNFS.2008-03-10.02-12.trace.csv', 'parsed.MSNFS.2008-03-10.02-22.trace.csv', 'parsed.MSNFS.2008-03-10.02-32.trace.csv', 'parsed.MSNFS.2008-03-10.02-42.trace.csv', 'parsed.MSNFS.2008-03-10.02-53.trace.csv', 'parsed.MSNFS.2008-03-10.03-03.trace.csv', 'parsed.MSNFS.2008-03-10.03-13.trace.csv', 'parsed.MSNFS.2008-03-10.03-23.trace.csv', 'parsed.MSNFS.2008-03-10.03-33.trace.csv', 'parsed.MSNFS.2008-03-10.03-43.trace.csv', 'parsed.MSNFS.2008-03-10.03-53.trace.csv', 'parsed.MSNFS.2008-03-10.04-03.trace.csv', 'parsed.MSNFS.2008-03-10.04-14.trace.csv', 'parsed.MSNFS.2008-03-10.04-24.trace.csv', 'parsed.MSNFS.2008-03-10.04-34.trace.csv', 'parsed.MSNFS.2008-03-10.04-44.trace.csv', 'parsed.MSNFS.2008-03-10.04-54.trace.csv', 'parsed.MSNFS.2008-03-10.05-04.trace.csv', 'parsed.MSNFS.2008-03-10.05-14.trace.csv', 'parsed.MSNFS.2008-03-10.05-24.trace.csv', 'parsed.MSNFS.2008-03-10.05-35.trace.csv', 'parsed.MSNFS.2008-03-10.05-45.trace.csv', 'parsed.MSNFS.2008-03-10.05-55.trace.csv', 'parsed.MSNFS.2008-03-10.06-05.trace.csv', 'parsed.MSNFS.2008-03-10.06-15.trace.csv', 'parsed.MSNFS.2008-03-10.06-25.trace.csv', 'parsed.MSNFS.2008-03-10.06-35.trace.csv', 'parsed.MSNFS.2008-03-10.12-41.trace.csv', 'parsed.MSNFS.2008-03-10.12-51.trace.csv']
    to_process = [paths+os.sep+i for i in files]
    """
    to_process = [ 'parsed.CFS.2008-03-10.01-06.trace.csv','parsed.CFS.2008-03-10.01-16.trace.csv',
    'parsed.CFS.2008-03-10.01-26.trace.csv',
    'parsed.CFS.2008-03-10.01-36.trace.csv',
    'parsed.CFS.2008-03-10.01-47.trace.csv',
    'parsed.CFS.2008-03-10.01-57.trace.csv',
    'parsed.CFS.2008-03-10.02-07.trace.csv',
    'parsed.CFS.2008-03-10.02-17.trace.csv',
    'parsed.CFS.2008-03-10.02-27.trace.csv',
    'parsed.CFS.2008-03-10.02-37.trace.csv',
    'parsed.CFS.2008-03-10.02-47.trace.csv',
    'parsed.CFS.2008-03-10.02-58.trace.csv',
    'parsed.CFS.2008-03-10.03-08.trace.csv',
    'parsed.CFS.2008-03-10.03-18.trace.csv',
    'parsed.CFS.2008-03-10.03-28.trace.csv',
    'parsed.CFS.2008-03-10.03-38.trace.csv',
    'parsed.CFS.2008-03-10.03-48.trace.csv',
    'parsed.CFS.2008-03-10.03-58.trace.csv',
    'parsed.CFS.2008-03-10.04-09.trace.csv',
    'parsed.CFS.2008-03-10.04-19.trace.csv',
    'parsed.CFS.2008-03-10.04-29.trace.csv',
    'parsed.CFS.2008-03-10.04-39.trace.csv',
    'parsed.CFS.2008-03-10.04-49.trace.csv',
    'parsed.CFS.2008-03-10.04-59.trace.csv',
    'parsed.CFS.2008-03-10.05-09.trace.csv',
    'parsed.CFS.2008-03-10.05-19.trace.csv',
    'parsed.CFS.2008-03-10.05-30.trace.csv',
    'parsed.CFS.2008-03-10.05-40.trace.csv',
    'parsed.CFS.2008-03-10.05-50.trace.csv',
    'parsed.CFS.2008-03-10.06-00.trace.csv',
    'parsed.CFS.2008-03-10.06-10.trace.csv',
    'parsed.CFS.2008-03-10.06-20.trace.csv',
    'parsed.CFS.2008-03-10.06-30.trace.csv',
    'parsed.CFS.2008-03-10.06-41.trace.csv',
    'parsed.CFS.2008-03-10.06-51.trace.csv',
    'parsed.CFS.2008-03-10.12-56.trace.csv',]
    """
    procs = 4
    # load all files in parallel
    res = Pool(procs).map(loader,to_process)
    # res has all loaded data frames
    # need to apply change_process on all of them
    print("\nLoaded all files succesfully")
    data = Pool(procs).map(change_process,res)
    data = pd.concat(data, 
          axis=0, 
          join='outer', 
          join_axes=None, 
          ignore_index=True
    )
    data.sort_values(by = 'TimeStamp')
    data.to_csv("..\..\..\MSNStorageFileServer_sortedFrame.csv",
                # columns = ['TimeStamp',
                #             'Disk Operation',
                #             'Process Name ( PID)'],
                index = False,
                index_label = False)
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print((end-start)/60)