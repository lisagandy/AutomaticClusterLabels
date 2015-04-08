import csv
from SpreadsheetClass import SpreadsheetClass
import os

class ReadSpreadsheets:

    def __init__(self):
        self.lsSpreadsheets = []
        self.lsSpreadsheetObjs = []
    
    #read all spreadsheets, creating appropriate SpreadSheet class
    def readSpreadsheets(self, new_spreadsheets):
        self.lsSpreadsheets = new_spreadsheets

        for fileName in self.lsSpreadsheets:
            fRead = csv.reader(open(fileName,'rU'))#,dialect="excel-tab")
            lsRows = fRead.next()
            print 'labels: {}'.format(lsRows)
            
            sc = SpreadsheetClass(fileName)
            self.lsSpreadsheetObjs.append(sc)
            #add labels in their original order
            sc.addLabels(lsRows)
            
            fDRead = csv.DictReader(open(fileName,'rU'))#,dialect="excel-tab")
            for row in fDRead:
                sc.addRow(row)
            
            #determine original order of labels
            sc.detLabelOrder()
            #sc.findAbbreviations()  
            #clean stuff up as much as possible (put abbrev detection here?)
            try:
                sc.cleanLabels()
            except Exception as e:
                print 'Exception in cleanLabels(): {}'.format(e)
            sc.determineColumnType()
            sc.getColls()
        
        