"""Use xml.sax to analysis huge xml-data on the fly"""
import xml.sax
import os
import multiprocessing
import datetime
from clean_and_write import clean_and_write
from clean_and_write import init
from pathlib import Path

class XMLHandler (xml.sax.handler.ContentHandler):

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        # Store the current scanned tag: <title>, <text>
        self.current_tag = None
        # List: Store the last scanned title (no string, title'name as an element stored in a list)
        self.tag_title = None
        # List: Store the last scanned text (raw text are split and stored in a list)
        self.tag_text = None
        # String: convert tag_title to a string
        self.title_string = ""
        # String: clean the raw text, and convert the cleaned text to a string
        self.text_string = ""

        # Store the number of handled articles
        self.counter = 0
        # Store the number of exception articles
        self.exception_counter = 0
        # Store the number of corpus files
        self.corpus_index = 0
        # number of cpus of this computer
        self.cpu_count = multiprocessing.cpu_count()
        # lock for the file, so two processes don't write simultaneously on it
        self.l = multiprocessing.Lock()
        # counting-semaphore to only apply one workload on a process at one time
        self.s = multiprocessing.Semaphore(self.cpu_count-1)
        # pool of (cpu_count - 1) processes
        self.proc_pool = multiprocessing.Pool(processes=self.cpu_count-1, initializer=init, initargs=(self.l,self.s,))
    
    
    """Opening tag of element, this method runs to find a "opening" tag, and access the tag
       if tag is 'title' or 'text', set the tag to the var current_tag
       and then create a list -- buffer_text to store the content in the tag.
    """

    def startElement(self, tag, attrs):
        if tag in ('title', 'text'):
            self.current_tag = tag
            if tag == 'title':
                self.tag_title = []
            if tag == 'text':
                self.tag_text = []

    """Characters between opening and closing tags, this method runs if startElement has found a opening tag
       add the content between the opening and closing tags in to the list -- buffer_text
    """

    def characters(self, content):
        if self.current_tag == 'title':
            self.tag_title.append(content)
        if self.current_tag == 'text':
            self.tag_text.append(content)

    """Closing tag of element, this method runs if a ending tag has be found
       if the closing tag is 'title' or 'text', then print them
       if the closing tag is 'page', then print a page line
    """
    def endElement(self, tag):

        if tag == self.current_tag:
            if self.current_tag == 'title':
                self.title_string = ''.join(self.tag_title)
                self.counter = self.counter + 1

            if self.current_tag == 'text':
                try:
                # eliminate the article with title's name "List of **"
                # if title's name contains "List of ", then don't extract the text
                    if 'List of' in self.title_string:
                        self.text_string = ''
                # eliminate some exceptions
                    elif 'Wikipedia:' in self.title_string:
                        self.text_string = ''
                    elif 'Portal:' in self.title_string:
                        self.text_string = ''
                    elif 'Template:' in self.title_string:
                        self.text_string = ''
                    elif 'Draft:' in self.title_string:
                        self.text_string = ''
                    elif 'MediaWiki:' in self.title_string:
                        self.text_string = ''
                    elif 'File:' in self.title_string:
                        self.text_string = ''
                    elif 'Module:' in self.title_string:
                        self.text_string = ''
                    elif 'Category:' in self.title_string:
                        self.text_string = '' 
             
                 # eliminate the redirected article
                # if tag_text[0] contains "#REDIRECT", then don't extract the text
                    elif '#REDIRECT' in str(self.tag_text[0]):
                        self.text_string = ''

                # use method : Cleaner.clean_text(tag_text) to extract all useful information
                # and write it into the corpus**.txt
                    else:
                    # acquire one from the semaphore to only ever apply one tag_text to one process at the same time
                        self.s.acquire()
                        #print('acquired semaphore')
                    # apply the workload to a free process: clean the tag_text and write title + cleaned text to the file
                        self.proc_pool.apply_async(clean_and_write, (self.corpus_index, self.title_string, self.tag_text))
  
                    # Check the size of corpus file, if it is bigger than 80MB, then create a new corpus file
                        
                        file = 'corpus0' + str(self.corpus_index) + '.txt'
                        pathfile = Path(file)
                        if pathfile.is_file():
                            size = os.path.getsize(file)
                            if size >= (1024*1024*80):
                                self.corpus_index = self.corpus_index + 1

                # Use try: except: module to handle exception of article-extraction
                # If exception happens: print the information of exception and pass
                except (ValueError, IndexError):
                    self.exception_counter = self.exception_counter + 1
                    print("Exception", self.exception_counter, ': ', self.title_string, ' ', self.counter)
                    pass
