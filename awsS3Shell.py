#!usr/bin/python3

import uuid
import boto3


# session = boto3.Session(profile_name='kaylee')
# dev_s3_client = session.client('s3')

def other():
    list_buckets_resp = dev_s3_client.list_buckets()
    for bucket in list_buckets_resp['Buckets']:
        if bucket['Name'] == bucket_name:
            print('(Just created) --> {} - there since {}'.format(
                bucket['Name'], bucket['CreationDate']))

    bucket_name = 'test-{}'.format(uuid.uuid4())
    print('Creating new bucket with name: {}'.format(bucket_name))
    dev_s3_client.create_bucket(Bucket=bucket_name)


def login():
    file = open("config.ini", "r")
    info = file.read().splitlines()
    print(len(info))
    print(info[1])

    client = boto3.client('s3', info[1], info[2])


def availableCommands():
    print("Available commands:")
    print("cd <~ , .., dir name> - changes to specified directory")
    print("cp <S3 object name> <S3 object name> - copies an object from one S3 location to another")
    print("download <S3 object name> <local filename> - copies S3 object to local file system")
    print("exit - terminates connection")
    print("login <username> - logs a user into AWS, if <username> is not passed the default will be used")
    print("logout - terminates connection")
    print("ls <-l> - lists buckets or the objects in a bucket, <-l> is an optional parameter to print long form descrition")
    print("mkbucket <S3 bucket name> - makes a S3 bucket in AWS")
    print("mkdir - makes a directory")
    print("mv <S3 object name> <S3 object name> - moves an object from one S3 location to another")
    print("pwd - displays position in the directory tree")
    print("quit - terminates connection")
    print("rm <S3 object name> - deletes object")
    print("rmdir - removes directory")
    print("upload <local filename> <S3 object name> - copies local file to S3 object store")


def main():
    print("> ", end='')
    userInput = input()
    if userInput == "help":
        availableCommands()
    elif "cd " in userInput:
        print("WIP")
    elif "cp " in userInput:
        print("WIP")
    elif "download " in userInput:
        print("WIP")
    elif userInput == "exit" or userInput == "logout" or userInput == "quit":
        print("BYE!")
        exit(1)
    elif "login" in userInput:
        login()
    elif "ls" in userInput:
        print("WIP")
    elif "mkbucket" in userInput:
        print("WIP")
    elif "mkdir" in userInput:
        print("WIP")
    elif "mv " in userInput:
        print("WIP")
    elif "pwd" in userInput:
        print("WIP")
    elif "rmdir" in userInput:
        print("WIP")
    elif "rm " in userInput:
        print("WIP")
    elif "upload" in userInput:
        print("WIP")
    else:
        print("Invalid command")


if __name__ == "__main__":
    print("Please enter a command\nType 'help' to list available commands")
    while(True):
        main()
