# Ontological Approach for Competency-Based Curriculum Analysis

## Software Purpose

This software is designed for loading data into an ontological model of a competency-based curriculum, extracting data from the ontology, and analyzing the consistency of the curriculum in terms of input requirements for the study of disciplines and learning outcomes in previous periods.

## Scripts

1. `data.py` - primary data of the educational program
2. `load.py` - loading data from the `data.py` file into the ontological model (after data loading, the ontology is saved in the `competencies2.rdf` file)
3. `display.py` - extracting the curriculum and competency tree with terminal output
4. `check.py` - analyzing the consistency of the curriculum
5. `empty.rdf` - template ontology of the educational program (curriculum)
