from DoGrouping import MergeSpreadsheet
from ReadSpreadsheets import ReadSpreadsheets
import csv
import utilities as utils
import pickle
from LabelClass import *

ls = ['/var/www/static/test_file.csv', '/var/www/static/test_file2.csv']
dg = MergeSpreadsheet()
dA = dg.getAllScores(ls)
lsMerged,lsAlone = dg.doGrouping(dA)

print [lc.strTextAfterChanges for lc in lsMerged]
