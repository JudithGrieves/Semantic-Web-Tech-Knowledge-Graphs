# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 15:01:35 2021

@author: judith.grieves@city.ac.uk

INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework


Ontology Alignment (Task OA) - Subtask OA.2 

This code loads i) the created ontology, (ii) the pizzaStanford.owl ontology and 
(iii) the computed alignment (without the data) and performs reasoning
,specifically listing the number of unsatisfiable classes.]
    
"""
from rdflib import Graph

import owlrl

import os
from os.path import dirname, abspath, join



def inconsistentQuery(g):
    

    print("Unsatisfiable classes:")
    

    qres = g.query(
    """SELECT DISTINCT ?subject   WHERE
                { 
                owl:Nothing rdfs:subClassOf ?subject  .}  
                """)    

    if Display:
        for row in qres:
            print(row.subject) 
        
    print("Number of unsatisfiable classes = ", len(qres))
        

def alignInference():
    
    print("\nStarting alignInference")
    
    global Display
    Display=False

    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    
    ontology_file="myPizzaOnt.owl"
    ontology_file = os.path.join(data_dir,ontology_file)
    
    pizza_file="pizzaStanford.owl"
    pizza_file = os.path.join(data_dir,pizza_file)
    
    align_file="align-pizzaStanford-myPizzaOnt.owl"
    align_file = os.path.join(data_dir,align_file)
    
    
    g = Graph()
    
    print("Reading file: ",pizza_file)   
    g.parse(pizza_file)
    
    print("Loaded '" + str(len(g)) + "' triples.")    

    print("Reading file: ",ontology_file)   
    g.load(ontology_file) 
    
    print("Triples including ontology: '" + str(len(g)) + "'.")  
    
    print("Reading file: ",align_file)   
    g.load(align_file) 
    
    print("Triples including alignment: '" + str(len(g)) + "'.")    
    
    #  apply reasoning and expand the graph with new triples 
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)
    
    print("Triples after OWL 2 RL reasoning: '" + str(len(g)) + "'.")
    
    # output the results as owl
    
    file_output="pizza-reasoned.ttl"
    file_output = os.path.join(data_dir,file_output)
    
    print("writing out to file: ",file_output)
    g.serialize(destination=file_output, format='ttl')
    
    # get unsatisfiable classes
    
    inconsistentQuery(g)
        
    
    print("Finished alignInference")
    
    
def main():

    alignInference()


if __name__ == "__main__":

    main()


