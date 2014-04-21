def divideCOCA():
	txt = open("/home/gandy1l/60k_acad_collocates_gandy.txt").read()
	txt = txt.split("Davies")[1]
	txt=txt.split("]")[1]
	txt = txt.replace("-","")
	open('/home/gandy1l/coca_60k_new.txt','w').write(txt)
	

if __name__ == '__main__':
	
	divideCOCA()