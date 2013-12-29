def divideCOCA():
	txt = file.open("/home/gandy1l/60k_acad_collocates_gandy.txt").read()
	txt = txt.split("Davies")[1]
	
	file.open('/home/gandy1l/coca_60k_new.txt').write(txt,"w")
	

if __name__ == '__main__':
	
	divideCOCA()