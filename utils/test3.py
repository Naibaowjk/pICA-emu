import psutil
import random

def my_func():
    # 在函数开始时获取当前进程的 CPU 使用率和内存占用情况
    process = psutil.Process()
    cpu_percent_start = process.cpu_percent()
    mem_info_start = process.memory_info()

    # 执行函数的操作
    num_of_randoms = 10000
    random_numbers = [random.randint(1, 100) for _ in range(num_of_randoms)]

    # 对随机数进行排序
    sorted_numbers = sorted(random_numbers)

    # 在函数结束时获取当前进程的 CPU 使用率和内存占用情况
    cpu_percent_end = process.cpu_percent()
    mem_info_end = process.memory_info()

    # 计算 CPU 使用率和内存占用的差值
    cpu_count = psutil.cpu_count()
    cpu_times = process.cpu_times()
    cpu_core_used = cpu_percent_end / 100 * cpu_count * max(cpu_times) / psutil.cpu_freq().current
    cpu_percent_diff = cpu_percent_end - cpu_percent_start
    mem_diff = mem_info_end.rss - mem_info_start.rss
    print(f"CPU core used: {cpu_count}")
    print(f"CPU 使用率变化: {cpu_percent_diff}%")
    print(f"内存占用变化: {mem_diff} bytes")

my_func()