#######################################################
#
# Name: tasks.py
# Description:  Implements the tasks required for Text Categorization.
# Created on:   12-Apr-2010
# Author:       Paul White
#
#######################################################
import dataClasses
import math
from lxml import etree
from subprocess import call
from nltk.stem import *

class CalcCategoryTermFrequency:
    #This calculates the probability of a term given a category and forms
    #part of the supervised learning for a Naive Bayes based text
    #categorization routine.  It should be run over Training Document instances
    #and their associated Document Feature instances.
    def calcCategoryTermFrequency(self, wrkFileLoc):
        #constants
        DELIM = "~"
        NO = "no"
        YES = "yes"
        dbReplace = 'mysqlimport -u root -p --lines-terminated-by="\\r\\n"' + \
        ' --fields-terminated-by="~" --delete --password="fjXhcvbj" --local hj801 '

        lineEnd = '\n'

        #variables
        categoryEntity = dataClasses.Category()
        categoryTerm = dataClasses.CategoryTerm()
        categoryTermFile = open(wrkFileLoc + 'category_term.txt', 'w')
        documentCategory = dataClasses.DocumentCategory()
        documentTermDict = dict()
        newDocumentTermDict = dict()
        termEntity = dataClasses.Term()

        #get current key value
        categoryTermId = categoryTerm.getLastKeyValue()

        #load starter terms dict
        termList = termEntity.get()
        if termList is not None:
            for t in termList:
                documentTermDict[t.termId] = 0

        #calculate the frequency (probability) of a term
        #given a particular class
        categoryList = categoryEntity.get() #get all categories
        if categoryList is not None:
            for c in categoryList:
                categoryId = c.categoryId

                #read all documents for this class
                totalTermsForCategoryCount = 0 #reset
                documentCategory = dataClasses.DocumentCategory()
                documentCategoryList = documentCategory.getDocumentByCategory(categoryId)
                if documentCategoryList is not None:
                    for dc in documentCategoryList:

                        #now get all terms for document list
                        documentTerm = dataClasses.DocumentTerm()
                        documentTermList = documentTerm.getByDocument(dc.documentId)
                        if documentTermList is not None:
                            for df in documentTermList:
                                #accumulate term frequency
                                totalTermsForCategoryCount = totalTermsForCategoryCount + \
                                 df.termFrequency
                                categoryTermCount = documentTermDict.get(df.termId, 0)
                                documentTermDict[df.termId] = categoryTermCount + \
                                 df.termFrequency

                #end of terms for this category
                #check for zero frequency records, if found apply Laplace correction
                #(if requested)
                laplaceCorrectionRequired = NO #assume not required
                if totalTermsForCategoryCount > 0:
                    if documentTermDict is not None:
                        for terms in documentTermDict.items():
                            if terms[1] == 0: #check for any zero count terms
                                laplaceCorrectionRequired = YES
                                break #leave loop if found

                        if laplaceCorrectionRequired == YES:
                            totalTermsForCategoryCount = 0 #reset
                            for terms in documentTermDict.items():
                                #add 1 to all term counts
                                #this ensures that this is no zero counts
                                newDocumentTermDict[terms[0]] = terms[1] + 1
                                totalTermsForCategoryCount = totalTermsForCategoryCount + \
                                 terms[1] + 1

                            documentTermDict = newDocumentTermDict

                #now read back dictionary of terms and write category term record
                if totalTermsForCategoryCount > 0:
                    if documentTermDict is not None:
                        for terms in documentTermDict.items():
                            categoryTermId = categoryTermId + 1
                            termId = terms[0]
                            normalizedCategoryTermFrequency = float(terms[1]) / totalTermsForCategoryCount
                            tmpStr = str(categoryTermId) + DELIM + str(categoryId) + \
                             DELIM + str(termId) + DELIM + str(normalizedCategoryTermFrequency)  + \
                              lineEnd
                            categoryTermFile.write(tmpStr)

                            #reset dict for next category
                            if documentTermDict is not None:
                                for t in documentTermDict.iterkeys():
                                    documentTermDict[t] = 0

        categoryTermFile.close()
        callStr = dbReplace + wrkFileLoc + 'category_term.txt'
        call(callStr, shell=True) #batch import into RDBMS

class CalcNumberOfDoc:
    #The purpose of this task is to calculate how many documents exist in a
    #given set.  It will return an integer holding this value.
    def calcNumberOfDoc(self, documentLocation, documentType):
        #use xpath statement to count number of documents for a given type at a given location
        doc = etree.parse(documentLocation)
        xpathString = "count(//document[type='" + documentType + "'])"
        numberOfDocuments = doc.xpath(xpathString)
        return(numberOfDocuments)

class CategorizeDocument:
    #This uses a Naive Bayes based algorithm to assign one or more categories
    #to a given document.
    def categorizeDocument(self, documentType, wrkFileLoc, numberOfCategoriesToAssign = 1):
        #constants
        TEST_DOCUMENT = "TEST"
        GIVEN = 1
        CALCULATED = 2

        dbAppend = 'mysqlimport -u root -p --lines-terminated-by="\\r\\n"' + \
        ' --fields-terminated-by="~" --password="fjXhcvbj" --local hj801 '
        lineEnd = '\n'
        DELIM = "~"

        #variables
        categoryDict = dict()
        categoryEntity = dataClasses.Category()
        categoryTerm = dataClasses.CategoryTerm()
        categoryTermDict = dict()
        categoryTermProbDict = dict()
        document = dataClasses.Document()
        documentCategory = dataClasses.DocumentCategory()
        documentCategoryFile = open(wrkFileLoc + 'document_category.txt', 'w')
        documentTerm = dataClasses.DocumentTerm()
        givenCategorySet = set()

        #get last key value for Document Category entity
        documentCategoryId = documentCategory.getLastKeyValue()

        #read all category records into memory
        categoryList = categoryEntity.get()
        if categoryList is not None:
            for c in categoryList:
                categoryDict[c.categoryId] = c.normalizedCategoryFrequency

        #read all category term records into memory
        categoryTermList = categoryTerm.get()
        if categoryTermList is not None:
            for ct in categoryTermList:
                catTermStr = str(ct.categoryId) + ":" + str(ct.termId)
                categoryTermDict[catTermStr] = ct.normalizedCategoryTermFrequency

        #read current given document classes into memory
        documentCategoryList = documentCategory.getByDocumentType(TEST_DOCUMENT, GIVEN)
        if documentCategoryList is not None:
            for dc in documentCategoryList:
                docCategoryStr = (str(dc.documentId) + ':' + str(dc.categoryId))
                givenCategorySet.add(docCategoryStr)

        #Set loop to read all TEST Documents
        documentList = document.getDocumentByType(documentType)
        if documentList is not None:
            for d in documentList:
                documentId = d.documentId
                documentTermList = documentTerm.getByDocument(documentId)

                #compare each category for this document as per Naive Bayes
                #first P(Category)
                if categoryDict is not None:
                    for c in categoryDict.iteritems():
                        categoryId = c[0]
                        categoryTermProbDict[categoryId] = math.log(c[1])
                        #now calculate P(Term|Category)
                        if documentTermList is not None:
                            for dt in documentTermList:
                                #now retrieve P(Term|Category)
                                catTermStr = str(categoryId) + ":" + str(dt.termId)
                                if catTermStr in categoryTermDict:
                                    categoryTermProbDict[categoryId] = \
                                     categoryTermProbDict.get(categoryId,0) + \
                                     math.log(categoryTermDict.get(catTermStr,0))

                #read back classes and write document class record
                ds = 0
                categoriesToAssign = numberOfCategoriesToAssign
                if categoryTermProbDict is not None:
                    for ct in sorted(categoryTermProbDict.iteritems(), \
                     key=lambda (k,v): (v,k), reverse=True):
                        if ds < categoriesToAssign:
                            ds = ds + 1
                            documentCategoryId = documentCategoryId + 1
                            categoryId = ct[0]
                            categoryWeight = ct[1]
                            categoryWeightTypeId = CALCULATED
                            positive_assignment = 0

                            #check if assigned class is part of given class set
                            docCategoryStr = (str(documentId) + ':' + str(categoryId))
                            if docCategoryStr in givenCategorySet:
                                givenCategorySet.discard(docCategoryStr)
                                positive_assignment = 1

                            tmpStr = str(documentCategoryId) + DELIM + str(documentId) + \
                             DELIM + str(categoryId) + DELIM + str(categoryWeight) + \
                             DELIM + str(categoryWeightTypeId) + DELIM + \
                              str(positive_assignment) + lineEnd
                            documentCategoryFile.write(tmpStr)

        #end
        documentCategoryFile.close()

        print("Load document classes.....")
        callStr = dbAppend + wrkFileLoc + 'document_category.txt'
        call(callStr, shell=True)

class CheckResults:
    #Used to add the meta-data required to check the effectiveness of the
    #text categorization run.
    def checkResults(self, wrkFileLoc):
        #constants
        TEST_DOCUMENT = "TEST"
        NO = "no"
        YES = "yes"
        DELIM = "~"
        GIVEN = 1
        CALCULATED = 2
        dbReplace = 'mysqlimport -u root -p --lines-terminated-by="\\r\\n"' + \
        ' --fields-terminated-by="~" --delete --password="fjXhcvbj" --local hj801 '

        lineEnd = '\n'

        #variable
        document = dataClasses.Document()
        documentAuditFile = open(wrkFileLoc + 'document_audit.txt', 'w')
        documentCategory = dataClasses.DocumentCategory()
        documentDict = dict()
        firstTimeThru = YES
        givenCategorySet = set()
        svDocumentID = int()
        documentAuditId = int()
        truePositive = int()
        falsePositive = int()

        #read document category count into memory
        documentType = TEST_DOCUMENT
        documentList = document.getDocumentByType(documentType)
        if documentList is not None:
            for d in documentList:
                documentDict[d.documentId] = d.documentCategoryCount

        #read current given document classes into memory
        documentType = TEST_DOCUMENT
        categoryWeightTypeId = GIVEN
        documentCategoryList = documentCategory.getByDocumentType(documentType, \
         categoryWeightTypeId)
        if documentCategoryList is not None:
            for dc in documentCategoryList:
                docCategoryStr = (str(dc.documentId) + ':' + str(dc.categoryId))
                givenCategorySet.add(docCategoryStr)

        documentType = TEST_DOCUMENT
        categoryWeightTypeId = CALCULATED
        categoryForDocumentList = documentCategory.getByDocumentType(documentType, \
         categoryWeightTypeId)
        if categoryForDocumentList is not None:
            for cd in categoryForDocumentList:
                documentId = cd.documentId
                categoryId = cd.categoryId
                positiveAssignment = cd.positiveAssignment
                categoryWeightTypeId = cd.categoryWeightTypeId
                #have any control fields changed
                if (svDocumentID != documentId):
                    if firstTimeThru == NO:
                        #write new audit record
                        documentCategoryCount = documentDict.get(svDocumentID, 0)
                        documentAuditId = documentAuditId + 1
                        tmpStr = str(documentAuditId) + DELIM + str(svDocumentID) + DELIM + \
                         str(categoryWeightTypeId) + DELIM + str(truePositive) + DELIM + \
                         str(falsePositive) + DELIM + str(documentCategoryCount) + lineEnd
                        documentAuditFile.write(tmpStr)
                    else:
                        firstTimeThru = NO

                    svDocumentID = documentId
                    truePositive = 0
                    falsePositive = 0

                #check is assigned class is part of given class set
                docCategoryStr = (str(documentId) + ':' + str(categoryId))

                if positiveAssignment == 1:
                    truePositive = truePositive + 1
                else:
                    falsePositive = falsePositive + 1

            #remember to write last record
            if firstTimeThru == NO:
                #write new audit record
                documentCategoryCount = documentDict.get(svDocumentID, 0)
                documentAuditId = documentAuditId + 1
                tmpStr = str(documentAuditId) + DELIM + str(documentId) + DELIM + \
                 str(categoryWeightTypeId) + DELIM + str(truePositive) + DELIM + \
                 str(falsePositive) + DELIM + str(documentCategoryCount) + lineEnd
                documentAuditFile.write(tmpStr)

        documentAuditFile.close()

        callStr = dbReplace + wrkFileLoc + 'document_audit.txt'
        call(callStr, shell=True)

class TermReduction:
    #This is used to reduce the number of terms in the Term Dictionary.  The
    #normalized document frequency (number of documents that the term appears
    #in divided by the total number of documents) is used as selection criteria.
    def reduceTerm(self, wrkFileLoc, thresholdFrequency):
        #variables
        termEntity = dataClasses.Term()

        #delete terms by document frequency
        termEntity.deleteByFrequency(thresholdFrequency)

class DocumentTermReduction:
    #This is used to reduce the dimensionality of the Document Term vector by
    #applying logic that reduces the vector to those terms that are the most
    #appropriate, from a semantic sense, to represent the document.
    def reduceDocumentTerm(self, documentType, wrkFileLoc, thresholdPercentage):
        #constants
        DELIM = "~"
        dbAppend = 'mysqlimport -u root -p --lines-terminated-by="\\r\\n"' + \
        ' --fields-terminated-by="~" --password="fjXhcvbj" --local hj801 '
        lineEnd = '\n'

        #variables
        #document = dataClasses.Document()
        documentTerm = dataClasses.DocumentTerm()
        documentTermFile = open(wrkFileLoc + 'document_term.txt', 'w')

        #get current key values
        documentTermId = documentTerm.getLastKeyValue()

        #read each Document and calculate number of terms to keep.
        documentTermList = documentTerm.getTermCountByDocument()
        if documentTermList is not None:
            for df in documentTermList:
                termCount = 0
                documentTermThreshold = \
                 int(math.ceil((float(df.documentTermCount * thresholdPercentage) / 100)))

                #set new loop to process existing document terms for this document
                documentTermList2 = documentTerm.getByDocumentTfIdfOrder(df.documentId)
                if documentTermList2 is not None:
                    for df2 in documentTermList2:
                        termCount = termCount + 1
                        if termCount <= documentTermThreshold:
                            documentTermId = documentTermId + 1
                            tmpStr = str(documentTermId) + DELIM + str(df2.termId) + \
                             DELIM + str(df2.documentId) + DELIM + str(df2.normalizedTermFrequency) + \
                             DELIM + str(df2.tfIdf)+ DELIM + str(df2.termFrequency) + lineEnd
                            documentTermFile.write(tmpStr)
                        else:
                            break

        #remove existing instances
        documentTerm.deleteByDocumentType(documentType)

        #close file and write new document term records
        documentTermFile.close()
        callStr = dbAppend + wrkFileLoc + 'document_term.txt'
        call(callStr, shell=True)

class IndexDocument:
    #This converts a given document(s) into a vector of terms that can be used
    #to represent that document in a semantic sense.
    def indexDocument(self, documentLocation, documentType, wrkFileLoc):
        #constants
        NO = "no"
        YES = "yes"
        DELIM = "~"

        dbAppend = 'mysqlimport -u root -p --lines-terminated-by="\\r\\n"' + \
        ' --fields-terminated-by="~" --password="fjXhcvbj" --local hj801 '
        lineEnd = '\n'

        #variables
        categoryDict = dict()
        categoryEntity = dataClasses.Category()
        classesExist = NO
        doc = etree.parse (documentLocation)
        document = dataClasses.Document()
        documentCategory = dataClasses.DocumentCategory()
        documentCategoryCount = int()
        documentCategoryDict = dict()
        documentCategoryFile = open(wrkFileLoc + 'document_category.txt', 'w')
        documentTerm = dataClasses.DocumentTerm()
        documentTermCount = int()
        documentTermFile = open(wrkFileLoc + 'document_term.txt', 'w')
        documentFile = open(wrkFileLoc + 'document.txt', 'w')
        termOccurenceDict = dict()
        firstTimeThru = YES
        stemmer = PorterStemmer()
        stopChar = dataClasses.StopChar()
        stopCharacter = list()
        stopWord = dataClasses.StopWord()
        stopWords = list()
        termEntity = dataClasses.Term()
        normalizedTermFrequencyDict = dict()
        termDict = dict()
        word = str()

        #get current key values
        documentId = document.getLastKeyValue()
        documentCategoryId = documentCategory.getLastKeyValue()
        documentTermId = documentTerm.getLastKeyValue()

        #load categories
        categoryEntity = dataClasses.Category()
        categoryList = categoryEntity.get()
        if categoryList is not None:
            for c in categoryList:
                categoryDict[c.categoryName] = c.categoryId

        #load terms
        termEntity = dataClasses.Term()
        termList = termEntity.get()
        if termList is not None:
            for t in termList:
                termDict[t.term] = t.termId
                normalizedTermFrequencyDict[t.termId] = t.normalizedTermFrequency

        #load Stop Words
        stopWordList = stopWord.get()
        for s in stopWordList: #decode list of tuples into simple stop char list
            stopWords.append(s.stopWord)

        stopCharList = stopChar.get()
        for s in stopCharList: #decode list of tuples into simple stop char list
            stopCharacter.append(s.stopChar)


        #main processing of XML Document
        xpathString = "/documents/document[type='" + documentType + "']"
        for d in doc.xpath(xpathString): #read through XML document and parse nodes
            if len(d) > 0:
                for e in d:
                    if e.tag == "title": #title & new document
                        if firstTimeThru == NO: #write a new record for previous document & reset variables
                            #only write document record if classes exist for document
                            if classesExist == YES:
                                tmpStr = str(documentId) + DELIM + str(documentName) + \
                                 DELIM + str(documentType) + DELIM + str(documentCategoryCount) + \
                                  lineEnd
                                documentFile.write(tmpStr)

                                #write document classes
                                if documentCategoryDict is not None:
                                    for dc in documentCategoryDict.iteritems():
                                        documentCategoryId = documentCategoryId + 1
                                        tmpStr = str(documentCategoryId) + DELIM + \
                                         str(documentId) + DELIM + str(dc[0]) + \
                                         DELIM + str(dc[1]) + DELIM + '1' + DELIM + '1' + lineEnd
                                        documentCategoryFile.write(tmpStr)

                                #write document terms
                                if termOccurenceDict is not None:
                                    for t in termOccurenceDict.iteritems():
                                        documentTermId = documentTermId + 1
                                        termId = t[0]
                                        termFrequency = int(t[1])
                                        if int(t[1]) > 0:
                                            normalizedTermFrequency = (float(termFrequency) / documentTermCount)
                                        else:
                                            normalizedTermFrequency = 0

                                        #calculate tf-idf
                                        tfIdf = float()
                                        inverseDocumentFrequency = \
                                         (1 / float(normalizedTermFrequencyDict.get(termId, 0)))
                                        tfIdf = normalizedTermFrequency * inverseDocumentFrequency
                                        tmpStr = str(documentTermId) + DELIM + \
                                         str(termId) + DELIM + str(documentId) + \
                                         DELIM + str(normalizedTermFrequency) + DELIM + str(tfIdf) + \
                                         DELIM + str(termFrequency) + lineEnd
                                        documentTermFile.write(tmpStr)

                                #reset variables
                                documentName = ""
                                documentType = ""
                                documentTermCount = 0
                                documentCategoryCount = 0
                                documentCategoryDict.clear()
                                termOccurenceDict.clear()
                                classesExist = NO
                                documentId = documentId + 1

                        else:
                            firstTimeThru = NO
                            documentId = documentId + 1

                        #document name
                        if e.text is not None:
                            titleText = e.text
                            documentName = e.text.strip()
                            documentName = documentName.replace("'", "")
                            documentName = documentName.replace('"', '')
                            documentName = documentName.replace("\n", '')
                        else:
                            documentName = ""
                            titleText = ""

                    elif e.tag == "type": #document type
                        if e.text is not None:
                            documentType = e.text.strip()
                        else:
                            documentType = ""

                    elif e.tag == "classification": #possible multiple classifications
                        if e.text is not None:
                            #get class id
                            if e.text.strip() in categoryDict:
                                categoryId = categoryDict.get(e.text.strip())
                                if categoryId not in documentCategoryDict:
                                    documentCategoryDict[categoryId] = int(1)
                                    documentCategoryCount = documentCategoryCount + 1
                                    classesExist = YES

                    elif e.tag == "text": #text likely to be split over several lines
                        #this bit takes each line and strips out individual terms
                        if e.text is not None:
                            totalText = titleText + " " + e.text
                        else:
                            totalText = titleText
                        if totalText is not None:
                            for s in totalText:
                                if ord(s) > 64: #65 is the start of the alphabet
                                    if s not in stopCharacter:
                                        word = word + s.lower()
                                else:
                                    if word not in stopWords:
                                        word = stemmer.stem_word(word)
                                        termId = termDict.get(word, 0)
                                        if termId > 0:
                                            documentTermCount = documentTermCount + 1
                                            termOccurence = termOccurenceDict.get(termId, 0)
                                            termOccurenceDict[termId] = termOccurence + 1
                                    word = "" #reset word to empty

                            #process last word
                            if word not in stopWords:
                                word = stemmer.stem_word(word)
                                termId = termDict.get(word, 0)
                                word = str()
                                if termId > 0:
                                    documentTermCount = documentTermCount + 1
                                    termOccurence = termOccurenceDict.get(termId, 0)
                                    termOccurenceDict[termId] = termOccurence + 1


        #write last header record
        if firstTimeThru == NO:
            if classesExist == YES:
                tmpStr = str(documentId) + DELIM + str(documentName) + DELIM + \
                 str(documentType) + DELIM + str(documentCategoryCount) + lineEnd
                documentFile.write(tmpStr)

                #write document classes
                if documentCategoryDict is not None:
                    for dc in documentCategoryDict.iteritems():
                        documentCategoryId = documentCategoryId + 1
                        tmpStr = str(documentCategoryId) + DELIM + str(documentId) + \
                         DELIM + str(dc[0]) + DELIM + str(dc[1]) + DELIM + '1' + \
                         DELIM + '1' + lineEnd
                        documentCategoryFile.write(tmpStr)

                #write document terms
                if termOccurenceDict is not None:
                    for t in termOccurenceDict.iteritems():
                        documentTermId = documentTermId + 1
                        termId = t[0]
                        termFrequency = int(t[1])
                        if documentTermCount > 0:
                            normalizedTermFrequency = (float(termFrequency) / documentTermCount)
                        else:
                            normalizedTermFrequency = 0

                        #calculate tf-idf
                        inverseDocumentFrequency = \
                         (1 / float(normalizedTermFrequencyDict.get(termId, 0)))
                        tfIdf = normalizedTermFrequency * inverseDocumentFrequency

                        tmpStr = str(documentTermId) + DELIM + str(termId) + \
                         DELIM + str(documentId) + DELIM + str(normalizedTermFrequency) + \
                         DELIM + str(tfIdf) + DELIM + str(termFrequency) + lineEnd
                        documentTermFile.write(tmpStr)

        #close load files
        documentFile.close()
        documentCategoryFile.close()
        documentTermFile.close()

        #Load data
        print("Load documents.....")
        callStr = dbAppend + wrkFileLoc + 'document.txt'
        call(callStr, shell=True)

        print("Load document categories.....")
        callStr = dbAppend + wrkFileLoc + 'document_category.txt'
        call(callStr, shell=True)

        print("Load document terms.....")
        callStr = dbAppend + wrkFileLoc + 'document_term.txt'
        call(callStr, shell=True)

class PopulateCategory:
    #This uses a given document set to create a set of Categories.
    def populateCategory(self, documentLocation, documentType, wrkFileLoc, numberOfDocuments):
        #constants
        DELIM = "~"
        dbReplace = 'mysqlimport -u root -p --lines-terminated-by="\\r\\n"' + \
        ' --fields-terminated-by="~" --delete --password="fjXhcvbj" --local hj801 '

        lineEnd = '\n'

        #variables
        categoryId = int()
        categoryDict = dict()
        doc = etree.parse (documentLocation)

        #using xpath, look for all categories
        categoryType = "classification"
        xpathString = "/documents/document[type='" + documentType + "']/" + categoryType
        for d in doc.xpath(xpathString):
            if d.text is not None:
                categoryName = d.text.strip()
                categoryCount = categoryDict.get(categoryName, 0)
                categoryDict[categoryName] = categoryCount + 1

        #populate categories
        if categoryDict is not None:
            categoryFile = open(wrkFileLoc + 'category.txt', 'w')
            for c in categoryDict.items():
                categoryId = categoryId + 1
                categoryName = c[0]
                normalizedCategoryFrequency = float(c[1]) / numberOfDocuments
                tmpStr = str(categoryId) + DELIM + categoryName + DELIM + \
                 str(normalizedCategoryFrequency) + lineEnd
                categoryFile.write(tmpStr)

            categoryFile.close()
            callStr = dbReplace + wrkFileLoc + 'category.txt'
            print(callStr)
            call(callStr, shell=True)

class PopulateTerm:
    #This uses a given document set to create a set of Terms (known as
    #the Term Dictionary).
    def populateTerm(self, documentLocation, documentType, wrkFileLoc, numberOfDocuments):
        #constants
        DELIM = "~"
        dbReplace = 'mysqlimport -u root -p --lines-terminated-by="\\r\\n"' + \
        ' --fields-terminated-by="~" --delete --password="fjXhcvbj" --local hj801 '

        lineEnd = '\n'

        #variables
        doc = etree.parse(documentLocation)
        docWordSet = set()
        stemmer = PorterStemmer()
        stopChar = dataClasses.StopChar()
        stopCharList = stopChar.get()
        stopWord = dataClasses.StopWord()
        stopWordList = stopWord.get()
        stopCharacter = list()
        stopWords = list()
        wordParseDict = dict()
        termFile = open(wrkFileLoc + 'term.txt', 'w')
        termId = int()
        word = str()

        for s in stopWordList: #decode list of tuples into simple stop char list
            stopWords.append(s.stopWord)

        for s in stopCharList: #decode list of tuples into simple stop char list
            stopCharacter.append(s.stopChar)

        #look for all terms
        #process the title & text nodes in the document xml
        xpathString = "/documents/document[type='" + documentType + "']"
        for d in doc.xpath(xpathString): #read through XML document and parse nodes
            if len(d) > 0:
                for e in d:
                    docWordSet.clear()
                    if e.tag == "title":
                        if e.text is not None:
                            titleText = e.text
                        else:
                            titleText = ""
                    if e.tag == "text":
                        if e.text is not None:
                            totalText = titleText + " " + e.text
                        else:
                            totalText = titleText
                        if totalText is not None:
                            for s in totalText:
                                if ord(s) > 64: #65 is the start of the alphabet
                                    if s not in stopCharacter:
                                        word = word + s.lower()
                                else:
                                    if word not in stopWords:
                                        word = stemmer.stem_word(word)
                                        if word != "":
                                            #check if already seen in this document
                                            if not word in docWordSet:
                                                docWordSet.add(word)
                                                wordCount = wordParseDict.get(word, 0)
                                                wordParseDict[word] = wordCount + 1

                                    word = "" #reset

                        #remember to write last word
                        if word != "":
                            wordCount = wordParseDict.get(word, 0)
                            wordParseDict[word] = wordCount + 1

        #populate terms
        if wordParseDict is not None:
            for t in wordParseDict.items(): #read word dict and update persistent store
                term = t[0]
                termId = termId + 1
                if numberOfDocuments > 0:
                    normalizedTermFrequency = float(t[1]) / numberOfDocuments
                else:
                    normalizedTermFrequency = 0
                tmpStr = str(termId) + DELIM + term + DELIM + \
                 str(normalizedTermFrequency) + lineEnd
                termFile.write(tmpStr)

        termFile.close()
        callStr = dbReplace + wrkFileLoc + 'term.txt'
        call(callStr, shell=True)

class ResetSystem:
    #This clears all persistent data that pertains to previous training and
    #testing runs.
    def resetSystem(self):
        #constants

        #variables
        categoryEntity = dataClasses.Category()
        categoryTerm = dataClasses.CategoryTerm()
        document = dataClasses.Document()
        documentTerm = dataClasses.DocumentTerm()
        documentCategory = dataClasses.DocumentCategory()
        term = dataClasses.Term()

        #Reset persistent data
        categoryTerm.delete() #Delete Category Term Instances
        documentCategory.delete() #Delete Document Category Instances
        documentTerm.delete() #Delete Document Term Instances
        categoryEntity.delete() #Delete Category Instances
        document.delete() #Delete Document Instances
        term.delete() #Delete Term Instances