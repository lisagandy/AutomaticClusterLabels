from ReadSpreadsheets import ReadSpreadsheets
import csv
import utilities as utils
import pickle
from LabelClass import *
import copy

MIN_COSINE = 0.6

class MergeSpreadsheet:

    def findGrouped(self, labelObj1, lsPossible):
        global MIN_COSINE
        # for each label, look for corresponding label with highest cosine OVER .... if exists, also 
        # only pair dates with other dates
        lsLabels = [val[0] for val in lsPossible]
        lsCosine = [val[1] for val in lsPossible]
       
        # sort by cosine here
        lsBoth = zip(lsCosine, lsLabels)
        lsSort = sorted(lsBoth)
        lsSort.reverse()
        lsCosine, lsLabels = zip(*lsSort)
        
        lsRetLabel = []
        
        for i, label0 in enumerate(lsLabels):
            cos = lsCosine[i]

#             if labelObj1.strTextAfterChanges.find('pathological') > -1 and label0.strTextAfterChanges.find('clinical') > -1:
#                 cos = 0
#             elif labelObj1.strTextAfterChanges.find('clinical') > -1 and label0.strTextAfterChanges.find('pathological') > -1:
#                 cos = 0
#             elif labelObj1.strType == 'date' and label0.strType != 'date':
#                 cos = 0 
#             elif label0.strType == 'date' and labelObj1.strType != "date":  
#                 cos = 0
#             elif labelObj1.strType == "id" and label0.strType != "id":
#                 cos = 0
#             elif label0.strType == "id" and labelObj1.strType != "id":
#                 cos = 0
#             elif lsCosine <= MIN_COSINE:
#                 cos = 0
                     
            lsRetLabel.append([label0, cos])
            
        return lsRetLabel

    def getAllScores(self,lsSpreadsheets):
            
        rs = ReadSpreadsheets() 
        
        for f1 in lsSpreadsheets:
            rs.addSpreadsheet(f1)
        
         # rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/2010_04_11 Chung 197 CEL clinical_NO ID.csv')
        #        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Califano_44-HNSCCs&25-Normal_Update-1.csv')
        #        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Rickman.csv')
        #        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/SampleInformationFile.OralCavity-MDACC.csv')
        #        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Winter\'s.csv')
        print 'reading spreadsheets'
        rs.readSpreadsheets()

        dAllCombos = {}
        # dAll2 = {}
        print 'comparing spreadsheets'
        i = 0
        for spreadObj in rs.lsSpreadsheetObjs[0:-1]:
            # print spreadObj
            for spreadObj2 in rs.lsSpreadsheetObjs[i + 1:]:
                    dAll = {}
                    for key, labelObj in spreadObj.dLabels.items():
                        #print labelObj
                        # find all possible groupings between one label and all other labels
                        d1 = labelObj.dCollocates
                        d1.update(labelObj.dCollocatesOther)
                        lsPossible = []
                        
                        
                        for key2, labelObj2 in spreadObj2.dLabels.items():
                            # already paired this label...
                            d2 = labelObj2.dCollocates
                            d2.update(labelObj2.dCollocatesOther)
                            c_sim = utils.cosine_sim(d1, d2)
                            lsPossible.append([labelObj2, c_sim])
                        
                        # find cosine sim between all labels                         
                        lsObjAll = self.findGrouped(labelObj, lsPossible)
                        if len(lsObjAll) == 0:
                            continue
    
                        dAll[labelObj] = lsObjAll
                    if not spreadObj in dAllCombos.keys():
                        dAllCombos[spreadObj] = {}
                    dAllCombos[spreadObj][spreadObj2] = dAll    
            i += 1
                    
        return dAllCombos

    
    def findMaxGroup(self, lsMatrix, dMapRev):
        # print lsMatrix
        # print dMapRev
        global MIN_COSINE
        lsGrouping = []
        lsGroupingIndex = []
        lsGroupingScore = []
        
        for i in range(0, len(lsMatrix)):
            # get max num in each column
            lsCol = []
            for j in range(i, len(lsMatrix)):
                currElem = lsMatrix[j][i]
                lsCol.append(currElem)

            maxNum = max(lsCol)
            
            # figure out grouping
            if maxNum >= MIN_COSINE:
                # col (have to add i since its a staggered matrix)
                maxIndex = i + lsCol.index(maxNum)

                # look if already stored as grouping, if so overwrite
                found = False
                for lIndex, lsTemp in enumerate(lsGroupingIndex):
                    if maxIndex in lsTemp or i in lsTemp:  # if in there
                        # if new pairing is greater then update
                        if lsGroupingScore[lIndex] < maxNum:
                            lsGrouping[lIndex] = [dMapRev[i], dMapRev[maxIndex]]
                            lsGroupingIndex[lIndex] = [i, maxIndex]
                            lsGroupingScore[lIndex] = maxNum
                            found = True
                            break
                        found = True
                             
                
                if not found:
                    lsGrouping.append([dMapRev[i], dMapRev[maxIndex]])
                    lsGroupingIndex.append([i, maxIndex])
                    lsGroupingScore.append(maxNum)
                
        # delete groupings
        for lsTemp in lsGroupingIndex:
            if lsTemp[0] in dMapRev:
                del dMapRev[lsTemp[0]]
            if lsTemp[1] in dMapRev:
                del dMapRev[lsTemp[1]]
        
        # now add singles
        for key, val in dMapRev.items():
            lsGrouping.append([val])        
        
        return lsGrouping
    
    def okayGroup(self, ls1, ls2):
        # find if the two lists share an element
        lsNew = copy.copy(ls1)
        lsNew.extend(ls2)
        
        # if they share an element good!
        if len(list(set(lsNew))) < len(lsNew):
            # check to see if the remaining elements are in the the
            # same spreadsheet if so not good
            lsSet1 = copy.copy(set(ls1))
            lsSet2 = copy.copy(set(ls2))
            lsNew2 = list(lsSet1.symmetric_difference(lsSet2))
            # print lsNew2
            lsSpread = []
            for obj in lsNew2:
                if obj.strSpreadsheetName in lsSpread:
                    return False
                lsSpread.append(obj.strSpreadsheetName)
            
            # okay to merge
            return True
        # nothing in common, don't merge
        return False
    
    def findName(self,ls1): 
        my_list = [len(labelC.strOrigText) for labelC in ls1]
        val, indexMin = min((val, idx) for (idx, val) in enumerate(my_list))
        newName = ls1[indexMin].strOrigText
        
        for labelC in ls1:
            labelC.mergedText = newName
        
        return ls1
        
    
    
    def doGrouping(self, dCombos):
        # turn into a matrix
        # assign each label a number
        # add this for easy lookup
        # dGrouping={}
        print 'merging spreadsheets'
        lsGroupingAll = []
        for spread1, dTemp2 in dCombos.items():
            for spread2, dTemp in dTemp2.items():
                # iterate through all labels for the two spreadsheets
                # set up dNumsRev and dNums
                dNumsRev = {}
                dNums = {}
                i = 0
                for key, val in dTemp.items():
                    if len(val) == 0:
                        continue
                            
                    if not key in dNums:
                        dNums[key] = i
                        dNumsRev[i] = key
                        i += 1
                        
                    for label in val:
                        if not label[0] in dNums:
                            dNums[label[0]] = i
                            dNumsRev[i] = label[0]
                            i += 1
            
                # create matrix, fill in 0s for this spreadsheet combo
                lsMatrix = []
                for j in range(0, i):
                    lsInner = []
                    for k in range (0, j + 1):
                        lsInner.append(0)
                    lsMatrix.append(lsInner)
            
                # fill in matrix with cos
                for key, val in dTemp.items():        
                    index1 = dNums[key]
                    for label in val:
                        index2 = dNums[label[0]]
                        cos = label[1]
                        if index1 > index2:
                            lsMatrix[index1][index2] = cos
                        else:
                            lsMatrix[index2][index1] = cos
       
                lsGrouping = self.findMaxGroup(lsMatrix, dNumsRev)
                lsGroupingAll.append(lsGrouping)

        # look through all combos of labels in different spreadsheets
        lsMerged = []
        lsAlone = []
        for lsGrouping in lsGroupingAll:
                
                lsGroupingS1 = [lsObj for lsObj in lsGrouping if len(lsObj) > 1]
                lsAlone.extend([lsObj[0] for lsObj in lsGrouping if len(lsObj) == 1])
                
                if len(lsMerged) == 0:
                    lsMerged = lsGroupingS1
                    continue
                
                while len(lsGroupingS1) > 0:
                        append = False
                        lsPair = lsGroupingS1.pop(0)
                        # look through every merged pair
                        for i, lsObj in enumerate(lsMerged):
                            if self.okayGroup(lsObj, lsPair) == True:
                                lsMerged[i].extend(lsPair)
                                lsMerged[i] = list(set(lsMerged[i]))
                                append = True
                        if not append:
                            lsMerged.append(lsPair)
                    
                        
          
                     
        lsMerged = [list(set(lsObj)) for lsObj in lsMerged]
        #create new name
        lsMerged2=[]
        for ls1 in lsMerged:
            ls2 = self.findName(ls1)
            lsMerged2.extend(ls2)
                        
        return lsMerged2, list(set(lsAlone))             
  

    def averagePosition(self, lsMerged):
        
        count = 0
        total = 0
        
        for lsObj in lsMerged:
            total += lsObj.iPlace
            count += 1
        return total / float(count)
    
    def pickName(self,lsObj):
        maxObj = lsObj[0]
        for obj in lsObj[1:]:
            if len(obj.strTextAfterChanges) < len(maxObj.strTextAfterChanges) and len(obj.strTextAfterChanges) > 0:
                maxObj =  obj
        
        return maxObj.strTextAfterChanges
    
    def getNewNames(self,lsLabels):
        lsNewNames=[]
        for lsObj in lsLabels:
            if len(lsObj) == 1:
                lsNewNames.append(lsObj[0].strTextAfterChanges)
            else:
                lsNewNames.append(self.pickName(lsObj))
        
        return lsNewNames
        
    
    def makeSpreadsheet(self, lsMerged, lsAlone):
        # get the average position for each group and alone order fields
        lsNew = copy.copy(lsMerged)
        lsNew.extend([[obj] for obj in lsAlone])   
        #lsPlace = [self.averagePosition(lsObj) for lsObj in lsNew]   
        
        #lsSort = sorted(zip(lsPlace, lsNew))
        #lsPlace,lsNew = zip(*lsSort)
        
        #get new names for labels (better or merged)
        #lsNames = self.getNewNames(lsNew)
        for obj in lsNew:
            for obj2 in obj:
                print obj2 
            #print name
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            print ""
    
    def writeSpreadsheet(self,lsMerged,lsAlone):
        print 'writing master spreadsheet'
        export_file = open('spreadsheets/export.csv', 'w+')
        max_num = max([len(x.lsOrigColumnValues) for x in lsMerged] + [len(x.lsOrigColumnValues) for x in lsAlone])
    
        for i in xrange(max_num+2):
            for label in lsMerged:
                if i==0:
                    export_file.write('{},{},'.format(label.strTextAfterChanges,label.mergedText))
                elif i==1:
                    export_file.write('{},,'.format(label.strSpreadsheetName))
                else:
                    try:
                        export_file.write('{},,'.format(label.lsOrigColumnValues[i-2]))
                    except:
                        export_file.write(',,')
        
            for label in lsAlone:
                if i==0:
                    export_file.write('{},'.format(label.strTextAfterChanges))
                elif i==1:
                    export_file.write('{},'.format(label.strSpreadsheetName))
                else:
                    try:
                        export_file.write('{},'.format(label.lsOrigColumnValues[i-2]))
                    except:
                        export_file.write(',')
            export_file.write('\n')
        export_file.close()
   
if __name__ == '__main__': 
    import sys
    
    lsSpreadsheets = sys.argv
    lsSpreadsheets = ['/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/2010_04_11 Chung 197 CEL clinical_NO ID.csv','/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Califano_44-HNSCCs&25-Normal_Update-1.csv']
    lsSpreadsheets = ['/home/gandy1l/AutomaticClusterLabels/SampleAnnotations/HNSCC/GSE3292.csv','/home/gandy1l/AutomaticClusterLabels/SampleAnnotations/HNSCC/GSE6791.csv']
    dg = MergeSpreadsheet()
    dAllCombos = dg.getAllScores(lsSpreadsheets)
    lsMerged,lsAlone = dg.doGrouping(dAllCombos)
    print lsMerged 
    for labelC in lsMerged:
		print labelC.strTextAfterChanges
    print ""


    print lsAlone
    assert 0
    dg.writeSpreadsheet(lsMerged,lsAlone)
    
    
