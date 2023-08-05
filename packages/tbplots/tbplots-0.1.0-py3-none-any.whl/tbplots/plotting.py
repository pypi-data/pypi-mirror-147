
import os
from os import walk
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import numpy as np

from .math import GetAverageSTD,GetAverageConfidence,GetMedian
from .tbUtils import LoadTensorboard

DEFAULT_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def PlotTensorflowData(path,gFilter,iFilter,metric,saveName,labels=None,
    title=None,xlabel=None,ylabel=None,xbounds=None,ybounds=None,plotStyle="Median",
    showReplicates=False,smoothing=False,smoothingWindow=11,savePath=""):
    """ Function Description: TBC"""

    assert(len(gFilter)<len(DEFAULT_COLORS), "Recieved >10 independent experiments. Reduce number to be plotted.")

    #Metric can be string or list. If input is a list, then the
    if isinstance(metric,str):
        metric=[metric]*len(iFilter)

    #If no Labels are provided, defaults to using
    if labels is None:
        labels = iFilter
    else:
        assert(len(labels)==len(iFilter), "The length of labels is different from the specified iFilter")

    print("Plotting Tensorboard Data with the following configs: \n\tgFilter:{} | filePath:{} \n\tiFilters:{}".format(gFilter,path,iFilter))
    #Iterating through the specified directory looking for matches to the specified characteristics.
    dataFiles = {}
    for name,label in zip(iFilter,labels):
        dataFiles[label]=[]
        for (dirpath, dirnames, filenames) in walk(path):
            if len(filenames) != 0:
                if gFilter in dirpath:
                    if name in dirpath:
                        for filename in filenames:
                            if "events.out.tfevents" in filename:
                                dataFiles[label].append(LoadTensorboard("{}/{}".format(dirpath,filename)))
                                print("\tLoaded data from: {}/{}".format(dirpath,filename))
                                continue

    i=0
    fig = plt.figure(figsize=(6.5, 4))
    for label,data in dataFiles.items():

        if plotStyle in ["Average","Mean"]:
            ave,std,x,replicates =GetAverageSTD(data,metric[i])
            if smoothing:
                if len(ave)>smoothingWindow:
                    std = savgol_filter(std, smoothingWindow, 3)
                    ave = savgol_filter(ave, smoothingWindow, 3)
            if showReplicates:
                label += " ({})".format(replicates)
            plt.plot(x,ave,label=label,color=DEFAULT_COLORS[i])
            plt.fill_between(x, ave-std, ave+std,alpha=0.05,color=DEFAULT_COLORS[i])
            plt.plot(x,ave-std,alpha=0.25,color=DEFAULT_COLORS[i],linestyle=':')
            plt.plot(x,ave+std,alpha=0.25,color=DEFAULT_COLORS[i],linestyle=':')

        if plotStyle in ["Confidence"]:
            ave,conf,x,replicates =GetAverageConfidence(data,metric[i])
            if smoothing:
                if len(ave)>smoothingWindow:
                    conf = savgol_filter(conf, smoothingWindow, 3)
                    ave = savgol_filter(ave, smoothingWindow, 3)
            if showReplicates:
                label += " ({})".format(replicates)
            plt.plot(x,ave,label=label,color=DEFAULT_COLORS[i])
            plt.fill_between(x, ave-conf, ave+conf,alpha=0.05,color=DEFAULT_COLORS[i])
            plt.plot(x,ave-conf,alpha=0.25,color=DEFAULT_COLORS[i],linestyle=':')
            plt.plot(x,ave+conf,alpha=0.25,color=DEFAULT_COLORS[i],linestyle=':')

        elif plotStyle == "Median":
            median, upperQuart, lowerQuart, x,replicates  = GetMedian(data,metric[i])
            bounds=np.stack([median-lowerQuart,upperQuart-median])
            if smoothing:
                if len(median)>smoothingWindow:
                    median = savgol_filter(median, smoothingWindow, 3)
                    upperQuart = savgol_filter(upperQuart, smoothingWindow, 3)
                    lowerQuart = savgol_filter(lowerQuart, smoothingWindow, 3)

            if showReplicates:
                label += " ({})".format(replicates)
            plt.plot(x,median,label=label,color=DEFAULT_COLORS[i])
            plt.fill_between(x, lowerQuart, upperQuart,alpha=0.05,color=DEFAULT_COLORS[i])
            plt.plot(x,lowerQuart,alpha=0.25,color=DEFAULT_COLORS[i],linestyle=':')
            plt.plot(x,upperQuart,alpha=0.25,color=DEFAULT_COLORS[i],linestyle=':')

        i+=1

    plt.xlim(xbounds)
    plt.ylim(ybounds)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend()
    plt.savefig(os.path.join(savePath,saveName+".png"),bbox_inches='tight')
    plt.clf()
