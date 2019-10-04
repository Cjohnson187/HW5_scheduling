"""
HW5 Scheduling
9/30/19
Chris Johnson
"""
import re
from collections import deque


###########################################################################


def read_file(processes_file, output_file):

    r_processes = dict(dict())

    for line in processes_file:
        stripped_line = line.rstrip('\n')
        stripped_line = stripped_line.rstrip(' ')
        line_read = stripped_line.split(",")
        process_key = int(re.sub('\D', '', line_read[0]))

        r_processes[process_key] = { 'process_id'   : line_read[0],
                                     'arrival_time' : int(line_read[1]),
                                     'priority'     : int(line_read[2]),
                                     'cpu_burst'    : int(line_read[3]) }

    for keys in r_processes:
        output_file.write(str(r_processes[keys]['process_id'])+ ","+
              str(r_processes[keys]['arrival_time'])+ ","+
              str(r_processes[keys]['priority'])+ ","+
              str(r_processes[keys]['cpu_burst'])+ "\n")
    output_file.write('\n')
    return r_processes


###############################################################################


def order(processes, val_to_sort, high_low):

    ordered_processes = dict(dict())

    if high_low == "highest_first" :
        ordered_list_of_keys = sorted(processes.keys(), key=lambda k: processes[k][val_to_sort], reverse = True)
    else:
        ordered_list_of_keys = sorted(processes.keys(), key=lambda k: processes[k][val_to_sort])

    for i in range(len(processes)):
        ordered_processes[i+1] = processes[ordered_list_of_keys[i]]

    return ordered_processes


############################################################################


def print_current_process(current_time, current_process_id, output_file):
    output_file.write('At time '+ str(current_time)+  ' ms '+ 'CPU starts running process '+ current_process_id+ ',\n')


#################################################################


def np_SJF(processes, current_time, output_file):

    if processes != {}:
        processes_with_current_time = dict(dict())
        ordered_processes = order(processes, "cpu_burst", "not_needed")

        try:
            for keys in ordered_processes:
                if ordered_processes[keys]["arrival_time"] <= current_time:
                    processes_with_current_time[keys] = ordered_processes[keys]
            sorted_processes_with_current_time = order(processes_with_current_time, "cpu_burst", "not_needed")
            print_current_process(current_time, sorted_processes_with_current_time[1]['process_id'], output_file)
            current_time += sorted_processes_with_current_time[1]['cpu_burst']

            p_id_to_delete = sorted_processes_with_current_time[1]['process_id']
            key_to_delete = None
            for keys in processes:
                if p_id_to_delete == processes[keys]['process_id']:
                    key_to_delete = keys
            del processes[key_to_delete]

            np_SJF(processes, current_time, output_file)

        except Exception as e:
            print('exception = ', e)
            #pass

    else:
        pass


#############################################################################


def np_priority_scheduling(processes, current_time, output_file):
    if processes != {}:
        processes_with_current_time = dict(dict())
        ordered_processes = order(processes, "priority", "highest_first")
        new_sorted_processes_with_current_time = dict(dict())

        try:
            for keys in ordered_processes:
                if ordered_processes[keys]["arrival_time"] <= current_time:
                    processes_with_current_time[keys] = ordered_processes[keys]

            sorted_processes_with_current_time = order(processes_with_current_time, "priority", "highest_first")

            priority_value = sorted_processes_with_current_time[1]["priority"]
            for keys in sorted_processes_with_current_time:
                if sorted_processes_with_current_time[keys]["priority"] == priority_value:
                    new_sorted_processes_with_current_time[keys] = sorted_processes_with_current_time[keys]

            if len(new_sorted_processes_with_current_time) > 1 and new_sorted_processes_with_current_time != {}:
                sorted_processes_with_current_time = order(new_sorted_processes_with_current_time, "arrival_time", " ! highest_first")

            print_current_process(current_time, sorted_processes_with_current_time[1]['process_id'], output_file)
            current_time += sorted_processes_with_current_time[1]['cpu_burst']

            p_id_to_delete = sorted_processes_with_current_time[1]['process_id']
            key_to_delete = None
            for keys in processes:
                if p_id_to_delete == processes[keys]['process_id']:
                    key_to_delete = keys
            del processes[key_to_delete]

            np_priority_scheduling(processes, current_time, output_file)

        except Exception as e:
            print('exception = ', e)
            pass

    else:
        pass


##############################################################################


def round_robin(processes, current_time, que, quantum, buffer, output_file):

    keys_to_delete = []
    processes_with_current_time = dict(dict())
    ordered_processes = dict(dict())

    if processes:
        ordered_processes = order(processes, "arrival_time", "not_needed")

    for keys in ordered_processes:
        if ordered_processes[keys]["arrival_time"] <= current_time:
            processes_with_current_time[keys] = ordered_processes[keys]
            keys_to_delete.append(keys)

    for items in keys_to_delete:
        del ordered_processes[items]

    for keys in processes_with_current_time:
        que.append(processes_with_current_time[keys])

    while buffer:
        que.append(buffer.popleft())

    if que:
        current_process = que.popleft()
        print_current_process(current_time, current_process['process_id'], output_file)

        if current_process['cpu_burst'] == quantum:
            current_time += quantum
        elif current_process['cpu_burst'] <= quantum:
            current_time += current_process['cpu_burst']
        elif current_process['cpu_burst'] >= quantum:
            current_process['cpu_burst'] -= quantum
            current_time += quantum
            buffer.append(current_process)

    if que or buffer or processes:
        round_robin(ordered_processes, current_time, que, quantum, buffer, output_file)


###############################################################################


if __name__ == '__main__':

    output_file = open('testResults.txt', 'w+')

    processes_file = open('processes.txt', 'r')
    processes = read_file(processes_file, output_file)
    processes_file.close()

    processes_priority = processes.copy()
    processes_RR = processes.copy()

    current_time_sjf = 0
    output_file.write('---Scheduling results of non preemptive Shortest Job First\n')
    np_SJF(processes, current_time_sjf, output_file)
    output_file.write('---End of the results of non preemptive Shortest Job First\n\n')

    current_time_p = 0
    output_file.write('---Scheduling results of non preemptive Priority\n')
    np_priority_scheduling(processes_priority, current_time_p, output_file)
    output_file.write('---End of the results of non preemptive Priority\n\n')

    current_time_RR = 0
    quantum = 10
    que = deque()
    buffer = deque()
    output_file.write('---Scheduling results of Round Robin\n')
    round_robin(processes_RR, current_time_RR, que,  quantum, buffer, output_file)
    output_file.write('---End of the results of Round Robin\n\n')

    output_file.close()