# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 18:46:57 2021

@author: judit_k4b0noc
"""


import pandas as pd

import os
from os.path import dirname, abspath


def testDecode():
    
    string_with_nonASCII = "àa string withé fuünny charactersß."
    encoded_string = string_with_nonASCII.encode("ascii", "ignore")
    decode_string = encoded_string.decode()
    print(decode_string)



def cleanFunc(pizza):
    
    # run through specified columns in dataframe and print out cleaned data
    
    # translation table for non-ascii chars
    
    asciiDict = { 'é':'e', 'ë':'e','ê':'e', 'ở':'o', 'ò':'o'}
    
    # for each column in the df - only seems to be name,categories with non-ascii data
    
    for subject_col in ['name','categories']: # 'address','city','country','state',,'menu item','item description'
        
        print("SUBJECT COL: ",subject_col)
        
        for instanceName in (pizza[subject_col].unique()):
            
            
            # search and replace the non-ascii characters using the dict
            
            for letter,replacement in asciiDict.items():
                if letter in str(instanceName):
                    print("**** replacing from dict ****", letter,"/",replacement, " : ", instanceName)
                    instanceName = instanceName.replace(letter,replacement)
                    
            # remove all other non-ascii chars  (not in dict)      
            
            if str(instanceName).encode("ascii", "ignore").decode() != instanceName:
                #print(subject_col," : ",instanceName," : ",str(instanceName).encode("ascii", "ignore").decode())
                print("**** replacing other non ascii ****", instanceName)
                instanceName = str(instanceName).encode("ascii", "ignore").decode()
                    
                
def cleanString(oldString):
    
    # return oldString cleaned of non-ascii chars
    
    # translation table for non-ascii chars
    
    asciiDict = { 'é':'e', 'ë':'e','ê':'e', 'ở':'o', 'ò':'o'}
    
    # search and replace the non-ascii characters using the dict
    
    for letter,replacement in asciiDict.items():
        if letter in str(oldString):
            #print("**** replacing from dict ****", letter,"/",replacement, " : ", oldString)
            oldString = oldString.replace(letter,replacement)
            
    # remove all other non-ascii chars  (not in dict)      
    
    if str(oldString).encode("ascii", "ignore").decode() != oldString:
        
        #print("**** replacing other non ascii ****", oldString)
        oldString = str(oldString).encode("ascii", "ignore").decode()
        
    oldString=oldString.replace('nan','')
    
    #print("done cleanString for: ",oldString)            
    
    return oldString            
                     
    
    
def cleanFile(inFile):
    # when running in isolation    
    # read in CSV file, convert to a dataframe, clean and write back out
    
    data_dir = os.path.join(dirname(dirname(abspath(__file__))), 'data')
    
    inFile = os.path.join(data_dir,inFile)    
    
    print("Reading file: ",inFile)        
    pizza = pd.read_csv(inFile, sep=',', quotechar='"',escapechar="\\") 
   
    # replace DF pizza with cleaned cells
    pizza =  pizza.applymap(cleanString) 
    
    
    # write out the updated contents to check
    
    outFile="testCSV.csv"
    print("writing file: ",outFile)   
    pizza.to_csv(outFile,index=False)

    
                
def main():
    
    #print("\nStarting  cleanDF")   
# 
    
    inFile = "pizza_full.csv" 
    #cleanFile(inFile)
    
    
    # test cleanString
    ##print(cleanString("Bamcaf��"))
    #print(cleanString(" Brix Wine Café"))
    #print("\nFinished  cleanDF....")  
    
main()