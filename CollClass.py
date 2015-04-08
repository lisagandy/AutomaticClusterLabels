import pymysql as mdb
import re
import pySettings as pySet

class CollClass:
    
    conn=None
    cursor=None
    
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
               #print 'GETTING DB' + word
        #if single character
               if len(word)==1:
                    return []
                    
        #verbRE = re.compile('.*ing$')
        #print re.match(verbRE,word)

        #is part of speech is a noun
        #if pos.find("NN") > -1:# and not re.match(verbRE,word):
               sqlStr = "Select MI,word1 from collocate_1 where word2='" + word + "' and pos2='n' and pos1 = 'j';" 
               self.cursor.execute(sqlStr)
               rows2 = self.cursor.fetchall()
               lsWords2 = self.sortByMI(rows2)
               sqlStr = "Select MI,word1 from collocate_1 where word2='" + word + "' and pos2='n' and pos1 = 'v';"
               self.cursor.execute(sqlStr)
               rows2 = self.cursor.fetchall()
               lsWords1 = self.sortByMI(rows2)   
               lsWords1.extend(lsWords2)
       #elif pos.find("JJ") > -1:
               sqlStr = "Select MI,word2 from collocate_1 where word1='" + word + "' and pos1 = 'j' and pos2='n';"
               self.cursor.execute(sqlStr)
               rows2 = self.cursor.fetchall()
               lsWords2 = self.sortByMI(rows2)
        #elif pos.find('VB') > -1: #or re.match(verbRE,word):
               sqlStr = "Select MI,word2 from collocate_1 where word1='" + word + "' and pos2='n' and pos1 = 'v';"
               #print sqlStr
               self.cursor.execute(sqlStr)
               rows2 = self.cursor.fetchall()
               lsWords3 = self.sortByMI(rows2)
               lsWords2.extend(lsWords1)
               lsWords2.extend(lsWords3)
               return list(set(lsWords2)) 
        #else:
               #return []
       
    #sorts by mutual information and returns top 5 collocates    
    def sortByMI(self,rows):
        
        lsMI = [d['MI'] for d in rows]
        try:
            lsWords = [d['word1'] for d in rows]
        except Exception:
            lsWords = [d['word2'] for d in rows]
            
        lsSort = zip(lsMI,lsWords)
        sorted(lsSort)

        lsMI = [ls[0] for ls in lsSort]
        lsWords = [ls[1] for ls in lsSort]
        return lsWords[1:6]
        
   
if __name__ == '__main__':  
    cc = CollClass()
    cc.getNewConnect();     
    print cc.getColls('sex','V');
    print cc.getColls('gender','')
