import eventlet
from cleaner import WikiCleaner
"""
    cleans the tag_text via the Cleaner-class
    writes title, cleaned text and separators in the file
"""
def clean_and_write(corpus_index, title_string, tag_text):
    try:
        # cleaning text tag
        text_string = WikiCleaner.clean_text(tag_text) 
        file = 'corpus0' + str(corpus_index) + '.txt'
        # writing to the file
        file_lock.acquire()
        with open(file, "a", encoding='utf-8') as f:
            f.write(title_string + '\n')
            f.write(text_string + '\n')
            f.write("==========")
        file_lock.release()
    except (ValueError, IndexError):
        print("Exception in:", title_string)
        pass
    proc_semaphore.release()
    return exception_counter

""" 
    initializes the global file_lock and proc_semaphore, so each process has access to them.
    this cannot be done via parameters of the clean_and_write method for some technical reasons in python
"""
def init(l, s):
    global file_lock
    global proc_semaphore
    file_lock = l
    proc_semaphore = s
