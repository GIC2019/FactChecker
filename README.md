# Guideline of FactChecker

### Corpus_Generator (no multi-processing part)

####  1. Generate Corpus

1. Step: Download the  file "enwiki-latest-pages-articles.xml.bz2"  from web-address: <https://dumps.wikimedia.org/enwiki/latest/>.

   This file is English Wikipedia database dump file. A warning for this download, this file is very large, in size 16GB.

2. Step: Unzip the file "enwiki-latest-pages-articles.xml.bz2" into the folder ".\FactChecker\Code\dumpfile". And rename the unzipped file with the filename "dumpfile.xml".

   In the folder ".\FactChecker\Code\dumpfile" there's already a pattern of dumpfile.xml there in size 93MB. You can use it to test the code. But if you want to generate the entire corpus, you must delete this pattern.

3. Step: Run the module "generate_corpus.py", then you can get the 164 corpus files stored in the folder ".\FactChecker\Code\Corpus_Generator\Corpus" .

> **Notice:** You don't need to generate corpus files, because the 164 corpus files are already there. But if you still want to generate these corpus files, please **delete(or replace)** all corpus files at first.

#### 2. Module Description

+ XMLHandler.py

  This module contains a class "XMLHandler". This class is the subclass of xml.sax.handler.ContentHandler. 

  In this subclass we rewrite 3 methods to handle the .xml file tag by tag.

  + startElement(tag, attrs): 

    find the the blocks with opening tag \<title> or  \<text>

  + characters(content):

    if the tag \<title> or  \<text> has been found, then store the content between opening tag and closing tag.

  + endElement(tag):

    if the closing tag \<\title> or \<\text> has been found, then preprocess the stored content and write them into corpus with the following form:

    ​				article title
    
    ​				article text
    
    ​				==========
    
    ​				article title
    
    ​				article text
    
    ​				==========
    
    ​				$\dots\dots$
    
    Each corpus file is in size 45MB.

+ WikiCleaner.py

  This module contains a class "WikiCleaner". This class contains a static method: 

  + clean_text(list):

    The parameter "list" contains the content between the opening tag \<text> and closing tag\<\text>, through this method you can extract the useful information for the FactChecker and convert it into a string.

* clean_and_write.py

  This module contains two methods:

  + clean_and_write(corpus_index, title_string, tag_text):

    use "WikiCleaner" to get the cleaned string and write them into the corpus

+ generate_corpus.py

  Run this module to generate corpus directly.

### Server

#### 1. Check the Fact

Run the module "check_fact.py" in the folder "Server", then you can get two result files:

+ file: training_result.ttl

  This result file stores all results for the facts in file "SNLP2019_training.tsv".

+ file: result.ttl

  This result file stores all results for the facts in file "SNLP2019_test.tsv".

> **Notice:** Both of the result files have been already generated. If you want to generate the both files yourself, please delete the both files or clear the contents of the both files.

#### 2. Module Description

+ InputFileAnalyser.py

  The goal of this module is extracting the information of each statement, and store them in a corresponding list. It contains four methods:

  + get_factID(filename):

    Get FactID of each statement in the file "filename", and store them in a list.

  + get_statements(filename):

    Get content of each statement in the file "filename", eliminate all symbols except for letter and number, and store the preprocessed statements in a list.

  + get_statements_tokens(filename):

    Tokenize all preprocessed statements, and store all token-lists in a list.

  + get_statements_names(filename):

    Extract all names from the tokens-list for each statement, and store all name-lists in a list.

+ check_fact.py

  Run this module, you can get two result files: one for training file, another for test file. It contains four methods:

  + is_sublist(list1, list2):

    Check whether list1 is subset of list2. If so, return True, otherwise, return False.

  + check_fact(filename, max_corpus_index):

    Utilize the generated corpus to check facticity of each statement in the file "filename".

    And store all results (0.0 or 1.0) in a list.

  + generate_result(filename, max_corpus_index):

    According to the result of "check_fact" generate a result file: "result.ttl". The filename should be a test file.

  + generate_training_result(filename, max_corpus_index):

    According to the result of "check_fact" generate a result file: "training_result.ttl". The filename should be a training file.

  