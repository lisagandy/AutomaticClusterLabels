import utilities as util
import pyUtilities as pyU
from CollClass import CollClass
import nltk
from nltk import stem

stemmer = stem.PorterStemmer()

class LabelClass:
    
    strOrigText = None
    strTextAfterChanges=None
    lsOrigColumnValues=None
    lsOrigColumnValuesSet=None
    lsValuesAfterChanges=None
    lsValuesAfterChangesSet=None
    dValueMapping=None
    dCollocates=None
    dCollocatesOther=None
    strType=None
    iPlace = None
    
    #get the orig name of the label
    def __init__(self,name):
        self.strOrigText=name
        self.strTextAfterChanges=""
        self.lsOrigColumnValues=[]
        self.lsOrigColumnValuesSet=[]
        self.lsValuesAfterChanges=[]
        self.lsValuesAfterChangesSet=[]
        self.dValueMapping={}
        self.dCollocates={}
        self.dCollocatesOther={}
        self.strType=""
        self.iPlace=-1
    
    #set place in spreadsheet (1st, 2nd, or 3rd portion of spreadsheet)
    def setIPlace(self,iplace):
        self.iPlace=iplace  

    #add value for this label   
    def addValue(self,strColumnValue):
        self.lsOrigColumnValues.append(strColumnValue)
        self.lsOrigColumnValuesSet = list(set([word.strip() for word in self.lsOrigColumnValues]))
    
    #if a mapping for values inside the column heading
    #remove and use
    def getValueMapping(self):
        self.dValueMapping = util.getEquiv(self.strOrigText)
        dNew={}
        for key,val in self.dValueMapping.items():
            newKey = pyU.removePunctuation(key,lsExcept=['-','+'])
            newVal = pyU.removePunctuation(val,lsExcept=['-','+'])
            dNew[newKey.strip().lower()]=newVal.strip().lower()
        self.dValueMapping = dNew
    
    #get collocates for value mapping (if any) and unique column values
    def getCollsValueCol(self):
        dRet={}
        
        #print "STRING TYPE"
        #print self.strType      
        if self.strType=="numeric" or self.strType=="date":
            self.dCollocatesOther = {}
            return

        #get value mapping collocates
        for key,val in self.dValueMapping.items():
            #check if key isn't number or isn't yes/no
            if util.hasAlphabet(key) and not util.hasYESNO([key]):
                newKey = self.cleanUp(key)
                if len(newKey) > 1:
                    dRet.update(self.getColls2(newKey))
            if util.hasAlphabet(val) and not util.hasYESNO([val]):
                newVal = self.cleanUp(val)
                if len(newVal) > 1:
                    dRet.update(self.getColls2(newVal))

        #get column value collocates
        for word in self.lsOrigColumnValuesSet:
            if util.hasAlphabet(word) and not util.hasYESNO([word]):
                newWord = self.cleanUp(word)
                if len(newWord) > 1:
                    dRet.update(self.getColls2(newWord))
        
        self.dCollocatesOther = dRet
            
    def cleanUp(self,word):
        strNew=""
        sTemp = pyU.removePunctuation(word,lsExcept=["=",'-','+'])
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
        return strNew       


    #clean up label, includes splitting on certain words,
    #getting rid of certain punctuation, cleaning up abbreviations  
    def cleanLabel(self,label=True):
        self.getValueMapping()
        strNew = self.cleanUp(self.strOrigText)
        strNew = util.cleanEquivLabel(strNew)
        self.strTextAfterChanges = strNew
    
    def getColls2(self,text):
        cc = CollClass()
        dRet={}
        for word in text.split():
            #stem here
            word2 = stemmer.stem(word)
            if len(word2) == 1:
                continue
            try:
                lsRet =  cc.getColls(word,'')
            except Exception,ex:
                print ex
                print word
                continue
            lsRet2 = [stemmer.stem(word3) for word3 in lsRet]
            dRet[word2] = lsRet2
            #self.dCollocates[word2] = lsRet2
        return dRet

    #get collocates of all words in the label
    #later possibly change for pos  
    def getCollsLabel(self):
        self.dCollocates = self.getColls2(self.strTextAfterChanges)
        
    
    #get the type of the column, for instance, id or date
    def getColumnType(self):
        
        lsWords = self.strTextAfterChanges.split()
        if self.strTextAfterChanges.find('record number') > -1:
            self.strType="id"
            return
         
   
        #just check for simple things first
        for word in lsWords:
            if word=="date":
                self.strType = "date"
                return
            elif word=="id":
                self.strType = "id"
                return
            elif word=="age":
                self.strType = "numeric"
                return
            elif word=="class":
                self.strType="enum"
                return
        
        #check if yes/no
        if len(self.lsOrigColumnValuesSet) <= 4:
            yes_no = util.hasYESNO(self.lsOrigColumnValuesSet)
            if yes_no:
                self.strType = "yes_no"
                return
        

        if float(len(self.lsOrigColumnValuesSet))/len(self.lsOrigColumnValues) < 0.2:
                self.strType="enum"  
                return
        #look for date here
        
        #find ids and numeric   
        dTemp={}
        for word2 in self.lsOrigColumnValuesSet:
            lsWords = word2.split()
            #print lsWords
            #look at one whole set of words at a time (per value)
            for index,word in enumerate(lsWords):
                #print "index " + str(index)
                #print word
                
                if word.lower().find("n/a") > -1 or word.strip()=="":
                    continue

                if not index in dTemp:
                    dTemp[index]=0  

                if util.hasAlphabet(word):
                    dTemp[index] = dTemp[index]+1
        
        #for weird cases like Califano, notes patrick
        if len(dTemp.keys()) >= 10:
            self.strType="enum"
            return
            
        #for cases like tobacco pack years
        for key,val in dTemp.items():
            if val<=1: #1 for some type of error (noisy spreadsheets :/)
                self.strType="numeric"  
                return
           
        self.strType="id"
    
    def __str__(self):
        retString = "Orig Label: " + self.strOrigText
        retString += "\nRefined Label:" + self.strTextAfterChanges
        retString += "\nPlace in Spreadsheet:" + str(self.iPlace)
        retString += "\nLabel Type:" + self.strType
        retString += "\nSet of Column Values" + str(self.lsOrigColumnValuesSet)
        #retString += "\n" + str(float(len(self.lsOrigColumnValuesSet))/len(self.lsOrigColumnValues))
        if self.dValueMapping==None:
            self.dValueMapping={}
        retString += "\nCollocates:" + str(self.dCollocates)
        retString += "\nValue Mapping:" + str(self.dValueMapping)
        retString += "\nCollocates Other:" + str(self.dCollocatesOther)
        #retString = retString + "\nOrig Values: " + ','.join([val for val in self.strOrigColumnValues])    
        return retString + "\n"
        
if __name__ == '__main__':
    lc = LabelClass('Gender Female =0    Male =1')
    lc.cleanLabel()
    print lc.dValueMapping
    print lc.strTextAfterChanges
    lc.getCollsValueCol()
    print lc.dCollocatesOther
    assert 0
     # Spreadsheet: /Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Califano_44-HNSCCs&25-Normal_Update-1.csv
    #   Orig Label: Race 1= Caucasian, 2=African american, 3=Asian
    #   Refined Label:race
    #   Place in Spreadsheet:1
    #   Label Type:enum
    #   Set of Column Values['1', '', '2', 'Other']
    #   Collocates:{'race': ['hors', 'finish', 'tough', 'divid', 'auto', 'car', 'ethnic', 'mind', 'matter', 'base', 'enter', 'close', 'democrat', 'arm', 'presidenti']}
    #   Value Mapping:{'1': 'caucasian', '3': 'asian', '2': 'african american'}
    #   Collocates Other:{'other': ['word', 'inspir', 'depend', 'countri', 'commun', 'perceiv', 'hand', 'blame', 'thing', 'vari', 'fortun', 'still', 'disagre', 'side', 'countless']}   
    # 
    # Spreadsheet: /Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Califano_44-HNSCCs&25-Normal_Update-1.csv
    # Orig Label: Disease status at Last FU 1=NED,2=AWD,3= DOD, 4= DUC 
    # Refined Label:disease status at last follow up
    # Place in Spreadsheet:2
    # Label Type:enum
    # Set of Column Values['', '3', '1', '? 3-4', '2', '4']
    # Collocates:{'statu': ['enjoy', 'special', 'relat', 'current', 'maintain', 'econom', 'low', 'physic', 'achiev', 'improv'], 'diseas': ['protect', 'develop', 'mental', 'rare', 'reduc', 'terribl', 'fight', 'common', 'seriou', 'caus'], 'last': ['week', 'minut', 'day', 'hour', 'month'], 'up': [], 'at': [], 'follow': ['ophthalm', 'lead', 'instruct', 'trail', 'suit', 'path']}
    # Value Mapping:{'1': 'ned', '3': 'dod', '2': 'awd', '4': 'duc'}
    # Collocates Other:{}



    lc = LabelClass('Amplification')
    lc.cleanLabel()
    lc.lsOrigColumnValuesSet = ['Nugen Ovation_3', 'Nugen_FFPE', 'Nugen Ovation_1', 'Nugen_FFPE_beta', 'Nugen Ovation_2']
    #lc.getCollsLabel()
    lc.getCollsValueCol()
    #print lc.dCollocates
    print lc.dCollocatesOther
    
    
    #lc.getColls()
            
        