# Experiment Controller #

# Run Anamoloy using stress-ng controller
# Execute Actions with scripts or stackstorm
# Return MTTRasdsa
# Run file as .py with params stressng, action and print out MTTR

import ansible.playbook as Playbook
import requests as r
import sys
import os
import sys
import json
import os
import time
import subprocess
from requests.auth import HTTPBasicAuth
import pandas as pd
import random
import string
import numpy as np
import math

# take token for st2 authentication

def get_token():
    token = os.system('sudo docker exec -it st2docker_stackstorm_1 st2 auth st2admin -p "sS+u4DLX" -t')
    return token

def get_token_ss():

    username='st2admin'
    password='sS+u4DLX'

    req = r.post('https://localhost/auth/v1/tokens', auth=HTTPBasicAuth(username, password),verify=False)
    time.sleep(30)
    a = req.text.split()
    return a[6][:-1]

def normal_state_qos():
    client_ip = "10.0.42.24"
    command1 =  f'rsync -chavzP --stats -e "ssh -i hani.pem"  ubuntu@{client_ip}:/opt/bitflow/client/client.bin /home/syed/Documents/Master_Thesis/'
    process1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
    process1.wait()

    command2 = "java -cp /home/syed/Documents/Master_Thesis/bitflow4j/target/bitflow4j.jar bitflow4j.script.Main -s '/home/syed/Documents/Master_Thesis/client.bin -> out.csv'"
    process2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
    process2.wait()

    c = pd.read_csv("out-0.csv")
    c1 = c.tail(5)

    bytes_s = c1['bytes/s'].mean()
    streams = c1['streams'][c1.index[-1]]
    qos = bytes_s / streams
    os.system("rm out-0.csv")
    return qos

def calc_impact(scenario):
    client_ip = "10.0.42.24"
    command1 =  f'rsync -chavzP --stats -e "ssh -i hani.pem"  ubuntu@{client_ip}:/opt/bitflow/client/client.bin /home/syed/Documents/Master_Thesis/'
    process1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
    process1.wait()

    command2 = "java -cp /home/syed/Documents/Master_Thesis/bitflow4j/target/bitflow4j.jar bitflow4j.script.Main -s '/home/syed/Documents/Master_Thesis/client.bin -> out.csv'"
    process2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
    process2.wait()

    #scenario = 0
    c = pd.read_csv(f"out-{scenario}.csv")
    c1 = c.tail(3)
    bytes_s = c1['bytes/s'].mean()
    streams = c1['streams'][c1.index[-1]]
    qos = bytes_s / streams
    os.system(f"rm out-{scenario}.csv")
    time.sleep(5)
    return qos

def impact_average(val):

    client_ip = "10.0.42.24"
    command1 =  f'rsync -chavzP --stats -e "ssh -i hani.pem"  ubuntu@{client_ip}:/opt/bitflow/client/client.bin /home/syed/Documents/Master_Thesis/'
    process1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
    process1.wait()

    command2 = "java -cp /home/syed/Documents/Master_Thesis/bitflow4j/target/bitflow4j.jar bitflow4j.script.Main -s '/home/syed/Documents/Master_Thesis/client.bin -> out.csv'"
    process2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
    process2.wait()

    #scenario = 0
    c = pd.read_csv(f"out-0.csv")
    c1 = c.tail(val)
    bytes_s = c1['bytes/s'].mean()
    streams = c1['streams'][c1.index[-1]]
    qos = bytes_s / streams
    os.system("rm out-0.csv")
    time.sleep(5)
    return qos

def impact_errors_percentage(val):

    client_ip = "10.0.42.24"
    command1 =  f'rsync -chavzP --stats -e "ssh -i hani.pem"  ubuntu@{client_ip}:/opt/bitflow/client/client.bin /home/syed/Documents/Master_Thesis/'
    process1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
    process1.wait()

    command2 = "java -cp /home/syed/Documents/Master_Thesis/bitflow4j/target/bitflow4j.jar bitflow4j.script.Main -s '/home/syed/Documents/Master_Thesis/client.bin -> out.csv'"
    process2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
    process2.wait()

    #scenario = 0
    c = pd.read_csv(f"out-0.csv")
    c1 = c.tail(val)
    bytes_s = c1['errors'].mean()
    streams = c1['opened'][c1.index[-1]]
    error_percentage = bytes_s / streams
    os.system("rm out-0.csv")
    time.sleep(5)
    return error_percentage

# token
# token = get_token_ss()

# Take in arguments: stressng action instance_id/name
if __name__ == "__main__":
    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3]

# 1. Run anamoloy using stress-ng controller
#curl -X POST --header 'asdasContent-Type: application/json' --header 'Accept: application/json' -d '{"parameter":"--cpu=2 --cpu-load=80"}' 0.0.0.0:7999/api/anomalies/stress_cpu/

param = ''
name = str(b)
ip = str(c)

# Open log file
f= open("results.csv","a+")

def get_ips():
    x = subprocess.Popen('openstack floating ip list',stdout=subprocess.PIPE,shell=True)
    time.sleep(5)
    out = str(x.communicate()[0])
    item = out.split('|\\n|')
    i = 0
    while(i< len(item)-1):

        if(item[i].split()[4]) == 'None':
            get_floating_ip = item[i].split()[2]
        i=i+1

    return get_floating_ip

def get_private_ip(name):
    x = subprocess.Popen(f'openstack server list --name {name}', stdout=subprocess.PIPE, shell=True)
    out = str(x.communicate()[0])
    item = out.split(',')
    i = 0
    return item[0][-9:]

def ping_server():
    start_time = time.time()
    final_time = 0
    while(final_time  < 60):
        hostname = "10.0.42.43"  # example
        response = os.system("ping -c 1 " + hostname)
        # and then check the response...
        if response == 0:
            print(hostname, 'is up!')
            break
        else:
            print(hostname, 'is down!')
            end_time = time.time()
            final_time = end_time - start_time
            print(start_time, end_time, final_time)

    #source os creds
    server_ip = subprocess.check_output(f"openstack server list --name {name}",shell=True)
    print(str(server_ip).split()[20])

def softreboot(normal_qos):
    qos1 = calc_impact(0)

    #token = get_token_ss()
    start_time = time.time()
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'name': name}
    req = r.post('https://localhost/api/v1/webhooks/serversoftreboot', data=json.dumps(payload), headers=headers,
                 verify=False)
    # take execution id of last command
    ex = ''
    while (ex != 'completed'):
        exectime = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex = str(exectime).split('has')[1].split()[0]

    action_status = str(exectime).split('status=')[1].split(')')[0]

    # get execution id
    exec_id = str(exectime).split('Execution')[1].split()[0]

    # exection action of actions with wait until complete

    ttt = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id, shell=True)
    action_exec_time = str(ttt).split('(')[1][0:3]

    getip_start = time.time()

    # source os creds
    #get_ip = subprocess.check_output(f"openstack server list --name {name}", shell=True)
    server_ip = ip

    getip_end = time.time()
    get_ip_time = getip_end - getip_start

    payload = {'ip': server_ip}
    ansible_req = r.post('https://localhost/api/v1/webhooks/vidserver', data=json.dumps(payload), headers=headers,
                         verify=False)

    # find execution time of ansible
    ex2 = ''
    while (ex2 != 'completed'):
        exectime2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                        shell=True)
        ex2 = str(exectime).split('has')[1].split()[0]

    exec_id2 = str(exectime2).split('RECAP')[1].split('failed=')[1].split()[5]
    ansible_action_status = str(exectime).split('status=')[1].split(')')[0]

    if ansible_action_status!="failed":
        ttt2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id2, shell=True)
        action_exec_time2 = str(ttt2).split('(')[1][0:3]
    else:
        action_exec_time2=0


    end_time = time.time()
    final_time = end_time - start_time

    val = math.ceil(final_time) + 300
    qos_average = impact_average(val)
    error_percentage = impact_errors_percentage(val)

    qos2 = calc_impact(0)
    qos_difference = qos2 - qos1
    return "\n" + "soft_reboot" + ","  + str(action_exec_time) +  "," + str(action_exec_time2) + "," + str(get_ip_time) +  "," + str(final_time) + "," + str(qos_difference) + "," + str(qos_average) + "," + str(error_percentage) + "," +  "Stop Server"  + "," + str(normal_qos) + "," + str(action_status)

def hardreboot(normal_qos):
    qos1 = calc_impact(0)
    # token = get_token_ss()
    start_time = time.time()
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'name':name}
    req=r.post('https://localhost/api/v1/webhooks/serverhardreboot',data=json.dumps(payload),headers=headers,verify=False)
    # take execution id of last command
    ex = ''
    while (ex != 'completed'):
        exectime = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                           shell=True)
        ex = str(exectime).split('has')[1].split()[0]

    action_status = str(exectime).split('status=')[1].split(')')[0]

    # get execution id
    exec_id = str(exectime).split('Execution')[1].split()[0]

    # exection action of actions with wait until complete

    ttt = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id, shell=True)
    action_exec_time = str(ttt).split('(')[1][0:3]

    getip_start = time.time()
    # source os creds
    get_ip = subprocess.check_output(f"openstack server list --name {name}", shell=True)
    server_ip = str(get_ip).split()[20]
    getip_end = time.time()
    get_ip_time = getip_end - getip_start

    payload = {'ip': server_ip}
    ansible_req = r.post('https://localhost/api/v1/webhooks/vidserver', data=json.dumps(payload), headers=headers,
                         verify=False)

    # find execution time of ansible
    ex2 = ''
    while (ex2 != 'completed'):
        exectime2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                        shell=True)
        ex2 = str(exectime).split('has')[1].split()[0]

    exec_id2 = str(exectime2).split('RECAP')[1].split('failed=')[1].split()[5]
    ansible_action_status = str(exectime).split('status=')[1].split(')')[0]

    if ansible_action_status!="failed":
        ttt2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id2, shell=True)
        action_exec_time2 = str(ttt2).split('(')[1][0:3]
    else:
        action_exec_time2=0

    end_time = time.time()
    final_time = end_time - start_time

    ##

    time.sleep(300)

    ##

    val = math.ceil(final_time) + 300
    qos_average = impact_average(val)
    error_percentage = impact_errors_percentage(val)
    qos2 = calc_impact(0)
    qos_difference = qos2 - qos1


    return "\n" + "hard_reboot" + "," + str(action_exec_time) + "," + str(action_exec_time2) + "," + str(get_ip_time) + "," + str(final_time) + "," + str(qos_difference) + "," + str(qos_average) + "," + str(error_percentage) + "," + "Stop Server" + "," + str(normal_qos) + "," + str(action_status)

def scale_up(normal_qos):
     qos1 = calc_impact(0)
    # # create a new vm
     start_time = time.time()

     def randomString(stringLength=5):
         letters = string.ascii_lowercase
         return ''.join(random.choice(letters) for i in range(stringLength))

     scaled_server_name = randomString(5)

     headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
     payload = {'server_name': scaled_server_name,'image_name':'video-server-video-1'}
     create_req = r.post('https://localhost/api/v1/webhooks/create', data=json.dumps(payload), headers=headers,
                  verify=False)

    # find execution time
     ex = ''
     while (ex != 'completed'):
            exectime = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                                shell=True)
            ex = str(exectime).split('has')[1].split()[0]

     exec_id = str(exectime).split('Execution')[1].split()[0]

     ttt = subprocess.check_output(
         'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id, shell=True)
     action_exec_time = str(ttt).split('(')[1][0:3]
     #assign floatin IP from available pool

     assign_start_time = time.time()
     floatng_ip = get_ips()
     payload = {'ip':floatng_ip,'server_name':scaled_server_name}
     assign_req = r.post('https://localhost/api/v1/webhooks/assign', data=json.dumps(payload), headers=headers,verify=False)
     assign_end_time = time.time()
     final_assign_time = assign_end_time - assign_start_time

    # find execution time

     ex1 = ''
     while (ex1 != 'completed'):
            exectime1 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                                shell=True)
            ex1 = str(exectime1).split('has')[1].split()[0]

     exec_id1 = str(exectime1).split('Execution')[1].split()[0]

     ttt1 = subprocess.check_output(
         'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id1, shell=True)
     action_exec_time1 = str(ttt1).split('(')[1][0:3]

    ### either SS or Ansible ###
    # start service
    # start injector

     get_ip = subprocess.check_output(f"openstack server list --name {scaled_server_name}", shell=True)
     server_ip = str(get_ip).split()[20]

     payload = {'ip': server_ip}
     ansible_req = r.post('https://localhost/api/v1/webhooks/vidserver', data=json.dumps(payload), headers=headers,
                        verify=False)
    # find execution time of ansible
     ex2 = ''
     while (ex2 != '0'):
        exectime2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                        shell=True)
        ex2 = str(exectime2).split('RECAP')[1].split('failed=')[1][0]

     exec_id2 = str(exectime2).split('RECAP')[1].split('failed=')[1].split()[5]

     ttt2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id2, shell=True)
     action_exec_time2 = str(ttt2).split('(')[1][0:3]

     # add to load balancer
     load_balancer_ip = '10.0.42.76'
     addtoconfig = f"ssh -o StrictHostKeychecking=no -tt -i hani.pem ubuntu@{load_balancer_ip} 'sudo docker exec -ti rtmp-balancer sh -c \"echo server {server_ip} {server_ip}:1935 check >> /usr/local/etc/haproxy/haproxy.cfg\"'"
     process = subprocess.Popen(addtoconfig, shell=True, stdout=subprocess.PIPE)
     process.wait()
     restartservice = f"ssh -o StrictHostKeychecking=no -tt -i hani.pem ubuntu@{load_balancer_ip} 'sudo docker kill -s HUP rtmp-balancer'"
     process = subprocess.Popen(restartservice, shell=True, stdout=subprocess.PIPE)
     process.wait()


     end_time = time.time()
     final_time = end_time - start_time

     ##

     time.sleep(300)

     ##

     val = math.ceil(final_time) + 300
     qos_average = impact_average(val)
     error_percentage = impact_errors_percentage(val)
     qos2 = calc_impact(0)
     qos_difference = qos2 - qos1

     return '\nScale Up' + ","  + str(final_time) + ","  +  str(action_exec_time) + "," + str(action_exec_time1) + "," + str(action_exec_time2) + "," + str(final_assign_time) + "," + str(qos_difference) + "," + str(qos_average) + "," + str(error_percentage) + "," + "Stop Server" + "," + str(normal_qos)

def migrate(normal_qos):
    qos1 = calc_impact(0)
    #token = get_token_ss()
    start_time =  time.time()

    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'volume': name}
    create_snapshot = r.post('https://localhost/api/v1/webhooks/createimageforsnapshot', data=json.dumps(payload), headers=headers,
                        verify=False)

    ex = ''
    while (ex != 'completed'):
        exectime = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex = str(exectime).split('has')[1].split()[0]

    exec_id = str(exectime).split('Execution')[1].split()[0]

    ttt = subprocess.check_output(
        'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id, shell=True)
    snapshot_create_time = str(ttt).split('(')[1][0:3]

    new_name = 'mig_vm'
    payload2 = {'name':new_name,'image':'video-server-video-1'}
    createinstancefromsnapshot = r.post('https://localhost/api/v1/webhooks/createinstancefromsnapshot', data=json.dumps(payload2), headers=headers,
                        verify=False)

    ex1 = ''
    while (ex1 != 'completed'):
        exectime1 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex1 = str(exectime1).split('has')[1].split()[0]

    exec_id1 = str(exectime1).split('Execution')[1].split()[0]

    ttt1 = subprocess.check_output(
        'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id1, shell=True)
    create_vm_from_snapshot_time = str(ttt1).split('(')[1][0:3]

    # assign floatin IP from available pool

    floatng_ip = get_ips()
    payload = {'ip': floatng_ip, 'server_name': new_name}
    assign_req = r.post('https://localhost/api/v1/webhooks/assign', data=json.dumps(payload), headers=headers,
                        verify=False)

    # find execution time

    ex2 = ''
    while (ex2 != 'completed'):
        exectime2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex2 = str(exectime2).split('has')[1].split()[0]

    exec_id2 = str(exectime2).split('Execution')[1].split()[0]

    ttt2 = subprocess.check_output(
        'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id2, shell=True)
    assign_ip_time = str(ttt2).split('(')[1][0:3]

    ### either SS or Ansible ###
    # start service
    # start injector

    #get_ip = subprocess.check_output(f"openstack server list --name {new_name}", shell=True)
    #server_ip = str(get_ip).split()[20]

    payload = {'ip': ip}
    ansible_req = r.post('https://localhost/api/v1/webhooks/vidserver', data=json.dumps(payload), headers=headers,
                         verify=False)
    #
    ex3 = ''
    while (ex3 != '0'):
        exectime2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex3 = str(exectime2).split('RECAP')[1].split('failed=')[1][0]

    exec_id3 = str(exectime2).split('RECAP')[1].split('failed=')[1].split()[5]

    ttt3 = subprocess.check_output(
        'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id2, shell=True)
    ansbile_playbook_exec_time = str(ttt3).split('(')[1][0:3]

    # add to load balancer

    load_bal_start_time = time.time()

    public_ip= floatng_ip
    #private_ip = '10.0.0.5'
    load_balancer_ip='10.0.42.76'

    # add to load balancer
    addtoconfig = f"ssh -o StrictHostKeychecking=no -tt -i hani.pem ubuntu@{load_balancer_ip} 'sudo docker exec -ti rtmp-balancer sh -c \"echo server {public_ip} {public_ip}:1935 check >> /usr/local/etc/haproxy/haproxy.cfg\"'"
    process = subprocess.Popen(addtoconfig, shell=True, stdout=subprocess.PIPE)
    process.wait()
    restartservice = f"ssh -o StrictHostKeychecking=no -tt -i hani.pem ubuntu@{load_balancer_ip} 'sudo docker kill -s HUP rtmp-balancer'"
    process = subprocess.Popen(restartservice, shell=True, stdout=subprocess.PIPE)
    process.wait()

    load_bal_end_time = time.time()
    load_bal_add_total_time = load_bal_end_time - load_bal_start_time

    end_time = time.time()
    final_time = end_time - start_time

    ##

    time.sleep(300)

    ##

    val = math.ceil(final_time) + 300
    qos_average = impact_average(val)
    error_percentage = impact_errors_percentage(val)
    qos2 = calc_impact(0)
    qos_difference = qos2 - qos1

    return '\nMigrate' + "," + str(final_time) +","  + \
            "," + str(create_vm_from_snapshot_time) + "," + str(assign_ip_time) \
           + "," + str(ansbile_playbook_exec_time) + "," + str(load_bal_add_total_time) + "," + str(qos_difference) + "," + str(qos_average) + "," + str(error_percentage) + "," + "Stop Server" + "," + str(normal_qos)

def restartservice(normal_qos):

    qos1 = calc_impact(0)
    start_time = time.time()
    print("1")

    os.system(f"ssh -o StrictHostKeychecking=no -tt -i hani.pem ubuntu@{ip} \"sudo docker container restart rtmp-server\"")
    #process = subprocess.Popen(restartservice, shell=True, stdout=subprocess.PIPE)
    #process.wait()

    print("2")
    end_time = time.time()
    final_time = end_time - start_time

    ##

    time.sleep(5)

    ##
    print("3")
    val = math.ceil(final_time)
    qos_average = impact_average(val)
    error_percentage = impact_errors_percentage(val)
    qos2 = calc_impact(0)
    qos_difference = qos2 - qos1

    return '\nRestart_Service' + ","  + str(final_time) +  "," + str(qos_difference) + "," + str(qos_average) + "," + str(error_percentage) + "," + "Stop Server" + "," + str(normal_qos) + "," + "failed"

def resize(normal_qos):

    qos1 = calc_impact(0)
    start_time = time.time()
    #token = get_token_ss()
    flavor = 'm1.large'

    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'name': name,'size':flavor}
    server_resize = r.post('https://localhost/api/v1/webhooks/serverresize', data=json.dumps(payload),
                             headers=headers,
                             verify=False)

    # find execution time

    ex = ''
    while (ex != 'completed'):
        exectime = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex = str(exectime).split('has')[1].split()[0]

    exec_id = str(exectime).split('Execution')[1].split()[0]

    ttt = subprocess.check_output(
        'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id, shell=True)
    server_resize_time = str(ttt).split('(')[1][0:3]

    # server resize completer

    payload = {'name': name}
    server_resize_confirm = r.post('https://localhost/api/v1/webhooks/serverresizeconfirm', data=json.dumps(payload),
                           headers=headers,
                           verify=False)

    # find execution time

    ex1 = ''
    while (ex1 != 'completed'):
        exectime1 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                           shell=True)
        ex1 = str(exectime1).split('has')[1].split()[0]

    exec_id1 = str(exectime1).split('Execution')[1].split()[0]

    ttt1 = subprocess.check_output(
        'sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id1, shell=True)
    server_resize_confirm_time = str(ttt1).split('(')[1][0:3]

    # restart docker services

    payload = {'ip': ip}
    ansible_req = r.post('https://localhost/api/v1/webhooks/vidserver', data=json.dumps(payload), headers=headers,
                         verify=False)
    ex2 = ''
    while (ex2 != '0'):
        exectime2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex2 = str(exectime2).split('RECAP')[1].split('failed=')[1][0]

    exec_id2 = str(exectime2).split('RECAP')[1].split('failed=')[1].split()[5]

    ansible_action_status = str(exectime2).split('status=')[1].split(')')[0]

    if ansible_action_status!="failed":
        ttt2 = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution get ' + exec_id2, shell=True)
        ansbile_playbook_exec_time = str(ttt2).split('(')[1][0:3]
    else:
        ansbile_playbook_exec_time=0

    end_time = time.time()
    total_time = end_time - start_time


    ##

    time.sleep(300)

    ##

    val = math.ceil(total_time) + 300
    qos_average = impact_average(val)
    error_percentage = impact_errors_percentage(val)
    qos2 = calc_impact(0)
    qos_difference = qos2 - qos1

    return '\nServer_resize' + "," + str(server_resize_time) + "," + str(server_resize_confirm_time) +  "," + str(total_time) + "," + str(ansbile_playbook_exec_time) + "," + str(qos_difference) + "," + str(qos_average) + "," + str(error_percentage) + "," + "Stop Server" + "," + str(normal_qos)


def private_ip():
    get_ip = subprocess.check_output(f"openstack server list --name deployment", shell=True)
    return str(get_ip).split('=')[1].split(',')[0]

def startVidService():
    #token = get_token_ss()
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'ip': ip}
    ansible_req = r.post('https://localhost/api/v1/webhooks/vidserver', data=json.dumps(payload), headers=headers,verify=False)

def ansibleclient():
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'ip': ip}
    ansible_req = r.post('https://localhost/api/v1/webhooks/ansibleclient', data=json.dumps(payload), headers=headers,
                         verify=False)

def softreboot_2():
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'name': name}
    req = r.post('https://localhost/api/v1/webhooks/serversoftreboot', data=json.dumps(payload), headers=headers,
                 verify=False)

def hardreboot_2():
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'name': name}
    req = r.post('https://localhost/api/v1/webhooks/serverhardreboot', data=json.dumps(payload), headers=headers,
                 verify=False)

def stressCPU(ip):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    payload = {"parameter":"--cpu=2 --cpu-load=80"}
    req = r.post(f"http://{ip}:7999/api/anomalies/stress_cpu/", data=json.dumps(payload), headers=headers)
    print(req.text)

def stopStressCPU(ip):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    req = r.delete(f"http://{ip}:7999/api/anomalies/stress_cpu/", headers=headers)
    print(req.text)

def addtobalancer():
    ip = "10.0.42.17"
    os.system("ssh -tt -i hani.pem ubuntu@10.0.42.76 'sudo docker exec -ti rtmp-balancer sh -c \"echo server 10.0.42.17 10.0.42.17:1935 check >> /usr/local/etc/haproxy/haproxy.cfg\"'")
    os.system("ssh -tt -i hani.pem ubuntu@10.0.42.76 'sudo docker kill -s HUP rtmp-balancer'")

def stop_server_anamoly():
    headers = {'Content-type': 'application/json', 'Accept': 'application/json',
               'X-Auth-Token': 'a55c79caa22d4395a9dc70d3f0799abd'}
    payload = {'ip': name}
    stop_server_anamoly = r.post('https://localhost/api/v1/webhooks/stopserver', data=json.dumps(payload), headers=headers,
                         verify=False)

    ## find executon time

    ex = ''
    while (ex != 'completed'):
        exectime = subprocess.check_output('sudo docker exec -it st2docker_stackstorm_1 st2 execution tail last',
                                            shell=True)
        ex = str(exectime).split('has')[1].split()[0]

    ex = str(exectime).split('status=')[1].split(')')[0]
    if ex == 'failed':
        return "Server restart failed"
    else:
        return "Server restarted"


if a == '0':
   ping_server()
if a == '1':
   param = hardreboot()
if a == '2':
   param = softreboot()
if a == '3':
   param = restartservice(b) # to do
if a == '4':
    param = scale_up()
if a == '5':
    param = resize(b) # to do
if a == '6':
    param = migrate() # to do
if a == '9':
    print(get_token())
if a=='10':
    print(get_private_ip('deployment'))
    #print(get_ips())
if a=='11':
    print(get_token_ss())
if a=='12':
    print(get_ips())
if a=='13':
    print(private_ip())
if a=='14':
    #os.system('sudo docker exec -it st2docker_stackstorm_1 \"ssh-keygen -f \"/root/.ssh/known_hosts\" -R \"10.0.42.57\"\"')
    startVidService()
if a == '15':
    print(calc_impact(2))
if a == '16':
    stressCPU(ip)
    stopStressCPU(ip)
if a == '17':
    addtobalancer()
if a == '18':
    stop_server_anamoly()
if a == '19':
    print(impact_average(10))
    os.system("rm out-0.csv")
    time.sleep(10)
    print(impact_errors_percentage(10))
    os.system("rm out-0.csv")
if a == '20':
   hardreboot_2()
if a == '21':
    ansibleclient()


# Stress CPU - soft reboot
if a == 's1-1':
    stressCPU(ip)
    time.sleep(60)
    param = softreboot('CPU_Stress')
    os.system("rm out-0.csv")
    os.system("rm out-1.csv")

# Stress CPU - hard reboot
if a == 's1-2':
    stressCPU(ip)
    time.sleep(60)
    param = hardreboot('CPU_Stress')
    os.system("rm out-0.csv")
    os.system("rm out-1.csv")

# Stress CPU - resize
if a == 's1-3':
    #os.system("ssh-keygen -f \"/root/.ssh/known_hosts\" -R \"10.0.42.57\"")
    stressCPU(ip)
    time.sleep(60)
    param = resize('CPU_Stress')
    os.system("rm out-0.csv")
    os.system("rm out-1.csv")

# Stress CPU - restart service
if a == 's1-4':
    stressCPU(ip)
    time.sleep(5)
    os.system("ssh-keygen -f \"/root/.ssh/known_hosts\" -R \"10.0.42.57\"")
    param = restartservice('CPU_Stress')
    os.system("rm out-0.csv")
    os.system("rm out-1.csv")


# Stress CPU - scale up
if a == 's1-5':
    stopStressCPU(ip)
    stressCPU(ip)
    time.sleep(60)
    os.system("ssh-keygen -f \"/root/.ssh/known_hosts\" -R \"10.0.42.36\"")
    param = scale_up('CPU_Stress')
    os.system("rm out-0.csv")
    os.system("rm out-1.csv")

# Stress CPU - migrate
if a == 's1-6':
    stopStressCPU(ip)
    stressCPU(ip)
    time.sleep(60)
    os.system("ssh-keygen -f \"/root/.ssh/known_hosts\" -R \"10.0.42.36\"")
    param = migrate('CPU_Stress')
    os.system("rm out-0.csv")
    os.system("rm out-1.csv")

if a == 's2-1':
    normal_qos = normal_state_qos()
    stop_server_anamoly()

    # wait 5 mins for videos to complete and go for new streaming
    # time.sleep(300)

    param = softreboot(normal_qos)

if a == 's2-2':
    normal_qos = normal_state_qos()
    stop_server_anamoly()

    # wait 5 mins for videos to complete and go for new streaming
    # time.sleep(300)

    param = hardreboot(normal_qos)


if a == 's2-3':
    normal_qos = normal_state_qos()
    stop_server_anamoly()

    # wait 5 mins for videos to complete and go for new streaming
    # time.sleep(300)

    param = scale_up(normal_qos)


if a == 's2-4':
    normal_qos = normal_state_qos()
    stop_server_anamoly()

    # wait 5 mins for videos to complete and go for new streaming
    # time.sleep(300)

    param = migrate(normal_qos)

if a == 's2-5':
    normal_qos = normal_state_qos()
    stop_server_anamoly()
    time.sleep(15)
    # wait 5 mins for videos to complete and go for new streaming
    # time.sleep(300)
    param = resize(normal_qos)

if a == 's2-5':
    normal_qos = normal_state_qos()
    stop_server_anamoly()
    time.sleep(15)
    # wait 5 mins for videos to complete and go for new streaming
    # time.sleep(300)
    param = resize(normal_qos)

if a == 's2-6':
    #normal_qos = normal_state_qos()
    #stop_server_anamoly()
    #time.sleep(5)
    # wait 5 mins for videos to complete and go for new streaming
    # time.sleep(300)
    param = restartservice(0)

#print(stop_server_anamoly())
# write results to a file

f.write(param)
f.close()

# 4. Return MTTR
#print("MTTR is :" + param)
#print("MTTR is :" + param)
