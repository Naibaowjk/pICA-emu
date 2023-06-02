# this file is to process the measurement data of PICA
"""
input: measurement/results_v4/nodes/..._cf.csv
output: new job file (.csv, e.g.), job_id | task_id | start_time | duration | cpu | storage
"""

import csv
import pandas as pd
import numpy as np
import pprint


def extract_measurement(configuration_name, node_):
    if node_ == 'client' or node_ == 'server':
        measure_data_file = configuration_name + node_ + '_cf.csv'

    else:
        measure_data_file = configuration_name + 'vnf' + str(node_) + '-s' + str(node_) + '_cf.csv'

    df_node = pd.read_csv(measure_data_file, header=None)

    if node_ == 'server':
        duration = df_node.iloc[i_time, 5]
        start_time = df_node.iloc[i_time, 1]
    else:
        duration = df_node.iloc[i_time, 7]
        start_time = df_node.iloc[i_time, 3]

    return duration, start_time


def client_server(job_nr, configuration_name):
    # todo: may change according to setup, i.e., if both will process or just one of them
    task_client = str(job_nr) + '_client'
    task_server = str(job_nr) + '_server'
    duration_client, start_time_client = extract_measurement(configuration_name, 'client')
    duration_server, start_time_server = extract_measurement(configuration_name, 'server')
    task_id_list.append(task_client)
    task_id_list.append(task_server)

    list_row = [job_nr, task_client, start_time_client, duration_client, None, None]
    new_job_pd.loc[len(new_job_pd)] = list_row

    list_row = [job_nr, task_server, start_time_server, duration_server, None, None]
    new_job_pd.loc[len(new_job_pd)] = list_row


number_test = 50

number_node = list(range(9))

number_job = len(number_node) * number_test

new_job_pd = pd.DataFrame(columns=["job_id", "task_id", "start_time", "duration", "cpu", "storage"])

job_nr = 0
task_id_list = []
path = '/home/zjj/comnets/codes/pica/pICA-emu/measurement/results_v4/'
for node in number_node:
    configuration_name = path + str(node) + 's/'
    task_nr = 0
    for i_time in range(number_test):
        job_nr += 1
        if node == 0:  # i.e., no intermediate node, only client + server
            client_server(job_nr, configuration_name)

        else:
            # even with intermediate nodes, client + server still exist

            client_server(job_nr, configuration_name)
            for i_node in range(node):
                # still need to append the server

                task_id = str(job_nr) + '_' + str(i_node)
                task_id_list.append(task_id)

                measure_data_file = configuration_name + 'vnf' + str(i_node) + '-s' + str(i_node) + '_cf.csv'
                df = pd.read_csv(measure_data_file, header=None)

                duration = df.iloc[i_time, 7]
                start_time = df.iloc[i_time, 3]
                list_row = [job_nr, task_id, start_time, duration, None, None]
                new_job_pd.loc[len(new_job_pd)] = list_row


# pprint.pprint(new_job_pd)

min_start_time = new_job_pd['start_time'].min()
new_job_pd['start_time'] -= min_start_time
new_job_pd.to_csv('new_job.csv')
