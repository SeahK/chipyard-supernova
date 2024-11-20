# with relin/sym/alg cost
# figure per each test
# with backsolve diff
import sys
import re
import csv
import numpy as np
from math import ceil
from math import isnan
from matplotlib import pyplot as plt

alg_label = ["ISAM2", "RA-ISAM2 (SuperNoVA Algorithm)"]
# set
num_supernova = [1, 2, 4]
hw_label = ["1 Set", "2 Sets", "4 Sets"]
#test_label = ["In1B", "In2S", "RA2S"]
#box_color = ['gainsboro','darkgrey','beige','wheat','honeydew', 'lightgreen','limegreen','lightcyan','lightskyblue', 'steelblue']
#box_color = ['lightgreen', 'lightskyblue']
#box_color = ['violet', 'lawngreen']
box_color = ['violet', 'green']
#box_color = ['greenyellow', 'mediumorchid']
benchmark_name = ['Sphere', 'M3500', 'CAB1', 'CAB2']
benchmark_name_lower = ['sphere', 'm3500', 'cab464', 'cab7k']
#file_name+num_supernova
test_name = ['incremental1', 'incremental2', 'incremental4', 'ra1', 'ra2', 'ra4']
#total_color = ['purple', 'dimgray', 'maroon', 'indigo']

TARGET = 33.3
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
#total2_regex = r"step (\d*) time: (\d+\.\d+) ms\b"
#profile_total_regex = r"step (\d*) node \d* total increment time: (\d*)\b"


end_regex = r"end of test\b"

positions = np.arange(0.5, len(test_name))
#total line graph
fig, axs = plt.subplots(1, 4, figsize=(18, 3.5))
x = np.arange(2)  # the label locations
#width = 1/(len(hw_label)*1.3)  # the width of the bars
#for b, folder in enumerate(sys.argv[1:]):

#filename = sys.argv[1]
find_test = False
for b in range(len(benchmark_name)):
    ax = axs[b]
    total_test_list = []
    num_thread = []
    hw_platform = []
    name_list = [] # hw + alg + thread
    step_list = []
    numeric_list = []
    step_list = []
    relin_list = []
    sym_list = []
    alg_list = []
    total_list = []

    numeric_this_list = []
    step_this_list = []
    relin_this_list = []
    sym_this_list = []
    alg_this_list = []
    for n in range(2):
        filename = sys.argv[1+n+2*b]
        print(filename)
        with open(filename, "r") as f:
            for line in f.readlines():
                end_search = re.search(end_regex, line)
                test_search = re.search(test_regex, line)
                total_search = re.search(total_regex, line)
                #total2_search = re.search(total2_regex, line)

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
                    benchmark = str(test_search.group(4))
                    #print(benchmark)
                    if benchmark == benchmark_name_lower[b]:
                        find_test = True
                        print("find test: ", benchmark)
                    else:
                        if find_test:
                            find_test = False
                            break

                    if find_test:
                        name_list.append(benchmark+"_"+algorithm+"_"+hw_platform+num_thread)

                        relin_file = benchmark+"_"+algorithm+"_"+hw_platform+num_thread+"_relin.txt"
                        sym_file = benchmark+"_"+algorithm+"_"+hw_platform+num_thread+"_sym.txt"
                        alg_file = benchmark+"_"+algorithm+"_"+hw_platform+num_thread+"_alg.txt"
                        if benchmark == "cab464":
                            interval = 1
                        else:
                            interval = 25
                        if hw_platform == "spatula":
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
                    #print(backsolve_this_list)
                    #print(numeric_this_list)
                    #numeric_this_list = [numeric_this_list[i]+backsolve_this_list[i] for i in range(len(numeric_this_list))]
                    #print(numeric_this_list)
                    print(len(numeric_this_list), len(relin_this_list), len(sym_this_list))
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



    for i in range(len(total_list)):
        total_max = max(total_list[i])
        total_avg = sum(total_list[i])/len(total_list[i])
        total_75 = np.percentile(np.array(total_list[i]), 75)
        print(name_list[i], " total: ", total_avg, total_75, total_max)
        total_num_max = max(total_num_list[i])
        total_num_avg = sum(total_num_list[i])/len(total_num_list[i])
        total_num_75 = np.percentile(np.array(total_num_list[i]), 75)
        print(name_list[i], " numeric: ", total_num_avg, total_num_75, total_num_max)

    for i in range(len(total_list)):
        scaled_list = np.array(total_list[i])
        #plt.plot(step_list[i], scaled_list, label=test_label[i])
        count_violated = sum(1 for elem in scaled_list if elem > TARGET)
        print(count_violated, count_violated / len(scaled_list))
        print([j for j, num in enumerate(scaled_list) if num > TARGET])
    print("max")
    # Divide element-wise
    for i in range(3):
        division_result = [x / y for x, y in zip(total_list[i+3], total_list[i])]
        min_value = min(division_result)
        min_index = division_result.index(min_value)
        print("RA ", i)
        print("value: ", min_value, "1-value: ", 1-min_value, "index: ", min_index*interval)

    incremental_list = total_list[0:3]
    ra_list = total_list[3:]
    # Box plot positions for the first and second 2D arrays
    positions1 = [0.5, 2.5, 4.5]
    positions2 = [1.5, 3.5, 5.5]

    max_val = max(incremental_list[0])

    # Plotting the box plots
    box1 = ax.boxplot(incremental_list, positions=positions1, widths=0.6, patch_artist=True, showmeans=True, meanline=True, whis=(0,100), boxprops=dict(facecolor=box_color[0], alpha=0.4), meanprops=dict(color='darkblue', linestyle='--', linewidth=1.5))
    box2 = ax.boxplot(ra_list, positions=positions2, widths=0.6, patch_artist=True, showmeans=True, meanline=True, whis=(0, 100), boxprops=dict(facecolor=box_color[1], alpha=0.4), meanprops=dict(color='darkblue', linestyle='--', linewidth=1.5))
    # Hide the median line
    for median in box1['medians']:
        median.set(color='None')  # Set color to 'None' to hide the median line
    for median in box2['medians']:
        median.set(color='None')  # Set color to 'None' to hide the median line
    #ax.set_xticks(positions, alg_label * len(num_supernova))#, rotation=90)
    ax.set_xticks([1, 3, 5], hw_label)

    #if b==0:
    for j in range(len(incremental_list)):
        miss_rate = ceil(sum(n > TARGET for n in incremental_list[j]) / len(incremental_list[j]) * 100)
        if max(incremental_list[0]) < TARGET:
            ax.text(positions1[j]-0.3, TARGET + 3, str(miss_rate) + "%", fontsize=16)
        else:
            ax.text(positions1[j]-0.3, max_val * 1.08, str(miss_rate) + "%", fontsize=16)
    for j in range(len(ra_list)):
        miss_rate = int(sum(n > TARGET for n in ra_list[j]) / len(ra_list[j]) * 100)
        print(miss_rate)
        if max(incremental_list[0]) < TARGET:
            ax.text(positions2[j]-0.3, TARGET + 3, str(miss_rate) + "%", fontsize=16)
        else:
            ax.text(positions2[j]-0.3, max_val * 1.08, str(miss_rate) + "%", fontsize=16)
    #if max(incremental_list[0]) < TARGET:
    ax.set_ylim(0, max(40, 1.2*max_val))
    ax.set_ylabel('Latency(ms)', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=18)#, pad=0.2)
    ax.tick_params(axis='y', pad=0.2)
    ax.axhline(y = TARGET, color = 'firebrick', linestyle = '-')
    ax.axvline(x=(positions.max() + positions.min()) / 3, color='grey', linestyle='--')
    ax.axvline(x=(positions.max() + positions.min()) * 2 / 3, color='grey', linestyle='--')
    ax.set_title('({}) {}'.format(chr(97 + b), benchmark_name[b]), y=-0.29, fontsize=20)  # Concatenate with the dynamically generated label


# Add custom legend
legend_elements = [
    plt.Rectangle((0,0),1,1,fc=box_color[0], edgecolor=box_color[0], linewidth=1, linestyle='-', label=alg_label[0], alpha=0.5),
    plt.Rectangle((0,0),1,1,fc=box_color[1], edgecolor=box_color[1], linewidth=1, linestyle='-', label=alg_label[1], alpha=0.5),
    plt.Line2D([0], [0], color='firebrick', linewidth=1, linestyle='-', label='Target Latency'),
    plt.Line2D([0], [0], color='black', linewidth=1, linestyle='-', label='Whiskers (0-100%)'),
    plt.Line2D([0], [0], color='darkblue', linewidth=1.5, linestyle='--', label='Mean'),
    #plt.Line2D([0], [0], color='saddlebrown', linewidth=1, linestyle='--', label='Median'),
    plt.Rectangle((0,0),1,1,fc='white', edgecolor='black', linewidth=1, linestyle='-', label='25-75% Box')
]

#plt.legend(handles=legend_elements, fontsize=12, framealpha=0)
fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5,1.095), ncols=6, fontsize=17.5, frameon=False)
plt.tight_layout()
plt.savefig('box.pdf', bbox_inches='tight', pad_inches=0.03, dpi=1000)


