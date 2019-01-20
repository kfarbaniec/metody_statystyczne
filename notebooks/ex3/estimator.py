

class Estimator:


    @staticmethod
    def estimate_x(t_marked_0_col, tasks_in_sys):
        """ function to estimate overall events in system"""
        assert len(t_marked_0_col) == len(tasks_in_sys)

        estimated = list(tasks_in_sys)
        tasks = list(tasks_in_sys)
        time_diffs = list(tasks_in_sys)

        for idx, task in enumerate(tasks_in_sys):
            if idx == len(tasks_in_sys) - 1:
                break
            tasks[idx] = task
            time_diffs[idx] = t_marked_0_col[idx + 1] - t_marked_0_col[idx]
        tasks = tasks[:-1]
        time_diffs = time_diffs[:-1]
        mults = [a * b for a, b in zip(tasks, time_diffs)]

        for idx, m in enumerate(mults):
            if idx == 0:
                continue
            else:
                estimated[idx] = sum(mults[:idx]) / t_marked_0_col[idx]

        return estimated[3:-1]

    @staticmethod
    def estimate_R(R):
        """
        function to estimate overall time in system per task

        :param R: time per task
        """
        #     assert len(t_arr_cumul) == len(R), "Must have equal length"
        estimated = list(R)
        vals = list(R)
        for idx, t in enumerate(R):
            vals[idx] = t
            if len(vals[:idx]) == 0:
                continue
            else:
                estimated[idx - 1] = sum(vals[:idx]) / (len(vals[:idx]) + 0.0001)
        return estimated[:-1]

    @staticmethod
    def estimate_xw(t_queue_0_col, x_w):
        """ function to estimate tasks in queue"""
        assert len(t_queue_0_col) == len(x_w)

        estimated = list(x_w)
        queued = list(x_w)
        time_diffs = list(x_w)

        for idx, queue in enumerate(x_w):
            if idx == len(x_w) - 1:
                break
            queued[idx] = queue
            time_diffs[idx] = t_queue_0_col[idx + 1] - t_queue_0_col[idx]
        queued = queued[:-1]
        time_diffs = time_diffs[:-1]
        mults = [a * b for a, b in zip(queued, time_diffs)]

        for idx, m in enumerate(mults):
            if idx == 0:
                continue
            else:
                estimated[idx] = sum(mults[:idx]) / t_queue_0_col[idx]

        return estimated[3:-1]
