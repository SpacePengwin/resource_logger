from nis import cat
from re import sub
import subprocess
from unicodedata import decimal
from pprint import pprint
# get mem in MB: free -t -m
# get CPU avg across all cores: top -bn2 | grep '%Cpu' | tail -1 | grep -P '(....|...) id,'|awk '{print "CPU Usage: " 100-$8 "%"}'
# Get battery percentage: acpi -b

def get_cpu_usage():
    output = {}
    cpu_usage = subprocess.check_output(["mpstat"]).decode().splitlines()
    headers = cpu_usage[2].split(" ")
    values = cpu_usage[3].split(" ")
    headers = [header for header in headers if header != ""]
    values = [value for value in values if value != ""]
    for (category, value) in zip(headers, values):
        if "%" in category:
            output.update({category: float(value)})
    total_cpu_used = 100.00 - output["%idle"]
    total_cpu_used = float("{: .2f}".format(total_cpu_used).strip())
    output.update({"%total_used": total_cpu_used})
    return output

def get_mem_stats():
    mem_free = subprocess.check_output(["free", "-t", "-m"]).decode("utf-8").split("\n")[-2]
    mem_free = [mem for mem in mem_free.split(" ") if mem != ""]
    _header, total, used, free = mem_free
    return {"total": total, "used": used, "free": free}

def get_battery_percentage():
    battery_percentage = subprocess.check_output(["acpi"]).decode().split(",")[1].strip().replace("%", "") 
    return {"battery_percentage": battery_percentage}
    

def main():
    mem = get_mem_stats()
    bat = get_battery_percentage()
    pprint(mem)
    pprint(bat)

main()