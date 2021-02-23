import psutil

def check_computer_info():
    print("check cpu_times")
    print(psutil.cpu_times())
    print(psutil.cpu_percent())
    print(psutil.cpu_times_percent(interval=None, percpu=False))
    print(psutil.cpu_count(logical=True))
    print(psutil.cpu_stats())
    print(psutil.cpu_freq(percpu=False))
    print(psutil.getloadavg())
    print()
    print()

check_computer_info()