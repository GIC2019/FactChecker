"""Use xml.sax to analysis huge xml-data on the fly"""
import xml.sax

class XMLHandler (xml.sax.handler.ContentHandler):

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self.current_tag = None
        self.tag_text = None
        self.text = {}

    """Opening tag of element, this method runs to find a "opening" tag, and access the tag
       if tag is 'title' or 'text', set the tag to the var current_tag
       and then create a list -- buffer_text to store the content in the tag.
    """

    def startElement(self, tag, attrs):
        if tag in ('title', 'text'):
            self.current_tag = tag
            self.tag_text = []

    """Characters between opening and closing tags, this method runs if startElement has found a opening tag
       add the content between the opening and closing tags in to the list -- buffer_text
    """

    def characters(self, content):
        if self.current_tag:
            self.tag_text.append(content)

    """Closing tag of element, this method runs if a ending tag has be found
       if the closing tag is 'title' or 'text', then print them
       if the closing tag is 'page', then print a page line
    """

    def endElement(self, tag):
        if tag == self.current_tag:
            print(self.current_tag)
            self.text[tag] = ' '.join(self.tag_text)
            print(self.text)


        if tag == 'page':

            print("#######################################################")


if __name__ == "__main__":

    dumpfile = 'enwiki-latest-pages-articles.xml'
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = XMLHandler()
    parser.setContentHandler(handler)
    parser.parse(dumpfile)
