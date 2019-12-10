import os
import sys
import inspect
from io import open




dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
filename = "SNLP2019_test.tsv"
resultsname= "results.txt"
filepath = os.path.join(dirname,filename)
testfile = open(filepath,"r", encoding="utf-8")
id={}

testfile.readline()
line = testfile.readline()

while line:
	n = line[:7]
	string = line[8:]
	id[int(n)] = string
	line = testfile.readline()
testfile.close()
#For the moment this function is not completed but the idea is that has to take the results from somewhere. Now it just multiply the id for 5.
def results_generator(id):
    results=id * 5
    return results
	
if __name__ == '__main__':
	with open(os.path.join(dirname, resultsname), 'w', encoding="utf-8") as resultfile:
	
		for key,val in id.items():
			valueResult = results_generator(key)
			resultfile.write(str(key)+"--->"+ str(valueResult)+" " + val + "\n")
	resultfile.close()           