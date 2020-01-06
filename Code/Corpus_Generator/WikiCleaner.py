import re

"""
clean the raw text which is extracted from the wikipedia dump-file
"""
class WikiCleaner(object):

    def __init__(self):
        self.str = ''

    @staticmethod
    def clean_text(list):

        # handle the extracted text in list-level
        """
        find the first bold and italic word with '''''word''''' or
        find the first bold word with '''word'''in the list
        delete all elements before this found element
        Notice: First bold (and italic) word is in general the same as the article title,
        this is the beginning of first section of a wiki-article
        """

        for i in range(len(list)):
            if '\'\'\'\'\'' in str(list[i]) and str(list[i])[0:1] != '|':
                break
            elif '\'\'\'' in str(list[i]) and str(list[i])[0:1] != '|':
                break
            else:
                list[i] = ''
        for text in list:
            if '' in list:
                list.remove('')

        """
        Count the elements with "==", because "==subtitle==", store the number of that in counter
        The upper bound of counter can be setted to control how much information is be extracted
        """
        counter = 0
        index = "not change"
        for i in range(len(list)):
            if '==' in list[i] and counter == 1:
                index = i
                break
            elif '==' in list[i] and counter < 1:
                counter += 1
        # index == "not change", iff there's no "==subtitle=="
        if index != "not change":
            while len(list) > index:
                list.pop()


        #handle the grabbed text in string-level

        string = ' '.join(list)

        """
        find all patterns like {{!}} and delete them, 
        this always appears in the reference {{cite: **{{i}}****}}
        """
        pattern1 = re.compile(r'\{\{\!\}\}')
        string = ''.join(re.split(pattern1, string))

        """
        find all patterns like {{content}}
        and delete them
        """
        pattern2 = re.compile(r'\{\{[^\{\}]+\}\}')
        string = ''.join(re.split(pattern2, string))

        pattern3 = re.compile(r'[^a-zA-Z0-9]')
        string = ' '.join(re.split(pattern3, string))

        """
        eliminate all unwanted white-spaces, '', '\n', '\t' etc. 
        """
        pattern4 = re.compile(r'[\s]+')
        string = re.sub(pattern4, ' ', string)

        return string