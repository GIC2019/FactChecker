import eventlet
from cleaner import Cleaner
"""
cleans the tag_text via the Cleaner-class
writes title, cleaned text and separators in the file
"""
def clean_and_write(title_string, tag_text, counter, exception_counter):
    #print('Process runs')
    try:
		# cleaning the text
        get_text = False
        text_string= " "
        eventlet.monkey_patch()
        with eventlet.Timeout(5, False):
            text_string = Cleaner.clean_text(tag_text)
            get_text = True
        if not get_text:
            text_string = " "
			
		# writing to file
        file_index = int(counter/100000)
        file = 'corpus0' + str(file_index) + '.txt'
        file_lock.acquire()
        with open(file, "a", encoding='utf-8') as f:
            f.write(title_string + '\n' + '---------------' + '\n'+text_string + '\n' + '====================================================' + '\n')
        file_lock.release()
		
    except (ValueError, IndexError):
        print("Exception", exception_counter, ': ', title_string, ' ', counter)
        exception_counter = exception_counter + 1
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