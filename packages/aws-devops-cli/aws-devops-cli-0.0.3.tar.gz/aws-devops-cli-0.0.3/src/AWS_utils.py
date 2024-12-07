import boto3

ecs_client = boto3.client('ecs')
ec2 = boto3.resource('ec2')

def get_name_tag(tags):
    for tag in tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return 'No Name Tag'

def list_ec2_instances():
    res = []
    for instance in ec2.instances.all():
        if instance.state['Name'] == 'running':
            res.append(f"{instance.id} - {get_name_tag(instance.tags)}")
    return res


def list_ecs_clusters():
    res = []
    response = ecs_client.list_clusters()
    for cluster in response['clusterArns']:
        res.append(cluster)
    if 'nextToken' in response:
        while 'nextToken' in response:
            response = ecs_client.list_clusters(nextToken=response['nextToken'])
            for cluster in response['clusterArns']:
                res.append(cluster)

    for i in range(len(res)):
        res[i] = res[i].split('/')[-1]
    return res

def list_cluster_services(cluster):
    res = []
    response = ecs_client.list_services(cluster=cluster)
    for service in response['serviceArns']:
        res.append(service)
    if 'nextToken' in response:
        while 'nextToken' in response:
            response = ecs_client.list_services(cluster=cluster, nextToken=response['nextToken'])
            for service in response['serviceArns']:
                res.append(service)

    for i in range(len(res)):
        res[i] = res[i].split('/')[-1]
    return res

def list_service_tasks(cluster, service):
    res = []
    response = ecs_client.list_tasks(cluster=cluster, serviceName=service)
    for task in response['taskArns']:
        res.append(task)
    if 'nextToken' in response:
        while 'nextToken' in response:
            response = ecs_client.list_tasks(cluster=cluster, serviceName=service, nextToken=response['nextToken'])
            for task in response['taskArns']:
                res.append(task)

    for i in range(len(res)):
        res[i] = res[i].split('/')[-1]
    return res

def list_task_container_instances(cluster, task):
    res = []
    response = ecs_client.describe_tasks(cluster=cluster, tasks=[task])
    for container_instance in response['tasks'][0]['containers']:
        if container_instance["lastStatus"] == "RUNNING":
            res.append(container_instance["name"])
    return res