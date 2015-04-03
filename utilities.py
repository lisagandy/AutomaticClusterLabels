import json
import re
from math import sqrt
import pyUtilities as pyU

dAbbrev = None
dAbbrev = json.loads(open('/home/gandy1l/AutomaticClusterLabels/inData/medical_abbrevs.txt').read())

lsStopWords = ['date','stage','status','age']

def scalar(collection): 
  total = 0 
  for coin, count in collection.items(): 
    total += count * count 
  return sqrt(total) 

def similarity(A,B): 
  total = 0 
  for kind in A:
    if kind in B: 
      total += A[kind] * B[kind] 
  if scalar(A)==0 or scalar(B)==0:
      return 0
      
  return float(total) / (scalar(A) * scalar(B))

def findD(dLabel):
    dRet={}
    
    for key,lsVal in dLabel.items():
        if key.lower().strip() not in lsStopWords:
            dRet[key] = 1
        else:
            continue
            
        for val in lsVal:
            dRet[val] = 1
    return dRet

#find cosine similarity (just get rid of stopwords and do present or not)
#also stem... 
def cosine_sim(dLabel,dLabel2):
    dSend1 = findD(dLabel)
    dSend2 = findD(dLabel2)
    return similarity(dSend1,dSend2)


def hasYESNO(lsYesNo):
	#flags=re.IGNORECASE
	matchY = re.compile("(\s+|^)yes(\s+|$)$",flags=re.IGNORECASE)
	matchN = re.compile("(\s+|^)no(\s+|$)$",flags=re.IGNORECASE)
	matchNA1 = re.compile("(\s+|^)n\a(\s+|$)$",flags=re.IGNORECASE)
	matchNA2 = re.compile("(\s+|^)na(\s+|$)$",flags=re.IGNORECASE)
	matchNA3 = re.compile("(\s+|^)n/a(\s+|$)$",flags=re.IGNORECASE)
	
	matchY2 = re.compile("(\s+|^)y(\s+|$)$",flags=re.IGNORECASE)
	matchN2 = re.compile("(\s+|^)n(\s+|$)$",flags=re.IGNORECASE)
	
	match0 = re.compile("(\s+|^)0(\s+|$)$",flags=re.IGNORECASE)
	match1 = re.compile("(\s+|^)1(\s+|$)$",flags=re.IGNORECASE)
	
	for word in lsYesNo:
		if word.strip()=="":
			continue
		if not re.match(matchY,word) and not re.match(matchN,word):
			if not re.match(matchNA1,word) and not re.match(matchNA2,word) and not re.match(matchNA3,word):
				if not re.match(matchY2,word) and not re.match(matchN2,word):
					if not re.match(match0,word) and not re.match(match1,word):
							return False
	
	
		
	return True	

#has alphabetic character
def hasAlphabet(strTemp):
	pattern = re.compile(".*[A-Za-z].*")
	match = pattern.match(strTemp)
	if match:
		return True
	return False




def splitOnWord(sTemp,word2):
	pattern = "(" + word2 + ")(\s+)|(" + word2 + ")$|(" + word2+ ")([A-Z]+[a-z]*)"
	#print pattern
	indivWords= re.split(pattern,sTemp)
	#print indivWords
	return ' '.join([word for word in indivWords if word!=None])

def getEquiv(sTemp):
	dRet={}
	pattern='(\d+\w*\s*=\s*)'
	
	indivWords = re.split(pattern,sTemp)
	foundMatch=False
	lastWord = None
	for word in indivWords:
		if re.match(pattern,word):
			dRet[word.replace("=",'').strip()]=None
			foundMatch=True
			lastWord=word.replace("=",'').strip()
		elif foundMatch==True:
			dRet[lastWord] = word.strip()
		else:
			continue
	
	if len(dRet.keys())==0:
		return getEquiv2(sTemp)
	
	return dRet	

def getEquiv2(sTemp):
	dRet={}
	pattern='(\w+\s*=\s*)'
	
	indivWords = re.split(pattern,sTemp)
	foundMatch=False
	lastWord = None
	for word in indivWords:
		if re.match(pattern,word):
			dRet[word.replace("=",'').strip()]=None
			foundMatch=True
			lastWord=word.replace("=",'').strip()
		elif foundMatch==True:
			dRet[lastWord] = word.strip()
		else:
			continue

	
	return dRet
	
def cleanEquivLabel(sText):
	pattern="\s+\d+\s*=.*|\s+\w+\s*=.*"
	newString = re.sub(pattern,'',sText,count=1).strip()

	return newString
	


#cleanEquivLabel('tumor site 1 =oral cavity 2 =oropharynx 3 = larynx 4 = hypopharynx')
#assert 0	
def splitOnNumbers(sTemp):
	pattern = "(\d+)"
	indivWords= re.split(pattern,sTemp)
	
	return ' '.join(indivWords)


def getAbbrev(abbrev): 
	lsIgnore=['bm','cm','c','b','n/a','n\a','p','st','nd','rd','on','or','post','at','id','no','vs','all','m']
	
	dOther={'etoh':'alcohol','pos':'positive','lfu':'last follow up','on fu':'on follow up','w':'white','o':'other','oc':'oral cavity','op':'oropharynx','hp':'hypopharynx','xrt':'radiation therapy','oct':'optimal cutting temperature','ffpe':'formula fixed paraffin embedded','ln':'lymph node','pyr':'pack years','doc':'died of other causes','dod':'died of disease','ned':'no evidence of disease','awd':'alive with disease','f':'female','cn':'clinical n','pn':'pathological lymph node','tx':'treatment','loc':'local','dt':'date','path':'pathological','mrn':'medical record number','chemo':'chemotherapy','dxt':'deep x ray therapy','clin':'clinical','sur':'surgery','cgh':'comparative genome hybridization','rtpcr':'reverse transcriptase polymerase chain reaction','rx':'treatment','tnm':'tumor node metastases','ish':'in situ hybridization','pcr':'polymerase chain reaction','t':'tumor','n':'lymph node','od':'of','stat':'status','dx':'diagnosis','diff':'differentiation','rec':'recurrence','recc':'recurrence','fu':'follow up'}
	
	if abbrev in lsIgnore:
		return None,False
	
	if abbrev in dOther:
		return [dOther[abbrev]],True
	
	if abbrev in dAbbrev.keys():
		return dAbbrev[abbrev],True
	else:
		#determine if abbrev or not
		if len(abbrev) < 4:
		    return None,True
		elif not pyU.bIsDictionaryWord(abbrev):
		    return None,True
		else:
		    return None,False
		
	
def split_words(instring, prefix = '', words = None):
    if not instring:
        return []  
    
    if words is None:
        words=set()
        with open('/usr/share/dict/words') as f:
            for line in f:
                words.add(line.strip())
    
    if (not prefix) and (instring in words):
         return [instring]
    prefix, suffix = prefix + instring[0], instring[1:]
    
    solutions = []
    # Case 1: prefix in solution
    if prefix in words:
        try:
            solutions.append([prefix] + split_words(suffix, '', words))
        except ValueError:
            pass
    # Case 2: prefix not in solution
    try:
        solutions.append(split_words(suffix, prefix, words))
    except ValueError:
        pass
    if solutions:
        return sorted(solutions,
                      key = lambda solution: [len(word) for word in solution],
                      reverse = True)[0]
    else:
        raise ValueError('no solution')

		

if __name__ == '__main__':
	print(split_words('recdate'))
	print(split_words('tableprechaun', words = set(['tab', 'table', 'leprechaun'])))
	
	#print getAbbrev('fhx')	
