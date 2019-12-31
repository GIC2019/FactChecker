import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)

from Mini_Project.Corpus_Generator.XMLHandler import XMLHandler
import datetime
import xml.sax
if __name__ == '__main__':
    print(datetime.datetime.now())
    dirname = os.path.abspath('..')
    print(type(dirname))
    filename = '\dumpfile\dumpfile.xml'
    dumpfile = dirname + filename
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = XMLHandler()
    parser.setContentHandler(handler)
    parser.parse(dumpfile)
    print(datetime.datetime.now())
    print('Done!!!!!')