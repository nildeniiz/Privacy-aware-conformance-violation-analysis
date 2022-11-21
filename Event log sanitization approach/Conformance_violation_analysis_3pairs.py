import os
import pm4py
import pandas
import numpy as np
import time
from ctypes import alignment
from collections import Counter
from hashlib import algorithms_available
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.conformance.alignments import algorithm as alignments
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments

#Import the log and the model
log = xes_importer.apply('Event log file path')
#Select the respective n value for the k value that satisfies k-anonymity
filtered_log = pm4py.filter_variants_top_k(log, n)
net, initial_marking, final_marking = pnml_importer.apply('PNML file file path')
tic = time.perf_counter()

#Compute the aligments using Dijkstra's algorithm 
model_cost_function = dict()
sync_cost_function = dict()
for t in net.transitions:
    # if the label is not None, we have a visible transition
    if t.label is not None:
        # associate cost 1 to each move-on-model associated to visible transitions
        model_cost_function[t] = 1
        # associate cost 1 to each move-on-log
        sync_cost_function[t] = 1
    else:
        # associate cost 0 to each move-on-model associated to hidden transitions
        model_cost_function[t] = 0
parameters_dijkstra = {}
parameters_dijkstra[alignments.Variants.VERSION_DIJKSTRA_NO_HEURISTICS.value.Parameters.PARAM_MODEL_COST_FUNCTION] = model_cost_function
parameters_dijkstra[alignments.Variants.VERSION_DIJKSTRA_NO_HEURISTICS.value.Parameters.PARAM_SYNC_COST_FUNCTION] = sync_cost_function

parameters_a_star = {}
parameters_a_star[alignments.Variants.VERSION_STATE_EQUATION_A_STAR.value.Parameters.PARAM_MODEL_COST_FUNCTION] = model_cost_function
parameters_a_star[alignments.Variants.VERSION_STATE_EQUATION_A_STAR.value.Parameters.PARAM_SYNC_COST_FUNCTION] = sync_cost_function

aligned_traces_dijkstra = alignments.apply_log(filtered_log, net, initial_marking, final_marking, parameters=parameters_dijkstra, variant=alignments.Variants.VERSION_DIJKSTRA_NO_HEURISTICS)
#aligned_traces_a_star = alignments.apply_log(log, net, initial_marking, final_marking, parameters=parameters_a_star, variant=alignments.Variants.VERSION_STATE_EQUATION_A_STAR)


#Print all the alignments generated with Dijkstra
def printTraces():
    print("----------------------START OF TRACES---------------------")
    for a in aligned_traces_dijkstra:
        print(a)
    print("----------------------END OF TRACES---------------------")

#printTraces()

#Generate the list of misalignments and store the misalignment tuples with the activity tuples before and after the misalignment & if they dont exist add "beginning of the process" or "end of the process"
list_of_misaligments = []

for i in range(len(aligned_traces_dijkstra)):
    for j in range(len(aligned_traces_dijkstra[i]['alignment'])):
        pair = aligned_traces_dijkstra[i]['alignment'][j]
        if(pair[0] != pair[1] and (pair[0] != None and pair[1] != None)):
            if(j == 1):
                list_of_misaligments.append(["(beginning of the process)", pair, aligned_traces_dijkstra[i]['alignment'][j+1], len(aligned_traces_dijkstra[i]['alignment'])])
            elif(j == len(aligned_traces_dijkstra[i]['alignment'])-1):
                list_of_misaligments.append([aligned_traces_dijkstra[i]['alignment'][j-1], pair, "(end of the process)", len(aligned_traces_dijkstra[i]['alignment'])])
            else:
                list_of_misaligments.append([aligned_traces_dijkstra[i]['alignment'][j-1], pair, aligned_traces_dijkstra[i]['alignment'][j+1], len(aligned_traces_dijkstra[i]['alignment'])])

def CountFrequency(my_list):
    # Creating an empty dictionary
    freq = {}
    sum = {}

    #String operations in order to store the length of the traces
    for item in my_list:
        if (str(str(item[0]) + str(item[1]) + str(item[2])) in freq):
            freq[str(str(item[0]) + str(item[1]) + str(item[2]))] += 1
            sum[str(str(item[0]) + str(item[1]) + str(item[2]))] += item[3] 
        else:
            freq[str(str(item[0]) + str(item[1]) + str(item[2]))] = 1
            sum[str(str(item[0]) + str(item[1]) + str(item[2]))] = item[3] 
    
    #sort frequency counter dictionary
    freq = sorted(freq.items(), key=lambda item: item[1])
    
    #print frequenct counter dictionary (value = count)
    total_inf=0
    for key, value in freq:
        information_preserved = value*3/(sum[key]/value)
        if (value > 0):
            #Print the conformance violation pairs of 3, the number of occurence, the information preserved
            print ("Pairs of 3:", key, "Number of Occurence:" , value,  "Information Preserved:" , 3/(sum[key]/value))
            total_inf += information_preserved

    print("Total Preserved Information=" , total_inf)     

CountFrequency(list_of_misaligments)

#Calculate time
toc = time.perf_counter()
print(f"Computed the conformance violations in {toc - tic:0.4f} seconds")