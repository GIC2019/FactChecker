from Mini_Project.Server.InputFileAnalyser import get_factID
from Mini_Project.Server.InputFileAnalyser import get_statements_tokens
from Mini_Project.Server.InputFileAnalyser import get_statements_names
import os
import re
import datetime

#determine whether list1 is sublist of list2
def is_sublist(list1, list2):
    for i in range(len(list1)):
        if not(list1[i] in list2):
            return False
    return True

"""
check the facts 
"""
def check_fact(filename, max_corpus_index):

    pattern1 = re.compile(r'[^a-zA-Z0-9]')
    pattern2 = re.compile(r'[ ]+')
    tokenslist = get_statements_tokens(filename)
    for i in range (len(tokenslist)):
        for j in range (len(tokenslist[i])):
            tokenslist[i][j] = tokenslist[i][j].lower()
    nameslist = get_statements_names(filename)

    #Initialize the results
    results = []
    for i in range(len(tokenslist)):
        results.append('0.0')

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for i in range(max_corpus_index+1):
        print(datetime.datetime.now(), ': processing corpus0', str(i))
        corpus = base_path + '\Corpus_Generator\Corpus\corpus0' + str(i) + '.txt'
        file = open(corpus, 'r', encoding="utf-8")
        last_line = "==========\n"
        line = file.readline()
        while line:
            if last_line == "==========\n":
                # line now is a article title
                line = re.sub(pattern1, ' ', line)
                title_tokens = re.split(pattern2, line)
                # eliminate the all elements '' in list token
                title_tokens = list(filter(None, title_tokens))
                for j in range(len(title_tokens)):
                    title_tokens[j] = title_tokens[j].lower()

                #nextline is the content with this article title
                line = file.readline()
                line = re.sub(pattern1, ' ', line)
                content_tokens = re.split(pattern2, line)
                content_tokens = list(filter(None, content_tokens))
                for j in range(len(content_tokens)):
                    content_tokens[j] = content_tokens[j].lower()

                #if article_title_tokens in corpus is sublist of tokenslist of a statement
                #then if all names of this statement appear in the content of this article title
                #then fact is true, otherwise fact is false
                for j in range(len(tokenslist)):
                    if not (results[j] == '1.0'):
                        if is_sublist(title_tokens, tokenslist[j]):
                            if is_sublist(nameslist[j], content_tokens):
                                results[j] = '1.0'

            last_line = line
            line = file.readline()
        file.close()
    return results

"""
generate the result file for test file
"""
def generate_result(filename, max_corpus_index):
    id_list = get_factID(filename)
    results = check_fact(filename, max_corpus_index)

    file = open('result.ttl', 'a', encoding="utf-8" )
    for i in range(len(id_list)):
        fact_uri = '<http://swc2017.aksw.org/task2/dataset/' + id_list[i] + '>'
        prop_uri = '<http://swc2017.aksw.org/hasTruthValue>'
        value = '\"'+results[i]+'\"^^'
        type = '<http://www.w3.org/2001/XMLSchema#double> .\n'
        result = fact_uri + prop_uri+value+type
        file.write(result)
    file.close()

"""
generate the result file for training file
"""
def generate_training_result(filename, max_corpus_index):
    id_list = get_factID(filename)
    results = check_fact(filename, max_corpus_index)

    file = open('training_result.ttl', 'a', encoding="utf-8" )
    for i in range(len(id_list)):
        fact_uri = '<http://swc2017.aksw.org/task2/dataset/' + id_list[i] + '>'
        prop_uri = '<http://swc2017.aksw.org/hasTruthValue>'
        value = '\"'+results[i]+'\"^^'
        type = '<http://www.w3.org/2001/XMLSchema#double> .\n'
        result = fact_uri + prop_uri+value+type
        file.write(result)
    file.close()


generate_training_result('SNLP2019_training.tsv', 163)
generate_result('SNLP2019_test.tsv', 163)
