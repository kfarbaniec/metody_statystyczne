import numpy as np
from matplotlib import pyplot as plt


class Events:
    empty = True

    def __init__(self):
        self.t_arr_cumul = [0]  # task arrival time
        self.t_serv = [0]
        self.t_in = [0]  # task input time
        self.t_out = [0]  # task out time
        self.t_marked = [0]
        self.tasks_in_sys = [0]
        self.time_in_sys = None
        self.task_queue = None

    def add_event(self, t_arrive, t_service):
        #         if self.empty:
        #             self.empty = not self.empty
        self.t_arr_cumul.append(self.t_arr_cumul[-1] + t_arrive)
        self.t_serv.append(t_service)
        self.t_in.append(max(t_arrive + self.t_arr_cumul[-1], self.t_out[-1]))
        self.t_out.append(t_service + self.t_in[-1])

    def prepare_total_marked(self):
        t_marked = np.ones((len(self.t_arr_cumul) + len(self.t_out), 2))
        show_up_stamp = 0
        out_stamp = 1

        for idx, k in enumerate(self.t_arr_cumul):
            t_marked[idx, 0] = k
            t_marked[idx, 1] = show_up_stamp
        offset = len(self.t_arr_cumul)

        for idx, k in enumerate(self.t_out):
            t_marked[offset + idx, 0] = k
            t_marked[offset + idx, 1] = out_stamp
        ind = np.argsort(t_marked[:, 0]);
        self.t_marked = t_marked[ind]

    def calc_tasks_in_sys(self):
        tasks_in_system = np.zeros(len(self.t_marked))
        last_gen_idx = 0
        for idx, ev in enumerate(self.t_marked):
            if ev[1] == 0:
                tasks_in_system[idx] = tasks_in_system[idx - 1] + 1
                last_gen_idx = idx
            else:
                tasks_in_system[idx] = tasks_in_system[idx - 1] - 1
        self.tasks_in_sys = tasks_in_system

    def plot_tasks_in_sys(self, a=0, b=50):
        # plt.plot(total_marked[:last_gen_idx,0], tasks_in_system[:last_gen_idx])
        plt.plot(self.t_marked[:, 0], self.tasks_in_sys)
        plt.title("Total tasks in system")
        plt.xlabel("time [minutes]")
        plt.ylabel("tasks count")
        plt.show()
        plt.scatter(self.t_marked[a:b, 0], self.tasks_in_sys[a:b])
        plt.title("Tasks in system partial")
        plt.xlabel("time [minutes]")
        plt.ylabel("tasks count")
        plt.show()

    def calc_time_in_sys(self):
        time_in_sys = np.ones(len(self.t_arr_cumul))
        for idx, arr in enumerate(self.t_arr_cumul[1:]):
            time_in_sys[idx] = self.t_out[idx + 1] - arr
        self.time_in_sys = time_in_sys

    def prepare_queue(self):
        t_queue = np.ones((len(self.t_arr_cumul) + len(self.t_in), 2))
        show_up_stamp = 0
        in_stamp = 1

        for idx, k in enumerate(self.t_arr_cumul):
            t_queue[idx, 0] = k
            t_queue[idx, 1] = show_up_stamp
        offset = len(self.t_arr_cumul)

        for idx, k in enumerate(self.t_in):
            t_queue[offset + idx, 0] = k
            t_queue[offset + idx, 1] = in_stamp
        ind = np.argsort(t_queue[:, 0]);
        self.t_queue = t_queue[ind]

    def calc_queue(self, show_up_stamp=0, in_stamp=1):
        tasks_in_queue = np.zeros(len(self.t_queue))
        last_gen_idx = 0
        for idx, ev in enumerate(self.t_queue):
            if ev[1] == show_up_stamp:
                tasks_in_queue[idx] = tasks_in_queue[idx - 1] + 1
                last_gen_idx = idx
            else:
                tasks_in_queue[idx] = tasks_in_queue[idx - 1] - 1
        self.task_queue = tasks_in_queue