
import numpy as np

def ProcessDicts(dicts,metric):
    finalDictList = []
    for dict in dicts:
        if metric in dict:
            finalDictList.append(dict)
    return finalDictList

def GetAverageSTD(dicts,metric):
    dictsFinal = ProcessDicts(dicts,metric)
    length=0
    #Finding the longest array
    for dict in dictsFinal:
        if len(dict[metric]["data"])>length:
            length = len(dict[metric]["data"])
    data = []
    x = []
    for dict in dictsFinal:
        if len(dict[metric]["data"])==length:
            data.append(dict[metric]["data"])
            x.append(dict[metric]["step"])
        else:
            for i in range(length-len(dict[metric]["data"])):
                dict[metric]["data"].append(np.nan)
                dict[metric]["step"].append(np.nan)
            data.append(dict[metric]["data"])
            x.append(dict[metric]["step"])
    try:
        average = np.nanmean(np.stack(data),axis=0)
        x_average = np.nanmean(np.stack(x),axis=0)
        std = np.nanstd(np.stack(data),axis=0)
    except ValueError:
        average = np.asarray([0])
        std = np.asarray([0])
        x_average = np.asarray([0])
    return average,std,x_average,len(dictsFinal)


def GetAverageConfidence(dicts,metric,tval=1.0):
    dictsFinal = ProcessDicts(dicts,metric)
    length=0
    #Finding the longest array
    for dict in dictsFinal:
        if len(dict[metric]["data"])>length:
            length = len(dict[metric]["data"])
    data = []
    x = []
    for dict in dictsFinal:
        if len(dict[metric]["data"])==length:
            data.append(dict[metric]["data"])
            x.append(dict[metric]["step"])
        else:
            for i in range(length-len(dict[metric]["data"])):
                dict[metric]["data"].append(np.nan)
                dict[metric]["step"].append(np.nan)
            data.append(dict[metric]["data"])
            x.append(dict[metric]["step"])
    try:
        average = np.nanmean(np.stack(data),axis=0)
        x_average = np.nanmean(np.stack(x),axis=0)
        confidence = tval*np.nanstd(np.stack(data),axis=0)/np.sqrt(len(dictsFinal))
    except ValueError:
        average = np.asarray([0])
        confidence = np.asarray([0])
        x_average = np.asarray([0])
    return average,confidence,x_average,len(dictsFinal)


def GetMedian(dicts,metric):
    dictsFinal = ProcessDicts(dicts,metric)
    length=0
    #Finding the longest array
    for dict in dictsFinal:
        if len(dict[metric]["data"])>length:
            length = len(dict[metric]["data"])
    data = []
    x = []
    for dict in dictsFinal:
        if len(dict[metric]["data"])==length:
            data.append(dict[metric]["data"])
            x.append(dict[metric]["step"])
        else:
            for i in range(length-len(dict[metric]["data"])):
                dict[metric]["data"].append(np.nan)
                dict[metric]["step"].append(np.nan)
            data.append(dict[metric]["data"])
            x.append(dict[metric]["step"])
    try:
        median = np.nanmedian(np.stack(data),axis=0)
        upperQuart = np.nanquantile(np.stack(data),0.75,axis=0)
        lowerQuart = np.nanquantile(np.stack(data),0.25,axis=0)
        x_average = np.nanmean(np.stack(x),axis=0)
    except ValueError:
        median = np.asarray([0])
        upperQuart = np.asarray([0])
        lowerQuart = np.asarray([0])
        x_average = np.asarray([0])
    return median,upperQuart,lowerQuart,x_average,len(dictsFinal)
