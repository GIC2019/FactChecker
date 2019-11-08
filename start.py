from CorpusGenerator import XMLHandler
import datetime
import xml.sax
if __name__ == '__main__':
    print(datetime.datetime.now())
    dumpfile = 'enwiki-latest-pages-articles.xml'
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    handler = XMLHandler()
    parser.setContentHandler(handler)
    parser.parse(dumpfile)
    print('Done!!!!!')