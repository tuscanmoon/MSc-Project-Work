#######################################################
#
# Name: test.py
# Description:  Script to run test process for
#               Text Categorization process.
# Created on:   12-Apr-2010
# Author:       Paul White
#
#######################################################
import dataClasses
import task
from lxml import etree

if __name__ == "__main__":
    #constants
    TEST_DOCUMENT = "TEST"
    TRAINING_DOCUMENT = "TRAIN"
    documentLocation = 'C:/Users/paul/Documents/Education/MRes/Project/HJ801/data/reuters_full.xml'

    #variables
    doc = etree.parse(documentLocation)
    documentCategorizer = task.CategorizeDocument()
    document = dataClasses.Document()
    documentCategory = dataClasses.DocumentCategory()
    documentTerm = dataClasses.DocumentTerm()
    documentIndexer = task.IndexDocument()
    featureReducer = task.DocumentTermReduction()
    numberOfCategoriesToAssign = 1
    resultChecker = task.CheckResults()
    thresholdPercentage = 100
    wrkFileLoc = "C:/Users/paul/Documents/Education/MRes/Project/HJ801/data/"

    #Remove existing Test Documents from previous runs
    print("Remove existing Test Documents from previous runs.....")
    documentType = TEST_DOCUMENT
    documentCategory.deleteByDocumentType(documentType)
    documentTerm.deleteByDocumentType(documentType)
    document.deleteByDocumentType(documentType)

    #Index Document
    print("Parsing data.....")
    documentType = TEST_DOCUMENT
    documentIndexer.indexDocument(documentLocation, documentType, wrkFileLoc)

    #Reduce Feature
    print("Reduce Feature.....")
    documentType = TEST_DOCUMENT
    if thresholdPercentage < 100:
        featureReducer.reduceDocumentTerm(documentType, wrkFileLoc, \
         thresholdPercentage)

    #Categorize document
    print("Classifying document.....")
    documentType = TEST_DOCUMENT
    documentCategorizer.categorizeDocument(documentType, wrkFileLoc, \
     numberOfCategoriesToAssign)

    #Check results
    print("Checking results.....")
    resultChecker.checkResults(wrkFileLoc)
