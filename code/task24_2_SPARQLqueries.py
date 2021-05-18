'''
Created on 4 March 2021

@author: judith.grieves@city.ac.uk


INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

This code loads the inferred pizza ontology and instance data and executes
SPARQL queries over the graph.

SPARQL and Reasoning (Task SPARQL) - Subtask SPARQL.2-5 

https://www.kaggle.com/datafiniti/pizza-restaurants-and-the-pizza-they-sell


to do:
    
    SPARQL 2 filter for no tomato - needs inference to id pizza blanca
    SPARQL 4 los angeles,eg. has 2 states so is giving duplicated results,
     one for each state - data improvement required to fix

'''
from rdflib import Graph
import csv

import os
from os.path import dirname, abspath



def queryTest(g):
    
    # query to test/debug results
    #  """SELECT COUNT( DISTINCT ?subject) as ?instances, ?class WHERE
    
    qres = g.query(
    """SELECT DISTINCT ?subject   ?classx WHERE
                { ?subject jkg:hasCategory [] . 
                ?subject a ?classx .}  """)    

    for row in qres:
    #Row is a list of matched RDF terms: URIs, literals or blank nodes
        print(row.subject,row.classx)    
    

def query2(g,outFile):
    
    # Subtask SPARQL.2 Return all the details of the restaurants that sell 
    # pizzas without tomate (i.e., pizza bianca). 
    
    print("SPARQL.2")
    print("Restaurants that sell pizzas without tomato: \n")
    
     
      #FILTER regex(?pizza_label, "Bianca", "i" ) 
      
    qres = g.query(
    """SELECT DISTINCT   ?outlet_label  ?address_label ?city_label    where {   
      ?pizza rdf:type  jkg:MenuItem .       
      ?pizza jkg:servedAt  ?outlet .   
      ?outlet rdfs:label ?outlet_label .   
      ?pizza rdfs:label ?pizza_label . 
      ?outlet jkg:isLocatedAt ?address .    
      ?address jkg:addressLocatedIn  ?city .  
      ?city jkg:cityLocatedIn ?state .  
           
      ?address rdfs:label ?address_label .       
      ?city rdfs:label ?city_label . 
      ?state rdfs:label ?state_label . 
      FILTER regex(?pizza_label, "bianca", "i" ) 
    }     
    ORDER BY ASC( ?outlet_label)""")

    #SPARQL results into CSV     
    outFile=outFile.replace("?", "2") 
    
    with open(outFile, 'w', newline='', encoding='utf-8') as file:
        print("writing output to file: ",outFile)
        writer = csv.writer(file)            
        writer.writerow(["outlet","address","city"])
        for row in qres:
        #Row is a list of matched RDF terms: URIs, literals or blank nodes
            if Display:
                print( row.outlet_label, row.address_label, row.city_label)  
                
            writer.writerow([ row.outlet_label, row.address_label, row.city_label])
            
 
def query3(g,outFile):    
       
    #Subtask SPARQL.3 Return the average prize of a Margherita pizza
    
    print("SPARQL.3")    
    
    qres = g.query(
    """SELECT  (AVG(?price) AS ?avg_price) where {     
      ?pizza rdf:type  jkg:MenuItem .    
      ?pizza rdfs:label ?pizza_label .          
      ?pizza jkg:price  ?price .   
    FILTER regex(?pizza_label, "Margherita", "i" ) 
    }     """)
        
    outFile=outFile.replace("?", "3") 
    
    with open(outFile, 'w', newline='', encoding='utf-8') as file:
        print("writing output to file: ",outFile)
        writer = csv.writer(file)            
        writer.writerow(["avg price"])
        
        for row in qres:
            
            if Display:
                print("Average prize of a Margherita pizza: \n")
                print(row.avg_price)  
                
            writer.writerow([ row.avg_price])
            
            
def query4(g,outFile):
     
     
    #Subtask SPARQL.4 Return number of restaurants by city, sorted by state and number of restaurants
    
    print("SPARQL.4")  
        
    qres = g.query(
    """SELECT   ?state_label ?city_label (COUNT(?city_label) AS ?count_restaurant) where {  
      ?outlet jkg:isLocatedAt ?address .    
      ?address jkg:addressLocatedIn  ?city .  
      ?city jkg:cityLocatedIn ?state .      
      ?city rdfs:label ?city_label . 
      ?state rdfs:label ?state_label . 
    }     
    GROUP BY ?state_label ?city_label 
    ORDER BY ASC( ?state_label) DESC(?count_restaurant) """)
         
    outFile=outFile.replace("?", "4") 
    
    with open(outFile, 'w', newline='', encoding='utf-8') as file:
        print("writing output to file: ",outFile)
        writer = csv.writer(file)            
        writer.writerow(["state","city","restaurant count"])
        if Display:
            print("state","city","restaurant count")
        print("number of restaurants by city: \n")
        for row in qres:
        #Row is a list of matched RDF terms: URIs, literals or blank nodes            
            if Display:
                print(row.state_label,row.city_label,row.count_restaurant)  
                
            writer.writerow([ row.state_label, row.city_label,row.count_restaurant]) 
            
                    
def query5(g,outFile):
     
     
    print("SPARQL.5")   
    
    # Subtask SPARQL.5 Return the list of restaurants with missing postcode 
    
    qres = g.query(
    """SELECT ?outlet_label ?address_label ?city_label ?postcode where {      
      ?outlet rdf:type  jkg:PizzaOutlet .          
      ?outlet rdfs:label ?outlet_label .    
      ?outlet jkg:isLocatedAt ?address .     
      ?address rdfs:label ?address_label .    
      ?address jkg:addressLocatedIn  ?city .     
      ?city rdfs:label ?city_label .  
      FILTER NOT EXISTS { ?address jkg:postcode ?postcode .  }
    }     
    ORDER BY ASC( ?outlet_label)""")
    
    #for row in qres:
    #     print("%s  has no postcode" % row)    
         
    outFile=outFile.replace("?", "5") 
    
    with open(outFile, 'w', newline='', encoding='utf-8') as file:
        print("writing output to file: ",outFile)
        writer = csv.writer(file)            
        writer.writerow(["outlet","address","city","postcode"])
        
        for row in qres:
            
            if Display:
                print("Restaurant without postcode: ",row.outlet_label,row.address_label,row.city_label,row.postcode)    
                
            writer.writerow([ row.outlet_label,row.address_label,row.city_label,row.postcode])
         
  
            
def querySPARQL():

    
    print("\nStarting querySPARQL")
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    output_dir = os.path.join(dirname(dirname(abspath(__file__))), 'SPARQLresults')
        
        
    inFile="pizza_inference.ttl" 
    outFile=inFile.replace(".ttl", "-")+"q?-results.csv"  
    
    inFile = os.path.join(data_dir,inFile)
    outFile = os.path.join(output_dir,outFile)
    

    
    print("Load a graph from input file: ", inFile)
    g = Graph()    
    
    g.parse(inFile, format="ttl")     
    
    print("Loaded '" + str(len(g)) + "' triples.\n")
    
    
    #queryTest(g)
    query2(g,outFile)
    query3(g,outFile)
    query4(g,outFile)
    query5(g,outFile)     
    
    
    print("\nFinished querySPARQL")
          

Display=False       
#querySPARQL()

#