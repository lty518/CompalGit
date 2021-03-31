""" 
Parse output of nvidia-smi into a python dictionary.
This is very basic!
"""

import subprocess
import pprint
'''
{'Accounting Mode': 'Disabled',
 'Accounting Mode Buffer Size': '4000',     
 'Active Sessions': '0',
 'Applications Clocks Setting': 'Not Active',
 'Attached GPUs': '1',
 'Auto Boost': 'N/A',
 'Auto Boost Default': 'N/A',
 'Average FPS': '0',
 'Average Latency': '0',
 'Board ID': '0x100',
 'Bus': '0x01',
 'CUDA Version': '11.2',
 'Compute Mode': 'Default',
 'Compute instance ID': 'N/A',
 'Current': 'N/A',
 'DRAM Correctable': 'N/A',
 'DRAM Uncorrectable': 'N/A',
 'Decoder': '0 %',
 'Default Power Limit': 'N/A',
 'Device': '0x00',
 'Device Id': '0x219110DE',
 'Display Active': 'Enabled',
 'Display Clock Setting': 'Not Active',
 'Display Mode': 'Enabled',
 'Domain': '0x0000',
 'Double Bit ECC': 'N/A',
 'Driver Version': '461.40',
 'ECC Object': 'N/A',
 'Encoder': '0 %',
 'Enforced Power Limit': 'N/A',
 'Fan Speed': 'N/A',
 'Firmware': 'N/A',
 'Free': '27 MiB',
 'GPU Current Temp': '38 C',
 'GPU Max Operating Temp': '87 C',
 'GPU Part Number': 'N/A',
 'GPU Shutdown Temp': '100 C',
 'GPU Slowdown Temp': '95 C',
 'GPU Target Temperature': 'N/A',
 'GPU UUID': 'GPU-40e5bb06-e5b7-9055-ee68-02ab97550fb4',
 'GPU instance ID': 'N/A',
 'Gpu': '1 %',
 'Graphics': 'N/A',
 'HW Power Brake Slowdown': 'Not Active',
 'HW Slowdown': 'Not Active',
 'HW Thermal Slowdown': 'Not Active',
 'Host VGPU Mode': 'N/A',
 'Idle': 'Not Active',
 'Image Version': 'G001.0000.02.04',
 'Max': '16x',
 'Max Power Limit': 'N/A',
 'Memory': '6001 MHz',
 'Memory Current Temp': 'N/A',
 'Memory Max Operating Temp': 'N/A',
 'Min Power Limit': 'N/A',
 'Minor Number': 'N/A',
 'MultiGPU Board': 'No',
 'Name': 'Insufficient Permissions',
 'OEM Object': '1.1',
 'Pending': 'N/A',
 'Pending Page Blacklist': 'N/A',
 'Performance State': 'P8',
 'Persistence Mode': 'N/A',
 'Power Draw': '3.64 W',
 'Power Limit': 'N/A',
 'Power Management': 'N/A',
 'Power Management Object': 'N/A',
 'Process ID': '2068',
 'Product Brand': 'GeForce RTX',
 'Product Name': 'GeForce GTX 1660 Ti with Max-Q Design',
 'Relaxed Ordering Mode': 'N/A',
 'Remapped Rows': 'N/A',
 'Replay Number Rollovers': '0',
 'Replays Since Reset': '0',
 'Rx Throughput': '0 KB/s',
 'SM': '2100 MHz',
 'SRAM Correctable': 'N/A',
 'SRAM Uncorrectable': 'N/A',
 'SW Power Cap': 'Active',
 'SW Thermal Slowdown': 'Active',
 'Single Bit ECC': 'N/A',
 'Sub System Id': '0x8744103C',
 'Sync Boost': 'Not Active',
 'Total': '256 MiB',
 'Tx Throughput': '0 KB/s',
 'Type': 'C+G',
 'Used': '229 MiB',
 'Used GPU Memory': 'Not available in WDDM driver model',
 'VBIOS Version': '90.16.1F.00.1F',
 'Video': '1950 MHz',
 'Virtualization Mode': 'None'}
'''
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
parse_nvidia_smi()