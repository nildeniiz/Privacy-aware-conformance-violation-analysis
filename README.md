# Privacy-aware-conformance-violation-analysis

This repository contains the algorithm developed to analyze conformance violations with precedent and succedent events in a privacy aware way using a result sanitization approach which is explained in the master thesis: Privacy Aware Conformance Violation Analysis.

The input data is available in the input.zip. The XES formatted event logs and pnml files are in the folder but pnml file can also be generated with generatepnml.py

Conformance_violation_analysis_5pair.py , 3pairs and 1pair will generate the result sanitized conformance violation tuples when the desired k-anonymity by replacing k with 0 in "(value > 0)". 

In order to compare it with the event log sanitization method, respective pyton files can be run with entering the respective n (top_variants_filter) value that achieves the desired k-anonymity privacy level in the "Event log sanitization approach" file.

The detected conformance violations are available in Traffic Fine.xlsx Coselog.xlsx and Sepsis.xlsx files.
