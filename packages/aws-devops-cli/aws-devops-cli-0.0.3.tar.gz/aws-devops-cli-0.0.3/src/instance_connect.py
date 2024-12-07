import subprocess
import signal
import sys

from src.AWS_utils import *
import inquirer

def signal_handler(sig, frame):
    pass

def ec2_instance_connect():
    instances = list_ec2_instances()
    if len(instances) == 0:
        print('No instances found')
        return
    answers = inquirer.prompt([inquirer.List('instance',message="Select an instance",choices=instances)])
    instance = answers['instance'].split(' - ')[0]

    signal.signal(signal.SIGINT, signal_handler)
    subprocess.run(f"aws ssm start-session --target {instance}", shell=True)


def ecs_instance_connect():

    # Cluster
    clusters = list_ecs_clusters()
    if len(clusters) == 0:
        print('No clusters found')
        return
    answers = inquirer.prompt([inquirer.List('cluster',message="Select a cluster",choices=clusters)])
    cluster = answers['cluster']

    # Service
    services = list_cluster_services(cluster)
    if len(services) == 0:
        print('No services found')
        return
    answers = inquirer.prompt([inquirer.List('service',message="Select a service",choices=services)])
    service = answers['service']

    # Task
    tasks = list_service_tasks(cluster, service)
    if len(tasks) == 0:
        print('No tasks found')
        return
    answers = inquirer.prompt([inquirer.List('task',message="Select a task",choices=tasks)])
    task = answers['task']

    # Container
    container = list_task_container_instances(cluster, task)
    if len(container) == 0:
        print('No running container instances found')
        return
    answers = inquirer.prompt([inquirer.List('container',message="Select a container instance",choices=container)])
    container = answers['container']

    answers = inquirer.prompt([inquirer.Text("command", message="Enter the command to run (Default: bash)")])
    cmd = answers['command']
    if cmd == '':
        cmd = 'bash'

    signal.signal(signal.SIGINT, signal_handler)
    subprocess.run(f"aws ecs execute-command --cluster {cluster} --task {task} --container {container} --command '{cmd}' --interactive", shell=True)


def type_selector():
    questions = [
        inquirer.List('type',
                      message="What type of instance do you need?",
                      choices=['EC2', 'ECS'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['type']

def command():
    type = type_selector()
    if type == 'EC2':
        print('EC2 instance selected')
        ec2_instance_connect()
    elif type == 'ECS':
        print('ECS instance selected')
        ecs_instance_connect()
    else:
        print('Invalid selection')