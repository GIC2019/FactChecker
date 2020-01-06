from sklearn.metrics import roc_auc_score
import numpy as np
import inspect
import os
import re

special = "ŞŠŽšžŸÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïðñòóôõöùúûüýÿņģć"
normal =  "SSZszYAAAAAACEEEEIIIIDNOOOOOUUUUYaaaaaaceeeeiiiidnooooouuuuyyngc"
titledelete = {'</s>', '<s>'}

def clean_special_letters(text, special, normal):
    clean = text
    for i in range(len(special)):
        clean = clean.replace(special[i], normal[i])
    return clean

def coverage_of_A_in_B(A, B):
    I = A & B
    return len(I)/float(len(A))

def nameSplitDetector(tokens):
    bettertokens = []
    for i in range(len(tokens)):
        if '-' in tokens[i]:
            split = tokens[i].split('-')
            #print(split)
            if split[0][0].isupper():
                for k in range(len(split)):
                    bettertokens.append(split[k][0].upper()+split[k][1:])
        else:
            bettertokens.append(tokens[i])
    return bettertokens

def generateNameSet(tokens):
    names = []
    for i in range(len(tokens)):
        if (tokens[i][0].isupper() or tokens[i][0].isdigit()):
            names.append(tokens[i].lower())
    return set(names)

# PROCESS TRAINING FILE

dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
filename = "SNLP2019_training.tsv"
filepath = os.path.join(dirname,filename)
statementfile = open(filepath,"r", encoding="utf-8")

line = statementfile.readline()
line = statementfile.readline()

namesSetOfStatment = []
truth = []
k = 0
while line:
    splittedLine = line.split('\t')
    statement = splittedLine[1][:-1]
    truth.append(splittedLine[2][:-3])
    statement = clean_special_letters(statement, special, normal)
    statement = re.sub(r"[^a-zA-Z0-9\- ]", " ", statement)
    tokens = statement.split()
    tokens = nameSplitDetector(tokens)
    # calculate features
    namesSetOfStatment.append(generateNameSet(tokens))
    
    k = k + 1
    line = statementfile.readline()
statementfile.close()
truth_int = [int(i) for i in truth]


# PROCESS CORPUS

results = []
for i in range(k):
    results.append(0)
for i in range(39): # 39
    print("corpus ",str(i))
    corpusname = "corpus0"+str(i)+"_tokenized.txt"
    corpuspath = os.path.join(dirname,corpusname)
    corpusfile = open(corpuspath,"r", encoding="utf-8")
    line = corpusfile.readline()
    while line:
        title = ""
        content = "" 
        articleStart = True
        while not line == "==========\n":
            if articleStart:
                title = line
                articleStart = False
            else:
                content = content + line
            line = corpusfile.readline()
        line = corpusfile.readline()
        titleset = set(title.split()).difference(titledelete)
        contentset = set(content.split())
        articleset = titleset.union(contentset)
        for k in range(len(results)):
            if (results[k] < 1):   
                cov = coverage_of_A_in_B(namesSetOfStatment[k],articleset)
                if cov > results[k]:
                    results[k] = cov
    corpusfile.close()
    print('roc_auc =',roc_auc_score(truth_int, results))