from ReadSpreadsheets import ReadSpreadsheets
import csv
from math import sqrt
import utilities as utils



WintersAlone=['Nature of operation','Previous stage','Centre','Previous site','Previous_surgery','MainID','Tissue type','Age at major operation','Site','Side','Previous disease notes','Previous DXT']
ChungAlone = ['Path Diff','Path TNM at Dx','Clinical TNM at Dx','clinical stage at Dx','Cancer FHx','Research ID','Trial ID','Frozen ID','Tumor Source','Procurement','RNA isolation','Amplification']
CalifanoAlone = ['Recc #1 Site Local 1=Yes, 0= No',	'Recc #1 Site Regional 1=Yes, 0= No','Recc #1 Site Distant 1=Yes, 0= No','Recc #1 Rx, Sur 1=Yes, 0= No'	,'Recc #1 Rx, Chemotherapy 1=Yes, 0= No',	'Recc #1 Rx, Radiotherapy 1=Yes, 0= No','Post Surgery Radiotherapy','Post Surgery Chemotherapy','Primary chemotherapy yes=1, no= 0','Primary radiation Therapy yes=1, no= 0','Primary Surgical Therapy yes=1, no= 0','Prior Chemotherapy before enroll in the study','Prior Radiation before enroll in the study','age last alcohol','Current drinker 0=no, 1 = yes','Ethnicity',' Follow Up Status 1= On FU, 0= LFU','Date2nd Recc','Recc#2 1=Yes, 0= No','PCR. HPV16 status','HPV status clin/PCR combined','p16','HPV16 ISH','Tumor HAND ID','RNA HAND ID','DNA HAND ID','FFPE ID','MRN','DateTissue Harvest','Ethnicity 1= Hispanic,  0=Non Hispanic','Recc#2 1=Yes, 0= No', 'Date2nd Recc', 'Recc#2 Site Local 1=Yes, 0= No', 'Recc#2 Site Regional 1=Yes, 0= No', 'Recc#2 Site Distant 1=Yes, 0= No',    'Recc#2 Rx, Surgery 1=Yes, 0= No',    'Recc#2 Rx, chemotherapy 1=Yes, 0= No',   'Recc#2 Rx, Radiotherapy 1=Yes, 0= No','Recc#3 1=Yes, 0= No',   'Date 3rd Recc',    'Recc#3 Site Local 1=Yes, 0= No', 'Recc#3 Site Regional 1=Yes, 0= No', 'Recc#3 Site Distant 1=Yes, 0= No',    'Recc#3 Rx, Surgery 1=Yes, 0= No',    'Recc#3 Rx,Chemotherapy 1=Yes, 0= No',    'Recc#3 Rx, Radiotherapy 1=Yes, 0= No']   
RickmanAlone = ['post surgical treatment','differentiation','pathological lymph node status','clinical follow up (months)','Overall survival(months)','Patient','localization code','localization class','Affymetrix data (1=yes;0=no)','CGH data (1=yes;0=no)','RTPCR data  (1=yes;0=no)','Patients included in prediction study  (1=yes;0=no)*','4-gene prediction status (1=high risk; 0=low risk)','4-genes prediction score','RTP-CR  sample sets (134 cases)','Age class']
SampleAlone = ['nodal recur','nod recur dt','Tu-vs-NL','OC vs. OP','DM?','ecs','tx date']

ChungSample = [['AGE AT Dx','Age@Dx'],['Path N','pN stage'],['Primary Therapy','treatment'],['date of last follow up','last fu dt'],['Distant_Local','local recur'],['Diagnosis Date','dx date'],['Affy Microarray',"Filename"],['SEX','Gender']]
SampleWinters = [['cN stage','Clin.N_stage'],['pathological T stage','Clin.T_stage'],['Smoking Status','Smoke'],['Filename',"Cellfile ID"],['Gender','Gender']]
WintersChung = [['Alcohol','EtOH'],['tumor subsite','Anatomic Region'],["Cellfile ID",'Affy Microarray'],['Gender','SEX'],['Primary _or_recurrence','Rec']]
CalifanoRickman = [['pathological N stage 0=1, 1=2, 2=3, 2A=4, 2B=5, 2C=6, 3=7, 3B=8','pathological lymph node stage'],['Recc#1 0=no, 1= Yes ','recurrence status (1=M;0=NM)'],['DOB','Age (years)'],['Gender Female =0    Male =1','Sex(1=male;2=female)']]
ChungCalifano = [['Comments','notes, Katie'],['Path N','pathological N stage 0=1, 1=2, 2=3, 2A=4, 2B=5, 2C=6, 3=7, 3B=8'],['Path M','pathological M stage'],['EtOH','Alcohol 0=no, 1 = yes'],['Tobacco','Pack years'],['tumor subsite','Tumor Site 1=Oral cavity,  2=oropharynx, 3= larynx 4 = hypopharynx '],['Ethnicity','Race 1= Caucasian, 2=African american, 3=Asian'],['date of last follow up','Date Last FU'],['Distant_Local','Recc #1 Site Local 1=Yes, 0= No'],['RecurrenceDate','Date1st Recc 0=no, 1= Yes '],['Rec','Recc#1 0=no, 1= Yes '],['Ethnicity','Race 1= Caucasian, 2=African american, 3=Asian'],['Gender','Gender'],['DeathDate','Date of Death']]
CalifanoSample = [['pathological N stage 0=1, 1=2, 2=3, 2A=4, 2B=5, 2C=6, 3=7, 3B=8','pN stage'],['pathological T stage','pathological T stage'],['current Smoking 0=no, 1 = yes','Smoking Status'],['Disease status at Last FU 1=NED,2=AWD,3= DOD, 4= DUC ','survival last follow up'],['Date Last FU','last fu dt'],['Recc #1 Site Local 1=Yes, 0= No','local recur'],['Gender Female =0    Male =1','Gender']]
CalifanoWinters = [['Prior Chemotherapy before enroll in the study yes=1, no= 0','Previous chemo'],['pathological T stage','Clin.T_stage'],['Alcohol 0=no, 1 = yes','Alcohol'],['current Smoking 0=no, 1 = yes','Smoke'],['Tumor Site 1=Oral cavity,  2=oropharynx, 3= larynx 4 = hypopharynx ','Anatomic Region'],['Recc#1 0=no, 1= Yes ','Primary _or_recurrence'],['Gender Female =0    Male =1','Gender']]
RickmanChung = [['pathological stage','path stage at Dx'],[' pathological  T','Path T'],['recurrence status','Rec'],['Sex(1=male;2=female)','SEX'],['Actual status (1=alive;0=dead)','Disease state'],['HPV status','HPV Stat']]
SampleRickman = [['Gender','Sex(1=male;2=female)'],['vital','Actual status (1=alive;0=dead)']]
RickmanWinters = [['Sex(1=male;2=female)','Gender'],['recurrence status (1=M;0=NM)','Primary _or_recurrence']]

def test():
    text = open('/Users/lisa/Desktop/combine_labels_train.csv').read()
    for lsText in RickmanWinters:
        text1 = lsText[0] + "," + lsText[1]
        text2 = lsText[1] + "," + lsText[0]
        if text.find(text1) > -1 or text.find(text2) > -1:
            pass
        else:
            print lsText

def test2():
    text = open('/Users/lisa/Desktop/combine_labels_train.csv').read()
    for temp in SampleAlone:
        if text.find(temp) > -1:
            pass
        else:
            print temp


class CreateModelSpreadsheet:

    
    def findGroup3(self,lsIn,str1,str2):
        for lsTemp in lsIn:
           # if lsTemp[0].find('tumor') > -1 or lsTemp[1].find('tumor') > -1:
            #     print lsTemp[0]
            #     print lsTemp[1]
                
            if (lsTemp[0].strip().lower()==str1.strip().lower() and lsTemp[1].strip().lower()==str2.strip().lower()):
                    print 'found in group'
                    print str1
                    print str2
                    print ""
                    return 1
               
        return 0

    def findGroup2(self,sName1,sName2,lName1,lName2):
        if sName1.find('chung') > -1 and sName2.find('sample') > -1:
            myGroup = self.findGroup3(ChungSample,lName1,lName2)
        elif sName2.find('chung') > -1 and sName1.find('sample') > -1:
            myGroup = self.findGroup3(ChungSample,lName2,lName1)
        elif sName1.find('sample') > -1 and sName2.find('winter') > -1:    
            myGroup = self.findGroup3(SampleWinters,lName1,lName2)
        elif sName2.find('sample') > -1 and sName1.find('winter') > -1:    
            myGroup = self.findGroup3(SampleWinters,lName2,lName1)
        elif sName1.find('winter') > -1 and sName2.find('chung') > -1: 
            myGroup = self.findGroup3(WintersChung,lName1,lName2)
        elif sName2.find('winter') > -1 and sName1.find('chung') > -1: 
            myGroup = self.findGroup3(WintersChung,lName2,lName1)
        elif sName1.find('califano') > -1 and sName2.find('rickman') > -1:  
            myGroup = self.findGroup3(CalifanoRickman,lName1,lName2)
        elif sName2.find('califano') > -1 and sName1.find('rickman') > -1:  
            myGroup = self.findGroup3(CalifanoRickman,lName2,lName1)    
        elif sName1.find('chung') > -1 and sName2.find('califano') > -1:    
            myGroup = self.findGroup3(ChungCalifano,lName1,lName2)
        elif sName2.find('chung') > -1 and sName1.find('califano') > -1:    
            myGroup = self.findGroup3(ChungCalifano,lName2,lName1)  
        elif sName1.find('califano') > -1 and sName2.find('sample') > -1:   
            myGroup = self.findGroup3(CalifanoSample,lName1,lName2)
        elif sName2.find('califano') > -1 and sName1.find('sample') > -1:   
            myGroup = self.findGroup3(CalifanoSample,lName2,lName1)
        elif sName1.find('califano') > -1 and sName2.find('winter') > -1:  
            myGroup = self.findGroup3(CalifanoWinters,lName1,lName2)
        elif sName2.find('califano') > -1 and sName1.find('winter') > -1:  
            myGroup = self.findGroup3(CalifanoWinters,lName2,lName1)
        elif sName1.find('rickman') > -1 and sName2.find('chung') > -1: 
            myGroup = self.findGroup3(RickmanChung,lName1,lName2)
        elif sName2.find('rickman') > -1 and sName1.find('chung') > -1: 
            myGroup = self.findGroup3(RickmanChung,lName2,lName1)
        elif sName1.find('sample') > -1 and sName2.find('rickman') > -1:    
            myGroup = self.findGroup3(SampleRickman,lName1,lName2)
        elif sName2.find('sample') > -1 and sName1.find('rickman') > -1:    
            myGroup = self.findGroup3(SampleRickman,lName2,lName1)
        elif sName1.find('rickman') > -1 and sName2.find('winter') > -1:   
            myGroup = self.findGroup3(RickmanWinters,lName1,lName2)
        elif sName2.find('rickman') > -1 and sName1.find('winter') > -1:   
            myGroup = self.findGroup3(RickmanWinters,lName2,lName1)
        else:
            return -2   
        
        return myGroup
    
    def alone1(self,lsIn,lName):
        for word in lsIn:
            if word.strip().lower() == lName.strip().lower():
                return 'alone'
        return 'not alone'    

    def findGrouped(self,spreadObj,spreadObj2,labelObj,labelObj2):
        sName1 = spreadObj.strSpreadsheetName.lower()
        sName2 = spreadObj2.strSpreadsheetName.lower()
        lName1 = labelObj.strOrigText.strip()
        lName2 = labelObj2.strOrigText.strip()
        
        if sName1.find('cali') > -1 and self.alone1(CalifanoAlone,lName1)=="alone":
            return 0
        elif sName2.find('cali') > -1 and self.alone1(CalifanoAlone,lName2)=="alone":
            return 0
        elif sName1.find('chung') > -1 and self.alone1(ChungAlone,lName1)=="alone":
            return 0
        elif sName2.find('chung') > -1 and self.alone1(ChungAlone,lName2)=="alone":
            return 0
        elif sName1.find('winter') > -1 and self.alone1(WintersAlone,lName1)=="alone":
            return 0
        elif sName2.find('winter') > -1 and self.alone1(WintersAlone,lName2)=="alone":
            return 0
        elif sName1.find('sample') > -1 and self.alone1(SampleAlone,lName1)=="alone":
            return 0
        elif sName2.find('sample') > -1 and self.alone1(SampleAlone,lName2)=="alone":
            return 0
        elif sName1.find('rickman') > -1 and lName1 in self.alone1(RickmanAlone,lName1)=="alone":
            return 0
        elif sName2.find('rickman') > -1 and lName2 in self.alone1(RickmanAlone,lName2)=="alone":
            return 0
        else:
            return self.findGroup2(sName1,sName2,lName1,lName2)
            


    def start(self):
        rs = ReadSpreadsheets() 
        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/2010_04_11 Chung 197 CEL clinical_NO ID.csv')
        rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Califano_44-HNSCCs&25-Normal_Update-1.csv')
        #rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Rickman.csv')
        #rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/SampleInformationFile.OralCavity-MDACC.csv')
        #rs.addSpreadsheet('/Users/lisa/Desktop/AutomaticClusterLabels/Raw2/Winter\'s.csv')
        rs.readSpreadsheets()

        fOut = open("/Users/lisa/Desktop/combine_labels_train.csv",'w')
        lsCats = ['label1','label1_cleaned','collocates1','collocates_other1','label2','label2_cleaned','collocates2','collocates_other2','spreadname1','spreadname2','place_spreadsheet1','place_spreadsheet2','type1','type2','cosine_sim','grouped']
        fDWriter = csv.DictWriter(fOut,lsCats)
        fOut.write(','.join(lsCats)+"\n")
        i=0
        for spreadObj in rs.lsSpreadsheetObjs[0:-1]:
            for spreadObj2 in rs.lsSpreadsheetObjs[i+1:]:
                
                #print spreadObj
                #print spreadObj2
                #print "------"
                for key,labelObj in spreadObj.dLabels.items():
                   for key2,labelObj2 in spreadObj2.dLabels.items():
                       dOut={}
                       d1 = labelObj.dCollocates
                       d1.update(labelObj.dCollocatesOther)
                       d2 = labelObj2.dCollocates
                       d2.update(labelObj2.dCollocatesOther)
                      
                       c_sim = utils.cosine_sim(d1,d2)
                       dOut['label1'] = labelObj.strOrigText
                       dOut['label1_cleaned'] = labelObj.strTextAfterChanges
                       dOut['collocates1'] = labelObj.dCollocates
                       dOut['collocates_other1'] = labelObj.dCollocatesOther
                       dOut['label2'] = labelObj2.strOrigText
                       dOut['label2_cleaned'] = labelObj2.strTextAfterChanges
                       dOut['collocates2'] = labelObj2.dCollocates
                       dOut['collocates_other2'] = labelObj2.dCollocatesOther
                       dOut['spreadname1'] = spreadObj.strSpreadsheetName.split('/')[-1]
                       dOut['spreadname2'] = spreadObj2.strSpreadsheetName.split('/')[-1]
                       dOut['place_spreadsheet1'] = labelObj.iPlace
                       dOut['place_spreadsheet2'] = labelObj2.iPlace
                       dOut['type1'] = labelObj.strType
                       dOut['type2'] = labelObj2.strType
                       dOut['cosine_sim'] = c_sim
                       
                       grouped = self.findGrouped(spreadObj,spreadObj2,labelObj,labelObj2)
                       dOut['grouped'] = grouped
                       fDWriter.writerow(dOut)
            i+=1
        
        fOut.close()
        
        

if __name__ == '__main__':  
    cm = CreateModelSpreadsheet()
    cm.start()
    #print cm.findGroup2('chung','sample','Path N','pN stage')
    #print cm.findGroup3(ChungSample,'stuff','stuff')
    