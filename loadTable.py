#!usr/bin/python3
"""
Name: Kaylee Bigelow
Date: October 3, 2020
This program creates a tables on aws with boto3
"""

import boto3
import csv


def generateTable(file, tableName):
    """
    generates a table in aws dynamoDB
    req: file - csv file to use as data for table
         tableName - name of table to be generated
    """
    resource = boto3.resource('dynamodb', 'us-east-1')
    try:
        if file.split(".")[1] != "csv":
            print("Invalid file type")
            return
        # create tables
        table = resource.create_table(
            TableName=tableName,
            KeySchema=[
                {'AttributeName': 'commodity', 'KeyType': 'HASH'},
                {'AttributeName': 'variable#year', 'KeyType': 'RANGE'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'commodity', 'AttributeType': 'S'},
                {'AttributeName': 'variable#year', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table is creating...")
        table.wait_until_exists()
        print("Table has been created")
        # reads in csv file
        print("Adding information to table...")
        with open(file, encoding='utf-8-sig') as csv_file:
            read = csv.reader(csv_file, delimiter=",")
            for row in read:
                # puts rows from file into table
                table.put_item(
                    Item={
                        'variable#year': row[1]+"#"+row[2],
                        'commodity': row[0],
                        'variable': row[1],
                        'year': row[2],
                        'units': row[3],
                        'mfactor': row[4],
                        'value': row[5]
                    }
                )
        print("Information has been added to table")
    except Exception as e:
        print(e)


def main():
    print("To exit program enter 'exit'")

    while(True):
        print("Please enter CSV file name and table name:")
        userInput = input().split(" ")
        if userInput[0] == "exit":
            print("BYE!")
            exit(1)
        elif len(userInput) == 2:
            generateTable(userInput[0], userInput[1])
        else:
            print("Invalid input.\nExample input: file1.csv testTable")


if __name__ == "__main__":
    main()
