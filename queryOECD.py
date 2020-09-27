#!usr/bin/python3

import boto3
import csv


def queryTable(commodity):
    resource = boto3.resource('dynamodb', 'us-east-1')
    try:

    except Exception as e:
        print(e)


def main():
    print("To exit program enter 'exit'")

    while(True):
        print("Please enter the code for the commodity:")
        userInput = input().split(" ")
        if userInput[0] == "exit":
            print("BYE!")
            exit(1)
        elif len(userInput) == 1:
            queryTable(userInput[0])
        else:
            print("Invalid input.\nExample input: WT")


if __name__ == "__main__":
    main()
