
import tensorboard as tb
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from tensorboard.util import tensor_util

def LoadTensorboard(logdir):
    event_acc = EventAccumulator(logdir,size_guidance={"scalars":0,"tensors": 0})
    event_acc.Reload()
    dataDict={}
    for key in event_acc.scalars.Keys():
        time, step, val = zip(*event_acc.Scalars(key))
        dataDict[key] = {"data":list(val),"step":list(step),"time":list(time)}
    for key in event_acc.tensors.Keys():
        time, step, val = zip(*event_acc.Tensors(key))
        #Implementation Note: Tensorflow 2.0 logging only saves values as Tensors, even if they are scalars.
        # Tensors by default use encoded format, which requires use of a decoder.
        val = TensorToScalar(val)
        dataDict[key] = {"data":list(val),"step":list(step),"time":list(time)}
    return dataDict

def TensorToScalar(array):
    try:
        x = [tensor_util.make_ndarray(val).item() for val in array]
    except:
        raise TypeError("Only Scalar Values can be processed. The Array loaded from tensorboard does not have `shape = ()`")
    return x


if __name__=="__main__":
    dict = LoadTensorboard("../test_logs/events.out.tfevents.1649876321.nvs-main.5579.5.v2")
    print(dict)
