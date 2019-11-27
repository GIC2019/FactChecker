import inspect
import os
import re
# extract the statements
dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
filename = "SNLP2019_training.tsv"
filepath = os.path.join(dirname,filename)
statementfile = open(filepath,"r", encoding="utf-8")

line = statementfile.readline()
line = statementfile.readline()

statements = []
namesOfStatement = []
while line:
    statement = line.split('\t')[1][:-1]
    statements.append(statement)
    statement = re.sub(r"[^a-zA-Z0-9.!? ]", " ", statement)
    tokens = statement.split()
    names = []
    for i in range(len(tokens)):
        if (tokens[i][0].isupper()):
            names.append(tokens[i].lower())
    namesOfStatement.append(names)
    line = statementfile.readline()
statementfile.close()
# count "articles" for which the set of name-tokens of a statement is a subset of the tokens of that "article"
results = []
for i in range(len(statements)):
    results.append(0)
for i in range(52):
    print("corpus ",str(i))
    corpusname = "corpus0"+str(i)+"_tokenized.txt"
    corpuspath = os.path.join(dirname,corpusname)
    corpusfile = open(corpuspath,"r", encoding="utf-8")

    article = corpusfile.readline()
    while article:
        tokens = article.split()
        tokenset = set(tokens)
        for i in range(len(statements)):
            nameSetOfStatement = set(namesOfStatement[i])
            if (nameSetOfStatement.issubset(tokenset)):
                results[i] = results[i]+1
        article = corpusfile.readline()
    corpusfile.close()   
# print counts
for i in range(len(results)):
    print(results[i])