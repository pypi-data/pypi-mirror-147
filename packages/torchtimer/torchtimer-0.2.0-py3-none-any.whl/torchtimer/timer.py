from logging import LogRecord
import time
import torch
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
import mpld3

from .util import cuda_synchronize, convert_bytes
from .plugin import InteractiveLegendPlugin
from .table import TableLogger
class SegmentState:
  def __init__(
      self,
      start_time=None,
      end_time=None,
      max_memory_allocated_end=None,
      memory_allocated_start=None,
      memory_allocated_end=None
    ):
    self.start_time = start_time
    self.end_time = end_time
    self.max_memory_allocated_end = max_memory_allocated_end
    self.memory_allocated_start = memory_allocated_start
    self.memory_allocated_end = memory_allocated_end

  @property
  def elapsed_time(self):
    if self.end_time is not None and self.start_time is not None:
      return self.end_time - self.start_time
    else:
      return 0

  @property
  def net_memory_allocated(self):
    if self.memory_allocated_end is not None and self.memory_allocated_start is not None:
      return self.memory_allocated_end - self.memory_allocated_start
    else:
      return 0

  @property
  def peak_memory_allocated(self):
    if self.max_memory_allocated_end is not None and self.memory_allocated_start is not None:
      return self.max_memory_allocated_end - self.memory_allocated_start
    else:
      return 0

class ProfilingTimer:
  def __init__(self, enabled=True, device=None, stream=None, name="timer", allies=list()):
    self.name = name
    self._main_context_name = "main"
    self._states = {self._main_context_name : dict() }
    self.device = device
    self.stream = stream
    self._allies = allies
    self._disabled_context = set()
    self._enabled = enabled
    self._created_time = self.gct(relative=False)
    # self._created_time = GLOBAL_START_TIME
    for ally in self.allies:
      assert isinstance(ally, ProfilingTimer)
      ally._enabled = ally._enabled and self._enabled
      ally._created_time = self._created_time

  # def __del__(self):
  #   self.summarize()

  @property
  def allies(self):
    all_allies = set(self._allies)
    for ally in self._allies:
      all_allies.update(ally.allies)
    return list(all_allies)


  def synchronize(self):
    cuda_synchronize(self.device, self.stream)

  def enable(self):
    self._enabled = True

  def disable(self):
    self._enabled = False

  def create_context(self, context):
    def start(name):
      self.start(name=name, context=context)

    def stop(name):
      self.stop(name=name, context=context)

    return start, stop

  def disable_context(self, context):
    self._disabled_context.add(context)

  def enable_context(self, context):
    if context in self._disabled_context:
      self._disabled_context.remove(context)

  def gct(self, relative=True):
    """ get current time"""
    self.synchronize()
    current_time = time.perf_counter()# * 1000
    if relative:
      current_time = current_time - self._created_time
    return current_time

  def clear(self):
    self._states = { self._main_context_name : dict()}

  def remove(self, name, context=None):
    if self._enabled:
      if context is None:
        context = self._main_context_name
      if context in self._disabled_context:
        return
      assert context in self._states
      states = self._states[context]
      assert name in states.keys()
      del states[name]

  def start(self, name="default", context=None):
    if self._enabled:
      if context is None:
        context = self._main_context_name

      if context in self._disabled_context:
        return

      if context not in self._states:
        self._states[context] = dict()

      current_time = self.gct()
      state = SegmentState(
        start_time=current_time, 
        memory_allocated_start=torch.cuda.memory_allocated(self.device)
      )
      torch.cuda.reset_max_memory_allocated(self.device)
      if name not in self._states[context]:
        self._states[context][name] = [state]
      else:
        self._states[context][name].append(state)

  def end(self, name="default", context=None):
    if self._enabled:
      current_time = self.gct()
      if context is None:
        context = self._main_context_name
      if context in self._disabled_context:
        return
      assert context in self._states
      assert name in self._states[context]

      state = self._states[context][name][-1]
      state.end_time = current_time
      state.memory_allocated_end = torch.cuda.memory_allocated(self.device)
      state.max_memory_allocated_end = torch.cuda.max_memory_allocated(self.device)
      return state.elapsed_time 
      #  = end_time - self._states[context][name][-1]  
  
  def stop(self, name="default", context=None):
    return self.end(name, context)

  def stop_and_start(self, stop_name=None, start_name=None, context=None):
    elapsed_time = None
    if stop_name is not None:
      elapsed_time = self.stop(stop_name, context)
    if start_name is not None:
      self.start(start_name, context)
    return elapsed_time

  def clear_states(self):
    for context in self._states:
      if context in self._disabled_context:
        continue
      context_states = self._states[context]
      for seg_name in context_states:
        seg_states = context_states[seg_name]
        self._states[context][seg_name] = [state for state in seg_states if state.start_time is not None and state.end_time is not None]

  def summarize(self):
    if self._enabled:
      self.clear_states()
      for context in self._states:
        if context in self._disabled_context:
          continue
        states = list(self._states[context].items())
        if len(states) == 0:
          continue
        # elapsed_time = [(name, state) for state in states]
        states = sorted(states, key= lambda x: np.sum([s.elapsed_time for s in x[1]]), reverse=True)
        total_runtime = np.sum([ np.sum([s.elapsed_time for s in i[1]]) for i in states])
        
        print(f"###### {self.name}::{context}: (total runtime {np.round(total_runtime, 8)}s)")
        logger = TableLogger(
          col_labels=["name", "repeats", "average time", "total time", "% total time", "net mem alloc", "peak mem alloc"],
          col_lengths=[max(4, *[len(key.__repr__()) for key,val in states]), 10, 12, 12, 15, 20, 20],
          do_print=True,
          eol=""
        )

        # print(f"{'name':<50}|{'repeats':<10}|{'average time':<12}|{'total time':<12}|{'% total time':<15}|{'net mem alloc':<20}|{'peak mem alloc':<20}")
        # print(f" {'*'*48} | {'*'*8} | {'*'*10} | {'*'*10} | {'*'*13} | {'*'*18} | {'*'*18} ")
         
        for k, v in states:
          avg_time = np.round(np.mean([s.elapsed_time for s in v]), 8)
          tot_time = np.round(np.sum([s.elapsed_time for s in v]), 8)
          net_mem_alloc = min([s.net_memory_allocated for s in v]), max([s.net_memory_allocated for s in v])
          peak_mem_alloc = min([s.peak_memory_allocated for s in v]), max([s.peak_memory_allocated for s in v])
          net_mem_alloc = " - ".join([convert_bytes(i) for i in net_mem_alloc])
          peak_mem_alloc = " - ".join([convert_bytes(i) for i in peak_mem_alloc])
          relative_time = np.round(100*tot_time/total_runtime, 2)
          logger.add_row([k.__repr__(), len(v), avg_time, tot_time, relative_time, net_mem_alloc, peak_mem_alloc])
          # print(f"{k.__repr__():<50.50}|{len(v):<10}|{avg_time:<12.12}|{tot_time:<12.12}|{100*np.round(tot_time/total_runtime, 2):<15.15}|{net_mem_alloc:<20.20}|{peak_mem_alloc:<20.20}")
      for ally in self._allies:
        print()
        ally.summarize()
        # ally.disable()


  def summarize_to_file(self, path):
    if self._enabled:
      self.clear_states()
      lines = ["", f"##### {str(datetime.now())}"]
      
      for context in self._states:
        if context in self._disabled_context:
          continue
        states = list(self._states[context].items())
        states = sorted(states, key= lambda x: np.sum([s.elapsed_time for s in x[1]]), reverse=True)
        total_runtime = np.sum([ np.sum([s.elapsed_time for s in i[1]]) for i in states])
        if len(states) == 0:
          continue
        # state = sorted(state, key= lambda x: np.sum(x[1]), reverse=True)
        # total = np.sum([ np.sum(i[1]) for i in state])
        lines.append(f"###### {self.name}::{context}: (total runtime {np.round(total_runtime, 8)}s)")
        # lines.append(f"{'name':<50}|{'repeats':<10}|{'average time':<12}|{'total time':<12}|{'% total time':<15}|{'net mem alloc':<20}|{'peak mem alloc':<20}")
        # lines.append(f" {'*'*48} | {'*'*8} | {'*'*10} | {'*'*10} | {'*'*13} | {'*'*18} | {'*'*18} ")
        logger = TableLogger(
          col_labels=["name", "repeats", "average time", "total time", "% total time", "net mem alloc", "peak mem alloc"],
          col_lengths=[max(4, *[len(key.__repr__()) for key,val in states]), 10, 12, 12, 15, 20, 20],
          do_print=False,
          eol=""
        )
        lines.append(logger.title_line)
        lines.append(logger.dash_line)
        for k, v in states:
          avg_time = np.round(np.mean([s.elapsed_time for s in v]), 8)
          tot_time = np.round(np.sum([s.elapsed_time for s in v]), 8)
          net_mem_alloc = min([s.net_memory_allocated for s in v]), max([s.net_memory_allocated for s in v])
          peak_mem_alloc = min([s.peak_memory_allocated for s in v]), max([s.peak_memory_allocated for s in v])
          net_mem_alloc = " - ".join([convert_bytes(i) for i in net_mem_alloc])
          peak_mem_alloc = " - ".join([convert_bytes(i) for i in peak_mem_alloc])
          relative_time = np.round(100*tot_time/total_runtime, 2)
          line = logger.add_row([k.__repr__(), len(v), avg_time, tot_time, relative_time, net_mem_alloc, peak_mem_alloc])
          lines.append(line)
          # lines.append(f"{k.__repr__():<50.50}|{len(v):<10}|{avg_time:<12.12}|{tot_time:<12.12}|{100*np.round(tot_time/total_runtime, 2):<15.15}|{net_mem_alloc:<20.20}|{peak_mem_alloc:<20.20}")
          
        lines.append("")
      
      with open(path, "a") as f:
        f.write("\n".join(lines))

      for ally in self._allies:
        ally.summarize_to_file(path)
        ally.disable()

  def visualize(self, path, figsize=(1920, 960) ):
    if self._enabled:
      all_profilers = [self] + self.allies 
      # all_enabled_context = [timer for timer in all_timers]
      all_enabled_context = []
      for profiler_id, profiler in enumerate(all_profilers):
        profiler.clear_states()
        all_enabled_context += [(profiler_id, context) for context in profiler._states if context not in profiler._disabled_context and len(profiler._states[context]) > 0]
        
      px = 1 / plt.rcParams['figure.dpi']
      # fig = plt.figure()
      # axes = []
      fig, axes = plt.subplots(len(all_enabled_context), 1, sharex=True, sharey=True)
      fig.subplots_adjust(bottom=0.05, top=1.0, hspace=0.1)
      fig.set_figwidth(figsize[0] * px)
      fig.set_figheight(figsize[1] * px)
      ax_height = 1.0 / len(all_enabled_context)
      for context_id, (profiler_id, context) in enumerate(all_enabled_context):
        profiler = all_profilers[profiler_id]
        # ax = fig.add_axes(
        #   [0.1, context_id*ax_height, 0.8, ax_height], 
        #   # xticklabels=[], 
        #   # yticklabels=[], 
        #   # ylabel=f"{profiler.name}::{context}"
        # )
        # axes.append(ax)
        ax = axes[context_id]
        def covert_ms(ms):
          mins = ms // 60000
          secs = (ms % 60000) // 1000
          milsecs = (ms % 60000) % 1000
          return f"{mins}:{secs}:{milsecs} ms"

        # fig.add_artist(lines.Line2D([0, 1], [(context_id)*ax_height, (context_id)*ax_height] ))
        # ax = axes[context_id]
        # ax.xticks([])
        # ax.set_ylabel(context)
        # ax.set_title(f"{profiler.name}::{context}", loc="left", fontdict={'fontsize':11}, pad=-15)
        states = list(profiler._states[context].items())
        for seg_name, seg_states in states:
          fill_color = list(np.random.choice(range(96, 200), size=3).astype("float") / 255)
          xs = []
          ys = []
          mask = []
          for state_id, state in enumerate(seg_states):
            xs += [state.start_time, state.end_time, state.end_time+1e-6]
            ys += [state.memory_allocated_start, state.memory_allocated_end, 0]
            mask += [True, True, False]
            # if state_id == 0:
            #   ax.fill_between(x, 0, y, color=fill_color, label=seg_name)
            # else:
            #   ax.fill_between(x, 0, y, color=fill_color, label=seg_name)
        # ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
          ax.fill_between(xs, 0, ys, where=mask,color=fill_color, label=seg_name)
        # ax.xaxis.set_major_formatter(lambda x, pos: covert_ms(x))
        # ax.yaxis.set_major_formatter(lambda y, pos: convert_bytes(y))
        plt.text(
          0, 
          1 - (context_id+1)*ax_height + ax_height / 2, 
          # (context_id+1)*ax_height - ax_height / 2, 
          s=f"{profiler.name}\n::{context}", 
          wrap=True, 
          fontsize=11, 
          transform=fig.transFigure,
        )
        handles, labels = ax.get_legend_handles_labels()
        interactive_legend = InteractiveLegendPlugin(
          zip(handles, ax.collections),
          labels,
          ax=ax,
          alpha_unsel=0.5,
          alpha_over=1.5, 
          font_size=10,
          start_visible=True)
        
        mpld3.plugins.connect(fig, interactive_legend)
      axes[0].get_shared_x_axes().join(*axes)
      axes[0].get_shared_y_axes().join(*axes)
      # fig.savefig(path)
      mpld3.save_html(fig, path)

  def visualize_(self, path, figsize=(1920, 960) ):
    if self._enabled:
      all_profilers = [self] + self.allies 
      # all_enabled_context = [timer for timer in all_timers]
      all_enabled_context = []
      for profiler_id, profiler in enumerate(all_profilers):
        profiler.clear_states()
        all_enabled_context += [(profiler_id, context) for context in profiler._states if context not in profiler._disabled_context and len(profiler._states[context]) > 0]
        
      px = 1 / plt.rcParams['figure.dpi']
      # fig = plt.figure(figsize=figsize)
      fig = plt.figure()
      axes = []
      # fig, axes = plt.subplots(len(all_enabled_context), 1, sharex=True, sharey=True)
      fig.subplots_adjust(bottom=0.05, top=1.0, hspace=0.1)
      fig.set_figwidth(figsize[0] * px)
      fig.set_figheight(figsize[1] * px)
      ax_height = 1.0 / len(all_enabled_context)
      for context_id, (profiler_id, context) in enumerate(all_enabled_context):
        profiler = all_profilers[profiler_id]
        ax = fig.add_axes(
          [0.1, context_id*ax_height, 0.8, ax_height], 
          # xticklabels=[], 
          # yticklabels=[], 
          # ylabel=f"{profiler.name}::{context}"
        )
        axes.append(ax)
        # ax = axes[context_id]
        def covert_ms(ms):
          mins = ms // 60000
          secs = (ms % 60000) // 1000
          milsecs = (ms % 60000) % 1000
          return f"{mins}:{secs}:{milsecs} ms"

        # fig.add_artist(lines.Line2D([0, 1], [(context_id)*ax_height, (context_id)*ax_height] ))
        # ax = axes[context_id]
        # ax.xticks([])
        # ax.set_ylabel(context)
        # ax.set_title(f"{profiler.name}::{context}", loc="left", fontdict={'fontsize':11}, pad=-15)
        states = list(profiler._states[context].items())
        for seg_name, seg_states in states:
          fill_color = list(np.random.choice(range(96, 200), size=3).astype("float") / 255)
          xs = []
          ys = []
          mask = []
          for state_id, state in enumerate(seg_states):
            xs += [state.start_time, state.end_time, state.end_time+1e-6]
            ys += [state.memory_allocated_start, state.memory_allocated_end, 0]
            mask += [True, True, False]
            # if state_id == 0:
            #   ax.fill_between(x, 0, y, color=fill_color, label=seg_name)
            # else:
            #   ax.fill_between(x, 0, y, color=fill_color, label=seg_name)
        # ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
          ax.fill_between(xs, 0, ys, where=mask,color=fill_color, label=seg_name)
        # ax.xaxis.set_major_formatter(lambda x, pos: covert_ms(x))
        # ax.yaxis.set_major_formatter(lambda y, pos: convert_bytes(y))
        plt.text(
          0, 
          # 1 - (context_id+1)*ax_height + ax_height / 2, 
          (context_id+1)*ax_height - ax_height / 2, 
          s=f"{profiler.name}\n::{context}", 
          wrap=True, 
          fontsize=11, 
          transform=fig.transFigure,
        )
        handles, labels = ax.get_legend_handles_labels()
        interactive_legend = InteractiveLegendPlugin(
          zip(handles, ax.collections),
          labels,
          ax=ax,
          alpha_unsel=0.5,
          alpha_over=1.5, 
          font_size=10,
          start_visible=True)
        
        mpld3.plugins.connect(fig, interactive_legend)
      axes[0].get_shared_x_axes().join(*axes)
      axes[0].get_shared_y_axes().join(*axes)
      # fig.savefig(path)
      mpld3.save_html(fig, path)