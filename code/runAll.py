 # -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:58:14 2021

@author: judith.grieves@city.ac.uk

INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

Run all Python modules for the coursework.

"""
import task23_csvToRDF as rdf
import task24_1_OWLReasoning as owl
import task24_2_SPARQLqueries as sp
import task25_1_ontAlign as oa
import task25_2_Reasoning as rs
import task26_loadEmbed as em

def main(input_csv):
    
    print("Starting runAll() ...")
    
    # the initial CSV filename is supplied and drives all other modules
    
    #rdf.csvToRDF(input_csv)
    owl.OWLRLReasoning()
    sp.querySPARQL()    
    oa.ontAlign()    
    rs.alignInference()
    em.loadEmbeddings()

    print("Finished runAll() ...")
  
    
    
    
    
inFile="pizza_data_200.csv"    # file to run all for

main(inFile) 