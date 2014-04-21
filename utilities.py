import json
import re

dAbbrev = None
dAbbrev = json.loads(open('/Users/lisa/Desktop/medical_abbrevs.txt').read())

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
	lsIgnore=['p','st','nd','rd','on','or','post','at','id','no']
	
	dOther={'path':'pathological','mrn':'medical record number','chemo':'chemotherapy','dxt':'deep x ray therapy','clin':'clinical','sur':'surgery','cgh':'comparative genome hybridization','rtpcr':'reverse transcriptase polymerase chain reaction','rx':'treatment','tnm':'tumor node metastases','ish':'in situ hybridization','pcr':'polymerase chain reaction','t':'tumor','m':'metastases','n':'node','od':'of','stat':'status','dx':'diagnosis','diff':'differentiation','rec':'recommendation','recc':'recommendation','fu':'follow up'}
	
	if abbrev in lsIgnore:
		return None
	
	if abbrev in dOther:
		return [dOther[abbrev]]
	
	if abbrev in dAbbrev.keys():
		return dAbbrev[abbrev]
	else:
		return None
	
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