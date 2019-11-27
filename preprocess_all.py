import inspect
import os
import re

def elabFile(filein,fileout):
	in_file = open(filein,"r", encoding="utf-8")
	out_file = open(fileout, "a", encoding="utf-8")
	line = in_file.readline()
	cnt = 1
	while line:
		line = re.sub(r"[^a-zA-Z0-9.!? ]", " ", line)
		line = re.sub(r"[.!?]", " </s> <s> ", line)
		line = "<s> " + line.strip() + " </s>"
		line = line.replace("<s> </s>", " ")
		
		line = line.lower()
		
		token = line.split(" +")
		out_file.write(line+'\n')
		line = in_file.readline()
		cnt += 1
	in_file.close()
	out_file.close()

	
dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
for i in range(52):
	filename = 'corpus0'+str(i)
	filein = os.path.join(dirname,filename+'.txt')
	fileout = os.path.join(dirname, filename+'_tokenized.txt')
	elabFile(filein,fileout)