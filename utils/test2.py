import docker
import time
import atexit

def write_result():
    with open('profile.csv', 'a') as f:
        for i in range(len_c):
            if  i == len_c-2: 
                f.write('container,client,')
            elif i == len_c-1:
                f.write('container,server,')
            else:
                f.write('container,{}'.format(len_c - 3 - i))
            f.write('cpu_usage,{},'.format(max(cpu_percentages[i])))
            f.write('mem_usage,{}\n').format(max(memory_usages[i]))


client = docker.from_env()
container_ids = client.containers.list(filters={'ancestor': 'pica_dev:5'})
len_c = len(container_ids)
len_profiler = 10
print(f"***current pICA container: {container_ids}")
cpu_percentages = []
memory_usages = []
for i in range(len_c):
    cpu_percentages.append([])
    memory_usages.append([])
while True:
    for i in range(len_c):
        container = container_ids[i]
        stats = container.stats(stream=False)
        cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
        memory_usage = stats['memory_stats']['usage'] / 1024 / 1024
        cpu_percentages[i].append(cpu_percent)
        memory_usages[i].append(memory_usage)
        print(f"*** container_id : {container_ids[i]}, cpu_percent : %{cpu_percent}, memory_usage = {memory_usage}MB")
    time.sleep(0.1)
