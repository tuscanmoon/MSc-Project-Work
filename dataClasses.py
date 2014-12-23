#######################################################
#
# Name: DataClasses.py
# Description:  Defines the classes used in the Text CategorizationCategory system
#               It is abstracted one layer up from the persistent data storage,
#               this data storage is via a RDBMS.  The workings of the database
#               access are held in module dataPersistence
# Created on:   12-Apr-2010
# Author:       Paul White
#
#######################################################
import dataPersistence

class Category:
    #These are the categories used in the text categorization process.

    id = int() #The identifier for the category.

    name = str() #The name of the category.

    normalizedCategoryFrequency = float() #This is the number of documents that
    #the category has been assigned to in the Training Document Set, normalized
    #by the total number of training documents.  It is used as the probability
    #of a category for a document (P(category)).

    dbCategory = dataPersistence.DBCategory() #Link to data persistence layer.

    def get(self, categoryId = 0, categoryName = "%"): #Generic operation to
    #retrieve instances of Category.
        categoryList = self.dbCategory.read(categoryId, categoryName)
        return(categoryList)

    def delete(self, categoryId = 0): #Generic operation to delete instances
        self.dbCategory.delete(categoryId)
        #of Category.

class CategoryTerm:
    #This is used to hold the frequency relationship between Categories and
    #Terms.  This represents the probability of a Term given a Category.
    #This is an association class between the Category and Term data classes.

    id = int() #The identifier for the Category Term.

    categoryId = int() #The identifier of the category.

    termId = int() # The identifier of the term.

    normalizedCategoryTermFrequency = float() #The probability of a Term given
    #a Category.

    dbCategoryTerm = dataPersistence.DBCategoryTerm() #Link to data persistence
    #layer.

    def getLastKeyValue(self): #Retrieve the last key value for the category
    #term instances.
        categoryTermId = self.dbCategoryTerm.readLastKeyValue()
        return(categoryTermId)

    def get(self): #Generic operation to retrieve instances of Category Term.
        categoryTermList = self.dbCategoryTerm.read()
        return(categoryTermList)

    def getByTerm(self, termId): #Operation used to retrieve Category Term
    #instances given a particular Term.
        if termId!=0:
            categoryTermList = self.dbCategoryTerm.readByTerm(termId)
        else:
            categoryTermList = list()
        return(categoryTermList)

    def delete(self, categoryTermId = 0): #Generic operation to delete instances
    #of Category Term.
        self.dbCategoryTerm.delete(categoryTermId)

class Document:
    #This may be for example, an email or news feed article. For the purpose of
    #this research project, a document will be considered to be any discrete
    #unit that is composed of textual items (words, punctuation symbols,
    #letters, numbers, etc) that may or may not have an underlying structure.

    id = int() #The identifier for the Document.

    name = str() #The title of the Document.

    type = str() # Indicates if it is a Training or Test document.

    categoryCount = int() #Holds how many categories have been assigned to
    #this document.

    text = str() #The textual body of the document.

    dbDocument = dataPersistence.DBDocument() #Link to data persistence layer.

    def getLastKeyValue(self): #Retrieve the last key value for the Document
    #instances.
        documentId = self.dbDocument.readLastKeyValue()
        return(documentId)

    def getDocumentByType(self, documentType): #Operation to get Document
    #instances given a document type.  Document types equate to the
    #sub-classes of Document.
        documentList = self.dbDocument.readDocumentByType(documentType)
        return(documentList)

    def deleteByDocumentType(self, documentType): #Delete documents of a given
    #type.
        self.dbDocument.deleteByDocumentType(documentType)

    def delete(self, documentId = 0): #Generic operation to delete instances of
    #Documents.
        self.dbDocument.delete(documentId)

class DocumentCategory:
    #This is used to store the categories assigned to the Document.  This is an
    #association class between the Document and Category data classes.

    id = int() #The identifier for the Document Category.

    documentId = int() #The associated Document identifier.

    categoryId = int() #The associated Category identifier.

    classWeight = float() #The relative weight given to the instance that
    #indicates the likelihood that the category should be assigned to the document.

    classWeightTypeId = int() #The type of class weight (given, assigned)

    dbDocumentCategory = dataPersistence.DBDocumentCategory() #Link to data
    #persistence layer.

    def getDocumentByCategory(self, categoryId): #Operation to retrieve
    #Document Category instances given a particular Category.
        documentForCategoryList = self.dbDocumentCategory.readDocumentByCategory(categoryId)
        return(documentForCategoryList)
        self.dbDocumentCategory.con.close()

    def getLastKeyValue(self): #Retrieve the last key value for the Document
    #Category instances.
        documentCategoryId = self.dbDocumentCategory.readLastKeyValue()
        return(documentCategoryId)
        self.dbDocumentCategory.con.close()

    def getByDocumentType(self, documentType, categoryWeightTypeId = 0):
    #Operation to retrieve Document Category instances given a particular
    #Document Type (held on the related Document instance).
        categoryForDocumentList = self.dbDocumentCategory.readByDocumentType(documentType, \
         categoryWeightTypeId)
        return(categoryForDocumentList)
        self.dbDocumentCategory.con.close()

    def deleteByDocumentType(self, documentType): #Delete instances of a given
    #document type.
        self.dbDocumentCategory.deleteByDocumentType(documentType)

    def delete(self, documentCategoryId = 0): #Generic operation to delete
    #instances of Document Category.
        self.dbDocumentCategory.delete(documentCategoryId)

class DocumentTerm:
    #This is used to store the vector representation of the document.  Each
    #vector element is a term.

    id = int() #The identifier for the Document Term.

    termId = int() #The associated Term identifier.

    documentId = int() #The associated Document identifier.

    normalizedTermFrequency = float() #The number of times a Term appears in the
    #given document, normalized by the total number of Term instances
    #(features) in the document.

    tfIdf = float() #The term frequency - inverse document frequency for
    #the Document Feature.

    termFrequency = int() #The number of times a particular feature
    #(held as a term) appears in the document.  This is a raw, un-normalized, count.

    dbDocumentTerm = dataPersistence.DBDocumentTerm() #Link to data
    #persistence layer.

    def getLastKeyValue(self): ##Retrieve the last key value for the Document
    #Term instances.
        documentTermId = self.dbDocumentTerm.readLastKeyValue()
        return(documentTermId)

    def getByDocument(self, documentId = 0): #Operation to retrieve all
    #Document Feature instances for a particular Document.
        documentTermList = self.dbDocumentTerm.readByDocument(documentId)
        return(documentTermList)

    def getByDocumentTfIdfOrder(self, documentId = 0): #Operation to retrieve
    #all Document Feature instances descending tf-idf order.  Used to select
    #those features that are the most representative of the document in question.
        documentTermList = self.dbDocumentTerm.readByDocumentTfIdfOrder(documentId)
        return(documentTermList)

    def getTermCountByDocument(self, documentId = 0): #Operation to retrieve the
    #number of terms for a particular Document.
        documentTermList = self.dbDocumentTerm.readTermCountByDocument(documentId)
        return(documentTermList)

    def deleteByDocumentType(self, documentType):  #Delete instances of a given
    #document type.
        self.dbDocumentTerm.deleteByDocumentType(documentType)

    def delete(self, documentTermId = 0): #Generic operation to delete instances
    #of Document Feature.
        self.dbDocumentTerm.delete(documentTermId)

class StopChar:
    #Use to hold a list of characters that should be removed as part of the text
    #parsing process to extract words.  Examples include digits and common
    #punctuation symbols.

    id = int() #The identifier of the Stop Character.

    name = str() #The Stop Character.

    dbStopChar = dataPersistence.DBStopChar() #Link to data persistence layer.

    def get(self, stopCharId = 0, stopChar = "%"): #Generic operation to
    #retrieve instances of Stop Characters.
        stopCharList = self.dbStopChar.read(stopCharId, stopChar)
        return(stopCharList)

class StopWord:
    #Use to hold those words defined as Stop Words.  These are used to remove
    #those words that are common to most, if not all, documents and therefore
    #contribute little to the discriminating features that aid text categorization.

    id = int() #The identifier of the Stop Word.

    name = str() #The Stop Word.

    dbStopWord = dataPersistence.DBStopWord() ##Link to data persistence layer.

    def get(self, stopWordId = 0, stopWord = "%"):
        stopWordList = self.dbStopWord.read(stopWordId, stopWord)
        return(stopWordList)

class Term:
    #Terms are used to represent features in the Document Feature Vector.
    #They are the stemmed words derived from the Training Document set.
    #Terms do not contain Stop Words, which have been removed as part of
    #the training process.

    id = int() #The identifier for the Term.

    name = str() # The Term.

    normalizedTermFrequency = float() #The normalized number of documents that
    #the Term appears in.

    dbTerm = dataPersistence.DBTerm() #Link to data persistence layer.

    def get(self, termId = 0, term = "%"): #Generic operation to retrieve
    #instances of Terms.
        termList = self.dbTerm.read(termId, term)
        return(termList)

    def getNumberOfTerms(self): #Retrieve the total number of Terms from the
    #Term Dictionary.
        termList = self.dbTerm.readNumberOfTerms()
        return(termList)

    def getByDescendingFrequency(self, termId = 0, term = "%"): #Retrieve
    #Terms in descending order of their frequency.
        termList = self.dbTerm.readByDescendingFrequency(termId, term)
        return(termList)

    def deleteByFrequency(self, normalizedTermFrequency): #Delete Terms from
    #the Term Dictionary using a given threshold as a parameter.
        self.dbTerm.deleteByFrequency(normalizedTermFrequency)

    def delete(self, termId = 0): #Generic operation to delete instances of
    #Terms.
        self.dbTerm.delete(termId)
