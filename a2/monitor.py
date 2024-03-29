#!usr/bin/python3
"""
Name: Kaylee Bigelow
Date: November 1, 2020
This program takes template files and uses them to build ec2 instances
"""

import boto3
import paramiko
from scp import SCPClient


def getSystem(toParse):
    """
    This function finds the system in a given string
    req: toParse - the string in which the system info exists
    """
    try:
        if len(toParse.split("\"")) > 1:
            systemInfo = toParse.split("\"")
            system = systemInfo[1]+" "+systemInfo[3].split(" ")[0]
            return system
        else:
            print("unable to determine system")
            return 'error'
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


def getImages(toParse):
    """
    This function gets a list of instances from a string of docker output
    req: toParse - a string containing docker output
    """
    try:
        imageInfo = []
        dockerList = toParse.split("\\r\\n")
        for i in range(1, len(dockerList)-1):
            imageInfo.append(dockerList[i].split()[0])
        return imageInfo
    except Exception as e:
        print(e)


def main():
    try:
        client = boto3.client('ec2')
        ec2 = boto3.resource('ec2')
        instanceIds = []
        keyNames = []
        i = 0

        print("External Instance Information")
        print("{:<10}  {:<10}  {:<20}  {:<20}  {:<20}  {:<15}  {:<10}  {:<10}   {:<15}  {:<20}  {:<15}".format(
            "Name", "State", "Instance Id", "Availablity Zone", "Image Id", " Instance Type", "Volume Size", "Key Name", "PublicIP", "Security Groups", "Root Device Name"))
        for info in client.describe_instances()['Reservations']:
            if info['Instances'][0]['State']:
                if info['Instances'][0]['State']['Name'] != 'terminated':
                    curr = info['Instances'][0]
                    instanceIds.append(curr['InstanceId'])
                    keyNames.append(curr['KeyName'])

                    instance = ec2.Instance(curr['InstanceId'])
                    volumes = instance.volumes.all()
                    volumeSize = '8'
                    for volume in volumes:
                        if(volume.size != 8):
                            volumeSize = volume.size

                    print("{:<10}  {:<10}  {:<20}  {:<20}  {:<20}  {:<15}  {:<10}  {:<10}   {:<15}  {:<20}  {:<15}".format(
                        curr['Tags'][0]['Value'], curr['State']['Name'], curr['InstanceId'], curr['Placement']['AvailabilityZone'], curr['ImageId'], curr['InstanceType'], volumeSize, curr['KeyName'], curr['PublicIpAddress'], curr['SecurityGroups'][0]['GroupName'], curr['RootDeviceName']))

        print("\nInternal Instance Information")
        print("{:<20}  {:<15}  {:<15}".format(
            "Instance Id", "System", "Docker Containers"))
        for instance in instanceIds:
            current_instance = list(ec2.instances.filter(
                InstanceIds=[instance]))
            ip_address = current_instance[0].public_ip_address
            key = paramiko.RSAKey.from_private_key_file(keyNames[i]+".pem")
            i = i + 1
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            system = connectToSSH(client, ip_address, key)
            stdin, stdout, stderr = client.exec_command(
                "sudo docker images", get_pty=True)
            images = getImages(str(stdout.read()))
            print("{:<20}  {:<15}  {:<15}".format(
                instance, system, str(images)))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
