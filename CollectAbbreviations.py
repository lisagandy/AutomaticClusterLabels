import urllib
from BeautifulSoup import BeautifulSoup
import string
import json

#this code gets medical abbreviations from wikipedia and makes a dictionary for use
class CollectMedicalAbbrevs:
	
	dAbbrevs=None
	
	def __init__(self):
		self.dAbbrevs={}
	
	def dumpToFile(self):
		f = open('/Users/lisa/Desktop/med_project/medical_abbrevs.txt','w')
		json.dump(self.dAbbrevs,f)
		f.close()
		
	
	def loadFromWiki(self,strLetter):		
		url = 'http://en.wikipedia.org/wiki/List_of_medical_abbreviations:_' + strLetter
		strHTML = urllib.urlopen(url).read()
		bs = BeautifulSoup(strHTML)
		table = bs.find('table',{'class':'wikitable sortable'})
		
		rows = table.findAll('tr')
		for row in rows:
			cols = row.findAll('td')
			if len(cols) == 2:
					word = unicode(' '.join(cols[0].findAll(text=True)))
					#print word
					
					defs = [unicode(mydef.string) for mydef in cols[1].findAll('a')]
					#print defs
					if len(defs)==0:
						defs = [unicode(mydef.string) for mydef in cols[1].findAll(text=True)]
					#print defs
					self.dAbbrevs[word.lower()] = [stuff.lower() for stuff in defs]
		#print self.dAbbrevs
		
if __name__ == '__main__':	
	
	cm = CollectMedicalAbbrevs()
	
	for letter in string.uppercase:
		print letter
		print "_______________________"
		cm.loadFromWiki(letter)	
	cm.dumpToFile()