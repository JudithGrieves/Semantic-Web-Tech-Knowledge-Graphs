# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 15:01:35 2021

@author: judith.grieves@city.ac.uk

INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

SPARQL and Reasoning (Task SPARQL) - Subtask SPARQL.1 


This code loads .owl file for an Ontology and .ttl for a set of data instances
and performs OWL RL Reasoning on the triples, writing out a new file of 
the asserted and inferred triples (.ttl and .owl).

Instance data originally loaded from:
https://www.kaggle.com/datafiniti/pizza-restaurants-and-the-pizza-they-sell

    
"""
from rdflib import Graph

import owlrl

import os
from os.path import dirname, abspath


def testQueries(g):
    
    print("\nTest Queries: ")
    
    triple1 = "jkg:Bianca_Pizza jkg:servedAt jkg:Little_Pizza_Paradise ."
    triple2 = "jkg:Bianca_Pizza jkg:servedAt jkg:Bravo_Pizza_Hollywood ."
    
    askQueries(g, triple1)
    askQueries(g, triple2)
      
    
    
def askQueries(g, triple):
    
    # run an ASK query on the triple
    qres = g.query(
    """ASK {""" + triple + """ }""")

    #Single row with one boolean vale
    for row in qres:
        print("Does '" + triple + "' hold? " + str(row))

def OWLRLReasoning():
    
    print("\nStarting OWLRLReasoning")
    
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    
    ontology_file="myPizzaOnt.owl"
    ontology_file = os.path.join(data_dir,ontology_file)
    
    instance_file="pizza_data.ttl"
    #instance_file="pizza_cutdown.ttl"
    instance_file = os.path.join(data_dir,instance_file)
    
    output_file="pizza_inference"
    output_file = os.path.join(data_dir,output_file)
    
    
    g = Graph()
    
    print("Reading file: ",instance_file)   
    g.parse(instance_file, format="ttl")
    
    print("Loaded '" + str(len(g)) + "' triples.")    

    print("Reading file: ",ontology_file)   
    g.load(ontology_file) 
    
    print("Triples including ontology: '" + str(len(g)) + "'.")    
    
    #  apply reasoning and expand the graph with new triples 
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)
    
    print("Triples after OWL 2 RL reasoning: '" + str(len(g)) + "'.")
        
    # test queries
    testQueries(g)
    
    
    print("Writing file: ",output_file+'.ttl')
    g.serialize(destination=output_file+'.ttl', format='ttl')  
    
    print("Writing file: ",output_file+'.owl')
    g.serialize(destination=output_file+'.owl', format='xml')  
    
    
    print("Finished OWLRLReasoning")
    
    
#OWLRLReasoning()

