import csv
import pyUtilities as pyU
from nltk.corpus import wordnet as wn
from nltk import stem

stemmer = stem.PorterStemmer()
fileName = "/Users/lisa/Desktop/data mining/labels_only.csv"
fileNameOut = "/Users/lisa/Desktop/data mining/labels_syn.csv"

def getFirstLetters(strLabel):
    lsRet = []
    for word in strLabel.split():
        if word in [1234567890]:
            continue
        lsRet.append(word[0].lower())
    return list(set(lsRet))

def getSynonyms(strLabel):
    lsRet = []
    for word in strLabel.split():
        if word in [1234567890]:
            continue
        
        synsets = wn.synsets(word)
        
        for synset in synsets:
            lsRet.extend(synset.lemma_names)
    lsRet = [ret.replace("_"," ").lower() for ret in lsRet]
    return list(set(lsRet))

def readAndWriteLabels():
    global fileName
    global fileNameOut
    fDictReader = csv.DictReader(open(fileName,'rbU'))
    
    fields = ['docName','labelText']
    fOut = file(fileNameOut,'w')
    fOut.write("".join(fields)+"\n")
    fDictWriter = csv.DictWriter(fOut,fields)
    
    
    #print 'stuff'
    for row in fDictReader:
        strLabel = row['labels']
        strDocName = row['docnumber']
        print strDocName
        strLabel = pyU.removePunctuation(strLabel)
        lsLabel = strLabel.split()
        lsLabel = [word for word in lsLabel]
        #print lsLabel
        #print strLabel
        lsFirstChars = getFirstLetters(strLabel)
        #print lsFirstChars
        
        lsSynonyms = [word for word in getSynonyms(strLabel)]
        #print lsSynonyms
        #print ""
        lsOut = lsLabel
        lsOut.extend(lsFirstChars)
        lsOut.extend(lsSynonyms)
        lsOut = [pyU.removePunctuation(word) for word in lsOut]
        lsOut = [word.split() for word in lsOut]
        #print lsOut
        lsOut2 = []
        for lsOut in lsOut:
            lsOut2.extend(lsOut)
        
        lsOut2 = [stemmer.stem(word.lower()) for word in lsOut2]
        lsOut2 = list(set(lsOut2))
        print lsOut2
        strOut = " ".join(lsOut2)
        d={}
        d['docName'] = strDocName.split(" ")[0] + " " + strLabel
        d['labelText'] = strOut
        fDictWriter.writerow(d)
    fileOut.close()
        
        
        

if __name__ == '__main__':
    readAndWriteLabels()
    
