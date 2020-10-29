#!usr/bin/python3
"""
Name: Kaylee Bigelow
Date: October 3, 2020
This program ...
"""

import boto3
import csv
import paramiko
from scp import SCPClient


def readFiles():
    templates = []
    containers = []
    instances = []
    try:
        with open('template.csv', encoding='utf-8-sig') as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            for row in read:
                temp = {}
                temp['templateName'] = row[0]
                temp['ami'] = row[1]
                temp['instanceType'] = row[2]
                temp['size'] = row[3]
                temp['securityGroup'] = [row[4]]
                temp['zone'] = row[5]
                templates.append(temp)

        with open('container.csv', encoding='utf-8-sig') as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            for row in read:
                temp = {}
                temp['containerName'] = row[0]
                temp['container'] = row[1]
                temp['location'] = row[2]
                temp['script'] = row[3]
                containers.append(temp)

        with open('instances.csv', encoding='utf-8-sig') as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            for row in read:
                temp = {}
                temp['templateName'] = row[0]
                temp['instanceName'] = row[1]
                temp['sshKey'] = row[2]
                temp['containerName'] = row[3]
                instances.append(temp)

        return templates, containers, instances
    except Exception as e:
        print(e)


def getUserName(toParse):
    if len(toParse.split("\"")) > 1:
        return toParse.split("\"")[1]
    else:
        return 'root'


def getSystem(toParse):
    print(toParse.split("\""))
    if len(toParse.split("\"")) > 1:
        print("hi")
        return toParse.split("\"")[1]
    else:
        print("unable to determine system")
        return 'error'


def installDocker(client, system):
    print("here")
    if system == "Amazon Linux" or system == "Linux":
        stdin, stdout, stderr = client.exec_command(
            "sudo yum install docker -y", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "sudo service docker start", get_pty=True)
        print(stdout.read())
    elif system == "Ubuntu":
        stdin, stdout, stderr = client.exec_command(
            "sudo apt update -y", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "sudo apt install apt-transport-https ca-certificates curl software-properties-common -y", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable\"", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "sudo apt update -y", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "apt-cache policy docker-ce -y", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "sudo apt install docker-ce -y", get_pty=True)
        print(stdout.read())
        stdin, stdout, stderr = client.exec_command(
            "sudo systemctl status docker", get_pty=True)
        print(stdout.read())


def createInstances(templates, containers, instances):
    try:
        for data in instances:
            currTemplate = {}
            currContainers = []
            for find in templates:
                if find['templateName'] == data['templateName']:
                    currTemplate = find
            for find in containers:
                if find['containerName'] == data['containerName']:
                    currContainers.append(find)
            print("")
            print("instance = " + str(data))
            print("template = " + str(currTemplate))
            print("container = " + str(currContainers))
            ec2 = boto3.resource('ec2', currTemplate['zone'])
            # if(isinstance(currTemplate, int)):
            #     instances = ec2.create_instances(
            #         ImageId=currTemplate['ami'],
            #         MinCount=1,
            #         MaxCount=1,
            #         InstanceType=currTemplate['instanceType'],
            #         KeyName=data['sshKey'].split(".")[0],
            #         SecurityGroups=currTemplate['securityGroup'],
            #         TagSpecifications=[
            #             {
            #                 'ResourceType': 'instance',
            #                 'Tags': [
            #                     {
            #                         'Key': 'Name',
            #                         'Value': data['instanceName']
            #                     },
            #                 ]
            #             }],
            #         BlockDeviceMappings=[
            #             {
            #                 'DeviceName': '/dev/xvda',
            #                 'Ebs': {
            #                     'VolumeSize': int(currTemplate['size'])
            #                 }
            #             }]
            #     )
            # else:
            #     instances = ec2.create_instances(
            #         ImageId=currTemplate['ami'],
            #         MinCount=1,
            #         MaxCount=1,
            #         InstanceType=currTemplate['instanceType'],
            #         KeyName=data['sshKey'].split(".")[0],
            #         SecurityGroups=currTemplate['securityGroup'],
            #         TagSpecifications=[
            #             {
            #                 'ResourceType': 'instance',
            #                 'Tags': [
            #                     {
            #                         'Key': 'Name',
            #                         'Value': data['instanceName']
            #                     },
            #                 ]
            #             }]
            #     )
            # print("id = " + str(instances[0].id))
            # print(instances)
            # instances[0].wait_until_running()
            current_instance = list(ec2.instances.filter(
                InstanceIds=["i-038d410d47bc28024"]))
            ip_address = current_instance[0].public_ip_address
            print("ip = " + str(ip_address))
            print(str(current_instance[0].platform))
            key = paramiko.RSAKey.from_private_key_file(data['sshKey'])
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=ip_address, username="root", pkey=key)
            stdin, stdout, stderr = client.exec_command(
                "echo Connected", get_pty=True)
            userName = getUserName(str(stdout.read()))

            print(userName)
            client.connect(
                hostname=ip_address, username=userName, pkey=key)
            stdin, stdout, stderr = client.exec_command(
                "echo Connected", get_pty=True)
            print(stdout.read())
            stdin, stdout, stderr = client.exec_command(
                "cat /etc/os-release", get_pty=True)
            system = getSystem(str(stdout.read()))
            installDocker(client, system)

            # scpClient = SCPClient(client.get_transport())
            # for curr in currContainers:

            #     if curr['script']:
            #         # put script
            #         scpClient.put(curr['script'], curr['script'])
            #     # run script

            #         stdin, stdout, stderr = client.exec_command(
            #             "chmod +x "+curr['script'], get_pty=True)
            #         print(stdout.read())
            #         stdin, stdout, stderr = client.exec_command(
            #             "sudo ./"+curr['script'], get_pty=True)
            #         print(stdout.read())
            #         stdin, stdout, stderr = client.exec_command(
            #             "sudo docker images", get_pty=True)
            #         print(stdout.read())
            #         stdin, stdout, stderr = client.exec_command(
            #             "sudo docker ps", get_pty=True)
            #         print(stdout.read())
            #     else:
            #         stdin, stdout, stderr = client.exec_command(
            #             "sudo docker pull "+curr['container'], get_pty=True)
            #         print(stdout.read())
            client.close()

    except Exception as e:
        print(e)


def main():
    templates, containers, instances = readFiles()
    createInstances(templates, containers, instances)


if __name__ == "__main__":
    main()
