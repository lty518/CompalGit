import time
import psutil
import GPUtil
import pprint
import subprocess
def memory():
    info = psutil.virtual_memory()
    return info[2]
def disk(): # 獲取磁碟使用情況
    info = psutil.disk_usage('/')
    return info[-1]#, info[-2]
def cpu(): # 獲取CPU使用率
    info = psutil.cpu_percent(1)
    return info
def gpu():
    return GPUtil.showUtilization()

def check_vm_information():
    print("check vm system information")
    print(psutil.cpu_times(percpu=False))
    # for x in range(10):
    #     print('cpu percent: {}'.format(psutil.cpu_percent(interval=0.3)))
    mem = psutil.virtual_memory()
    print("virtual_memory: ", mem)
    print("disk_io_counters: ",psutil.disk_io_counters())
    print("disk_usage: ",psutil.disk_usage)
    # print("disk_partitions: ",psutil.disk_partitions())
    print("net_io_counters: ",psutil.net_io_counters())
    # print()
    # print(psutil.pids()) # 系統所有正在執行的程序PID

def check_single_process(input_pid):
    p = psutil.Process(input_pid)
    print(p.name())  # 程序名
    print(p.status())  # 程序狀態
    print(p.cpu_times())  # 程序的cpu時間資訊,包括user,system兩個cpu資訊
    # print(p.cpu_affinity())  # get程序cpu親和度,如果要設定cpu親和度,將cpu號作為參考就好
    print("記憶體利用率",p.memory_percent())  # 程序記憶體利用率
    print("記憶體rss,vms資訊",p.memory_info())  # 程序記憶體rss,vms資訊
    print("IO資訊",p.io_counters())  # 程序的IO資訊,包括讀寫IO數字及引數

def getProcessInfo(p): 
    #"""取出指定程序佔用的程序名，程序ID，程序實際記憶體, 虛擬記憶體,CPU使用率"""
    try:
        cpu = int(p.cpu_percent(interval=0)) 
        rss, vms = p.get_memory_info() 
        name = p.name 
        pid = p.pid 
    except psutil.error.NoSuchProcess as e:
        name = "Closed_Process"
        pid = 0
        rss = 0
        vms = 0
        cpu = 0
    return [name.upper(), pid, rss, vms, cpu]
def getAllProcessInfo():
    #"""取出全部程序的程序名，程序ID，程序實際記憶體, 虛擬記憶體,CPU使用率"""
    instances = []
    all_processes = list(psutil.process_iter() )
    for proc in all_processes: 
        proc.cpu_percent(interval=0) 
        #此處sleep1秒是取正確取出CPU使用率的重點
        time.sleep(1) 
    for proc in all_processes: 
        print(getProcessInfo(proc))
        instances.append(getProcessInfo(proc))
    return instances

def parse_nvidia_smi():
    sp = subprocess.Popen(['nvidia-smi', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out_str = sp.communicate()
    out_list = out_str[0].decode("utf-8").split('\n')

    out_dict = {}

    for item in out_list:
        try:
            key, val = item.split(':')
            key, val = key.strip(), val.strip()
            out_dict[key] = val
        except:
            pass
    return out_dict
    # pprint.pprint(out_dict)
# check_vm_information()
# print(getAllProcessInfo())
# print(memory())
# print(cpu())
# print(disk())
# GPUtil.showUtilization()
# check_single_process(23652)
