import csv
import pyUtilities as pyU
from nltk.corpus import wordnet as wn
from nltk import stem

stemmer = stem.PorterStemmer()
fileName = "/Users/lisa/Desktop/AutomaticClusterLabels/input_csvs/labels_collocates_only.csv"
fileNameOut = "/Users/lisa/Desktop/AutomaticClusterLabels/output_csvs/labels_collocates_done.csv"

def removeNumbers(strLabel):
    number = strLabel.replace('0','')
    number = number.replace('1','')
    number = number.replace('2','')
    number = number.replace('3','')
    number = number.replace('4','')
    number = number.replace('5','')
    number = number.replace('6','')
    number = number.replace('7','')
    number = number.replace('8','')
    number = number.replace('9','')
    
    return number

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
    
    fields = ['docName','labelText','valuesText','numValues']
    fOut = file(fileNameOut,'w')
    fOut.write(",".join(fields)+"\n")
    fDictWriter = csv.DictWriter(fOut,fields)
    
    
    #print 'stuff'
    for row in fDictReader:
        print row
        strLabel = row['labels_coll']
        #strValues = row['values']
        strDocName = row['docnumber']
        strDocName2 = row['label']
        #parse the label text
        strLabel = pyU.removePunctuation(strLabel,spaces=True)
        lsLabel = strLabel.split()
        lsLabel = [word for word in lsLabel]
      
        #lsSynonyms = [word for word in getSynonyms(strLabel)]
       
        lsOut = lsLabel
        #lsOut.extend(lsFirstChars)
        #lsOut.extend(lsSynonyms)
        lsOut = [pyU.removePunctuation(word,spaces=True) for word in lsOut]
        lsOut = [removeNumbers(word) for word in lsOut]
        lsOut = [word.split() for word in lsOut]

        lsOut2 = []
        for lsOut in lsOut:
            lsOut2.extend(lsOut)
        
        lsOut2 = [stemmer.stem(word.lower()) for word in lsOut2]
        lsOut2 = list(set(lsOut2))
        strOut = " ".join(lsOut2)
        d={}
        d['labelText'] = strOut
        #strDocName = "_".join(strDocName.split(" "))
        #if len(strLabel) < 5:
            #d['docName'] = strDocName + "_" + strLabel.replace(" ","_")
        #else:
            #d['docName'] = strDocName + "_" + strLabel[0:20].replace(" ","_")
        d['docName'] = strDocName + "_" + strDocName2
        #parse the values text
        fDictWriter.writerow(d)

    fOut.close()
        
        
        

if __name__ == '__main__':
    readAndWriteLabels()
    
