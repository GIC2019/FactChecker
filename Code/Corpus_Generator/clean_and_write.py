from .WikiCleaner import WikiCleaner
"""
cleans the tag_text via the class WikiCleaner, convert the cleaned text into a string(stored in text_string)
write title and text in form:
    title_string
    text_string
    "=========="
"""
def clean_and_write(corpus_index, title_string, tag_text):
    try:
        # cleaning text tag
        text_string = WikiCleaner.clean_text(tag_text)
        if text_string != ' ' or text_string != '' or ('Please do not modify it' not in text_string):
            file = 'corpus0' + str(corpus_index) + '.txt'
            # writing to the file
            file_lock.acquire()
            with open(file, "a", encoding='utf-8') as f:
                f.write(title_string + '\n')
                f.write(text_string + '\n')
                f.write("==========" +'\n')
            file_lock.release()
    except (ValueError, IndexError):
        print("Exception in:", title_string)
        pass
    proc_semaphore.release()


"""
initializes the global file_lock and proc_semaphore, so each process has access to them.
this cannot be done via parameters of the clean_and_write method for some technical reasons in python
"""
def init(l, s):
    global file_lock
    global proc_semaphore
    file_lock = l
    proc_semaphore = s