import csv
from SpreadsheetClass import SpreadsheetClass
import os
import unicodedata

class ReadSpreadsheets:

    def __init__(self):
        self.lsSpreadsheets = []
        self.lsSpreadsheetObjs = []
    
    #read all spreadsheets, creating appropriate SpreadSheet class
    def readSpreadsheets(self, new_spreadsheets):
        self.lsSpreadsheets = new_spreadsheets

        for fileName in self.lsSpreadsheets:
            print fileName
            
            f = open(fileName,'rU')
            fRead = csv.reader(f)#,dialect="excel-tab")
            lsRows = fRead.next()
            lsRows = [unicodedata.normalize('NFKD', row.decode('unicode-escape')).encode('ascii', 'ignore').strip('\x00') for row in lsRows]
            f.close()
            
            sc = SpreadsheetClass(fileName)
            self.lsSpreadsheetObjs.append(sc)
            #add labels in their original order
            print 'ADDING LABELS'
            sc.addLabels(lsRows)
            
            f = open(fileName,'rU')
            fDRead = csv.DictReader(f)#,dialect="excel-tab")
            print 'ADDING VALUES'
            for row in fDRead:
                try:
                    row = {unicodedata.normalize('NFKD', key.decode('unicode-escape')).encode('ascii', 'ignore').strip('\x00'): unicodedata.normalize('NFKD', value.decode('unicode-escape')).encode('ascii', 'ignore').strip('\x00') for key, value in row.iteritems()}
                except Exception,ex:
                    print ex
                sc.addRow(row)
            
            f.close()
            #determine original order of labels
            #sc.detLabelOrder()
            #sc.findAbbreviations()  
            #clean stuff up as much as possible (put abbrev detection here?)
            #try:
            print 'CLEANING LABELS'
            sc.cleanLabels()
            #except Exception as e:
                #print 'Exception in cleanLabels(): {}'.format(e)
            print 'GETTING TYPE OF COLUMNS'
            sc.determineColumnType()
            
            print 'GETTING COLLOCATES'
            sc.getColls()
        
        
