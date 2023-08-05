# TorchTimer
TorchTimer is a tool for profiling GPU programs written in pytorch

## Install
```bash
$ pip3 install torchtimer
```

## Tutorial
Timing a block of code
```python
import torch
from torchtimer import ProfilingTimer
timer = ProfilingTimer()

device = "cuda:0"
a = torch.randn(1000, 1000, device=device)
b = torch.randn(1000, 1000, device=device)

timer.start()
# put the code block you want to time between timer.start and timer.stop
torch.matmul(a, b)

elapsed_time = timer.stop()
print(elapsed_time)
# Out: 
```