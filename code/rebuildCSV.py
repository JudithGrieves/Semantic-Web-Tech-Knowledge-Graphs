'''
Created on 20 May 2021

@author: judith.grieves@city.ac.uk


INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

This code runs a SPARQL query against the .ttl file and writes the results to 
a CSV file.  The aim of this is to rebuild the original CSV file to 
provid a comparison in order to test the KG build process.

https://www.kaggle.com/datafiniti/pizza-restaurants-and-the-pizza-they-sell


'''
from rdflib import Graph
import csv

import os
from os.path import dirname, abspath



def queryTest(g):
    
    
    # extract all the details of the original CSV file
    
    print("SPARQLtest")
    print("All original details \n")
    
           
    qres = g.query(
    """SELECT DISTINCT   ?name  ?address_label ?city_label ?country ?postcode ?state_label ?menu_item ?price  ?price_currency ?item_description where {   
      ?MenuItemKey rdf:type  jkg:MenuItem .       
      ?MenuItemKey jkg:servedAt  ?outlet .   
      ?outlet jkg:isLocatedAt ?address .    
      ?address jkg:addressLocatedIn  ?city .  
      ?city jkg:cityLocatedIn ?state .   
      ?state jkg:stateLocatedIn  ?country_key .  
      ?address jkg:postcode  ?postcode .       
      ?MenuItemKey jkg:price   ?price .         
      ?MenuItemKey jkg:price_currency    ?price_currency .   
      ?MenuItemKey jkg:item_description    ?item_description .   
      
      ?outlet rdfs:label ?name .   
      ?MenuItemKey rdfs:label ?menu_item .            
      ?address rdfs:label ?address_label .       
      ?city rdfs:label ?city_label . 
      ?state rdfs:label ?state_label . 
      ?country_key rdfs:label ?country . 
    }     
    ORDER BY ASC( ?state_label)  ASC( ?city_label)  ASC( ?name) ASC(?menu_item)""")

    
    with open(outFile, 'w', newline='', encoding='utf-8') as file:
        print("writing output to file: ",outFile)
        writer = csv.writer(file)            
        writer.writerow(["name","address","city","country","postcode","state","menu item","item value","currency","item description" ])
        for row in qres:
        #Row is a list of matched RDF terms: URIs, literals or blank nodes
            if Display:
                print( row.name, row.address_label, row.city_label, row.country, row.postcode, row.state_label, row.menu_item, row.price, row.price_currency, row.item_description)  
                
            writer.writerow([ row.name, row.address_label, row.city_label, row.country, row.postcode, row.state_label, row.menu_item, row.price, row.price_currency, row.item_description])
            
 
            
def querySPARQL():

    
    print("\nStarting rebuildCSV")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = os.path.join(dirname(dirname(abspath(__file__))), 'SPARQLresults')
        
    global outFile
    
    inFile="pizza_inference.ttl" 
    outFile="testRebuild.csv"  
    
    inFile = os.path.join(data_dir,inFile)
    outFile = os.path.join(output_dir,outFile)
    

    
    print("Load a graph from input file: ", inFile)
    g = Graph()    
    
    g.parse(inFile, format="ttl")     
    
    print("Loaded '" + str(len(g)) + "' triples.\n")
    
    
    queryTest(g)
    
    
    print("\nFinished rebuildCSV")
          

Display=True  

def main():
    
    querySPARQL()


if __name__ == "__main__":

    main()

#