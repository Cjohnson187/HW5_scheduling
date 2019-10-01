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

        '''
        print('line_read = ', line_read)
        print ('process_id 0 = ', line_read[0],
            '\narrival_time 1= ', line_read[1],
            '\npriority 2= ', line_read[2],
            '\ncpu_burst 3= ', line_read[3])
        '''

        r_processes[process_key] = {
                                    'process_id' : line_read[0],
                                    'arrival_time' : int(line_read[1]),
                                    'priority' : int(line_read[2]),
                                    'cpu_burst' : int(line_read[3])
                                    }

    for keys in r_processes:
        print(r_processes[keys]['process_id'], ",",
              r_processes[keys]['arrival_time'], ",",
              r_processes[keys]['priority'], ",",
              r_processes[keys]['cpu_burst'] )

    return r_processes

###############################################################################
#
#
#   TODO method to print output of each scheduling process ->
#   ---Scheduling results of <name of the scheduling algorithm>
#   At time <…> ms, CPU starts running process <process ID>,
#   at time <…> ms, CPU starts running process <process ID>,
#   at time <…> ms, CPU starts running process <process ID>,
#
#
###############################################################################


def order(processes, val_to_sort, high_low):

    ordered_processes = dict(dict())

    if high_low == "highest_first" :
        ordered_list_of_keys = sorted(processes.keys(), key=lambda k: processes[k][val_to_sort], reverse = True)
        #print("highest first")
    else:
        ordered_list_of_keys = sorted(processes.keys(), key=lambda k: processes[k][val_to_sort])
    '''
    #print("new_dict   =   ", ordered_list_of_keys)
    #print('val to  sort = ', val_to_sort)
    #print("new_dict 2 priority  =   ", ordered_list_of_keys[2])
    '''

    for i in range(len(processes)):
        ordered_processes[i+1] = processes[ordered_list_of_keys[i]]
    '''
    print('ordered processes new dict = ', ordered_processes)
    for keys1 in ordered_processes:
        print (val_to_sort,' = ', ordered_processes[keys1]["process_id"], ordered_processes[keys1][val_to_sort])
    '''

    return ordered_processes


############################################################################


def print_process(current_time, current_process_id):
    print('At time ', current_time,  ' ms', 'CPU starts running process ', current_process_id, ',')


#################################################################

# TODO non preemptive short job first  (SJF)

def np_SJF(processes, queue, current_time):

    new_processes = dict(dict())
    final_ordered_processes = dict(dict())
    sorted_processes_with_current_time = dict(dict())

    processes_with_current_time = processes
    processes_after_process_pop = processes

    #current_time = 0

    for keys in processes:
        if processes[keys]["cpu_burst"] <= current_time:
            processes_with_current_time[keys] = processes[keys]
            del processes[keys]
#            sorted_processes_with_current_time = order(processes_with_current_time, "cpu_burst", "not_needed")

    if len(processes_with_current_time) > 1:
        final_ordered_processes = order(processes_with_current_time, "cpu_burst", "not_needed")

    for keys in final_ordered_processes:
        print()




#############################################################################


# TODO non preemptive priority scheduling

def np_Preemptive_scheduling(processes):
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



    if processes == {}:
        print("cowabunga dude")

    sorted_processes = order(processes, "cpu_burst", "highest_firs")
    print("size of processes dict = ", len(sorted_processes))
    #del sorted_processes[2]
    for keys in sorted_processes:
        print("keys = ", keys, " | sorted process key = ", sorted_processes[keys])