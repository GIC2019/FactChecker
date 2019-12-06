import inspect
import os
import re
import datetime
from sklearn.metrics import roc_auc_score

def is_sublist(list1, list2):
    for i in range(len(list1)):
        if not(list1[i] in list2):
            return False
    return True

#First part: extract the statements
dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
filename = "SNLP2019_training.tsv"
filepath = os.path.join(dirname, filename)
statementfile = open(filepath, "r", encoding="utf-8")

line = statementfile.readline()
line = statementfile.readline()

#list which stores all statements
statements = []
#list which stores all ground truths
ground_truths = []

#list which stores all tokens for each statement
tokenized_statement = []

#list which stores all names
names_of_statements = []

pattern1 = re.compile(r'[^a-zA-Z0-9]')
pattern2 = re.compile(r'[ ]+')


while line:

    statement = line.split('\t')[1][:-1]
    statements.append(statement)

    truth = line.split('\t')[2][0:3]
    ground_truths.append(truth)

    statement = re.sub(pattern1, ' ', statement)
    tokens = re.split(pattern2, statement)
    # eliminate the all elements '' in list token
    tokens = list(filter(None, tokens))

    names = []

    # Extract names for each statement
    for i in range(len(tokens)):
        if (tokens[i][0].isupper() or tokens[i] == 'von'):
           names.append(tokens[i].lower())
    names_of_statements.append(names)
    line = statementfile.readline()

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
    tokenized_statement.append(tokens)

    with open('training.txt', 'a', encoding="utf-8") as f:
        f.write(str(tokens) + ' ## ' + str(names) + '\n')

starttime = datetime.datetime.now()


print(starttime)
results = []
for i in range(len(tokenized_statement)):
    results.append('0.0')

for i in range(59):
    print("Corpus", i, "is in processing")
    corpus = '.\Corpus\corpus0' + str(i) + '.txt'

    file_in = open(corpus, 'r', encoding="utf-8")
    last_line = "==========\n"
    line = file_in.readline()

    while line:
        if last_line == "==========\n":
            # line now is a article title
            line = re.sub(pattern1, ' ', line)
            title_tokens = re.split(pattern2, line)
            # eliminate the all elements '' in list token
            title_tokens = list(filter(None, title_tokens))
            for m in range(len(title_tokens)):
                title_tokens[m] = title_tokens[m].lower()

            # next_line is a content of a article
            line = file_in.readline()
            line = re.sub(pattern1, ' ', line)
            content_tokens = re.split(pattern2, line)
            content_tokens = list(filter(None, content_tokens))
            for m in range(len(content_tokens)):
                content_tokens[m] = content_tokens[m].lower()

            for j in range(len(tokenized_statement)):
                if not (results[j] == '1.0'):
                    if is_sublist(title_tokens, tokenized_statement[j]):
                        if is_sublist(names_of_statements[j], content_tokens):
                            results[j] = '1.0'

        last_line = line
        line = file_in.readline()

endtime = datetime.datetime.now()
print(endtime)

for i in range(len(statements)):
    if ground_truths[i] == '1.0' and  results[i] == '1.0':
        with open('training_result.txt', 'a', encoding="utf-8") as file_out:
            file_out.write('TP' + '\t' + str(i+1) + ' statement: ' + statements[i] + '\t' + results[i] + '\n')
    elif ground_truths[i] == '0.0' and results[i] == '0.0':
        with open('training_result.txt', 'a', encoding="utf-8") as file_out:
            file_out.write('TN' + '\t' + str(i+1) + ' statement: ' + statements[i] + '\t' + results[i] + '\n')
    elif ground_truths[i] == '0.0' and results[i] == '1.0':
        with open('training_result.txt', 'a', encoding="utf-8") as file_out:
            file_out.write('FP' + '\t' + str(i+1) + ' statement: ' + statements[i] + '\t' + results[i] + '\n')
    elif ground_truths[i] == '1.0' and  results[i] == '0.0':
        with open('training_result.txt', 'a', encoding="utf-8") as file_out:
            file_out.write('FN' + '\t' + str(i+1) + ' statement: ' + statements[i] + '\t' + results[i] + '\n')

TP = 0
TN = 0
FP = 0
FN = 0

for i in range(len(ground_truths)):

    if ground_truths[i] == '1.0' and  results[i] == '1.0':
        TP += 1
    elif ground_truths[i] == '0.0' and  results[i] == '0.0':
        TN += 1
    elif ground_truths[i] == '0.0' and  results[i] == '1.0':
        FP += 1
    elif ground_truths[i] == '1.0' and  results[i] == '0.0':
        FN += 1






