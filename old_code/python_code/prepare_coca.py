def divideCOCA():
	txt = open("/Users/lisa/Desktop/misc/60k_acad_collocates_gandy.txt").read()
	txt = txt.split("Davies")[1]
	txt=txt.split("]")[1]
	txt = txt.replace("-","")
	open('/Users/lisa/Desktop/misc/coca_60k_new.txt','w').write(txt)
	

if __name__ == '__main__':
	
	divideCOCA()