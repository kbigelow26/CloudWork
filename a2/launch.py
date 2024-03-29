#!usr/bin/python3
"""
Name: Kaylee Bigelow
Date: November 1, 2020
This program takes template files and uses them to build ec2 instances
"""

import boto3
import csv
import paramiko
import time
from scp import SCPClient
import os


def readFiles():
    """
    This function reads in the template files and stores them in a usuable format
    """
    templates = []
    containers = []
    instances = []
    try:
        print("Reading in files...")
        # reads and stores template information
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

        # reads and stores container information
        with open('container.csv', encoding='utf-8-sig') as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            for row in read:
                temp = {}
                temp['containerName'] = row[0]
                temp['container'] = row[1]
                temp['location'] = row[2]
                temp['script'] = row[3]
                containers.append(temp)

        # reads and stores instance information
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
        print('Unable to load in config files')
        return "error", "error", "error"


def getUserName(toParse):
    """
    This function finds the username in a given string
    req: toParse - the string in which the username exists
    """
    try:
        if len(toParse.split("\"")) > 1:
            return toParse.split("\"")[1]
        else:
            return 'root'
    except Exception as e:
        print(e)


def connectToSSH(client, ip_address, key):
    """
    This function finds the username in a given string
    req: client - the shh client
         ip_address - the ip address of the instance
         key - the key pair used in the instance
    """
    try:
        # trys to connect as root to get error message
        client.connect(
            hostname=ip_address, username="root", pkey=key)
        stdin, stdout, stderr = client.exec_command(
            "echo Connected", get_pty=True)
        userName = getUserName(str(stdout.read()))
        # connects with correct username
        client.connect(
            hostname=ip_address, username=userName, pkey=key)
        stdin, stdout, stderr = client.exec_command(
            "echo Connected", get_pty=True)
        stdin, stdout, stderr = client.exec_command(
            "cat /etc/os-release", get_pty=True)
        # gets system info after connection
        system = getSystem(str(stdout.read()))
        return system
    except Exception as e:
        print(e)


def formatConsoleLogs(toFormat):
    """
    This function formats output from the instance
    req: toParse - the string to format
    """
    try:
        outputArray = toFormat.split('\\r\\n')
        for x in outputArray:
            try:
                outputArray2 = x.split('\\r')
                for y in outputArray2:
                    print(y)
            except:
                print(x)
    except Exception as e:
        print(e)


def createDockerImages(client, currContainers, scpClient):
    """
    This function finds the username in a given string
    req: toParse - the string in which the username exists
    """
    try:
        for curr in currContainers:
            if curr['script']:
                # put script
                scpClient.put(curr['script'], curr['script'])
                # run script
                stdin, stdout, stderr = client.exec_command(
                    "chmod +x "+curr['script'], get_pty=True)
                formatConsoleLogs(str(stdout.read()))
                stdin, stdout, stderr = client.exec_command(
                    "sudo ./"+curr['script'], get_pty=True)
                formatConsoleLogs(str(stdout.read()))
                stdin, stdout, stderr = client.exec_command(
                    "sudo docker images", get_pty=True)
                formatConsoleLogs(str(stdout.read()))
                stdin, stdout, stderr = client.exec_command(
                    "sudo docker ps", get_pty=True)
                formatConsoleLogs(str(stdout.read()))
            else:
                if curr['location'] == 'Local system':
                    os.system(
                        "docker save -o " + curr['container'] + "Image.tar " + curr['container'] + ":latest")
                    scpClient.put(curr['container']+"Image.tar",
                                  curr['container']+"Image.tar")
                    # run script
                    stdin, stdout, stderr = client.exec_command(
                        "chmod +x "+curr['container']+"Image.tar", get_pty=True)
                    formatConsoleLogs(str(stdout.read()))
                    stdin, stdout, stderr = client.exec_command(
                        "sudo docker load -i " + curr['container'] + "Image.tar ", get_pty=True)
                    formatConsoleLogs(str(stdout.read()))
                else:
                    # if no script just pull image
                    stdin, stdout, stderr = client.exec_command(
                        "sudo docker pull "+curr['container'], get_pty=True)
                    formatConsoleLogs(str(stdout.read()))
        # verifies images are correctly there
        stdin, stdout, stderr = client.exec_command(
            "sudo docker images", get_pty=True)
        formatConsoleLogs(str(stdout.read()))
    except Exception as e:
        print(e)


def installDocker(client, system):
    """
    This function instals docker based on the system
    req: client - the ssh client
         system - the system type
    """
    try:
        # uses yum to install on linux
        if system == "Amazon Linux" or system == "Linux":
            stdin, stdout, stderr = client.exec_command(
                "sudo yum install docker -y", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "sudo service docker start", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
        # uses apt to unstall on Ubuntu
        elif system == "Ubuntu":
            stdin, stdout, stderr = client.exec_command(
                "sudo apt update -y", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "sudo apt install apt-transport-https ca-certificates curl software-properties-common -y", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable\"", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "sudo apt update -y", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "apt-cache policy docker-ce", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "sudo apt install docker-ce -y", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
            stdin, stdout, stderr = client.exec_command(
                "sudo docker version", get_pty=True)
            formatConsoleLogs(str(stdout.read()))
    except Exception as e:
        print(e)


def getSystem(toParse):
    """
    This function finds the system in a given string
    req: toParse - the string in which the system info exists
    """
    try:
        if len(toParse.split("\"")) > 1:
            return toParse.split("\"")[1]
        else:
            print("unable to determine system")
            return 'error'
    except Exception as e:
        print(e)


def isInt(i):
    """
    This function checks if a string is an int
    req: string to check
    """
    try:
        int(i)
        return True
    except ValueError:
        return False


def createInstances(templates, containers, instances):
    """
    This function creates AWS ec2 instances
    req: templates - list of all templates
         containers - list of all containers
         instances - list of all instances
    """
    try:
        for data in instances:
            currTemplate = {}
            currContainers = []
            # gets info to use in instance creation
            for find in templates:
                if find['templateName'] == data['templateName']:
                    currTemplate = find
            for find in containers:
                if find['containerName'] == data['containerName']:
                    currContainers.append(find)

            # creates the instance
            print("Creating instance...")
            ec2 = boto3.resource('ec2', currTemplate['zone'])
            if(isInt(currTemplate['size'])):
                instances = ec2.create_instances(
                    ImageId=currTemplate['ami'],
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=currTemplate['instanceType'],
                    KeyName=data['sshKey'].split(".")[0],
                    SecurityGroups=currTemplate['securityGroup'],
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': data['instanceName']
                                },
                            ]
                        }],
                    BlockDeviceMappings=[
                        {
                            'DeviceName': '/dev/xvda',
                            'Ebs': {
                                'VolumeSize': int(currTemplate['size'])
                            }
                        }]
                )
            else:
                instances = ec2.create_instances(
                    ImageId=currTemplate['ami'],
                    MinCount=1,
                    MaxCount=1,
                    InstanceType=currTemplate['instanceType'],
                    KeyName=data['sshKey'].split(".")[0],
                    SecurityGroups=currTemplate['securityGroup'],
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': data['instanceName']
                                },
                            ]
                        }]
                )

            # verifies instance is running before doing commands
            print("Waiting for instance to be running...")
            instances[0].wait_until_running()
            time.sleep(15)

            # creates info required to connect for ssh
            current_instance = list(ec2.instances.filter(
                InstanceIds=[str(instances[0].id)]))
            ip_address = current_instance[0].public_ip_address
            key = paramiko.RSAKey.from_private_key_file(data['sshKey'])
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect for ssh
            system = connectToSSH(client, ip_address, key)

            # install docker on the system
            print("Installing docker...")
            installDocker(client, system)

            # create docker images
            print("Creating images...")
            scpClient = SCPClient(client.get_transport())
            createDockerImages(client, currContainers, scpClient)

            client.close()

    except Exception as e:
        print(e)


def main():
    templates, containers, instances = readFiles()
    if(templates != "error"):
        createInstances(templates, containers, instances)


if __name__ == "__main__":
    main()
