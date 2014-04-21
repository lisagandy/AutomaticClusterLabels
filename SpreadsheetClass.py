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
	
	#add labels in their original order
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
				
	def cleanLabels(self):
		
		for key,lsObj in self.dLabels.items():
			lsObj.cleanLabel()

	def getColls(self):
		for key,lsObj in self.dLabels.items():
			lsObj.getColls()
		
				
	def __str__(self):
		#print self.dLabels
		
		strRet=""
		for key,lsObj in self.dLabels.items():
			strRet += "\nSpreadsheet: " + self.strSpreadsheetName + "\n" + str(lsObj)
		return strRet