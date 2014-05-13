from ReadSpreadsheets import ReadSpreadsheets
import csv
import utilities as utils

MIN_COSINE=0.28

class DoGrouping:

    def findGrouped(self,labelObj1,lsPossible):
        #for each label, look for corresponding label with highest cosine OVER .... if exists, also 
        #only pair dates with other dates
        lsLabels = [val[0] for val in lsPossible]
        lsCosine = [val[1] for val in lsPossible]
       
        #sort by cosine here
        lsBoth = zip(lsCosine,lsLabels)
        lsSort = sorted(lsBoth)
        lsSort.reverse()
        lsCosine,lsLabels = zip(*lsSort)
        
        lsRetLabel = []
        
        for i,label0 in enumerate(lsLabels):
            if labelObj1.strType == 'date' and not label0.strType == 'date':
                continue  
            elif label0.strType=='date' and labelObj1.strType!="date":  
                continue
            elif labelObj1.strType == "id" and not label0.strType=="id":
                continue
            elif label0.strType=="id" and not labelObj1.strType=="id":
                 continue
            else:
                 pass
                     
            if lsCosine[i] >= 0.28:
                lsRetLabel.append([label0,lsCosine[i]])
        
        return lsRetLabel

    def getAllScores(self):
        rs = ReadSpreadsheets() 
        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/2010_04_11 Chung 197 CEL clinical_NO ID.csv')
        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Califano_44-HNSCCs&25-Normal_Update-1.csv')
        #rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Rickman.csv')
        #rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/SampleInformationFile.OralCavity-MDACC.csv')
        #rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Winter\'s.csv')
        rs.readSpreadsheets()

        #fOut = open("/Users/lisa/Desktop/possible_groupings.csv",'w')
        #lsCats = ['label1_cleaned','label2_cleaned','cosine_sim']
        #lsCats = ['label1','label1_cleaned','collocates1','collocates_other1','label2','label2_cleaned','collocates2','collocates_other2','spreadname1','spreadname2','place_spreadsheet1','place_spreadsheet2','type1','type2','cosine_sim','grouped']
        #fDWriter = csv.DictWriter(fOut,lsCats)
        #fOut.write(','.join(lsCats)+"\n")
        #i=0
        lsPossible=[]
        dAll = {}
        dAll2 = {}
        
        i=0
        for spreadObj in rs.lsSpreadsheetObjs[0:-1]:
            print spreadObj
            for spreadObj2 in rs.lsSpreadsheetObjs[i+1:]:
                
                for key,labelObj in spreadObj.dLabels.items():
                    #find all possible groupings between one label and all other labels
                    d1 = labelObj.dCollocates
                    d1.update(labelObj.dCollocatesOther)
                    lsPossible=[]
                    
                    
                    for key2,labelObj2 in spreadObj2.dLabels.items():
                        #already paired this label...
                        d2 = labelObj2.dCollocates
                        d2.update(labelObj2.dCollocatesOther)
                        c_sim = utils.cosine_sim(d1,d2)
                        lsPossible.append([labelObj2,c_sim])
                    
                        #find cosine sim between the two labels                          
                    lsObjAll = self.findGrouped(labelObj,lsPossible)

                    dAll[labelObj] = lsObjAll
                    #do reverse
                    for labelTemp,cosTemp in lsObjAll:
                        if not labelTemp in dAll:
                            dAll2[labelTemp]=[]
                        dAll2[labelTemp].append([labelObj,cosTemp])

                    
            i+=1
        return dAll,dAll2
        #print dAll
        #assert 0    

    def findMax(self,ls1):
        maxCos = -1
        maxLabel = None
        
        for label,cos in ls1:
            if cos > maxCos:
                maxLabel = label
                maxCos = cos
                
        return maxLabel    

    #now here we will keep grouping labels until no change
    def findSameChange(self,dAll,dAll2):
        dLabel = {}
        lsAnswer = []
        
        for i in range(0,300): #figure this out....
            #get overlapping labels between all labels
            for labelObj,lsAllObjs in dAll.items():
                if lsAllObjs == None: #if has already been paired
                    continue
                
                j=0
                while (j < len(lsAllObjs)):
                    topLabel = lsAllObjs[j][0]
                    topCosine = lsAllObjs[j][1]
                    if dAll2[topLabel]!=None:
                        break
                    j+=1
                
                #store by value (easy lookup)
                if not topLabel in dLabel:
                    dLabel[topLabel] = []
                
                dLabel[topLabel].append([labelObj,topCosine])
        
            #print "DLABEL"
            #print dLabel
            
            #print dLabel
            #assert 0    
            #for overlapping labels get max cosine pair
            for keyLabel,lsVal in dLabel.items():
                if len(lsVal) > 1:
                    maxLabel = self.findMax(lsVal)
                else:
                    maxLabel = lsVal[0][0]
                    
                #null out    
                dAll2[keyLabel] = None
                dAll[maxLabel] = None
                lsAnswer.append([maxLabel,keyLabel])
                
        
            #print lsAnswer   
            #print dAll
            #print dAll2
            #print "-----"     
            #dLabel={}   
        #print dAll2.values()            
        #print dAll.values()    
        #print lsAnswer    
        i=0
        dAnswer = {}
        for lsObj in lsAnswer:
           if lsObj[0] in dAnswer:
               continue
           else:
               dAnswer[lsObj[0]] = lsObj[1]
        for key,val in dAnswer.items():
            print key.strTextAfterChanges
            print val.strTextAfterChanges
            print ""
            
             
if __name__ == '__main__': 
    dg = DoGrouping()
    dAll,dAll2 = dg.getAllScores()                    
    dg.findSameChange(dAll,dAll2)
    #dg.findSameChange({1:[[3,1],[5,0.8]],2:[[3,0.9],[6,0.4]]},{3:[[1,1],[2,0.9]],5:[[1,0.8]],6:[[2,0.4]]})