# with relin/sym/alg cost
# figure per each test
import sys
import re
import csv
import numpy as np
from math import ceil
from math import isnan
from matplotlib import pyplot as plt

test_label = ["Incremental\n2Sets", "RA-ISAM2\n2Sets", "RA-ISAM2\n4Sets"]
box_color = ['gainsboro','darkgrey','beige','wheat','honeydew', 'lightgreen','limegreen','lightcyan','lightskyblue', 'steelblue']

total_color = ['purple', 'dimgray', 'maroon', 'black']

test_name = ["incremental2", "ra2", "ra4"]

J_ACCEL_THREAD = 1
ACCEL_THREAD = 2
interval = 25

#thread_cycle_storage = [[0 for i in range(len(core_count))] for j in range(num_app)]
#print(num_app, thread_cycle_storage)
#total_cycle_storage = [[0 for i in range(len(core_count))] for j in range(num_app)]

#stat, dynam
test_regex = r"\.*(\w*)_(\w*)(\d)_(\w*)\.*\b"
# these are for total perf line graph
numeric_list = []
step_list = []
relin_list = []
sym_list = []
alg_list = []
total_list = []
total_regex = r"step (\d*) slam total cycle: (\d*)\b"
total2_regex = r"step (\d*) time: (\d+\.\d+) ms\b"
#profile_total_regex = r"step (\d*) node \d* total increment time: (\d*)\b"


end_regex = r"end of test\b"
end1_regex = r"Passed\b"
end_profile_regex = r"done profiling\b"
start_regex = r"create threading\b"

num_thread = []
hw_platform = []
name_list = [] # hw + alg + thread
step_list = []

numeric_this_list = []
step_this_list = []
relin_this_list = []
sym_this_list = []
alg_this_list = []

#total line graph
total_test_list = []
store_step = True
single_profile = False
num_thread = 0
is_accel = False
boom_scale = False

#filename = sys.argv[1]
TARGET = 33
benchmark_input = sys.argv[-1]
if benchmark_input == "m3500":
    TARGET = 31.2

find_test = False

for j in range(len(test_name)):
    testname = test_name[j]+"_"+benchmark_input
    #filename = file_dir+'/'+files[j]
    for filename in sys.argv[1:3]:
        print(filename, testname)
        with open(filename, "r") as f:
            for line in f.readlines():
                end_search = re.search(end_regex, line)
                end1_search = re.search(end1_regex, line)
                test_search = re.search(test_regex, line)
                total_search = re.search(total_regex, line)
                total2_search = re.search(total2_regex, line)

                if total_search and find_test:
                    #step = int(step_search.group(1))
                    this_step = int(total_search.group(1))
                    this_cycles = int(total_search.group(2))
                    numeric_this_list.append(this_cycles)
                    step_this_list.append((this_step+1)*interval)
                elif test_search:
                    hw_platform = test_search.group(1)
                    algorithm = test_search.group(2)
                    num_thread = (test_search.group(3))
                    benchmark = test_search.group(4)
                    if benchmark == benchmark_input and test_name[j] == algorithm+str(num_thread):
                        find_test = True
                        print("found test :", benchmark, test_name[j])
                    else:
                        if find_test == True:
                            find_test = False
                            #break
                        else:
                            find_test = False
                    if find_test == True:
                        name_list.append(benchmark+"_"+algorithm+"_"+hw_platform+num_thread)

                        relin_file = benchmark+"_"+algorithm+"_"+hw_platform+num_thread+"_relin.txt"
                        sym_file = benchmark+"_"+algorithm+"_"+hw_platform+num_thread+"_sym.txt"
                        alg_file = benchmark+"_"+algorithm+"_"+hw_platform+num_thread+"_alg.txt"
                        if benchmark == "cab464":
                            interval = 1
                        else:
                            interval = 25
                        if hw_platform == "spatula" or hw_platform == "old":
                            relin_file = benchmark+"_"+algorithm+"_"+"supernova"+num_thread+"_relin.txt"
                            sym_file = benchmark+"_"+algorithm+"_"+"supernova"+num_thread+"_sym.txt"
                            alg_file = benchmark+"_"+algorithm+"_"+"supernova"+num_thread+"_alg.txt"
                        if hw_platform == "dsp":
                            relin_file = benchmark+"_"+algorithm+"_"+"pi"+num_thread+"_relin.txt"
                            sym_file = benchmark+"_"+algorithm+"_"+"pi"+num_thread+"_sym.txt"
                            alg_file = benchmark+"_"+algorithm+"_"+"pi"+num_thread+"_alg.txt"
                        print(relin_file, sym_file, alg_file)
                        with open("overheads/"+relin_file, 'r') as file:
                            for line in file:
                                relin_this_list.append(int(line.strip()))
                        with open("overheads/"+sym_file, 'r') as file:
                            for line in file:
                                sym_this_list.append(int(line.strip()))
                                if algorithm == "incremental":
                                    alg_this_list.append(0)
                        if algorithm == "ra":
                            with open("overheads/"+alg_file, 'r') as file:
                                for line in file:
                                    alg_this_list.append(int(line.strip()))


                elif end_search and find_test:
                    #numeric_this_list = [numeric_this_list[i]+backsolve_this_list[i] for i in range(len(numeric_this_list))]
                    temp_list = [numeric_this_list[i]+relin_this_list[i]+sym_this_list[i]+alg_this_list[i] for i in range(len(numeric_this_list))]
                    total_list.append(temp_list)
                    numeric_list.append(numeric_this_list[:len(temp_list)])
                    numeric_this_list = []
                    relin_list.append(relin_this_list[:len(temp_list)])
                    relin_this_list = []
                    sym_list.append(sym_this_list[:len(temp_list)])
                    sym_this_list = []
                    alg_list.append(alg_this_list[:len(temp_list)])
                    alg_this_list = []
                    step_list.append(step_this_list[:len(temp_list)])
                    step_this_list = []


#print(len(numeric_list), numeric_list)
#print(len(relin_list), relin_list)
#print(len(sym_list), sym_list)
#print(len(alg_list), alg_list)
#print(step_list)

scaled_list = [np.array(sublist) * 1e-6 for sublist in total_list]
total_list = scaled_list
scaled_list = [np.array(sublist) * 1e-6 for sublist in alg_list]
total_alg_list = scaled_list
scaled_list = [np.array(sublist) * 1e-6 for sublist in sym_list]
total_sym_list = scaled_list
scaled_list = [np.array(sublist) * 1e-6 for sublist in relin_list]
total_relin_list = scaled_list
scaled_list = [np.array(sublist) * 1e-6 for sublist in numeric_list]
total_num_list = scaled_list

'''
division_result = [x / y for x, y in zip(total_relin_list[2], total_relin_list[1])]
#min_value = min(division_result)
min_value = min([x for x in division_result if not isnan(x)])
min_index = division_result.index(min_value)
print("i: ", i, "j: ", j)
print("value: ", min_value, "1-value: ", 1-min_value, "index: ", min_index*interval)
min_value = min([x for x in division_result if (not isnan(x) and x != 0)])
min_index = division_result.index(min_value)
print("i: ", i, "j: ", j)
print("value: ", min_value, "1-value: ", 1-min_value, "index: ", min_index*interval)

division_result = [x / y for x, y in zip(total_sym_list[2], total_sym_list[1])]
#min_value = min(division_result)
min_value = min([x for x in division_result if not isnan(x)])
min_index = division_result.index(min_value)
print("i: ", i, "j: ", j)
print("value: ", min_value, "1-value: ", 1-min_value, "index: ", min_index*interval)
min_value = min([x for x in division_result if (not isnan(x) and x != 0)])
min_index = division_result.index(min_value)
print("i: ", i, "j: ", j)
print("value: ", min_value, "1-value: ", 1-min_value, "index: ", min_index*interval)
'''
for i in range(len(total_list)):
    total_max = max(total_list[i])
    total_avg = sum(total_list[i])/len(total_list[i])
    total_75 = np.percentile(np.array(total_list[i]), 75)
    print(name_list[i], " total: ", total_avg, total_75, total_max)
    total_num_max = max(total_num_list[i])
    total_num_avg = sum(total_num_list[i])/len(total_num_list[i])
    total_num_75 = np.percentile(np.array(total_num_list[i]), 75)
    print(name_list[i], " numeric: ", total_num_avg, total_num_75, total_num_max)
    total_sym_max = max(total_sym_list[i])
    total_sym_avg = sum(total_sym_list[i])/len(total_sym_list[i])
    total_sym_75 = np.percentile(np.array(total_sym_list[i]), 75)
    print(name_list[i], " symbolic: ", total_sym_avg, total_sym_75, total_sym_max)
    total_alg_max = max(total_alg_list[i])
    total_alg_avg = sum(total_alg_list[i])/len(total_alg_list[i])
    total_alg_75 = np.percentile(np.array(total_alg_list[i]), 75)
    print(name_list[i], " algorithm: ", total_alg_avg, total_alg_75, total_alg_max)



# Create the figure and subplots
figure_size = (15, 3.5)
#if file_dir == "cab7k_uartlogs":
#    figure_size = (15,3.5)

fig, axs = plt.subplots(1, 3, figsize=figure_size)
for i in range(len(total_list)):
    ax = axs[i]
    #x = [step_list[i][j] * interval for j in range(len(step_list[i]))]
    x = step_list[i]
    total = total_list[i]
    #ax.plot(x, total, color='black', label='Total')
    relin = total_relin_list[i]
    sym = total_sym_list[i]
    alg = total_alg_list[i]
    num = total_num_list[i]
    #print(len(x), len(total), len(sym), len(relin), len(num))
    # Plot the stacked area for relin, sym, num
    #ax.fill_between(x, total, total + relin, color='blue', alpha=0.5, label='Relin')
    #ax.fill_between(x, total + relin, total + relin + sym, color='green', alpha=0.5, label='Sym')
    #ax.fill_between(x, total + relin + sym, total + relin + sym + num, color='orange', alpha=0.5, label='Num')
    #ax.plot(x, num, color='orange', label='Numeric')
    #ax.plot(x, num+sym, color='green', label='Symbolic')
    #ax.plot(x, num+sym+relin, color='blue', label='Relinearization')


    ax.fill_between(x, 0, num, color='orange', alpha=0.5, label='Numeric')
    ax.fill_between(x, num, num + alg, color='coral', alpha=0.5, label='Algorithm (RA)')
    ax.fill_between(x, num + alg, num + sym + alg, color='green', alpha=0.5, label='Symbolic')
    ax.fill_between(x, num + sym + alg, total, color='blue', alpha=0.5, label='Relinearlization')
    ax.plot(x, total, color=total_color[-1], label='Total')

    ax.axhline(y=TARGET, color='brown', linestyle='--', label='Target')
    # Customize plot
    ax.set_xlabel('Steps', fontsize=26)
    #if i == 0:
    #    ax.plot(x, total_list[1][:len(total_list[0])], color=total_color[1], label='In2S Total from (b)')
    #    ax.plot(x, total_list[2][:len(total_list[0])], color=total_color[2], label='RA2S Total from (c)')
    #    ax.set_ylabel('Latency (ms)', fontsize=26)

    #print(np.max(total_list[0]))
    ax.set_ylim(0, np.max(total_list[0])+10)
    ax.tick_params(axis='both', which='major', labelsize=24)
    #ax.set_title(test_label[i])
    ax.text(-9, np.max(total_list[0])*0.72, test_label[i], fontsize=26)
    #ax.set_title(test_label[i], y=-0.38, fontsize=30)  # Concatenate with the dynamically generated label
    #ax.set_title('({}) {}'.format(chr(97 + i), test_label[i]), y=-0.32, fontsize=36)  # Concatenate with the dynamically generated label
#plt.legend(loc='upper center', ncols=6, frameon=False, fontsize=16)
labels=['Numeric', 'Algorithm (RA)', 'Symbolic', 'Relinearization', 'Total', 'Target']
#if file_dir == 'cab7k_uartlogs':
#    fig.legend(labels, loc='upper center', bbox_to_anchor=(0.5,1.29), ncols=4, fontsize=24, frameon=False)

plt.tight_layout()
#plt.savefig(file_dir+'_breakdown.png', bbox_inches='tight', pad_inches=0.05, dpi=700)
plt.savefig(benchmark_input+'_breakdown.pdf', bbox_inches='tight', pad_inches=0.05, dpi=700)



