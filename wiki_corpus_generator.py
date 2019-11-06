"""Use xml.sax to analysis huge xml-data on the fly"""
import xml.sax
import eventlet
import time
import multiprocessing
import datetime
from clean_and_write import clean_and_write
from clean_and_write import init

class XMLHandler (xml.sax.handler.ContentHandler):

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self.current_tag = None
        self.tag_text = None
        self.tag_title = None
        self.title_string = ""
        self.text_string = ""
        self.counter = 0
        self.exception_counter = 1
        self.jumping_counter = 0
        self.cpu_count = multiprocessing.cpu_count()
		# lock for the file, so two processes don't write simultaneously on it
        l = multiprocessing.Lock()
		# counting-semaphore to only apply one workload on a process at one time
        self.s = multiprocessing.Semaphore(self.cpu_count-1)
		# pool of cpu_count - 1 processes
        self.proc_pool = multiprocessing.Pool(processes=self.cpu_count-1, initializer=init, initargs=(l,self.s,))
    
    
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
				# acquire one from the semaphore to only ever apply one tag_text to one process at the same time
                self.s.acquire()
				# apply the workload to a free process: clean the tag_text and write title + cleaned text to the file
                self.proc_pool.apply_async(clean_and_write, (self.title_string, self.tag_text, self.counter, self.exception_counter))