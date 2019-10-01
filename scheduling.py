"""
HW5 Scheduling
9/30/19
Chris Johnson
"""
import re
from queue import Queue


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

    if high_low == " -highest_first- " :
        ordered_list_of_keys = sorted(processes.keys(), key=lambda k: processes[k][val_to_sort], reverse = True)
        print("highest first")
    else:
        ordered_list_of_keys = sorted(processes.keys(), key=lambda k: processes[k][val_to_sort])

    for i in range(len(processes)):
        ordered_processes[i+1] = processes[ordered_list_of_keys[i]]

    return ordered_processes


############################################################################


def print_current_process(current_time, current_process_id):
    print('At time ', current_time,  ' ms', 'CPU starts running process ', current_process_id, ',')


#################################################################


def np_SJF(processes, current_time):

    if processes != {}:
        processes_with_current_time = processes
        ordered_processes = order(processes_with_current_time, "cpu_burst", "not_needed")

        try:
            for keys in ordered_processes:
                if ordered_processes[keys]["arrival_time"] <= current_time:
                        print_current_process(current_time, ordered_processes[keys]['process_id'])
                        new_current_time = current_time + ordered_processes[keys]['cpu_burst']
                        del ordered_processes[keys]
                        np_SJF(ordered_processes, new_current_time)

        except Exception as e:
            pass
#            Todo -- ignore exception for "dictionary changed size during iteration"
#            print('exception in sjf = ', e)

    else:
        print("\n---   scheduling completed!   ---")


#############################################################################


# TODO non preemptive priority scheduling

def np_preemptive_scheduling(processes):
    print("in np_pre_pri_sched")


##############################################################################


# TODO Round Robin (RR) scheduling (10 milliseconds)

def round_robin(processes):
    print("in round robin")

################################################################################


# TODO run on class server

if __name__ == '__main__':

    processes_file = open('processes.txt', 'r')
    processes = read_file(processes_file)
    processes_file.close()

    queue = []
    current_time = 0

    np_SJF(processes, current_time)

    if processes == {}:
        print("cowabunga dude")





    # TODO run on class server
