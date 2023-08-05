# TB-Plots
This is a pip package that import Tensorboard logs and plots them in pre-specified manners for easy results tracking.

## Installation
`pip install https://github.com/Tran-Research-Group/TB-Plots.git`

## Usage
```
import tbplots
iFilter = ["XXX1","XXX2","XXX3"]
tbplots.PlotTensorflowData(path="/path/to/tblogs",gFilter="XXX",iFilter=iFilter,
      metric="winrate",saveName="FileName")
```
- `path` - The path containing all of the saved tensorboard logs. All subfolders are searched for relevant tensorboard logs.
- `gFilter` - A Global Filter used to identify subset of logs. For example one could use this to filter all logs from a particular environment.
- `iFilter` - Specifies a list of different experiments that are to be plotted.
- `metric` - Specifies the metric[s] to be plotted for the different experiments.
- `saveName` - Specifies the name of the saved image

## Example code for adding Logging to Script

### Tensorflow Example
```
LOG_PATH="./logs/EXP_NAME"
writer = tf.summary.create_file_writer(LOG_PATH)
with writer.as_default():
  summary = tf.summary.scalar('winrate',0.565,step=100)
  writer.flush()
```
### Pytorch Example

*Requires Additional Packages `tensorboard-logger`*
```
from tensorboard_logger import configure, log_value
configure(LOG_PATH)
self.tb_logger = log_value
log_value('winrate',0.565,100)
```
