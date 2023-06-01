import psutil
import time
import subprocess
import asyncio

cpu_percent_list = []
memory_percent_list = []

async def task1():
    command = 'python3 test1.py'
    process = await asyncio.create_subprocess_shell(command)
    await process.wait()

async def main():
  
    # 每隔 0.1 秒获取一次 CPU 和内存使用情况，并将数据保存到列表中
    while True:
        cpu_percent_list.append(psutil.cpu_percent(interval=0.1, percpu=False))
        memory_percent_list.append(psutil.virtual_memory())
        time.sleep(0.1)
        task = asyncio.create_task(task1())
        await asyncio.wait([task])
            # 将 CPU 和内存使用情况保存到文件中
        with open('cpu_memory_usage.txt', 'w') as f:
            for cpu_percent, memory_percent in zip(cpu_percent_list, memory_percent_list):
                f.write(f"{cpu_percent},{memory_percent}\n")


asyncio.run(main())

