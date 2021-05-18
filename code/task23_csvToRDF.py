# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 15:01:35 2021

@author: judith.grieves@city.ac.uk

INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

Tabular Data to Knowledge Graph (Task RDF)

This code takes a CSV file of the Kaggle pizza dataset and creates a *.ttl 
file based on the created Pizza ontology.

    https://www.kaggle.com/datafiniti/pizza-restaurants-and-the-pizza-they-sell


outstanding work:
    
    create more ingredients to get more objProps
    fix menu items uniqueness
    fix pizza names uniqueness.
    handle non-state States
    
"""


import pandas as pd
import string
#import csv

import os
from os.path import dirname, abspath


from rdflib import Graph
from rdflib import Namespace
from rdflib import URIRef, Literal
from rdflib.namespace import OWL, RDF, RDFS, XSD

#from collections import Counter 
from entity import KGEntity 
from lookup import *

from cleanDF import cleanString 

        

def saveGraph(g, file_output):
        
        g.serialize(destination=file_output, format='ttl')
 

def getMetaData():       
    
    # get the file that details for each column of the CSV, which class
    # instances, object and data properties should be created.
    
    metaFile="metaData.csv"
    metaFile = os.path.join(data_dir,metaFile)
    
    metaData = pd.read_csv(metaFile, sep=',', quotechar='"',escapechar="\\")
    return metaData



def getExternalURI(type,instance):    
    
    if Display:
        print("Executing getExternalURI for   ",instance)
    
    # if not found    
    limit=20
    instance = instance.lower()

    try:
        kg = GoogleKGLookup()
            
        entities = kg.getKGEntities(instance, limit)
        
        # for each row returned from Google search
        for ent in  entities: 
            
            #print("entity row: ",ent)            
            #print("instance",instance," label", ent.label)
        
            # create a list of Google KG entity types for checking below
            typeList=[]            
            for t in ent.types:
                typeList.append(t)            
            
            # only return an ID if the entity has the required Types
            
            #print("ent type t: ",t)
            if type == 'State':
                if  ("http://schema.org/Place" in typeList and 'http://schema.org/AdministrativeArea' in typeList): 
                    #print("Correct types - ent.description: ",ent.desc)
                    # for state 2-char codes, check the description as there are many other similar entries
                    if (ent.desc == "US State"): 
                        #print("Correct description ent.desc: ", ent.label, ent.desc, "ID: ",ent.ident)
                        return ent.ident # set the entity to found external URI
                    
            elif type == 'City':
                
                # only continue if the search string matches the label of the found entity
                if instance in ent.label.lower():
                
                    if  ("http://schema.org/Place" in typeList and 'http://schema.org/City' in typeList):
                        #print("city", ent.label, ent.desc, "ID: ",ent.ident)
                        return ent.ident
                
            else: # assume all others are countries
                if  ("http://schema.org/Place" in typeList and 'http://schema.org/Country' in typeList):
                    #print("city", ent.label, ent.desc, "ID: ",ent.ident)
                    return ent.ident
                
    except:
        print("GoogleKGLookup exception: ", instance)    
    
    # if no external link found    
    return 99


def createTriples(pizza,g):  
    
    # main function to read dataframe 'pizza' and convert to RDF triples
    # on a graph 'g'.
    # The conversion is driven by the metaData file which cross references
    # the CSV columns with ontology entities.
    
    externalURI=True # where found, use external URIs for city, state, countries
    
    ns= "http:/www.city.ac.uk/ds/inm713/judith_grieves/"
    
    xsd = "http://www.w3.org/2001/XMLSchema#"
        
    # namespaces class to create directly URIRefs in python.           
    jkg = Namespace(ns)
        
    #Prefixes for the serialization
    g.bind("jkg", jkg)     
    g.bind("owl", OWL) 
    g.bind("rdfs", RDFS) 
    g.bind("xsd", XSD) 
    
    # get the column:entity mapping from file
    metaData = getMetaData() 
    
    # create a dictionary to hold the URIs
    stringToURI = dict()
    
    # For each row in metaData mapping, create entities
    
    for index, row in metaData.iterrows():
        
        print( "Processing metadata Column: ",row['column'],  "Class: ", row['classType'], "Datatype: ", row['labelDatatype'])
        
        subject_col = row['column']
        classType = row['classType']
        label_datatype = row['labelDatatype']
        
        
        if Display:
            print ("classes to create: ",subject_col, classType, label_datatype)        
        
        # for the current DF column, iterate over the row values 
        # values to create class type and label triples
        
        for instanceName in (pizza[subject_col].unique()):
                    
            if pd.isnull(instanceName):
                continue
            
            # remove all punctuation to create a URI
            instance = instanceName.translate(str.maketrans('', '', string.punctuation))
            
            # match to an external URI if that option is set (externalURI)
            
            if classType in ["State","City","Country"] and externalURI:
                externalURI = getExternalURI(classType,instance)
                if externalURI == 99:
                    stringToURI[instance] = ns + instance.replace(" ", "_")
                else:    
                    stringToURI[instance]  = externalURI                      
            else:
                stringToURI[instance] = ns + instance.replace(" ", "_")
                
                
            if Display:
                print("creating class ",classType," for instance ", instance, label_datatype, "URI: ",stringToURI[instance])
            
            # create triples for type NamedIndividual, the appropriate type and a label
            
            g.add((URIRef(stringToURI[instance]), RDF.type, OWL.NamedIndividual)) 
            g.add((URIRef(stringToURI[instance]), RDF.type, URIRef(ns + classType))) 
            g.add((URIRef(stringToURI[instance]), RDFS.label,  Literal(instanceName,datatype=xsd + label_datatype)) ) 
            
        # if the CSV column has associated data Properties to create, process them 
        
        # check for a data property in the meta file
        
        if  pd.notnull(row['dataProperty']): 
            
            # parse the metaData lists of property, column and type
            dataPropList = row.dataProperty.split(':') 
            colList = row.attrColumn.split(':') 
            typeList = row.attrType.split(':') 
            
            # add a data property for each item in the (: delimited ) list 
            
            for ind in range(len(dataPropList)):                
                
                attrCol=colList[ind]
                attrType=typeList[ind]
                dataProp = dataPropList[ind]
                
                # get a distinct list for the 2 columns: class name and attribute
                
                pairs = pizza[[subject_col,attrCol]].groupby([subject_col, attrCol]).count().reset_index()
                
                for subject, lit_value in zip(pairs[subject_col], pairs[attrCol]):
                    
                    if lit_value: # only do if the attribute is not empty in the DF
                            
                        subject = subject.translate(str.maketrans('', '', string.punctuation))
                        
                        if attrType=='float':
                            lit_value = float(lit_value)
                    
                        if Display:
                            print("create dataProperties for : ",subject," : with attr col/type: ",dataProp, lit_value, attrType)
                    
                        # add a triple for the data property
                        
                        g.add((URIRef(stringToURI[subject]), URIRef(ns + dataProp),  Literal(lit_value,datatype=xsd + attrType) ))
            
        
        # if the metaData file has object Property entries, process them 
        
        
        if  pd.notnull(row['objectProperty']): 
            
            # parse the lists of object property, object column from metaData
            
            objPropList = row.objectProperty.split(':') 
            colList = row.objPropColumn.split(':') 
            
            # add a data property for each item in the list
            
            for ind in range(len(objPropList)):
                
                objCol=colList[ind]
                objProp =  objPropList[ind]
                
                # get a distinct list for the 2 columns from pizza: class name and attribute
                
                pairs = pizza[[subject_col,objCol]].groupby([subject_col, objCol]).count().reset_index()
                
                for subject, obj in zip(pairs[subject_col], pairs[objCol]):
                    
                    if Display:
                        print("create object Properties for : ",subject," : with objProp: ", objProp, obj)
                
                    subject = subject.translate(str.maketrans('', '', string.punctuation))
                    obj = obj.translate(str.maketrans('', '', string.punctuation))
                    
                    # write a triple for the object property
                    g.add((URIRef(stringToURI[subject]), URIRef(ns + objProp), URIRef(stringToURI[obj]) ))
            
    
    # get a list of ingredients used in the DF
    
    ingredients=createIngredientList(pizza,'item description')
    
    # create Ingredient class instances for each ingredient

    for instance in ingredients:
                
        if Display:
            print("creating class Ingredient for instance ", instance)
        
        classType='Ingredient'
        label_datatype='string'
        stringToURI[instance] = ns + instance.replace(" ", "_")

        # add ingredient triples
        
        g.add((URIRef(stringToURI[instance]), RDF.type, OWL.NamedIndividual)) 
        g.add((URIRef(stringToURI[instance]), RDF.type, URIRef(ns + classType)))
        g.add((URIRef(stringToURI[instance]), RDFS.label,  Literal(instance,datatype=xsd + label_datatype)) )
    
    # parse the CSV row 'item description' column to identify ingredients 
    # in a menu item and create hasIngredient object properties to link them

    objProp = 'hasIngredient'
    subject_col='menu item'
    object_col='item description'
    

    # get a distinct list for the 2 columns: MenuItem class name and item desc
    # containing ingredients
    
    pairs = pizza[[subject_col,object_col]].groupby([subject_col, object_col]).count().reset_index()
    
    # for each menu item, compare the description column to lookup list of 
    # ingredients and, where matched, add a hasIngredient object property 
    
    for subject, obj in zip(pairs[subject_col], pairs[object_col]):
        
        subject = subject.translate(str.maketrans('', '', string.punctuation))
        
        for ing in ingredients:
            
            if ing in obj:
                
                if Display:
                    print("create objProperty for : ",subject," has ingredient ",ing )    
                    
                g.add((URIRef(stringToURI[subject]), URIRef(ns + objProp), URIRef(stringToURI[ing]) ))
        
    
    # get a list of categories used in the DF
    
    categories=createCategoryList(pizza,'categories')
    
    # create class instances of Category

    for instance in sorted(set(categories)):
        
        if Display:
            print("creating class category for instance:", instance,":",len(instance))
        
        classType= 'Category'
        label_datatype='string'
        stringToURI[instance] = ns + instance.replace(" ", "_").replace("&", "and")
        
        g.add((URIRef(stringToURI[instance]), RDF.type, OWL.NamedIndividual)) 
        g.add((URIRef(stringToURI[instance]), RDF.type, URIRef(ns + classType)))
        g.add((URIRef(stringToURI[instance]), RDFS.label,  Literal(instance,datatype=xsd + label_datatype)) )
  
    # create objectProperty of hasCategory for Pizza outlets
    
    objProp = 'hasCategory'
    subject_col='name'
    object_col='categories'
    
    # get a distinct list for the 2 columns:  name (PizzaOutlet) and 
    # categories (list of )
    
    pairs = pizza[[subject_col,object_col]].groupby([subject_col, object_col]).count().reset_index()
    
    for subject, obj in zip(pairs[subject_col], pairs[object_col]):
        
        
        subject = subject.translate(str.maketrans('', '', string.punctuation))
        
        for cat in sorted(set(categories)):
            
            if cat in obj.lower():
                if Display:
                    print("create objProperty for : ",subject," has category ",cat )        
                g.add((URIRef(stringToURI[subject]), URIRef(ns + objProp), URIRef(stringToURI[cat]) ))
        
    
def createIngredientList(pizza,column_name):
        
    # parse the 'column_name' (item description) column of the 'pizza' dataframe to identify 
    # suitable ingredients to create as Ingredient class instances
        
    ingredients=[]            
    
    # create list 'ingredients' with all listed in the item description column
    
    for instance in (pizza[column_name].unique()):
        
        if "," in str(instance):
            ingList = instance.split(',') 
            for ind in range(len(ingList)):
                text=ingList[ind]
                text=text.lower().lstrip()
                ingredients.append(text)
    
    
    if Display:
        print("number of ingredients found in csv: ",len(ingredients))
    
    # use the Counter to write the ingredients to a dictionary    
    
    '''
    dictIng = Counter(ingredients) # dict of ingredients and occurences
    print(dictIng)    # all from dictionary with items sorted by no of occurences

    '''
    
    # as the list from the full dataset is so long, for this exercise we will
    # hardcode the ingredients from the most popular in the list
    
    ingredients = ['pineapple','mozzarella','onion','mushroom','basil','tomato','cheese','garlic', 'green peppers', 'bacon','spinach', 'broccoli','pepperoni','sausage', 'oregano','chicken','meatballs','olives']
    
    '''
    for ing in sorted(set(ingredients)):
        print(ing)
    
    '''    
        
    return ingredients

def cleanCategory(text):

        # hardcoded data fixes
        
        text=text.replace("Streeterville","")
        text=text.lower().lstrip().rstrip()
        text=text.replace("restaurants","restaurant")
        text=text.replace("university university","university")
        text=text.replace("shoe stores","shoe store")
        
        return text
    
    
def createCategoryList(pizza,column_name):
            
    # parse the 'column_name' (Categories) column of the 'pizza' dataframe to identify 
    # suitable categories to create as Category class instances
        
    categories=[]       
     
    # create list 'categories' parsed from the item description column
    
    for instance in (pizza[column_name].unique()):
        
        catList = instance.replace("/",",").replace("and",",").replace("\\","").split(',') 
        
        for ind in range(len(catList)):
            
            text=cleanCategory(catList[ind])
            
            if text != '':
                categories.append(text)
    
    if Display:
        print("number of categories found in csv: ",len(categories))
        
    
        
    return categories

        
def csvToRDF(inFile="pizza_cutdown.csv"):   
     
    print("\nStarting csvToRDF ....")   
        
    global data_dir
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    
    externalURI=True
    Display=False    
    
    # read in CSV file and convert to a dataframe
        
    inFile = os.path.join(data_dir,inFile)
            
    
    print("Reading file: ",inFile)        
    pizza = pd.read_csv(inFile, sep=',', quotechar='"',escapechar="\\") 
    
    
    # replace DF pizza with cleaned version

    pizza =  pizza.applymap(cleanString)
     
    # create a graph, g, and load triples from CSV
    
    g = Graph()    
    createTriples(pizza,g) 
    
    # write completed graph to .ttl file
    
    outFile = "pizza_data.ttl" 
        
    outFile = os.path.join(data_dir,outFile)
    
    print("Writing file: ",outFile)
    saveGraph(g,outFile)
    
    
    print("Finished csvToRDF ....")




externalURI=True
Display=False 

# to run stand-alone
#csvToRDF("pizza_cutdown.csv")




#print(getExternalURI('City','Portland')) # test external id search