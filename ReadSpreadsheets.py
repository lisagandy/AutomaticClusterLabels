import csv
from SpreadsheetClass import SpreadsheetClass

class ReadSpreadsheets:
    
    lsSpreadsheets=[]
    lsSpreadsheetObjs = []
    
    
    def addSpreadsheet(self,strFile):
        self.lsSpreadsheets.append(strFile)
    
    #read all spreadsheets, creating appropriate SpreadSheet class
    def readSpreadsheets(self):
        
        for fileName in self.lsSpreadsheets:
            fRead = csv.reader(open(fileName,'rU'))
            lsRows = fRead.next()
            
            sc = SpreadsheetClass(fileName)
            self.lsSpreadsheetObjs.append(sc)
            #add labels in their original order
            sc.addLabels(lsRows)
            
            fDRead = csv.DictReader(open(fileName,'rU'))
            for row in fDRead:
                sc.addRow(row)
                
            sc.detLabelOrder()  
            sc.cleanLabels()
            sc.determineColumnType()
            sc.getColls()

            print sc


if __name__ == '__main__':
    
    rs = ReadSpreadsheets() 
    rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/2010_04_11 Chung 197 CEL clinical_NO ID.csv')
    rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Califano_44-HNSCCs&25-Normal_Update-1.csv')
    rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Rickman.csv')
    rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/SampleInformationFile.OralCavity-MDACC.csv')
    rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Winter\'s.csv')
    rs.readSpreadsheets()
        
        