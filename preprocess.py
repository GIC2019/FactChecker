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
		out_file.write(line)
		line = in_file.readline()
		cnt += 1
	in_file.close()
	out_file.close()

	
dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
filein = os.path.join(dirname, 'corpus00_small.txt')
fileout = os.path.join(dirname, 'corpus00_small_tokenized.txt')
elabFile(filein,fileout)