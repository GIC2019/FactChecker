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

        """
        find all patterns like [[alternate1|alternate2]]
        delete the first alternate1 and '|'
        [[alternate1|alternate2]]  --->  alternate2]]
        """

        # use regular expression to find [[alternate1|
        pattern1 = re.compile(r'\[\[[\w|\-| \(|\)|\'|\#]+\|')
        string = ' '.join(re.split(pattern1, string))

        """
        find all patterns like {{!}} and delete them, 
        this always appears in the reference {{cite: **{{i}}****}}
        """
        pattern10 = re.compile(r'\{\{\!\}\}')
        string = ''.join(re.split(pattern10, string))

        """
        find all patterns like {{content}}
        and delete them
        """
        pattern2 = re.compile(r'\{\{[^\{\}]+\}\}')
        string = ''.join(re.split(pattern2, string))

        """
        find all patterns like <content>
        and delete them
        """
        pattern3 = re.compile(r'\<[^\<\>]*\>')
        string = ''.join(re.split(pattern3, string))

        """
        find all patterns like (content)
        and delete them
        """
        pattern8 = re.compile(r'\([^\(\)]*\)')
        string = re.sub(pattern8, '', string)

        """
        eliminate all '[' and ']'
        """
        pattern4 = re.compile(r'[\[|\]]+')
        string = re.sub(pattern4, '', string)

        """
        eliminate all ''' or '''''
        """
        pattern5 = re.compile(r'[\'\'\']')
        string = re.sub(pattern5, '', string)
        pattern6 = re.compile(r'[\'\'\'\'\']')
        string = re.sub(pattern6, '', string)

        """
        eliminate all web site address
        """
        pattern7 = re.compile(r'http://[^ ]+')
        string = re.sub(pattern7, '', string)

        """
        eliminate other unwanted signs
        """
        string = string.replace('<', '')
        string = string.replace('>', '')
        string = string.replace('!', '')
        string = string.replace('-', '')
        string = string.replace(';', ' ')
        """
        eliminate all unwanted white-spaces, '', '\n', '\t' etc. 
        """
        pattern9 = re.compile(r'[\s]+')
        string = re.sub(pattern9, ' ', string)

        return string



