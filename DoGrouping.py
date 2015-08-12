from ReadSpreadsheets import ReadSpreadsheets
import csv
import utilities as utils
import pickle
from LabelClass import *
import copy
import pySettings as pySet

MIN_COSINE = 0.45

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
            lsRetLabel.append([label0, cos])
            
        return lsRetLabel

    def getAllScores(self,lsSpreadsheets):
            
        rs = ReadSpreadsheets()
        
        print 'READING SPREADSHEETS'
        rs.readSpreadsheets(lsSpreadsheets)

        dAllCombos = {}
        # dAll2 = {}
        print 'COMPARING SPREADSHEETS'
        i = 0
        for spreadObj in rs.lsSpreadsheetObjs[i:-1]:
            # print spreadObj
            for spreadObj2 in rs.lsSpreadsheetObjs[i+1:]:
                    dAll = {}
                    for key, labelObj in spreadObj.dLabels.items():
                        
                        # find all possible groupings between one label and all other labels
                        d1 = labelObj.dCollocates
                        d1.update(labelObj.dCollocatesOther)
                        lsPossible = []
                        
                        for key2, labelObj2 in spreadObj2.dLabels.items():
                            #if labelObj2.strOrigText.lower() in ['site','gender','anatomical sites','institute','tissue id','sex']:
                                #print labelObj.strOrigText
                                #print labelObj2.strOrigText
                           
                            #print labelObj2
                            # already paired this label...
                            #if same label just set cosine similarity to 1
                            c_sim = 0
                            #print "c_sim"
                            if labelObj.strTextAfterChanges == labelObj2.strTextAfterChanges:
                                c_sim = 1
                                #print c_sim
                            else:
                                d2 = labelObj2.dCollocates
                                d2.update(labelObj2.dCollocatesOther)
                                c_sim = utils.cosine_sim(d1, d2)
                                #print c_sim
                            lsPossible.append([labelObj2, c_sim])
                        
                                                
                        lsObjAll = self.findGrouped(labelObj, lsPossible)
                        if len(lsObjAll) == 0:
                            continue
    
                        dAll[labelObj] = lsObjAll
                    if not spreadObj in dAllCombos.keys():
                        dAllCombos[spreadObj] = {}
                    dAllCombos[spreadObj][spreadObj2] = dAll    
                    #print dAllCombos[spreadObj][spreadObj2]
                    
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
    
    def findNameAndSet(self,ls1,lsNames): 
        #print [obj.strOrigText for obj in ls1]
        
        #find most repeated name
        lsText=[]
        lsFreq = []
        #get counts of each name
        for obj in ls1:
            if obj.strOrigText in lsText:
                lsFreq[lsText.index(obj.strOrigText)] +=1
            else:
                lsText.append(obj.strOrigText)
                lsFreq.append(1)
        
        #find most repeated name
        val, indexMax = max((val, idx) for (idx, val) in enumerate(lsFreq))
        newName = lsText[indexMax]
        
        #if group name already taken use shortest name
        if newName in lsNames:
            #find shortest name
            my_list = [len(labelC.strOrigText) for labelC in ls1]
            val, indexMin = min((val, idx) for (idx, val) in enumerate(my_list))
            newName = ls1[indexMin].strOrigText
        
        #otherwise jsut make up a name
        if newName in lsNames:
            i = 2
            oldName = newName
            while newName in lsNames or i>=1000:
                    newName = oldName + str(i)
                    i+=1
        
        print newName
        print ""
        lsNames.append(newName)
        
        newLS = []
        for labelC in ls1:
            label2 = labelC
            label2.mergedText = newName
            newLS.append(label2)
        
        #namesLS = [newLS[0].strOrigText+"*"+newLS[0].strSpreadsheetName]
        #newLS2 = [newLS[0]]
        #for label in newLS[1:]:
            #strLabel = label.strOrigText+"*"+label.strSpreadsheetName
            #if strLabel not in namesLS:
                #namesLS.append(strLabel)
                #newLS2.append(label)
        
        return newLS,lsNames
        
    
    
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
                i=0
                dNums={}
                dNumsRev={}
                
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

        # look through all combos of labels in every 2 spreadsheets
        # and combine same groups
        lsMerged = []
        lsAlone = []
        lsTracker = []

        for lsGrouping in lsGroupingAll:
                
                lsGroupingS1 = [lsObj for lsObj in lsGrouping if len(lsObj) > 1]
                lsAlone.extend([lsObj[0] for lsObj in lsGrouping if len(lsObj) == 1])
                
                #first time through...
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
                                lsTracker.append(lsPair[0])
                                lsTracker.append(lsPair[1])
                                lsMerged[i] = list(set(lsMerged[i]))
                                append = True
                                break
                        if not append:
                            lsMerged.append(lsPair)
                            lsTracker.append(lsPair[0])
                            lsTracker.append(lsPair[1])
                    
        #nice and hacky
        lsAlone2 = []
        for obj in lsAlone:
            if obj not in lsTracker:
                lsAlone2.append(obj)

        #create new name
        lsNames=[]
        lsMerged2=[]
        for ls1 in lsMerged:
            print [obj.strOrigText for obj in ls1]
            ls2,lsNames = self.findNameAndSet(ls1,lsNames)
            
            for label in ls2:
                if not label in lsMerged2:
                    lsMerged2.append(label)
        
        #assert 0
        lsMergeNames = [obj.strOrigText + obj.strSpreadsheetName for obj in lsMerged2]
        #print lsMergeNames
        lsAloneNames = [obj.strOrigText + obj.strSpreadsheetName for obj in lsAlone2]
        #print ""
        #print lsAloneNames
        #print ""
        #assert 0
        #'nice and hacky'
        for index,name in enumerate(lsAloneNames):
            #print name
            #print index
            if name in lsMergeNames:
                lsAlone2[index] = 'NULL'
        
        #print lsAlone2
        #assert 0
        
        lsAlone3=[]
        for obj in lsAlone2:
            if obj != 'NULL':
                lsAlone3.append(obj)
        
        lsMergeNames = [obj.strOrigText + obj.strSpreadsheetName + obj.mergedText for obj in lsMerged2]
        #for name in lsMergeNames:
            #print name
        #print lsMergeNames
                        
        return lsMerged2, list(set(lsAlone3))             
  

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
  
    
    def writeSpreadsheet(self,lsMerged,lsAlone,output_name):
        print 'writing master spreadsheet'
        export_file = open(pySet.OUTPUT_PATH + '{}-values.csv'.format(output_name), 'w+')

        max_num = max([len(x.lsOrigColumnValues) for x in lsMerged] + [len(x.lsOrigColumnValues) for x in lsAlone])
    
        for i in xrange(max_num+2):
            for label in lsMerged:
                if i==0:
                    export_file.write('{},{},'.format(label.strOrigText,label.mergedText))
                elif i==1:
                    export_file.write('{},,'.format(label.strSpreadsheetName.split("/")[-1]))
                else:
                    try:
                        export_file.write('{},,'.format(label.lsOrigColumnValues[i-2]))
                    except:
                        export_file.write(',,')
        
            for label in lsAlone:
                if i==0:
                    export_file.write('{},{},'.format(label.strOrigText,label.strOrigText))
                elif i==1:
                    export_file.write('{},,'.format(label.strSpreadsheetName.split("/")[-1]))
                else:
                    try:
                        export_file.write('{},,'.format(label.lsOrigColumnValues[i-2]))
                    except:
                        export_file.write(',,')
            export_file.write('\n')
        export_file.close()
   
if __name__ == '__main__': 
    #import sys
    # lsMerged = pickle.loads(open('/Users/lisa/Desktop/objMerged.pickle').read())
    #     
    #     print [label.strOrigText+'*'+label.mergedText+'*' + label.strSpreadsheetName+"$" for label in lsMerged if label.strOrigText]
    #     #    
    #     #assert 0
    #     lsAlone = pickle.loads(open('/Users/lisa/Desktop/objAlone.pickle').read())
    #     print [label.strOrigText + "*"+label.strSpreadsheetName+"$" for label in lsAlone if label.strOrigText]
    #     #    #     for lc in lsMerged:
    #     #    #         print lc
    #     assert 0
          
    dAllCombos = pickle.loads(open('/Users/lisa/Desktop/dCombos.pickle').read())
   
    #lsSpreadsheets = ['/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Winter.csv','/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/2010_04_11 Chung 197 CEL clinical_NO ID.csv']
    #lsSpreadsheets = sys.argv
    #import os
    #lsSpreadsheets1 = os.listdir('/Users/lisa/Desktop/ECOLOGY 2/')
    #lsSpreadsheets = ['/Users/lisa/Desktop/ECOLOGY 2/' + strName for strName in lsSpreadsheets1 if strName.find('.csv') > -1 and strName.find('all')==-1]
    
    dg = MergeSpreadsheet()
    #dAllCombos = dg.getAllScores(lsSpreadsheets)
    #open('/Users/lisa/Desktop/dCombos.pickle','w').write(pickle.dumps(dAllCombos))
    lsMerged,lsAlone = dg.doGrouping(dAllCombos)
    dg.writeSpreadsheet(lsMerged,lsAlone,'output.csv')

    # print "MERGED"
    #     print [label.strOrigText+'*'+label.mergedText+'*' + label.strSpreadsheetName+"$" for label in lsMerged if label.strOrigText]
    #     print "ALONE"
    #     print [label.strOrigText+'*'+label.strSpreadsheetName for label in lsAlone if label.strOrigText]
    open("/Users/lisa/Desktop/objMerged.pickle",'w').write(pickle.dumps(lsMerged))
    open("/Users/lisa/Desktop/objAlone.pickle",'w').write(pickle.dumps(lsAlone))
    #     assert 0
    # 
    #    #print lsIn
    #    #assert 0
    # 
    # 
    # for lc in lsMerged:
    #     print lc
    # assert 0
    # 
    # print "ALONE"
    # print [lc for lc in lsAlone]
    

    
