# TorchTimer
TorchTimer is a tool for profiling GPU programs written in pytorch

## Install
```bash
$ pip3 install torchtimer
```

## Tutorial

#### Timing a code segment
```python
import torch
from torchtimer import ProfilingTimer
timer = ProfilingTimer()

device = "cuda:0"
a = torch.randn(1000, 1000, device=device)
b = torch.randn(1000, 1000, device=device)

timer.start()
# put the code segment you want to time between timer.start and timer.stop
torch.matmul(a, b)

elapsed_time = timer.stop()
print(elapsed_time)
# Out: 0.007798399999998651
```

#### Print a summary
```python
timer.summarize()

""" Out:
###### timer::main: (total runtime 0.5219481s)
| name      | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| --------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'default' | 1          | 0.5219481    | 0.5219481    | 100.0           | 0B - 0B              | 3.8MB - 3.8MB        |
"""
```
You can directly copy-paste the output of `timer.summarize()` into markdown files, they will be rendered as tables like this:
###### timer::main: (total runtime 0.5219481s)
| name      | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| --------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'default' | 1          | 0.5219481    | 0.5219481    | 100.0           | 0B - 0B              | 3.8MB - 3.8MB        |

What each column represents will be explained in more detail later

#### Timing iteratively
We can get the total and average elapsed time of repeatedly executed code segments
```python
timer = ProfilingTimer()

device = "cuda:0"

for i in range(1000):
  a = torch.randn(1000, 1000, device=device)
  b = torch.randn(1000, 1000, device=device)
  timer.start()
  torch.matmul(a, b)
  timer.stop()

timer.summarize()
```
And here is the summary rendered in markdown:
###### timer::main: (total runtime 1.610135s)
| name      | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| --------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'default' | 1000       | 0.00161013   | 1.610135     | 100.0           | 0B - 0B              | 3.8MB - 3.8MB        |
The statistic of 1000 runs is summarized in a single row.

#### Timing multiple code segments
```python
timer = ProfilingTimer()
device = "cuda:0"

for i in range(1000):
  timer.start("randn")
  a = torch.randn(1000, 1000, device=device)
  b = torch.randn(1000, 1000, device=device)
  timer.stop("randn")

  timer.start("matmul")
  c = torch.matmul(a, b)
  timer.stop("matmul")

  timer.start("sum")
  c_sum = c.sum(dim=-1)
  timer.stop("sum")

timer.summarize()
```

**summary:**
###### timer::main: (total runtime 3.3098865s)
| name     | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| -------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'randn'  | 1000       | 0.00163867   | 1.6386684    | 49.51           | 0B - 7.6MB           | 3.8MB - 7.6MB        |
| 'matmul' | 1000       | 0.00147231   | 1.4723084    | 44.48           | 0B - 3.8MB           | 3.8MB - 3.8MB        |
| 'sum'    | 1000       | 0.00019891   | 0.1989097    | 6.01            | 0B - 4.0KB           | 4.0KB - 4.0KB        |

The first argument for `timer.start` and `timer.stop` is `name`, it will be shown in the first column. If `name` isn't provided, then it will be set to `"default"`.

Different code segments in the same context must have unique names. ("context" will be explained later)

The fifth column, shows how much time each code segment took relative to the total time of all recorded code segments in the same context.

#### Timing in different context
Here we use a simple word2vec model as example.
The `Word2Vec` class has 2 important methods: `forward` and `most_similar`.
In `forward(x)`, we simply pass the input tensor `x` through an embedding layer and a linear layer.
`most_similar(word, k)` returns the most similar `k` words to the given word.

Can we find the performance bottlenecks in each class method?

```python
import torch
import torch.nn as nn
from torchtimer import ProfilingTimer

class Word2Vec(nn.Module):
  def __init__(self, vocab, emb_dim):
    super().__init__()
    self.vocab=vocab
    self.inverse_vocab={ token:i for i, token in enumerate(vocab)}
    self.emb_dim=emb_dim
    self.embedding = nn.Embedding(num_embeddings=len(vocab), embedding_dim=emb_dim)
    self.linear = nn.Linear(emb_dim, len(vocab), bias=False)

    self.timer = ProfilingTimer(name="Word2Vec")

  @staticmethod
  def cos_sim(a, b):
    a_norm = a.norm(dim=-1, keepdim=True)
    b_norm = b.norm(dim=-1, keepdim=True)
    return (a / a_norm) @ (b / b_norm).transpose(-1, -2)

  def forward(self, x):
    start, stop = self.timer.create_context("forward")
    start("embedding")
    y = self.embedding(x)
    stop("embedding")
    
    start("linear")
    y = self.linear(y)
    stop("linear")
    return y

  def most_similar(self, word, k=1):
    start, stop = self.timer.create_context("most_similar")

    start("embedding")
    word_idx = [self.inverse_vocab[word]]
    embs = self.embedding.weight[word_idx]
    stop("embedding")
    
    start("cos sim")
    sim = self.cos_sim(embs, self.embedding.weight)[0]
    stop("cos sim")

    start("topk")
    topk_val, topk_idx = sim.topk(k=k+1, dim=-1)
    stop("topk")

    start("finalize")
    result = [(self.vocab[topk_idx[i+1]], topk_val[i+1].item()) for i in range(k)]
    stop("finalize")
    return result

vocab = ["cat", "fat", "mat", "on", "sat", "the"]
batch_size = 128
device = "cuda:0"
w2v = Word2Vec(vocab, emb_dim=100).to(device)

for i in range(100):
  mock_data = torch.randint(len(vocab), size=[batch_size], device=device)
  logits = w2v.forward(mock_data)
  # ...

for word in vocab:
  print(w2v.most_similar(word, k=5))
  
w2v.timer.summarize()
``` 

**summary:**
###### Word2Vec::forward: (total runtime 0.583368s)
| name        | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| ----------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'linear'    | 100        | 0.00564517   | 0.5645173    | 96.77           | 3.0KB - 3.0KB        | 3.0KB - 3.0KB        |
| 'embedding' | 100        | 0.00018851   | 0.0188507    | 3.23            | 50.0KB - 50.0KB      | 50.0KB - 50.0KB      |
###### Word2Vec::most_similar: (total runtime 0.0109622s)
| name        | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| ----------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'finalize'  | 6          | 0.00072162   | 0.0043297    | 39.5            | 0B - 0B              | 0B - 0B              |
| 'cos sim'   | 6          | 0.00049202   | 0.0029521    | 26.93           | 5.5KB - 5.5KB        | 5.5KB - 5.5KB        |
| 'embedding' | 6          | 0.00040543   | 0.0024326    | 22.19           | 1.0KB - 1.0KB        | 1.0KB - 1.0KB        |
| 'topk'      | 6          | 0.00020797   | 0.0012478    | 11.38           | 1.0KB - 1.0KB        | 1.0KB - 1.0KB        |

Values under `% total time` are calculated relative to the total runtime of each context. 

`ProfilingTimer.create_context` takes context name as argument and returns 2 functions: `start` and `stop`. They can be used just like `ProfilingTimer.start` and `ProfilingTimer.stop`. 

In fact, 
```python
from time import sleep
from torchtimer import ProfilingTimer
timer = ProfilingTimer()
start, stop = timer.create_context("foo")

start("sleep")
sleep(1)
stop("sleep")
```
is identical to:
```python
from time import sleep
from torchtimer import ProfilingTimer
timer = ProfilingTimer()

timer.start("sleep", context="foo")
sleep(1)
timer.stop("sleep", context="foo")

```
You can use whichever you like.

#### Memory statistics
Now we'll talk about the last two columns: `net mem alloc` and `peak mem alloc`.
`net mem alloc` is the minimum and maximum **net** increase in the GPU memory allocated by pytorch. 
`peak mem alloc` is the minimum and maximum **peak** increase in the peak GPU memory allocated by pytorch.
In order to explain the difference between the two, let's go back to the one of the earlier examples:
```python
import torch
from torchtimer import ProfilingTimer
timer = ProfilingTimer()

device = "cuda:0"

for i in range(1000):
  a = torch.randn(1000, 1000, device=device)
  b = torch.randn(1000, 1000, device=device)
  timer.start()
  torch.matmul(a, b)
  timer.stop()

timer.summarize()
```
###### timer::main: (total runtime 1.610135s)
| name      | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| --------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'default' | 1000       | 0.00161013   | 1.610135     | 100.0           | 0B - 0B              | 3.8MB - 3.8MB        |

Both min and max `net mem alloc` is `0B`, it's because we didn't obtain a new tensor as a result of `matmul`. However both min and max `peak mem alloc` is `3.8MB`, because during the matrix multiplication, a temporary tensor of size `3.8MB` is allocated to store the results of `matmul`, but because we don't have any reference to that temporary tensor, python garbage collector automatically deleted it.

If we keep a reference to all temporary/deleted tensors allocated during a code segment, then `peak mem alloc` will be identical to `net mem alloc`

Here's an even simpler example:
```python
import torch
from torchtimer import ProfilingTimer
timer = ProfilingTimer()
device = "cuda:0"

timer.start("no reference")
torch.empty(1000, 1000, device=device)
timer.stop("no reference")

timer.start("delete")
a = torch.empty(1000, 1000, device=device)
del a
timer.stop("delete")

timer.start("with reference")
a = torch.empty(1000, 1000, device=device)
timer.stop("with reference")

timer.summarize()
```
**summary:**
###### timer::main: (total runtime 0.0018539s)
| name             | repeats    | average time | total time   | % total time    | net mem alloc        | peak mem alloc       |
| ---------------- | ---------- | ------------ | ------------ | --------------- | -------------------- | -------------------- |
| 'no reference'   | 1          | 0.0016119    | 0.0016119    | 86.95           | 0B - 0B              | 3.8MB - 3.8MB        |
| 'delete'         | 1          | 0.0001383    | 0.0001383    | 7.46            | 0B - 0B              | 3.8MB - 3.8MB        |
| 'with reference' | 1          | 0.0001037    | 0.0001037    | 5.59            | 3.8MB - 3.8MB        | 3.8MB - 3.8MB        |

As expected, only when we keep a reference to the allocated tensor, `net mem alloc` is equal to `peak mem alloc`

#### Save summary to a file
```python
file_path = "./summary.md"
timer.summarize_to_file(file_path)
```

#### Visualize as HTML
```python
file_path = "./vis.html"
timer.visualize(file_path, figsize=(1920, 900))
```
Open the html file with any major browser. 
X axis is time, Y axis is memory.
Use the tools at the bottom left corner to zoom-in or out, and move around.
Note: this is feature is experimental.

##### Demo:
![demo](media/vis2.gif)