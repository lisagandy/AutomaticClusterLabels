import csv
import pyUtilities as pyU
from nltk.corpus import wordnet as wn
from nltk import stem

stemmer = stem.PorterStemmer()
fileName = "/Users/lisa/Desktop/data mining/input_csvs/labels.csv"
fileNameOut = "/Users/lisa/Desktop/data mining/input_csvs/labels_syn_labels_values.csv"

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
        strLabel = row['label']
        strValues = row['values']
        strDocName = row['dnumber']

        #parse the label text
        strLabel = pyU.removePunctuation(strLabel,spaces=True)
        lsLabel = strLabel.split()
        lsLabel = [word for word in lsLabel]
      
        lsSynonyms = [word for word in getSynonyms(strLabel)]
       
        lsOut = lsLabel
        #lsOut.extend(lsFirstChars)
        lsOut.extend(lsSynonyms)
        lsOut = [pyU.removePunctuation(word,spaces=True) for word in lsOut]
        lsOut = [word.split() for word in lsOut]

        lsOut2 = []
        for lsOut in lsOut:
            lsOut2.extend(lsOut)
        
        lsOut2 = [stemmer.stem(word.lower()) for word in lsOut2]
        lsOut2 = list(set(lsOut2))
        strOut = " ".join(lsOut2)
        d={}
        d['labelText'] = strOut
        strDocName = "_".join(strDocName.split(" "))
        if len(strLabel) < 5:
            d['docName'] = strDocName + "_" + strLabel.replace(" ","_")
        else:
            d['docName'] = strDocName + "_" + strLabel[0:20].replace(" ","_")
        
        #parse the values text
        strValues = pyU.removePunctuation(strValues,spaces=True)
        lsValues = strValues.split()
        lsValues = [word for word in lsValues]
        lsSynonyms = [word for word in getSynonyms(strValues)]
        lsFirstChars = getFirstLetters(strValues)
        lsOut = lsValues
        #lsOut.extend(lsFirstChars)
        lsOut.extend(lsSynonyms)
        lsOut = [pyU.removePunctuation(word,spaces=True) for word in lsOut]
        lsOut = [word.split() for word in lsOut]

        lsOut2 = []
        for lsOut in lsOut:
            lsOut2.extend(lsOut)
        
        lsOut2 = [stemmer.stem(word.lower()) for word in lsOut2]
        lsOut2 = list(set(lsOut2))
        strOut = " ".join(lsOut2)
        d['valuesText'] = strOut
        d['numValues'] = row['num_values']
        fDictWriter.writerow(d)
    

    fOut.close()
        
        
        

if __name__ == '__main__':
    readAndWriteLabels()
    
