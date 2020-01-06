import re

class WikiCleaner(object):

    def __init__(self):
        self.str = ''

    @staticmethod
    def clean_text(list):

        #handle the grabbed text in list-level

        """
        find the first bold and italic word with '''''word'''''     or
        find the first bold word with '''word'''in the list
        delete all elements before this found element
        Notice: First bold (and italic) word is as same as the article title, this is the beginning of first section
        #       of wiki-article
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
        find the first element with "==", because "==subtitle=="
        content in subtitle are needless, so delete this element and all elements after it
        """
        index = "not change"
        for i in range(len(list)):
            if '==' in list[i]:
                index = i
                break
        # index == "not change", iff there's no "==subtitle=="
        if index != "not change":
            while len(list) > index:
                list.pop()


        #handle the grabbed text in string-level

        string = ' '.join(list)


        # use regular expression to find [[alternate1|
        pattern1 = re.compile(r'[^a-zA-Z0-9]')
        string = ' '.join(re.split(pattern1, string))

        """
        eliminate all unwanted white-spaces, '', '\n', '\t' etc. 
        """
        pattern9 = re.compile(r'[\s]+')
        string = re.sub(pattern9, ' ', string)

        return string