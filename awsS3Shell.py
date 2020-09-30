#!usr/bin/python3

import uuid
import boto3


def generatePath(client, path, newlocation):
    bucketArray = []
    for bucket in client.buckets.all():
        bucketArray.append(bucket.name)
    if not path:
        path = []
    else:
        path = path.split("/")

    if newlocation:
        if newlocation.split("/")[0] == "s3:":
            path = []
            print("yay")
            newlocation = newlocation.replace("s3:/", "", 1)
        if newlocation[-1:] == "/":
            newlocation = newlocation[:-1]
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
        print("Missing Arguements")
        return "error"


def checkExists(client, loc):
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
    try:
        originalPath = path
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
    if originalFile and newFile:
        try:
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

                client.Object(bucket2, filePath2).copy_from(
                    CopySource=bucket1+"/"+filePath1)
            else:
                print("Missing Argumnets")
        except Exception as e:
            print(e)

    else:
        print("Invalid argument")


def download(client, resource, path, originalFile=None, newFile=None):
    if originalFile and newFile:
        try:
            newPath = generatePath(resource, path, originalFile)
            if newPath == "error":
                return
            if len(newPath) > 0:
                bucket = newPath[0]
                newPath = '/'.join(newPath)
                filePath = newPath.replace(bucket+"/", "", 1)
                client.download_file(bucket, filePath, newFile)
        except Exception as e:
            print(e)

    else:
        print("Invalid argument")


def mkbucket(client, resource, name=None):
    if name:
        try:
            for bucket in resource.buckets.all():
                if bucket == name:
                    print("Bucket already exists")
                    return
            client.create_bucket(Bucket=name)
        except Exception as e:
            print(e)

    else:
        print("Missing argument")


def mkdir(client, resource, path, folder=None):
    if folder:
        try:
            newPath = generatePath(resource, path, folder)
            if newPath == "error":
                return
            if not checkExists(resource, newPath):
                if len(newPath) > 1:
                    bucket = newPath[0]
                    newPath = '/'.join(newPath)
                    folderPath = newPath.replace(bucket+"/", "", 1)
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
    try:
        cp(client, path, originalFile, newFile)
        rm(client, path, originalFile)
    except Exception as e:
        print(e)


def printAllInfo(client, bucketName, key, name):
    info = client.head_object(Bucket=bucketName, Key=key)
    print(str(info['ContentType']) + "\t" + str(info['ContentLength']) +
          "\t"+str(info['LastModified']) + "\t"+name)


def ls(resource, client, path, flag=None):
    try:
        if path:
            newPath = path.split("/")
            bucketName = newPath[0]
            bucket = resource.Bucket(bucketName)
            newPath = '/'.join(newPath) + "/"
            newPath = newPath.replace(bucketName+"/", "", 1)
            for my_bucket_object in bucket.objects.all():
                if newPath in my_bucket_object.key:
                    position = my_bucket_object.key.replace(newPath, "", 1)
                    if position[-1:] == "/" and len(position.split("/")) == 2:
                        if flag and flag == "-l":
                            printAllInfo(client, bucketName,
                                         my_bucket_object.key, position)
                        elif not flag:
                            print("-dir-  "+position)
                        else:
                            print("Invalid argument")
                    elif len(position.split("/")) == 1:
                        if flag and flag == "-l":
                            printAllInfo(client, bucketName,
                                         my_bucket_object.key, position)
                        elif not flag:
                            print("       "+position)
                        else:
                            print("Invalid argument")
        else:
            if flag and flag == "-l":
                # printAllInfo(bucket, my_bucket_object.key)
                print()
            elif not flag:
                for bucket in resource.buckets.all():
                    print("-dir-  "+bucket.name)
            else:
                print("Invalid argument")
    except Exception as e:
        print(e)


def pwd(path):
    if path:
        print("s3:/"+path)
    else:
        print("s3:/")


def rmdir(client, path, folder):
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
                print("Missing Arguments")

        except Exception as e:
            print(e)
    else:
        print("Invalid arguments")


def rm(client, path, file=None, flag=None):
    if file:
        try:
            newPath = generatePath(client, path, file)
            if newPath == "error":
                return
            exists = checkExists(client, newPath)
            if exists:
                if len(newPath) > 0:
                    bucket = newPath[0]
                    newPath = '/'.join(newPath)
                    filePath = newPath.replace(bucket+"/", "", 1)
                    if flag and flag == "-rf":
                        my_bucket = client.Bucket(bucket)
                        my_bucket.objects.filter(Prefix=filePath).delete()
                    else:
                        client.Object(bucket, filePath).delete()
                else:
                    print("Missing Arguments")
            else:
                print("Invalid Path")
        except Exception as e:
            print(e)
    else:
        print("Invalid argument")


def upload(client, resource, path, originalFile=None, newFile=None):
    if originalFile and newFile:
        try:
            newPath = generatePath(resource, path, newFile)
            if newPath == "error":
                return
            exists = checkExists(client, newPath)
            if exists:
                if len(newPath) > 0:
                    bucket = newPath[0]
                    newPath = '/'.join(newPath)
                    filePath = newPath.replace(bucket+"/", "", 1)
                    client.upload_file(originalFile, bucket, filePath)
                else:
                    print("Missing Arguments")
                    return
            else:
                print("Invalid Path")
        except Exception as e:
            print(e)

    else:
        print("Invalid argument")


def login(user=None):
    try:
        file = open("config.ini", "r")
        info = file.read().splitlines()
        userFound = False
        if user:
            for pos in range(len(info)):
                if info[pos] and info[pos][0] == "[" and info[pos].replace("[", "").replace("]", "") == user:
                    userFound = True
                    accessKeyId = info[pos+1].split("=")
                    secretKey = info[pos+2].split("=")
                    region = info[pos+3].split("=")
                    sessionToken = info[pos+4].split("=")
                    break
        else:
            userFound = True
            accessKeyId = info[1].split("=")
            secretKey = info[2].split("=")
            region = info[3].split("=")
            sessionToken = info[4].split("=")
        if userFound == False:
            print("Invalid user")
            return
        resource = boto3.resource(service_name='s3',
                                  region_name=region[1],
                                  aws_access_key_id=accessKeyId[1],
                                  aws_secret_access_key=secretKey[1],
                                  aws_session_token=sessionToken[1]
                                  )
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
    print("Available commands:")
    print("cd <~ , .., dir name> - changes to specified directory")
    print("cp <S3 object name> <S3 object name> - copies an object from one S3 location to another")
    print("download <S3 object name> <local filename> - copies S3 object to local file system")
    print("exit - terminates connection")
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
            else:
                print("Please login before executing a command")
        else:
            if userInput[0] == "help":
                availableCommands()
            elif userInput[0] == "cd":
                if len(userInput) == 2:
                    path = cd(resource, path, userInput[1])
                else:
                    print("Missing arguments")
            elif userInput[0] == "cp":
                if len(userInput) == 3:
                    cp(resource, path, userInput[1], userInput[2])
                else:
                    print("Missing arguments")
            elif userInput[0] == "download":
                if len(userInput) == 3:
                    download(client, resource, path,
                             userInput[1], userInput[2])
                else:
                    print("Missing arguments")
            elif userInput[0] == "exit" or userInput[0] == "logout" or userInput[0] == "quit":
                if len(userInput) == 1:
                    print("BYE!")
                    exit(1)
                else:
                    print("Too many arguments")
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
                    print("Missing arguments")
            elif userInput[0] == "mkdir":
                if len(userInput) == 2:
                    mkdir(client, resource, path, userInput[1])
                else:
                    print("Missing arguments")
            elif userInput[0] == "mv":
                if len(userInput) == 3:
                    mv(resource, path, userInput[1], userInput[2])
                else:
                    print("Missing arguments")
            elif userInput[0] == "pwd":
                if len(userInput) == 1:
                    pwd(path)
                else:
                    print("Too many arguments")
            elif userInput[0] == "rmdir":
                if len(userInput) == 2:
                    rmdir(resource, path, userInput[1])
                else:
                    print("Missing arguments")
            elif userInput[0] == "rm":
                if len(userInput) == 2:
                    rm(resource, path, userInput[1])
                elif len(userInput) == 3:
                    rm(resource, path, userInput[2], userInput[1])
                else:
                    print("Missing arguments")
            elif userInput[0] == "upload":
                if len(userInput) == 3:
                    upload(client, resource, path, userInput[1], userInput[2])
                else:
                    print("Invalid arguments")
            else:
                print("Invalid command")


if __name__ == "__main__":
    main()
