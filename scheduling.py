"""
HW5 Scheduling
9/30/19
Chris Johnson
"""
import re


# TODO read text file containing processes for stack processes.txt [P3, 5, 8, 20}
    #<process ID>, <arrival time>, <priority>, <CPU burst>


# TODO print values read from file in format below, format below is order of arrival ->
    #   P3, 5, 8, 20
    #   P4, 9, 3, 50
    #   P1, 9, 7, 35



###########################################################################

def read_file(processes_file):

    r_processes = dict(dict())

    for line in processes_file:
        stripped_line = line.rstrip('\n')
        stripped_line = stripped_line.rstrip(' ')
        line_read = stripped_line.split(",")
        process_key = int(re.sub('\D', '', line_read[0]))

        r_processes[process_key] = {
                                    'process_id' : line_read[0],
                                    'arrival_time' : line_read[1],
                                    'priority' : line_read[2],
                                    'cpu_burst' : line_read[3]
                                    }

    for keys in r_processes:
        print(r_processes[keys]['process_id'] + ",",
              r_processes[keys]['arrival_time'] + ",",
              r_processes[keys]['priority'] + ",",
              r_processes[keys]['cpu_burst'] )


    return r_processes

###############################################################################

# TODO method to find lowest value in specific spot of array

# TODO method to search processes for values that are greater or equal to current time

# TODO method to print output of each scheduling process ->
    # ---Scheduling results of <name of the scheduling algorithm>
    # At time <…> ms, CPU starts running process <process ID>,
    # at time <…> ms, CPU starts running process <process ID>,
    # at time <…> ms, CPU starts running process <process ID>,
    # ……
    # ---End of the results of <name of the scheduling algorithm>



############################################################################


# TODO non preemptive short job first  (SJF)

def np_SJF(processes):

    print("in sjf")



# TODO non preemptive priority scheduling

def np_Preemptive_scheduling(processes):
    print("in np_pre_pri_sched")



# TODO Round Robin (RR) scheduling (10 milliseconds)

def round_robin(processes):
    print("in round robin")



################################################################################



# TODO run on class server

if __name__ == '__main__':

    processes_file = open('processes.txt', 'r')
    processes = read_file(processes_file)
    processes_file.close()
    # processes is a dictionary inside dictionary
    # 1st key is p ID number second id name like process id or cpu burst


