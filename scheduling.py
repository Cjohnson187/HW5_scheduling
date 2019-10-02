"""
HW5 Scheduling
9/30/19
Chris Johnson
"""
import re
from collections import deque


###########################################################################


def read_file(processes_file):

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
        print(r_processes[keys]['process_id'], ",",
              r_processes[keys]['arrival_time'], ",",
              r_processes[keys]['priority'], ",",
              r_processes[keys]['cpu_burst'])
    print()
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


def print_current_process(current_time, current_process_id):
    print('At time ', current_time,  ' ms', 'CPU starts running process', current_process_id, ',')


#################################################################


def np_SJF(processes, current_time):

    if processes != {}:
        processes_with_current_time = dict(dict())
        ordered_processes = order(processes, "cpu_burst", "not_needed")

        try:
            for keys in ordered_processes:
                if ordered_processes[keys]["arrival_time"] <= current_time:
                    processes_with_current_time[keys] = ordered_processes[keys]
            sorted_processes_with_current_time = order(processes_with_current_time, "cpu_burst", "not_needed")
            print_current_process(current_time, sorted_processes_with_current_time[1]['process_id'])
            current_time += sorted_processes_with_current_time[1]['cpu_burst']

            p_id_to_delete = sorted_processes_with_current_time[1]['process_id']
            key_to_delete = None
            for keys in processes:
                if p_id_to_delete == processes[keys]['process_id']:
                    key_to_delete = keys
            del processes[key_to_delete]

            np_SJF(processes, current_time)

        except Exception as e:
            pass
#            print('exception in sjf = ', e)

    else:
        print("\n---   scheduling completed!   ---\n")


#############################################################################


def np_priority_scheduling(processes, current_time):
    if processes != {}:
        processes_with_current_time = dict(dict())
        ordered_processes = order(processes, "cpu_burst", "highest_first")
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

            print_current_process(current_time, sorted_processes_with_current_time[1]['process_id'])
            current_time += sorted_processes_with_current_time[1]['cpu_burst']

            p_id_to_delete = sorted_processes_with_current_time[1]['process_id']
            key_to_delete = None
            for keys in processes:
                if p_id_to_delete == processes[keys]['process_id']:
                    key_to_delete = keys
            del processes[key_to_delete]

            np_priority_scheduling(processes, current_time)

        except Exception as e:
            pass
#            print('exception in sjf = ', e)

    else:
        print("\n---   scheduling completed!   ---\n")


##############################################################################


def round_robin(processes, current_time, q, quantum):

    ordered_processes = dict(dict())
    new_ordered_processes = dict(dict())
    second_check = False

    if processes != {}:
        ordered_processes = order(processes, "arrival_time", "not_needed")
        if ordered_processes[1]['arrival_time'] <= current_time:
            q.append(ordered_processes[1])
            del ordered_processes[1]

    current_process = q.popleft()

    print_current_process(current_time, current_process['process_id'])

    if current_process['cpu_burst'] > quantum:
        current_process['cpu_burst'] -= quantum
        current_time += quantum

        if ordered_processes != {}:
            new_ordered_processes = order(ordered_processes, "arrival_time", "not_needed")
            if new_ordered_processes[1]['arrival_time'] <= current_time:
                q.append(new_ordered_processes[1])
                del new_ordered_processes[1]
                second_check = True
        q.append(current_process)

    elif current_process['cpu_burst'] < quantum:
        current_time += current_process['cpu_burst']

        if ordered_processes != {}:
            new_ordered_processes = order(ordered_processes, "arrival_time", "not_needed")
            if new_ordered_processes[1]['arrival_time'] <= current_time:
                q.append(new_ordered_processes[1])
                del new_ordered_processes[1]
                second_check = True

    elif current_process['cpu_burst'] == quantum:
        current_time += quantum

        if ordered_processes != {}:
            new_ordered_processes = order(ordered_processes, "arrival_time", "not_needed")
            if new_ordered_processes[1]['arrival_time'] <= current_time:
                q.append(new_ordered_processes[1])
                del new_ordered_processes[1]
                second_check = True

    if len(q) > 0 and second_check == True:
        round_robin(new_ordered_processes, current_time, q, quantum)
    elif len(q) > 0 and second_check == False:
        round_robin(ordered_processes, current_time, q, quantum)

    else:
        print("\n---   scheduling completed!   ---\n")


################################################################################


if __name__ == '__main__':

    processes_file = open('processes.txt', 'r')
    processes = read_file(processes_file)
    processes_file.close()

    processes_priority = processes.copy()
    processes_RR = processes.copy()

    current_time_sjf = 0
    np_SJF(processes, current_time_sjf)

    current_time_p = 0
    np_priority_scheduling(processes_priority, current_time_p)

    current_time_RR = 0
    quantum = 10
    q = deque()

    round_robin(processes_RR, current_time_RR, q,  quantum)

    if processes == {}:
        print("cowabunga dude!")


#     TODO run on class server
