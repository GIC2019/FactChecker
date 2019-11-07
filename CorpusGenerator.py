"""
Use xml.sax.handler.ContentHandler to analyse huge xml file on the fly.
ContentHandler scan xml file tag by tag and handle the content between the opening and closing tag.
We need to override the method: startElement, characters, and endElement; to reach the purpose.
"""

import xml.sax
import os
from FactChecker.cleaner2 import WikiCleaner

""" XMLHanler is base on xml.sax.handler.ContentHandler"""

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

    """
    Scan the opening tag:
        if tag is 'title' or 'text':
            then current_tag = tag
            and create initialize corresponding tag_title or tag_text as a list to store the content in the tag.
    Don't need to consider other tags 
    """

    def startElement(self, tag, attrs):
        if tag in ('title', 'text'):
            self.current_tag = tag
            if tag == 'title':
                self.tag_title = []
            if tag == 'text':
                self.tag_text = []

    """
    Scan the content between the opening tag and closing tag:
        if current_tag is 'title' or 'text':
            add the contents into the corresponding list: tag_title or tag_text
    """

    def characters(self, content):
        if self.current_tag == 'title':
            self.tag_title.append(content)
        if self.current_tag == 'text':
            self.tag_text.append(content)

    """
    Scan the closing tag:
        if closing tag matches with current_tag ('title' or 'text')
            covert the corresponding list (tag_title or tag_text) to a string (title_string or text_string)
            if the string is stored in the "title_string":
                then write it into the corpus
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

                    # eliminate the redirected article
                    # if tag_text[0] contains "#REDIRECT", then don't extract the text
                    elif '#REDIRECT' in str(self.tag_text[0]):
                        self.text_string = ''

                    # use method : Cleaner.clean_text(tag_text) to extract all useful information
                    # and write it into the corpus**.txt
                    else:

                        #print(self.counter, ': ')
                        self.text_string = WikiCleaner.clean_text(self.tag_text)
                        #print(self.text_string)
                        #print("=========================================")

                        file = 'corpus0' + str(self.corpus_index) + '.txt'
                        with open(file, "a", encoding='utf-8') as f:
                            f.write(self.text_string + '\n')

                        # Check the size of corpus file, if it is bigger than 80MB, then create a new corpus file
                        size = os.path.getsize(file)
                        if size >= (1024*1024*80):
                            self.corpus_index = self.corpus_index + 1

                # Use try: except: module to handle exception of article-extraction
                # If exception happens: print the information of exception and pass
                except (ValueError, IndexError):
                    self.exception_counter = self.exception_counter + 1
                    print("Exception", self.exception_counter, ': ', self.title_string, ' ', self.counter)
                    pass


if __name__ == "__main__":

    dumpfile = 'F:\Master\Statistical NLP\Mini_Project\FactChecker\SplitWikiXML\\xaa.xml'
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = XMLHandler()
    parser.setContentHandler(handler)
    parser.parse(dumpfile)
    print(handler.counter)
    print('Done!!!!!')