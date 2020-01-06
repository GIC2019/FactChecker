"""
Extract the information of each statement in the file SNLP2019_training.tsv
"""
import os
import re

"""
Get FactID of each statement, return a list storing all extracted FactIDs
"""
def get_factID(filename):

    dirname = os.path.dirname(os.path.abspath(__file__))
    filepath = dirname+'\\'+filename

    #read the training file
    statementfile = open(filepath, "r", encoding="utf-8")

    line = statementfile.readline()
    line = statementfile.readline()

    IDlist = []

    while line:
        id = line.split('\t')[0]
        IDlist.append(id)
        line = statementfile.readline()

    return IDlist

"""
Get all statements, preprocess them(eliminate all character except letter and number) 
and return a list storing all extracted preprocessed statements
"""
def get_statements(filename):

    dirname = os.path.dirname(os.path.abspath(__file__))
    filepath = dirname + '\\' + filename

    # read the training file
    statementfile = open(filepath, "r", encoding="utf-8")

    line = statementfile.readline()
    line = statementfile.readline()

    statements = []
    #pattern for preprocessing
    pattern = re.compile(r'[^a-zA-Z0-9]')


    while line:
        statement = line.split('\t')[1][:-1]
        statement = re.sub(pattern, ' ', statement)
        statements.append(statement)
        line = statementfile.readline()

    return statements

"""
tokenize all preprocessed statements and return a list storing all tokenized statements
"""
def get_statements_tokens(filename):

    pattern = re.compile(r'[ ]+')
    statements = get_statements(filename)
    tokenslist = []

    for i in range(len(statements)):
        tokens = re.split(pattern, statements[i])
        # eliminate the all elements '' in list token
        tokens = list(filter(None, tokens))
        tokenslist.append(tokens)

    return tokenslist


"""
get all names of each statements using the tokenlist, and return a list storing those names
"""
def get_statements_names(filename):

    tokenslist = get_statements_tokens(filename)
    nameslist = []
    names = []

    for i in range(len(tokenslist)):
        for j in range(len(tokenslist[i])):
            if (tokenslist[i][j][0].isupper() or tokenslist[i][j] == 'von'):
                names.append(tokenslist[i][j].lower())
        nameslist.append(names)
        names=[]

    return nameslist



