import torch
from collections.abc import Iterable
import numpy as np

def cuda_synchronize(device = None, stream : torch.cuda.Stream = None):
  if device in ("cpu", -1, torch.device("cpu")):
    return
  elif isinstance(device, Iterable):
    for d in device:
      torch.cuda.synchronize(d)
  elif stream is not None:
    stream.synchronize()
  else:
    torch.cuda.synchronize(device)
    # cp.cuda.runtime.deviceSynchronize()

def convert_bytes(size):
    sign = np.sign(size)
    size = abs(size)
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{np.round(sign * size, 1)}{x}"
            # return "%3.1f%s" % (size, x)
        size /= 1024.0

    return sign * size