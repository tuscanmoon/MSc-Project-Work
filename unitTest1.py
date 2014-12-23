#######################################################
# 
# Name: unitTest1.py
# Description:  Test script for the CalcNumberOfDoc module
# Created on:   22-Mar-2010
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
    documentLocation = 'C:/Users/paul/Documents/Education/MRes/Project/HJ801/data/test.xml'
    
    #variables
    doc = etree.parse(documentLocation)
    documentCounter = task.CalcNumberOfDoc()

    #Calculate number of documents
    documentType = TRAINING_DOCUMENT
    numberOfDocuments = documentCounter.calcNumberOfDoc(documentLocation, documentType)
    print(numberOfDocuments)
