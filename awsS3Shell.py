#!usr/bin/python3
"""
Name: Kaylee Bigelow
Date: October 3, 2020
This program acts as a shell for aws buckets
"""

import boto3


def generatePath(client, path, newlocation):
    """
    This function generates a path based on current location and given new location
    input: boto3 client, current path, new location
    output: new path
    """
    bucketArray = []
    for bucket in client.buckets.all():
        bucketArray.append(bucket.name)
    if not path:
        path = []
    else:
        path = path.split("/")

    if newlocation:
        # checks for absolute path
        if newlocation.split("/")[0] == "s3:":
            path = []
            newlocation = newlocation.replace("s3:/", "", 1)
        # removes / if it is folder
        if newlocation[-1:] == "/":
            newlocation = newlocation[:-1]
        # loops though given to generate new path
        for loc in newlocation.split("/"):
            if loc == "~":
                path = []
            elif loc == "..":
                if len(path) > 0:
                    path.pop()
            else:
                if loc in bucketArray and len(path) == 0:
                    path.append(loc)
                elif loc not in bucketArray and len(path) == 0:
                    print("Invalid Path")
                    return "error"
                else:
                    path.append(loc)
        return path
    else:
        print("Invalid Arguements")
        return "error"


def checkExists(client, loc):
    """
    This function checks if a given location exists
    input: boto3 client, location to check
    output: True if location exists, False if it does not
    """
    my_bucket = client.Bucket(loc[0])
    bucketName = loc[0]
    loc = '/'.join(loc)
    filePath = loc.replace(bucketName+"/", "", 1)
    for my_bucket_object in my_bucket.objects.all():
        if my_bucket_object.key[-1:] == "/":
            curr = my_bucket_object.key[:-1]
        else:
            curr = my_bucket_object.key
        if filePath == curr:
            return True
    return False


def cd(client, path, newlocation):
    """
    This function changes current location
    input: boto3 client, current path, new location
    """
    try:
        originalPath = path
        # gets new path
        path = generatePath(client, path, newlocation)
        if path == "error":
            return originalPath

        if len(path) > 0:
            my_bucket = client.Bucket(path[0])
            bucketName = path[0]
            if len(path) == 1:
                return bucketName
            path = '/'.join(path)
            path = path.replace(bucketName+"/", "", 1)
            # verifies path exists and is a folder
            for my_bucket_object in my_bucket.objects.all():
                if my_bucket_object.key[-1:] == "/":
                    curr = my_bucket_object.key[:-1]
                    isFolder = True
                else:
                    curr = my_bucket_object.key
                    isFolder = False
                if path == curr and isFolder:
                    return bucketName + "/" + path
            print("Invalid Path")
            return originalPath
        else:
            return None
    except Exception as e:
        print(e)


def cp(client, path, originalFile, newFile):
    """
    This function copies an s3 object to a new location
    input: boto3 client, current path, file to copy, new place for file
    """
    if originalFile and newFile:
        try:
            # gets paths
            newFilePath = generatePath(client, path, newFile)
            originalFilePath = generatePath(client, path, originalFile)
            if newFilePath == "error" or originalFilePath == "error":
                return
            if len(newFilePath) > 0 and len(originalFilePath) > 0:
                bucket2 = newFilePath[0]
                newFilePath = '/'.join(newFilePath)
                filePath2 = newFilePath.replace(bucket2+"/", "", 1)
                bucket1 = originalFilePath[0]
                originalFilePath = '/'.join(originalFilePath)
                filePath1 = originalFilePath.replace(bucket1+"/", "", 1)

                # copies files
                client.Object(bucket2, filePath2).copy_from(
                    CopySource=bucket1+"/"+filePath1)
            else:
                print("Invalid Argumnets")
        except Exception as e:
            print(e)

    else:
        print("Invalid argument")


def download(client, resource, path, originalFile=None, newFile=None):
    """
    This function downloads a file from s3 to the local system
    input: boto3 client, boto3 resource, file to copy, where to copy
    """
    if originalFile and newFile:
        try:
            # generates path to object
            newPath = generatePath(resource, path, originalFile)
            if newPath == "error":
                return
            if len(newPath) > 0:
                bucket = newPath[0]
                newPath = '/'.join(newPath)
                filePath = newPath.replace(bucket+"/", "", 1)
                # downloads object
                client.download_file(bucket, filePath, newFile)
        except Exception as e:
            print(e)

    else:
        print("Invalid arguments")


def mkbucket(client, resource, name=None):
    """
    This function creates a new bucket in aws s3
    input: boto3 client, boto3 resource, bucket name
    """
    if name:
        try:
            # verifies bucket does not exist
            for bucket in resource.buckets.all():
                if bucket == name:
                    print("Bucket already exists")
                    return
            # creates bucket
            client.create_bucket(Bucket=name)
        except Exception as e:
            print(e)

    else:
        print("Missing arguments")


def mkdir(client, resource, path, folder=None):
    """
    This function creates a directory on aws s3 bucket
    input: boto3 client, boto3 resource, current path, new folder name
    """
    if folder:
        try:
            # gets path
            newPath = generatePath(resource, path, folder)
            if newPath == "error":
                return
            # verifies path does not exist
            if not checkExists(resource, newPath):
                if len(newPath) > 1:
                    bucket = newPath[0]
                    newPath = '/'.join(newPath)
                    folderPath = newPath.replace(bucket+"/", "", 1)
                    # create folder
                    client.put_object(Bucket=bucket, Body='',
                                      Key=folderPath+"/")
                else:
                    print("Invalid arguments")
            else:
                print("Path already exists")
                return
        except Exception as e:
            print(e)
    else:
        print("Invalid arguments")


def mv(client, path, originalFile=None, newFile=None):
    """
    This function moves an s3 object to a new location
    input: boto3 client, current path, original file, new location
    """
    try:
        cp(client, path, originalFile, newFile)
        rm(client, path, originalFile)
    except Exception as e:
        print(e)


def printAllInfo(client, bucketName, key, name):
    """
    This function is used by ls to print info
    input: boto3 client, bucket name, object, name of object
    """
    info = client.head_object(Bucket=bucketName, Key=key)
    print(str(info['ContentType']) + "\t" + str(info['ContentLength']) +
          "\t"+str(info['LastModified']) + "\t"+name)


def ls(resource, client, path, flag=None):
    """
    This function lists everything at the current level
    input: boto3 resource, boto3 client, current path, flags for command
    """
    try:
        if path:
            newPath = path.split("/")
            bucketName = newPath[0]
            bucket = resource.Bucket(bucketName)
            newPath = '/'.join(newPath) + "/"
            newPath = newPath.replace(bucketName+"/", "", 1)
            # loops through all objects
            for my_bucket_object in bucket.objects.all():
                # verifies object is at current level
                if newPath in my_bucket_object.key:
                    position = my_bucket_object.key.replace(newPath, "", 1)
                    # checks if it is a folder
                    if position[-1:] == "/" and len(position.split("/")) == 2:
                        if flag and flag == "-l":
                            printAllInfo(client, bucketName,
                                         my_bucket_object.key, position)
                        elif not flag:
                            print("-dir-  "+position)
                        else:
                            print("Invalid arguments")
                    # checks if it is not a folder
                    elif len(position.split("/")) == 1:
                        if flag and flag == "-l":
                            printAllInfo(client, bucketName,
                                         my_bucket_object.key, position)
                        elif not flag:
                            print("       "+position)
                        else:
                            print("Invalid arguments")
        else:
            if flag and flag == "-l":
                # printAllInfo(bucket, my_bucket_object.key)
                print()
            elif not flag:
                for bucket in resource.buckets.all():
                    print("-dir-  "+bucket.name)
            else:
                print("Invalid arguments")
    except Exception as e:
        print(e)


def pwd(path):
    """
    This function prints current path
    input: current path
    """
    if path:
        print("s3:/"+path)
    else:
        print("s3:/")


def rmdir(client, path, folder):
    """
    This function removes a directory
    input: boto3 client, current path, new location
    """
    if folder:
        try:
            newPath = generatePath(client, path, folder)
            if newPath == "error":
                return
            if len(newPath) > 0:
                bucketName = newPath[0]
                newPath = '/'.join(newPath) + "/"
                folderPath = newPath.replace(bucketName+"/", "", 1)
                bucket = client.Bucket(bucketName)
                newPath = newPath.replace(bucketName+"/", "", 1)
                emptyFolder = True
                for my_bucket_object in bucket.objects.all():
                    if newPath in my_bucket_object.key:
                        if my_bucket_object.key != newPath:
                            emptyFolder = False
                if emptyFolder:
                    bucket.objects.filter(Prefix=folderPath).delete()
                else:
                    print("Directory must be empty")
            else:
                print("Invalid arguments")

        except Exception as e:
            print(e)
    else:
        print("Invalid arguments")


def rm(client, path, file=None, flag=None):
    """
    This function removes a file
    input: boto3 client, current path, new location, optional flags
    """
    if file:
        try:
            # gets path and check if it exists
            newPath = generatePath(client, path, file)
            if newPath == "error":
                return
            exists = checkExists(client, newPath)
            if exists:
                if len(newPath) > 0:
                    bucket = newPath[0]
                    newPath = '/'.join(newPath)
                    filePath = newPath.replace(bucket+"/", "", 1)
                    # deletes everything in a folder
                    if flag and flag == "-rf":
                        my_bucket = client.Bucket(bucket)
                        my_bucket.objects.filter(Prefix=filePath).delete()
                    else:
                        # deletes object
                        client.Object(bucket, filePath).delete()
                else:
                    print("Invalid arguments")
            else:
                print("Invalid Path")
        except Exception as e:
            print(e)
    else:
        print("Invalid arguments")


def upload(client, resource, path, originalFile=None, newFile=None):
    """
    This function uploads a file frm local system to s3
    input: boto3 client, boto3 for resource, current path, new location
    """
    if originalFile and newFile:
        try:
            # gets path and checks if it exists
            newPath = generatePath(resource, path, newFile)
            if newPath == "error":
                return
            exists = checkExists(client, newPath)
            if exists:
                if len(newPath) > 0:
                    bucket = newPath[0]
                    newPath = '/'.join(newPath)
                    filePath = newPath.replace(bucket+"/", "", 1)
                    # uploads a file
                    client.upload_file(originalFile, bucket, filePath)
                else:
                    print("Invalid arguments")
                    return
            else:
                print("Invalid Path")
        except Exception as e:
            print(e)

    else:
        print("Invalid arguments")


def login(user=None):
    """
    This function logs a user into aws
    input: username
    output: boto3 client, boto3 resource
    """
    try:
        file = open("config.ini", "r")
        info = file.read().splitlines()
        userFound = False
        if user:
            # searches for user
            for pos in range(len(info)):
                if info[pos] and info[pos][0] == "[" and info[pos].replace("[", "").replace("]", "") == user:
                    userFound = True
                    # saves information
                    accessKeyId = info[pos+1].split("=")
                    secretKey = info[pos+2].split("=")
                    region = info[pos+3].split("=")
                    sessionToken = info[pos+4].split("=")
                    break
        else:
            # saves information for default user
            userFound = True
            accessKeyId = info[1].split("=")
            secretKey = info[2].split("=")
            region = info[3].split("=")
            sessionToken = info[4].split("=")
        if userFound == False:
            print("Invalid user")
            return

        # creates boto3 resource
        resource = boto3.resource(service_name='s3',
                                  region_name=region[1],
                                  aws_access_key_id=accessKeyId[1],
                                  aws_secret_access_key=secretKey[1],
                                  aws_session_token=sessionToken[1]
                                  )
        # create boto3 client
        client = boto3.client(service_name='s3',
                              region_name=region[1],
                              aws_access_key_id=accessKeyId[1],
                              aws_secret_access_key=secretKey[1],
                              aws_session_token=sessionToken[1]
                              )
        return resource, client
    except Exception as e:
        print(e)


def availableCommands():
    """
    This function prints all commads
    """
    print("Available commands:")
    print("cd <~ , .., dir name> - changes to specified directory")
    print("cp <S3 object name> <S3 object name> - copies an object from one S3 location to another")
    print("download <S3 object name> <local filename> - copies S3 object to local file system")
    print("exit - terminates connection")
    print("help - lists all available commands")
    print("login <username> - logs a user into AWS, if <username> is not passed the default will be used")
    print("logout - terminates connection")
    print("ls <-l> - lists buckets or the objects in a bucket, <-l> is an optional parameter to print long form descrition")
    print("mkbucket <S3 bucket name> - makes a S3 bucket in AWS")
    print("mkdir <directory> - makes a directory")
    print("mv <S3 object name> <S3 object name> - moves an object from one S3 location to another")
    print("pwd - displays position in the directory tree")
    print("quit - terminates connection")
    print("rm <-rf> <S3 object name> - deletes object, <-rf> is an optional flag that recurrively deletes everything in a folder")
    print("rmdir <directory> - removes directory")
    print("upload <local filename> <S3 object name> - copies local file to S3 object store")


def main():
    """
    This function gets and checks user input
    """
    print("Please enter a command\nType 'help' to list available commands")
    userLoggedIn = False
    client = None
    resource = None
    path = None

    while(True):
        print("> ", end='')
        userInput = input().split(" ")

        if userLoggedIn == False:
            if userInput[0] == "help":
                availableCommands()
            elif userInput[0] == "login":
                try:
                    if len(userInput) == 1:
                        resource, client = login()
                        userLoggedIn = True
                        print("Login Successful")
                    elif len(userInput) == 2:
                        resource, client = login(userInput[1])
                        userLoggedIn = True
                        print("Login Successful")
                    else:
                        print("Invalid arguments")
                except Exception as e:
                    print("Please check you config file")
                    exit(1)
            else:
                print("Please login before executing a command")
        else:
            if userInput[0] == "help":
                availableCommands()
            elif userInput[0] == "cd":
                if len(userInput) == 2:
                    path = cd(resource, path, userInput[1])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "cp":
                if len(userInput) == 3:
                    cp(resource, path, userInput[1], userInput[2])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "download":
                if len(userInput) == 3:
                    download(client, resource, path,
                             userInput[1], userInput[2])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "exit" or userInput[0] == "logout" or userInput[0] == "quit":
                if len(userInput) == 1:
                    print("BYE!")
                    exit(1)
                else:
                    print("Invalid arguments")
            elif userInput[0] == "login":
                try:
                    if len(userInput) == 1:
                        resource, client = login()
                        userLoggedIn = True
                        print("Login Successful")
                        path = None
                    elif len(userInput) == 2:
                        resource, client = login(userInput[1])
                        userLoggedIn = True
                        print("Login Successful")
                        path = None
                    else:
                        print("Invalid arguments")
                except Exception as e:
                    print("Please check you config file")
            elif userInput[0] == "ls":
                if len(userInput) == 1:
                    ls(resource, client, path)
                elif len(userInput) == 2:
                    ls(resource, client, path, userInput[1])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "mkbucket":
                if len(userInput) == 2:
                    mkbucket(client, resource, userInput[1])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "mkdir":
                if len(userInput) == 2:
                    mkdir(client, resource, path, userInput[1])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "mv":
                if len(userInput) == 3:
                    mv(resource, path, userInput[1], userInput[2])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "pwd":
                if len(userInput) == 1:
                    pwd(path)
                else:
                    print("Invalid arguments")
            elif userInput[0] == "rmdir":
                if len(userInput) == 2:
                    rmdir(resource, path, userInput[1])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "rm":
                if len(userInput) == 2:
                    rm(resource, path, userInput[1])
                elif len(userInput) == 3:
                    rm(resource, path, userInput[2], userInput[1])
                else:
                    print("Invalid arguments")
            elif userInput[0] == "upload":
                if len(userInput) == 3:
                    upload(client, resource, path, userInput[1], userInput[2])
                else:
                    print("Invalid arguments")
            else:
                print("Invalid command")


if __name__ == "__main__":
    main()
