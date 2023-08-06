""" The long lasting worker thread as demo - just wait some time and create data periodically
Copyright Nanosurf AG 2021
License - MIT
"""
import time
import math
from PySide2.QtCore import Signal
from app import app_common, background_worker, module_base
from modules.demo_module import settings

class MyWorkerData(background_worker.WorkerData):
    def __init__(self):
        self.value = []
        self.last_index = -1

class MyWorker(background_worker.SingleRunWorker):
    
    sig_tick = Signal() # is emitted if par_send_tick is True

    """ parameter for the background work"""
    par_repetition = 10
    par_time_per_repetition = 2.0
    par_send_ticks = True
    par_time_between_ticks = 0.1
    par_plot_func_id = settings.PlotStyleID.PlotSin

    def __init__(self, my_module: module_base.ModuleBase):
        super().__init__(my_module)

    def do_work(self):
        """ This is the working funcition for the long task"""
        self.resulting_data = MyWorkerData()

        self.count = 0
        while (self.count < self.par_repetition) and not self.stop_request_flag:
            self.count += 1

            if self.par_send_ticks:
                self.tick_time = 0.0
                while self.tick_time < self.par_time_per_repetition and not self.stop_request_flag:
                    self.tick_time += self.par_time_between_ticks
                    time.sleep(self.par_time_between_ticks)
                    self.sig_tick.emit()
                    self.send_message(f"Tick: {self.tick_time:.2f}s")
            else:
                time.sleep(self.par_time_per_repetition)        
            
            if self.par_plot_func_id.value == settings.PlotStyleID.PlotSin:
                self.resulting_data.value.append(math.sin(self.count / self.par_repetition * math.pi))
            elif self.par_plot_func_id.value == settings.PlotStyleID.PlotCos:
                self.resulting_data.value.append(math.cos(self.count / self.par_repetition * math.pi))
            else:
                self.send_message("Unknown plot style", app_common.MsgType.Error)

            self.resulting_data.last_index += 1
            self.sig_new_data.emit()

    def get_result(self) -> MyWorkerData:
        return self.resulting_data

 