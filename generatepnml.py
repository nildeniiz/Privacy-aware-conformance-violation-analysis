import os
import pm4py
from pm4py.objects.log.log import EventLog
from pm4py.statistics.variants.log import get
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.conformance.alignments import algorithm as alignments
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.petrinet import visualizer as pn_visualizer

log = xes_importer.apply("Event log file path")


# discover model using inductive miner infrequent here
v = inductive_miner.Variants.IMf
parameters={inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD:0.2}
net, initial_marking, final_marking = inductive_miner.apply(log, variant=v, parameters=parameters)


#visualization of the generated process model
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)

#generate the PNML file
pm4py.write_pnml(net, initial_marking, final_marking, "PNML file destination path")