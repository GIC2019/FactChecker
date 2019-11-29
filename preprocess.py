import inspect
import os
import re

special = "ŞŠŽšžŸÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïðñòóôõöùúûüýÿ"
normal = "SSZszYAAAAAACEEEEIIIIDNOOOOOUUUUYaaaaaaceeeeiiiidnooooouuuuyy"

def clean_special_letters(text, special, normal):
    clean = text
    for i in range(len(special)):
        clean = clean.replace(special[i], normal[i])
    return clean

def elabFile(filein,fileout):
	in_file = open(filein,"r", encoding="utf-8")
	out_file = open(fileout, "a", encoding="utf-8")
	line = in_file.readline()
	cnt = 1
	while line:
		if not (line == "==========\n"):
			line = clean_special_letters(line, special, normal)
			line = re.sub(r"[^a-zA-Z0-9.!? ]", " ", line)
			line = re.sub(r"[.!?]", " </s> <s> ", line)
			line = "<s> " + line.strip() + " </s>"
			line = line.replace("<s> </s>", " ")
		
			line = line.lower()
		
			token = line.split(" +")
			out_file.write(line+'\n')
		else:
			out_file.write(line)
		line = in_file.readline()
		cnt += 1
	in_file.close()
	out_file.close()

	
dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
for i in range(39):
	filename = 'corpus0'+str(i)
	filein = os.path.join(dirname,filename+'.txt')
	fileout = os.path.join(dirname, filename+'_tokenized.txt')
	elabFile(filein,fileout)