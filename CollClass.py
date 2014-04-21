import MySQLdb as mdb

class CollClass:
    
    conn=None
    cursor=None
    
    def __init__(self):
        if self.conn==None:
            self.getNewConnect()
            
    def getNewConnect(self):
        self.conn = mdb.connect('localhost', 'root', '', 'COCA_Coll');
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
    
    def getColls(self,word):
        sqlStr = "Select MI,word2  from collocate_1 where word1='%s' and pos1='n' and pos2 in ('n','j')" % word;
        self.cursor.execute(sqlStr)
        rows = self.cursor.fetchall()
        #print rows
        #print ""
        lsWords1 = self.sortByMI(rows)
        sqlStr = "Select MI,word1 from collocate_1 where word2='%s' and pos2='n' and pos1 in ('n','j')" % word;
        self.cursor.execute(sqlStr)
        rows2 = self.cursor.fetchall()
        lsWords2 = self.sortByMI(rows2)

        lsWords1.extend(lsWords2)
        lsWords1 = list(set(lsWords1))
        return lsWords1
       
        
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
    print cc.getColls('acid');