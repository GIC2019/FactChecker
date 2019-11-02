"""Use xml.sax to analysis huge xml-data on the fly"""
import xml.sax
from FactChecker.cleaner import Cleaner

class XMLHandler (xml.sax.handler.ContentHandler):

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self.current_tag = None
        self.tag_text = None
        self.tag_title = None
        self.title_string = ""
        self.text_string = ""

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
                print(self.title_string)
            if self.current_tag == 'text':
                self.text_string = Cleaner.clean_text(self.tag_text)
                print(self.text_string)


        if tag == 'page':

            print()




if __name__ == "__main__":

    dumpfile = 'enwiki-latest-pages-articles.xml'
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = XMLHandler()
    parser.setContentHandler(handler)
    parser.parse(dumpfile)
