# -*- coding: utf-8 -*-
'''
Created on 28 Mar 2021

@author: judith.grieves@city.ac.uk

INM713 - Semantic Web Technologies & Knowledge Graphs - module coursework

Ontology Embeddings (Task Vector) -  Subtask Vector.1-2
 
Subtask Vector.3 to do

load pizza.embeddings file(s) (generated from OWL2Vec)

Select pairs of entities (for any of the tested configurations) and
discuss the similarity of their vectors 

'''
from gensim.models import KeyedVectors

import os
from os.path import dirname, abspath



def loadEmbeddings():
      
    # load embeddings file(s) from OWL2Vec & interrogate vectors
    
    print("\nstarting loadEmbeddings ...")
    
    embed_dir = os.path.join(dirname(dirname(abspath(__file__))), 'embeddings')
    
    # for each output file of 1-3 OWL2Vec configurations
    
    for embedFileNo in [1,2]:
        
        print("\nAnalyse embeddings for experiment: ",embedFileNo)
        
        fileName = 'pizza_inf' + str(embedFileNo) + '.embeddings'
        fileName = os.path.join(embed_dir, fileName)
            
        # load the vector embeddings
        
        wv = KeyedVectors.load(fileName, mmap='r')
        
        print("\n",fileName,": ",wv)
            
        
        wordlist=[['pizza','pizza'],['ingredient','topping'],['mozzarella','cheese'],['state','meatballs'],['state','city'],['taverns','bars'],['taverns','grocery']]
        
        # for each pair of words in the above list, calculate the vector similarity
        
        for pair in wordlist:
            
            similarity = wv.similarity(pair[0], pair[1])
            print(pair," : similarity: ",similarity)            
        
        
        print("\nGet the most similar entities/words for the following elements")
        
        wordlist=['angeles','puttenesca','TX','olives']
        
        # for each word in the above list, find most similar other words
        
        for word in wordlist:
            print("\nmost similar words to ",word,": ")
            # warning message most_similar_cosmul deprecated - use self.wv.most_similar_cosmul() instead
            result = wv.most_similar_cosmul(positive=[word])
            print(result)
       
        
        print("finished loadEmbeddings ...")
        
        
def main():

    loadEmbeddings()


if __name__ == "__main__":

    main()
