from LabelClass import LabelClass

class SpreadsheetClass:
	
	strSpreadsheetName=None
	#lsLabels=None
	dLabels=None
	dLabelsOrder=None
	
	def __init__(self,fileName):
		self.strSpreadsheetName = fileName
		self.lsLabels=[]
		self.dLabels={}
		self.dLabelsOrder={}
	
	
	#figure out if label is in 1st,2nd or last section
	#of the spreadsheet 
	def detLabelOrder(self):
		
		numKeys = len(self.dLabelsOrder.keys())
		third = numKeys / 3
		
		for key,i in self.dLabelsOrder.items():
			if i>=1 and i<1+third:
				self.dLabels[key].setIPlace(1)
			elif i>=1+third and i<1+(third*2):
				self.dLabels[key].setIPlace(2)
			else:
				self.dLabels[key].setIPlace(3)
	
	#add labels in their original order
	#as well to the class which keeps
	#track of label objects without 
	#caring about the order
	def addLabels(self,lsLabels):
		i = 1
		for key in lsLabels:
			if key.strip()=="":
				continue
			lsObj = LabelClass(key)
			self.dLabels[key]=lsObj
			self.dLabelsOrder[key] = i
			i+=1
			
	
	#add column values for each label
	def addRow(self,dDataRow):	
			for key,val in dDataRow.items():
				if key.strip()=="":
					continue
				lsObj = self.dLabels[key]
				lsObj.addValue(val)
				self.dLabels[key] = lsObj
	
	#clean all labels			
	def cleanLabels(self):
		
		for key,lsObj in self.dLabels.items():
			lsObj.cleanLabel()

	#get collocates for all labels
	def getColls(self):
		for key,lsObj in self.dLabels.items():
			lsObj.getCollsLabel()
		
		for key,lsObj in self.dLabels.items():
			lsObj.getCollsValueCol()
	
	#get column type for all labels
	def determineColumnType(self):
		 for key,lsObj in self.dLabels.items():
			lsObj.getColumnType()
		
		
				
	def __str__(self):
		#print self.dLabels
		
		strRet=""
		#strRet = "\nSpreadsheet: " + self.strSpreadsheetName
		#return strRet
		for key,lsObj in self.dLabels.items():
			strRet += "\nSpreadsheet: " + self.strSpreadsheetName + "\n" + str(lsObj)
		return strRet