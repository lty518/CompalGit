#read a txt file
vrmonitor_path = 'C:/Program Files (x86)/Steam/logs/vrmonitor.txt'
for line in open(vrmonitor_path,'r', encoding='utf-8'):
    if "Status Alert" in line:
        print(line)
    else:
        continue
# with open('C:/Program Files (x86)/Steam/logs/vrmonitor.txt','r', encoding='utf-8') as f:
#     lines = f.readlines()
# for line in lines:
#     if "Status Alert" in line:
#         print(line)
#     else:
#         continue
# f.close()
