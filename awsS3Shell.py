#!usr/bin/python3

import uuid
import boto3


# session = boto3.Session(profile_name='kaylee')
# dev_s3_client = session.client('s3')

def cd(client):
    print("WIP")


def cp(client):
    print("WIP")


def download(client):
    print("WIP")


def mkbucket(client, name=None):
    if name:
        try:
            client.create_bucket(Bucket=name)
        except Exception as e:
            print(e)

    else:
        print("Missing argument")


def mkdir(client):
    print("WIP")


def mv(client):
    print("WIP")


def ls(client):
    for bucket in client.buckets.all():
        print(bucket.name)


def pwd(client):
    print("WIP")


def rmdir(client):
    print("WIP")


def rm(client):
    print("WIP")


def upload(client):
    print("WIP")


def login():
    file = open("config.ini", "r")
    info = file.read().splitlines()

    region = info[1].split(" ")
    accessKeyId = info[2].split(" ")
    secretKey = info[3].split(" ")
    sessionToken = info[4].split(" ")

    client = boto3.resource(service_name='s3',
                            region_name=region[2],
                            aws_access_key_id=accessKeyId[2],
                            aws_secret_access_key=secretKey[2],
                            aws_session_token=sessionToken[2]
                            )
    return(client)


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
    print("Please enter a command\nType 'help' to list available commands")
    userLoggedIn = False
    client = None

    while(True):
        print("> ", end='')
        userInput = input().split(" ")

        if userLoggedIn == False:
            if userInput[0] == "help":
                availableCommands()
            elif userInput[0] == "login":
                try:
                    client = login()
                    userLoggedIn = True
                    print("Login Successful")
                except Exception as e:
                    print(e)
            else:
                print("Please login before executing a command")
        else:
            if userInput[0] == "help":
                availableCommands()
            elif userInput[0] == "cd":
                cd(client)
            elif userInput[0] == "cp":
                cp(client)
            elif userInput[0] == "download":
                download(client)
            elif userInput[0] == "exit" or userInput[0] == "logout" or userInput[0] == "quit":
                if len(userInput) == 1:
                    print("BYE!")
                    exit(1)
                else:
                    print("Invalid arguments")
            elif userInput[0] == "login":
                login()
            elif userInput[0] == "ls":
                ls(client)
            elif userInput[0] == "mkbucket":
                mkbucket(client, userInput[1])
            elif userInput[0] == "mkdir":
                mkdir(client)
            elif userInput[0] == "mv":
                mv(client)
            elif userInput[0] == "pwd":
                if len(userInput) == 1:
                    pwd(client)
                else:
                    print("Invalid arguments")
            elif userInput[0] == "rmdir":
                rmdir(client)
            elif userInput[0] == "rm":
                rm(client)
            elif userInput[0] == "upload":
                upload(client)
            else:
                print("Invalid command")


if __name__ == "__main__":
    main()
