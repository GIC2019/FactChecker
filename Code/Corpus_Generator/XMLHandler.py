import xml.sax
import os
import multiprocessing
from pathlib import Path
from .clean_and_write import init
from .clean_and_write import clean_and_write


""" 
The class XMLHanler is base on xml.sax.handler.ContentHandler.
Use xml.sax.handler.ContentHandler to analyse huge xml file on the fly.
ContentHandler scan xml-file tag by tag and handle the content between the opening and closing tag.
We need to override the method: startElement, characters, and endElement.
"""

class XMLHandler (xml.sax.handler.ContentHandler):

    # constructor
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        # Store the current scanned tag: <title>, <text>, ...
        self.current_tag = None
        # List: Store the last scanned title (no string, title'name as an element stored in a list)
        self.tag_title = None
        # List: Store the last scanned text (raw text are split and stored in a list)
        self.tag_text = None
        # String: convert tag_title to a string
        self.title_string = ""
        # String: clean the raw text, and convert the cleaned text to a string
        self.text_string = ""
        # Integer: Store the number of handled articles
        self.counter = 0
        # Integer: Store the number of exception articles
        self.exception_counter = 0
        # Store the number of corpus files, each corpus file'size is 45MB
        self.corpus_index = 0

        # number of processors in this computer
        self.cpu_count = multiprocessing.cpu_count()
        if self.cpu_count < 2:
            self.cpu_count = 2
		# lock for the file, so two processes don't write simultaneously on it
        self.l = multiprocessing.Lock()
        # counting-semaphore to only apply one workload on a process at one time
        self.s = multiprocessing.Semaphore(self.cpu_count - 1)
        # pool of (cpu_count-1) processes
        self.proc_pool = multiprocessing.Pool(processes=self.cpu_count-1, initializer=init, initargs=(self.l, self.s))

    """
    Scan the opening tag:
        if tag is 'title' or 'text':
            then current_tag = tag
            and initialize corresponding tag_title or tag_text as a list to store the content in the tag.
        else:
            ignore other tags.
    """
    def startElement(self, tag, attrs):
        if tag in ('title', 'text'):
            self.current_tag = tag
            if tag == 'title':
                self.tag_title = []
            if tag == 'text':
                self.tag_text = []

    """
    If current_tag is 'title' or 'text', then continue to scan the content between the opening tag and closing tag:
    """
    def characters(self, content):
        if self.current_tag == 'title':
            self.tag_title.append(content)
        if self.current_tag == 'text':
            self.tag_text.append(content)

    """
    if closing tag is <title>, then convert the content in tag <title> to string, store it in title_string
    if closing tag is <text>, then clean the content and convert the cleaned content into string, and store 
    it in text_string
    """

    def endElement(self, tag):
        if tag == self.current_tag:
            if self.current_tag == 'title':
                self.title_string = ''.join(self.tag_title)
                self.counter = self.counter + 1

            if self.current_tag == 'text':
                # Use try: except: module to handle exception of article-extraction
                # If exception happens: print the information of exception and pass
                try:
                    # if title's name contains "List of ", "Wikipedia:"..., then don't extract the text
                    if 'List of' in self.title_string:
                        self.text_string = ''
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

                    # if tag_text[0] contains "#REDIRECT", then don't extract the text
                    elif '#REDIRECT' in str(self.tag_text[0]):
                        self.text_string = ''

                    # use method : Cleaner.clean_text(tag_text) to extract all useful information
                    # and write it into the corpus**.txt
                    else:
                        self.s.acquire()
                        self.proc_pool.apply_async(clean_and_write,
                                                   (self.corpus_index, self.title_string, self.tag_text))
                        dirname = os.path.dirname(os.path.abspath(__file__))
                        file = dirname+'\Corpus\corpus0' + str(self.corpus_index) + '.txt'
                        pathfile = Path(file)
                        if pathfile.is_file():
                            # Check the size of corpus file, if it is bigger than 45MB, then create a new corpus file
                            size = os.path.getsize(file)
                            if size >= (1024 * 1024 * 45):
                                self.corpus_index = self.corpus_index + 1

                except (ValueError, IndexError):
                    self.exception_counter = self.exception_counter + 1
                    print("Exception", self.exception_counter, ': ', self.title_string, ' ', self.counter)
                    pass