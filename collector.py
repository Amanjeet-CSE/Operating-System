import psutil
import time
import json
import operator

while True:
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)

    # Per-process info
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'cpu_times']):
        try:
            info = proc.info
            info['memory_used'] = round(info['memory_info'].rss / (1024 * 1024), 2)
            info['cpu_time'] = round(info['cpu_times'].user + info['cpu_times'].system, 2)  # total CPU time in seconds
            del info['memory_info']
            del info['cpu_times']
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_processes = sorted(processes, key=operator.itemgetter('cpu_percent'), reverse=True)[:5]

    # System-wide CPU time breakdown
    cpu_times = psutil.cpu_times()
    cpu_breakdown = {
        "user": round(cpu_times.user, 2),
        "system": round(cpu_times.system, 2),
        "idle": round(cpu_times.idle, 2)
    }

    data = {
        "cpu_usage": cpu,
        "memory_used": round(mem.used / (1024 * 1024), 2),
        "memory_total": round(mem.total / (1024 * 1024), 2),
        "cpu_time_breakdown": cpu_breakdown,
        "processes": top_processes
    }

    with open("data.json", "w") as f:
        json.dump(data, f)

    time.sleep(1)
