 # -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:58:14 2021

@author: judith.grieves@city.ac.uk

INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

Run all Python modules for the coursework.

"""
import task23_csvToRDF as csvToRDF
import task24_1_OWLReasoning as OWLRLReasoning
import task24_2_SPARQLqueries as SPARQLqueries
import task25_1_ontAlign as ontAlign
import task25_2_Reasoning as alignInference
import task26_loadEmbed as loadEmbeddings

def runAll(input_csv):
    
    print("Starting runAll() ...")
    
    # the initial CSV filename is supplied and drives all other modules
    
    csvToRDF.csvToRDF(input_csv)
    OWLRLReasoning.OWLRLReasoning()
    SPARQLqueries.querySPARQL()    
    ontAlign.ontAlign()    
    alignInference.alignInference()
    loadEmbeddings.loadEmbeddings()

    print("Finished runAll() ...")
  
    
    
    
    
inFile="pizza_data.csv"    # file to run all for

runAll(inFile) 