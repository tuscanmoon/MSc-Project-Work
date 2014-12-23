#######################################################
#
# Name: DataPersistence.py
# Description:  MySQL RDBMS Model for persistent data
# Created on:   12-Apr-2010
# Author:       Paul White
#
#######################################################


import MySQLdb
from collections import namedtuple

class DBCategory:

    def read(self, categoryId, categoryName):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if categoryId != 0:
                SQL = "SELECT id, name, normalized_frequency " + \
                       "FROM category " +  \
                       "WHERE id = '" + str(categoryId) + \
                     "' ORDER BY name"
            else:
                SQL = "SELECT id, name, normalized_frequency " + \
                      "FROM category " + \
                      "WHERE name Like '" + categoryName + \
                    "' ORDER BY name"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            categoryNameTuple = namedtuple('categoryNameTuple', 'categoryId, \
             categoryName, normalizedCategoryFrequency')
            categoryNameList = list()
            for row in resultSet:
                categoryNameRecord = categoryNameTuple(row[0], row[1], row[2])
                categoryNameList.append(categoryNameRecord)
            cursor.close()
            con.close()
            return(categoryNameList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def delete(self, categoryId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if categoryId != 0:
                SQL = "DELETE FROM category " + \
                       "WHERE id = '" + categoryId + "'"
            else:
                SQL = "DELETE FROM category"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

class DBCategoryTerm:

    def readLastKeyValue(self):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT MAX(id) 'id' " + \
                   "FROM category_term"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            for row in resultSet:
                if row[0] is not None:
                    categoryTermId = row[0]
                else:
                    categoryTermId = 0
            cursor.close()
            con.close()
            return(categoryTermId)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def read(self):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT id, category_id, term_id, normalized_frequency " + \
                   "FROM category_term  " + \
                   "ORDER BY category_id, term_id"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            categoryTermTuple = namedtuple('categoryTermTuple', 'categoryTermId, \
             categoryId, termId, normalizedCategoryTermFrequency')
            categoryTermList = list()
            for row in resultSet:
                categoryTermRecord = categoryTermTuple(row[0], row[1], row[2], row[3])
                categoryTermList.append(categoryTermRecord)
            cursor.close()
            con.close()
            return(categoryTermList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readByTerm(self, termId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT id, category_id, term_id, normalized_frequency " + \
                   "FROM category_term " + \
                   "WHERE term_id = " + str(termId)  +  \
                  " ORDER BY term_id"

            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            categoryTermTuple = namedtuple('categoryTermTuple', 'categoryTermId, \
             categoryId, termId, normalizedCategoryTermFrequency')
            categoryTermList = list()
            for row in resultSet:
                categoryTermRecord = categoryTermTuple(row[0], row[1], row[2], row[3])
                categoryTermList.append(categoryTermRecord)
            cursor.close()
            con.close()
            return(categoryTermList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def delete(self, categoryTermId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if categoryTermId != 0:
                SQL = "DELETE FROM category_term " + \
                       "WHERE id = '" + categoryTermId + "'"
            else:
                SQL = "DELETE FROM category_term"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

class DBDocument:

    def readLastKeyValue(self):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT MAX(id) 'id' " + \
                   "FROM document"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            for row in resultSet:
                if row[0] is not None:
                    documentId = row[0]
                else:
                    documentId = 0
            return(documentId)
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readDocumentByType(self, documentType):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if documentType != "":
                SQL = "SELECT id, name, type, document_category_count " + \
                       "FROM document " + \
                       "WHERE type = '" + documentType + \
                     "' ORDER BY id"
            else:
                SQL = "SELECT id, name, type, document_category_count " + \
                       "FROM document " + \
                       "ORDER BY id"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            documentTuple = namedtuple('documentTuple', 'documentId, \
             documentName, documentType, documentCategoryCount')
            documentList = list()
            for row in resultSet:
                documentRecord = documentTuple(row[0], row[1], row[2], row[3])
                documentList.append(documentRecord)
            return(documentList)
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def deleteByDocumentType(self, documentType):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "DELETE FROM document " + \
                   "WHERE type = '" + documentType + "'"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def delete(self, documentId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if documentId != 0:
                SQL = "DELETE FROM document " + \
                       "WHERE id = '" + str(documentId) + "'"
            else:
                SQL = "DELETE FROM document"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

class DBDocumentCategory:

    def readDocumentByCategory(self, categoryId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT DISTINCT(document_id) 'document_id' " + \
                   "FROM document_category " + \
                   "WHERE category_id = " + str(categoryId)
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            documentForCategoryTuple = namedtuple('documentForCategoryTuple', \
             'documentId')
            documentForCategoryList = list()
            for row in resultSet:
                documentForCategoryRecord = documentForCategoryTuple(row[0])
                documentForCategoryList.append(documentForCategoryRecord)
            cursor.close()
            con.close()
            return(documentForCategoryList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readLastKeyValue(self):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT MAX(id) 'id' " + \
                   "FROM document_category"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            for row in resultSet:
                if row[0] is not None:
                    documentCategoryId = row[0]
                else:
                    documentCategoryId = 0
            cursor.close()
            con.close()
            return(documentCategoryId)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readByDocumentType(self, documentType, categoryWeightTypeId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if categoryWeightTypeId == 0:
                SQL = "SELECT t1.id, t1.document_id, t1.category_id, t1.category_weight, \
                 t1.category_weight_type_id, t1.positive_assignment " + \
                       "FROM document_category t1 JOIN document t2 ON t1.document_id = t2.id " + \
                       "WHERE t2.type = '" + documentType + \
                     "' ORDER BY t1.document_id"
            else:
                SQL = "SELECT t1.id, t1.document_id, t1.category_id, t1.category_weight, \
                 t1.category_weight_type_id, t1.positive_assignment " + \
                       "FROM document_category t1 JOIN document t2 ON t1.document_id = t2.id " + \
                       "WHERE t1.category_weight_type_id = '" + str(categoryWeightTypeId) + \
                        "' AND t2.type = '" + documentType + \
                       "' ORDER BY t1.document_id"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            categoryForDocumentTuple = namedtuple('categoryForDocumentTuple', \
             'documentCategoryId, documentId, categoryId, categoryWeight, \
              categoryWeightTypeId, positiveAssignment')
            categoryForDocumentList = list()
            for row in resultSet:
                categoryForDocumentRecord = categoryForDocumentTuple(row[0], \
                 row[1], row[2], row[3], row[4], row[5])
                categoryForDocumentList.append(categoryForDocumentRecord)
            cursor.close()
            con.close()
            return(categoryForDocumentList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def deleteByDocumentType(self, documentType):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "DELETE FROM document_category " + \
                   "WHERE document_id IN (SELECT id FROM document WHERE type = '" + \
                    documentType + "')"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def delete(self, documentCategoryId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if documentCategoryId != 0:
                SQL = "DELETE FROM document_category " + \
                       "WHERE id = '" + documentCategoryId + "'"
            else:
                SQL = "DELETE FROM document_category"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

class DBDocumentTerm:

    def readLastKeyValue(self):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT MAX(id) 'id' " + \
                   "FROM document_term"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            for row in resultSet:
                if row[0] is not None:
                    documentTermId = row[0]
                else:
                    documentTermId = 0
            cursor.close()
            con.close()
            return(documentTermId)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readByDocument(self, documentId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if documentId == 0:
                SQL = "SELECT id, term_id, document_id, normalized_frequency, tf_idf, frequency " + \
                       "FROM document_term " + \
                       "ORDER BY document_id, id"
            else:
                SQL = "SELECT id, term_id, document_id, normalized_frequency, tf_idf, frequency " + \
                       "FROM document_term WHERE document_id = " + str(documentId)
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            documentTermTuple = namedtuple('documentTermTuple', 'documentTermId, \
             termId, documentId, normalizedTermFrequency, tfIdf, termFrequency')
            documentTermList = list()
            for row in resultSet:
                documentTermRecord = documentTermTuple(row[0], row[1], \
                 row[2], row[3], row[4], row[5])
                documentTermList.append(documentTermRecord)
            cursor.close()
            con.close()
            return(documentTermList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readByDocumentTfIdfOrder(self, documentId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if documentId == 0:
                SQL = "SELECT id, term_id, document_id, normalized_frequency, tf_idf, term_frequency " + \
                       "FROM document_term " + \
                       "ORDER BY tf_idf DESC"
            else:
                SQL = "SELECT id, term_id, document_id, normalized_frequency, tf_idf, term_frequency " + \
                       "FROM document_term " + \
                       "WHERE document_id = " + str(documentId)  + \
                       " ORDER BY tf_idf DESC"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            documentTermTuple = namedtuple('documentTermTuple', 'documentTermId, \
             termId, documentId, normalizedTermFrequency, tfIdf, termFrequency')
            documentTermList = list()
            for row in resultSet:
                documentTermRecord = documentTermTuple(row[0], row[1], \
                 row[2], row[3], row[4], row[5])
                documentTermList.append(documentTermRecord)
            cursor.close()
            con.close()
            return(documentTermList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readTermCountByDocument(self, documentId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if documentId == 0:
                SQL = "SELECT t2.document_id, COUNT(*) 'document_term_count' " + \
                       "FROM document t1 JOIN document_term t2 on t1.id = t2.document_id " + \
                       "WHERE t1.type = 'TEST' " + \
                       "GROUP BY t2.document_id"
            else:
                SQL = "SELECT t2.document_id, COUNT(*) 'document_term_count' " + \
                       "FROM document t1 JOIN document_term t2 on t1.id = t2.document_id " + \
                       "WHERE t1.type = 'TEST' AND t2.document_id = " + str(documentId) +  \
                       " GROUP BY t2.document_id"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            documentTermTuple = namedtuple('documentTermTuple', \
             'documentId, documentTermCount')
            documentTermList = list()
            for row in resultSet:
                documentTermRecord = documentTermTuple(row[0], row[1])
                documentTermList.append(documentTermRecord)
            cursor.close()
            con.close()
            return(documentTermList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def deleteByDocumentType(self, documentType):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "DELETE FROM document_term " + \
                   "WHERE document_id IN \
                    (SELECT id FROM document WHERE type = '" + documentType + "')"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def delete(self, documentTermId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if documentTermId != 0:
                SQL = "DELETE FROM document_term " + \
                       "WHERE id = '" + str(documentTermId) + "'"
            else:
                SQL = "DELETE FROM document_term"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

class DBStopChar:

    def read(self, stopCharId, stopChar):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if stopCharId != 0:
                SQL = "SELECT id, name " + \
                       "FROM stop_char " + \
                       "WHERE id = '" + str(stopCharId) + \
                       "' ORDER BY name"
            else:
                SQL = "SELECT id, name " + \
                       "FROM stop_char " + \
                       "WHERE name Like '" + stopChar + \
                       "' ORDER BY name"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            stopCharTuple = namedtuple('stopCharTuple', 'stopCharId, stopChar')
            stopCharList = list()
            for row in resultSet:
                stopCharRecord = stopCharTuple(row[0], row[1])
                stopCharList.append(stopCharRecord)
            cursor.close()
            con.close()
            return(stopCharList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

class DBStopWord:

    def read(self, stopWordId, stopWord):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if stopWordId != 0:
                SQL = "SELECT id, name FROM stop_word " + \
                       "WHERE id = '" + str(stopWordId) + \
                       "' ORDER BY name"
            else:
                SQL = "SELECT id, name " + \
                       "FROM stop_word " + \
                       "WHERE name Like '" + stopWord + \
                       "' ORDER BY name"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            stopWordTuple = namedtuple('stopWordTuple', 'stopWordId, stopWord')
            stopWordList = list()
            for row in resultSet:
                stopWordRecord = stopWordTuple(row[0], row[1])
                stopWordList.append(stopWordRecord)
            cursor.close()
            con.close()
            return(stopWordList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

class DBTerm:

    def read(self, termId, term):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if termId != 0:
                SQL = "SELECT id, name, normalized_frequency " + \
                       "FROM term " + \
                       "WHERE id = '" + str(termId) + \
                       "' ORDER BY id"
            else:
                SQL = "SELECT id, name, normalized_frequency " + \
                       "FROM term " + \
                       "WHERE name LIKE '" + term + \
                       "' ORDER BY id"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            termTuple = namedtuple('termTuple', 'termId, term, normalizedTermFrequency')
            termList = list()
            for row in resultSet:
                termRecord = termTuple(row[0], row[1], row[2])
                termList.append(termRecord)
            cursor.close()
            con.close()
            return(termList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readNumberOfTerms(self):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "SELECT COUNT(*) 'number_of_terms' " + \
                   "FROM term"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            termTuple = namedtuple('termTuple', 'numberOfTerms')
            termList = list()
            for row in resultSet:
                termRecord = termTuple(row[0])
                termList.append(termRecord)
            cursor.close()
            con.close()
            return(termList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def readByDescendingFrequency(self, termId, term):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if termId != 0:
                SQL = "SELECT id, name, normalized_frequency " + \
                       "FROM Term " + \
                       "WHERE id = '" + str(termId) + \
                       "' ORDER BY normalized_frequency desc, id"
            else:
                SQL = "SELECT id, name, normalized_frequency " + \
                       "FROM Term " + \
                       "WHERE name LIKE '" + term + \
                       "' ORDER BY normalized_frequency desc, id"
            cursor.execute(SQL)
            resultSet = cursor.fetchall ()
            termTuple = namedtuple('termTuple', 'termId, term, normalizedTermFrequency')
            termList = list()
            for row in resultSet:
                termRecord = termTuple(row[0], row[1], row[2])
                termList.append(termRecord)
            cursor.close()
            con.close()
            return(termList)
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def deleteByFrequency(self, normalizedTermFrequency):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            SQL = "DELETE FROM term " + \
                   "WHERE normalized_frequency < '" + str(normalizedTermFrequency) + "'"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)

    def delete(self, termId):
        try:
            con = MySQLdb.connect (host = "localhost", user = "root", \
             passwd = "fjXhcvbj", db = "hj801")
            cursor = con.cursor()
            if termId != 0:
                SQL = "DELETE FROM term " + \
                       "WHERE id = '" + str(termId) + "'"
            else:
                SQL = "DELETE FROM term"
            cursor.execute(SQL)
            con.commit()
            cursor.close()
            con.close()
        except MySQLdb.Error as detail:
            print(detail)
        except AttributeError as detail:
            print(detail)