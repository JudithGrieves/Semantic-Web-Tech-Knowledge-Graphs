'''
Created on 28 Mar 2021

@author: judith.grieves@city.ac.uk

INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

Ontology Alignment (Task OA) - Subtask OA.1 

compare multiple classes & properties in 2 given OWL ontologies
write out successful matches to a ttl alignment file
    

'''
import rdflib

from rdflib import  URIRef

from owlready2 import *

import csv

import os
from os.path import dirname, abspath


import Levenshtein as lev 
from stringcmp import isub


from rdflib.namespace import OWL


def getBaseIRI(onto):        
    return onto.base_iri
            
def getClasses(onto):        
    return onto.classes()
    
def getDataProperties(onto):        
    return onto.data_properties()
    
def getObjectProperties(onto):        
    return onto.object_properties()
    
def getIndividuals(onto):    
    return onto.individuals()


def getRDFSLabelsForEntity(entity):
    if hasattr(entity, "label"):
        return entity.label



def writeComparisonResults(f1,f2,f3,f4,f5,f6,f7):
    
    # for testing/debugging
    # write the comparison results to a file for later analysis
    
    outFile= 'comparisonResults.csv'   
    with open(outFile, 'w', newline='') as file:
        writer = csv.writer(file)            
        writer.writerow(["string1", "string2","iri1","iri2", "lev","jaro","isub",])
        #print(f1,f2,f3,f4,f5,f6,f7)    
        writer.writerow([ f1,f2,f3,f4,f5,f6,f7])
        
        
        

def stringCompare(str1,str2):
    
    # for 2 given strings, compare using a chosen comparison method

    # Informally, the Levenshtein distance between two words is the minimum 
    # number of single-character edits required to change one word into the other.

    # set the chosen comparison method and threshold value
        
    method='iSub' #'jaro' # 'levDist' 'iSub'
    isubThr=0.9
    
    #method='jaro' 
    #jaroThr=0.91 # best so far 0.80 gives f-score 0.58
    
    #method='levDist'
    #levDistThr=4
    
    
    if method == 'jaro':
        
        jaroScore=lev.jaro_winkler(str1, str2)
        
        if  jaroScore >= jaroThr:
            if Display:
                print("Matched: ",str1," / ",str2,jaroScore)
            return 0
        
    if method == 'levDist':
        
        levDistScore = lev.distance(str1, str2)
        
        if  levDistScore <= levDistThr:
            if Display:
                print("Matched: ",str1," / ",str2,levDistScore)
            return 0
        
    if method == 'iSub':
        
        isubScore = isub(str1, str2)
        
        if  isubScore >= isubThr:
            if Display:
                print("Matched: ",str1," / ",str2,isubScore)
            return 0
    
    return 1

def compareObjects(objType,onto1,onto2,g):
    
    # given an object type and 2 ontologies, compare all pairs of entities 
    # and write alignment triples where a satisfactory match is found

    if Display:
        print("\nMatching a "+objType) #
        
    len1=str(len(list(getClasses(onto1))))
    
    count=0
    string1='' # because the first class/label is empty - find a better way
    string2=''
    
    # set the function to get the comparison value, depending on class type
    if objType == 'class':
        compareFunc=getClasses
        
    elif objType == 'objProp':
        compareFunc=getObjectProperties
        
    elif objType == 'dataProp':
        compareFunc=getDataProperties
    
    # for each entity in ontology1
    
    for cls1 in compareFunc(onto1):  
        count=count+1
        if count % 10 == 0:
            print ("processing ",count," of ",len1," class1")
         
        #for s in getRDFSLabelsForEntity(cls1):
            #print("label2: ",s)
            #string1=s
        
        # set the ontology1 string to compare
        
        string1=cls1.name
        if not string1:
            continue
        
        # for each entity in ontology 2
        
        for cls2 in compareFunc(onto2): 
            
            
            # set the ontology1 string to compare
            string2=cls2.name
            
            # compare the strings.  match=0 when successful
            match=stringCompare(string1,string2)  
            if match==0:
                subj=cls1.iri 
                obj=cls2.iri  
            
                # write a triple of the aligned entities
                
                if objType == 'class':
                    g.add((URIRef(subj),OWL.equivalentClass,URIRef(obj)))
                    
                elif objType == 'objProp' or objType == 'dataProp':
                    g.add((URIRef(subj),OWL.equivalentProperty,URIRef(obj)))
                
                #writeComparisonResults(string1,string2,subj,obj,0,0,0)
                    
def printClasses(onto):
    
    print("classes for ontology: ",onto)
    for cls in getClasses(onto):             
        #print(cls.iri)
        print("\t"+cls.name)  
        #Labels from RDFS label        
        #print("\t"+str(getRDFSLabelsForEntity(cls)))
                       
                    
                        
def compareOntology(owl1,owl2):
    
    Display=False
    
    # load the ontology with owlready method
    onto1 = get_ontology(owl1).load()
    if Display:
        printClasses(onto1)    
    
    onto2 = get_ontology(owl2).load()
    if Display:
        printClasses(onto2)    
    
    for name in [owl1,owl2]:
        print("reading and comparing files: ",name)
        
    baseIRI=[]
    
    # create a list of the base IRIs of the ontologies
    
    for onto in [onto1,onto2]:    
        
        print("Ontology ",os.path.basename(onto.name)," no of classes: ", str(len(list(getClasses(onto)))))
        baseIRI.append(getBaseIRI(onto))
    
    #print("base IRIs: ",baseIRI)    
    
    
    
    
    
    # create a graph for the alignment references
    
    g = rdflib.Graph()
    
    g.bind("owl", OWL) 
           
    # do lexical compare for each object type
    
    for objType in ['class','objProp','dataProp']:    
         
        compareObjects(objType,onto1,onto2,g)
            
    # output the results as ttl
    
    file_output="align-"+os.path.basename(onto1.name)+"-"+os.path.basename(onto2.name)+".ttl"
    file_output = os.path.join(data_dir,file_output)
    
    print("writing out to file: ",file_output)
    g.serialize(destination=file_output, format='ttl')
    
    
    # output the results as owl
    
    file_output="align-"+os.path.basename(onto1.name)+"-"+os.path.basename(onto2.name)+".owl"
    file_output = os.path.join(data_dir,file_output)
    
    print("writing out to file: ",file_output)
    g.serialize(destination=file_output, format='xml')


def ontAlign():
    
    print("starting ontAlign ...")

    # set up file variables
    
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')

            
    owl1="pizzaStanford.owl"
    owl2="myPizzaOnt.owl"
    
    owl1 = os.path.join(data_dir,owl1)
    owl2 = os.path.join(data_dir,owl2)
    
    # compare the ontologies
    
    compareOntology(owl1,owl2)
    
    print("finished ontAlign ...")


def main():

    ontAlign()


Display=False 

if __name__ == "__main__":

    main()
