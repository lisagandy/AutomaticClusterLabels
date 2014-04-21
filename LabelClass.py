import utilities as util
import pyUtilities as pyU
from CollClass import CollClass

class LabelClass:
	
	strOrigText = None
	strTextAfterChanges=None
	strOrigColumnValues=None
	strValuesAfterChanges=None
	dValueMapping=None
	dCollocates=None
	
	
	#get the orig name of the label
	def __init__(self,name):
		self.strOrigText=name
		self.strTextAfterChanges=""
		self.strOrigColumnValues=[]
		self.strValuesAfterChanges=[]
		self.dValueMapping={}
		self.dCollocates={}
	
	#add value for this label	
	def addValue(self,strColumnValue):
		self.strOrigColumnValues.append(strColumnValue)
		self.strOrigColumnValues = list(set(self.strOrigColumnValues))
	
	def getValueMapping(self):
		self.dValueMapping = util.getEquiv(self.strOrigText)
		dNew={}
		for key,val in self.dValueMapping.items():
			newKey = pyU.removePunctuation(key,lsExcept=['-','+'])
			newVal = pyU.removePunctuation(val,lsExcept=['-','+'])
			dNew[newKey.strip().lower()]=newVal.strip().lower()
		self.dValueMapping = dNew
		
	def cleanLabel(self):
		self.getValueMapping()
		strNew = ""
		sTemp = pyU.removePunctuation(self.strOrigText,lsExcept=["=",'-','+'])
		sTemp = util.splitOnWord(sTemp,"date")
		sTemp = util.splitOnWord(sTemp,"Date")
		sTemp = util.splitOnWord(sTemp,"id")
		sTemp = util.splitOnWord(sTemp,"ID")
		sTemp = util.splitOnNumbers(sTemp)
		sTemp = sTemp.lower()
		for text in sTemp.split():
			lsTemp = util.getAbbrev(text.lower())
			if lsTemp:
				strNew = strNew + ' ' + lsTemp[0]
			else:
				strNew = strNew + ' ' + text.lower()
		strNew = util.cleanEquivLabel(strNew)
		self.strTextAfterChanges = strNew
		
	def getColls(self):
		cc = CollClass()
		for word in self.strTextAfterChanges.split():
			self.dCollocates[word] = cc.getColls(word)
		#print self.dCollocates	
	
	def __str__(self):
		retString = "Orig Label: " + self.strOrigText
		retString += "\nRefined Label:" + self.strTextAfterChanges
		if self.dValueMapping==None:
			self.dValueMapping={}
		retString += "\nCollocates:" + str(self.dCollocates)
		#retString += "\nValue Mapping:" + str(self.dValueMapping)
		
		#retString = retString + "\nOrig Values: " + ','.join([val for val in self.strOrigColumnValues])	
		return retString + "\n"
		
if __name__ == '__main__':
	lc = LabelClass('MainID')
	lc.cleanLabel()
	#print lc
	
	lc.getColls()
			
		