# Guideline for our FactChecker

#### 1. Check the Fact

> **Notice:**  The result files (training_result.ttl and result.ttl) of this mini-project have been already generated and stored in the folder ".\FactChecker\Code\Server". If you want to generate the result files yourself, please delete the files, rename them or clear the content of these files first.

Run the FactChecker in command prompt:

1. Step: Use command 'cd filepath' to go to the folder ".\FactChecker\Code\Server\\".

2. Step: Use the following command line to run the file "check_fact.py"

   ​	\> python check_fact.py

After these two steps two result files will be generated:

+ file: training_result.ttl

  This result file stores all results for the facts in file "SNLP2019_training.tsv".

+ file: result.ttl

  This result file stores all results for the facts in file "SNLP2019_test.tsv".
  
  

> **Notice:** The corpus for the FactChecker has been generated and all the corpus files are already store in the file ".\FactChecker\Code\\Corpus_Generator\Corpus". If you want to generate these corpus files yourself, please **delete(or replace)** all corpus file first.

#### 2. Corpus_Generator

1. Step: Download the  file "enwiki-latest-pages-articles.xml.bz2"  from web-address: <https://dumps.wikimedia.org/enwiki/latest/>.

   This file is English Wikipedia database dump file. A warning for this download, this file is very large, in size 16GB.

2. Step: Unzip the file "enwiki-latest-pages-articles.xml.bz2" into the folder ".\FactChecker\Code\dumpfile". Rename the unzipped file with to "dumpfile.xml".  A warning for the  unzipped dumpfile, this file is in size 70GB.

3. Step: Use the command 'cd filepath' to go to the folder ".\FactChecker\Code\\Corpus_Generator\". 

4. Step: Use the following command line to run the module "generate_corpus.py": 

   ​	> python generate_corpus.py

 After the four steps you can get 164 corpus files, each file is in size 45MB. All files are stored in the subfolder ".\FactChecker\Code\\Corpus_Generator\Corpus". 
