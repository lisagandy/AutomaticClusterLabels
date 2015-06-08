

import re
import pySettings as pySet

#if pySet.PRODUCTION_V == True:
import pymysql as mdb
#else:
#import mysql as mdb

class CollClass:
    
    conn=None
    cursor=None
    dFound = {}
    
    def __init__(self):
        if self.conn==None:
            self.getNewConnect()
            
    def getNewConnect(self):
        
        if pySet.PRODUCTION_V == False:
            self.conn = mdb.connect('localhost', 'root', 'stuff0645', 'COCA_coll2');
        else:
            self.conn = mdb.connect('localhost', 'root', 'stuff0645', 'COCA_collocates');
        #print self.conn
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
    
    def getColls(self,word,pos):
                # if len(word)==1:
                #                     return []
                #             
                #                 if word in self.dFound:
                #                     print 'IN DICTIONARY '
                #                     return self.dFound[word]
                #                 print 'GETTING DB ' + word
        #if single character
               
                #try:    
        #verbRE = re.compile('.*ing$')
        #print re.match(verbRE,word)
               #print 'HITTING DATABASE'
        #is part of speech is a noun
        #if pos.find("NN") > -1:# and not re.match(verbRE,word):
                    sqlStr = "Select MI,word1 from collocate_1 where word2='" + word + "';" #+ "' and pos2='n' and pos1 = 'j';" 
                    self.cursor.execute(sqlStr)
                    rows2 = list(self.cursor.fetchall())

                    # sqlStr = "Select MI,word1 from collocate_1 where word2='" + word + "' and pos2='n' and pos1 = 'v';"
                    #                self.cursor.execute(sqlStr)
                    #                rows2 = self.cursor.fetchall()
                    #                lsWords1.extend(lsWords2)
                    #elif pos.find("JJ") > -1:
                    sqlStr = "Select MI,word2 from collocate_1 where word1='" + word + "';"" # and pos1 = 'j' and pos2='n';"
                    self.cursor.execute(sqlStr)
                    rows3 = list(self.cursor.fetchall())
                    rows2.extend(rows3)
                    lsWords1 = self.sortByMI(rows2)
                    #elif pos.find('VB') > -1: #or re.match(verbRE,word):
                    # sqlStr = "Select MI,word2 from collocate_1 where word1='" + word + "' and pos2='n' and pos1 = 'v';"
                    #               #print sqlStr
                    #               self.cursor.execute(sqlStr)
                    #               rows2 = self.cursor.fetchall()
                    #               lsWords3 = self.sortByMI(rows2)
                    #lsWords2.extend(lsWords1)
                    #               lsWords2.extend(lsWords3)
                    lsRet = []
                    for word2 in lsWords1:
                        if word2 not in lsRet:
                            lsRet.append(word2)
                   
                    
                    self.dFound[word] = lsRet
                    return lsRet[0:10]
                    #else:
                     #return []
                # except Exception,ex:
                #                     self.dFound[word] = []
                #                     print ex
                #                     return []
                    
    #sorts by mutual information and returns top 5 collocates    
    def sortByMI(self,rows):
        #print 'SORTING'
        
        lsMI = [float(d['MI']) for d in rows]
        
        lsWords=[]
        for dTemp in rows:
            if 'word1' in dTemp:
                lsWords.append(dTemp['word1'])
            else:
                lsWords.append(dTemp['word2'])
           
        lsSort = zip(lsMI,lsWords)
        lsSort = list(reversed(sorted(lsSort)))

        lsMI = [ls[0] for ls in lsSort]
        #print lsMI
        
        lsWords = [ls[1] for ls in lsSort]
        #print lsWords
        return lsWords
   
if __name__ == '__main__':  
    cc = CollClass()
    cc.getNewConnect();  
    print cc.getColls('sex','')   
    assert 0
    #print cc.getColls('Conductivity','V')
    print cc.getColls('extremities','')
    assert 0
    
    lsStuff = []
    for word in cc.getColls('sex',''):
        print word
        lsStuff.append(word)
        print "---------"
        for word2 in cc.getColls(word,''):
            lsStuff.append(word2)
            print word2

    print "A(*SD&(A*SFD(A*SF(*AS&F(*A&S(F*&AS(*F&(*AS&F*(A&SF)))))))))"
    
    for word in cc.getColls('gender',''):
        if word in lsStuff:
            print "FOUND"
        print word
        print "--------"
        for word2 in cc.getColls(word,''):
            if word2 in lsStuff:
                print "FOUND"
            print word2
            
