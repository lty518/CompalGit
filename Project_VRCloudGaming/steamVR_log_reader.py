from datetime import datetime
from dateutil.parser import parse
import time
import os
filename_vrserver              = 'C:/Program Files (x86)/Steam/logs/vrserver.txt'
filename_vrcompositor          = 'C:/Program Files (x86)/Steam/logs/vrcompositor.txt'
filename_vrclient_vrcompositor = 'C:/Program Files (x86)/Steam/logs/vrclient_vrcompositor.txt'
filename_vrdashboard           = 'C:/Program Files (x86)/Steam/logs/vrdashboard.txt'
filename_vrclient_vrdashboard  = 'C:/Program Files (x86)/Steam/logs/vrclient_vrdashboard.txt'
filename_vrmonitor             = 'C:/Program Files (x86)/Steam/logs/vrmonitor.txt'
filename_vrclient_vrmonitor    = 'C:/Program Files (x86)/Steam/logs/vrclient_vrmonitor.txt'

last_log_timeinfo =''
# for line in open(filename_vrmonitor,'r', encoding='utf-8'):
#     if "Status Alert" in line:
#         print(line)
#     else:
#         continue

def follow(thefile):
    '''generator function that yields new lines in a file '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)

    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line

if __name__ == '__main__':
    logfile = open("C:/Program Files (x86)/Steam/logs/vrmonitor.txt","r", encoding='utf-8')
    loglines = follow(logfile)
    # iterate over the generator
    for line in loglines:
        print(line)

with open(filename_vrmonitor,'r', encoding='utf-8') as f:
    lines = f.readlines()
for line in lines:
    
    line = line.split(' - ', 1)
    last_log_timeinfo = line[0]
    textinfo = line[1]
    dt = parse(line[0])

    # if "Status Alert" in line:
    #     print(line)
    # else:
    #     continue
f.close()

# from datetime import datetime
#
# datetime_str = '09/19/18 13:55:26'
#
# datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
#
# print(type(datetime_object))
# print(datetime_object)  # printed in default format
