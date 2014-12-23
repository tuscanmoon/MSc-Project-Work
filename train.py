#######################################################
#
# Name: train.py
# Description:  Script to run training process for
#               Text Categorization process.
# Created on:   12-Apr-2010
# Author:       Paul White
#
#######################################################

import task
from lxml import etree

if __name__ == "__main__":
    #constants
    RUN_DOCUMENT = "RUN"
    TEST_DOCUMENT = "TEST"
    TRAINING_DOCUMENT = "TRAIN"
    documentLocation = 'C:/Users/paul/Documents/Education/MRes/Project/HJ801/data/reuters_full.xml'
    NO = "no"
    YES = "yes"

    #variables
    calcCategoryTermFrequency = task.CalcCategoryTermFrequency()
    categoryPopulator = task.PopulateCategory()
    doc = etree.parse(documentLocation)
    documentCounter = task.CalcNumberOfDoc()
    documentIndexer = task.IndexDocument()
    featureReducer = task.DocumentTermReduction()
    termReducer = task.TermReduction()
    systemReset = task.ResetSystem()
    termPopulator = task.PopulateTerm()
    thresholdFrequency = 0.0
    wrkFileLoc = "C:/Users/paul/Documents/Education/MRes/Project/HJ801/data/"

    #Reset persistent data
    print("Reset persistent data.....")
    systemReset.resetSystem()

    #Calculate number of documents
    print("Calculate number of documents.....")
    documentType = TRAINING_DOCUMENT
    numberOfDocuments = documentCounter.calcNumberOfDoc(documentLocation, \
     documentType)

    #Populate Categories
    print("Populate categories.....")
    documentType = TRAINING_DOCUMENT
    categoryPopulator.populateCategory(documentLocation, documentType, \
     wrkFileLoc, numberOfDocuments)

    #Populate Terms
    print("Populate terms.....")
    documentType = 'TRAIN'
    termPopulator.populateTerm(documentLocation, documentType, wrkFileLoc, \
     numberOfDocuments)

    #Reduce Terms
    if thresholdFrequency > 0:
        print("Reducing terms.....")
        termReducer.reduceTerm(wrkFileLoc, thresholdFrequency)

    #Index Document
    print("Parsing data.....")
    documentType = 'TRAIN'
    documentIndexer.indexDocument(documentLocation, documentType, wrkFileLoc)

    #Calculate category term frequency - P(term|class)
    print("Calculate category term frequency.....")
    calcCategoryTermFrequency.calcCategoryTermFrequency(wrkFileLoc)
