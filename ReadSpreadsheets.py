import csv
from SpreadsheetClass import SpreadsheetClass

class ReadSpreadsheets:
	
	lsSpreadsheets=[]
	
	
	def addSpreadsheet(self,strFile):
		self.lsSpreadsheets.append(strFile)
	
	def readSpreadsheets(self):
		
		for fileName in self.lsSpreadsheets:
			fRead = csv.reader(open(fileName))
			lsRows = fRead.next()
			
			sc = SpreadsheetClass(fileName)
			#add labels in their original order
			sc.addLabels(lsRows)
			
			fDRead = csv.DictReader(open(fileName))
			for row in fDRead:
				sc.addRow(row)
			sc.cleanLabels()
			sc.getColls()
			print sc


if __name__ == '__main__':
	
	rs = ReadSpreadsheets()	
	rs.addSpreadsheet('/Users/lisa/Desktop/elana_data/elana_annotation_examples/2010_04_11 Chung 197 CEL clinical_NO ID_13.07.09_XXX.csv')
	rs.readSpreadsheets()		
		
		