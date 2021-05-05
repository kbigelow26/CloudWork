#!usr/bin/python3
"""
Name: Kaylee Bigelow
Date: October 3, 2020
This program queries tables in aws DynamoDB based on commodities to calculate what countries are part of north america for this data set
"""

import boto3
import csv
from boto3.dynamodb.conditions import Key, Attr


def queryTable(commodity):
    """
    This function queries 4 tables based on commodity to do calculations on the data
    req: commodity to query on
    """
    resource = boto3.resource('dynamodb', 'us-east-1')
    try:
        # checks if commodity exists in encodings
        encodingTable = resource.Table("encodings")
        response = encodingTable.query(
            KeyConditionExpression=Key('col').eq('commodity'))
        validComm = False
        for comm in response['Items']:
            if comm['short'] == commodity:
                validComm = True
            elif comm['expanded'] == commodity:
                commodity = comm['short']
                validComm = True
        if validComm == False:
            print("Invalid commodity")
            return

        # gets all variables from encodings table
        response = encodingTable.query(
            KeyConditionExpression=Key('col').eq('variable'))
        variables = response['Items']

        # gets table references using boto3
        tableNA = resource.Table("northamerica")
        tableCAN = resource.Table("canada")
        tableUSA = resource.Table("usa")
        tableMEX = resource.Table("mexico")
        OverallCANUSATally = 0
        OverallCANUSAMEXTally = 0
        OverallNeitherTally = 0
        # loops through all variables in encodings
        for var in variables:
            # gets from northamerica table for commodity given and variable
            responseNA = tableNA.query(KeyConditionExpression=Key('commodity').eq(
                commodity) & Key('variable#year').begins_with(var['short']))
            if responseNA['Items']:
                # add value to output table
                NAInfo = []
                YearInfo = []
                for curr in responseNA['Items']:
                    NAInfo.append(float(curr['value']))
                    YearInfo.append(curr['year'])

                # queries Canada table and adds values to output table
                CANInfo = []
                responseCAN = tableCAN.query(KeyConditionExpression=Key('commodity').eq(
                    commodity) & Key('variable#year').begins_with(var['short']))
                pos = 0
                for year in YearInfo:
                    if responseCAN['Items'][pos]['year'] == year:
                        CANInfo.append(
                            float(responseCAN['Items'][pos]['value']))
                        pos = pos + 1
                    else:
                        CANInfo.append(0)

                # queries USA table and adds values to output table
                USAInfo = []
                responseUSA = tableUSA.query(KeyConditionExpression=Key('commodity').eq(
                    commodity) & Key('variable#year').begins_with(var['short']))
                pos = 0
                for year in YearInfo:
                    if responseUSA['Items'][pos]['year'] == year:
                        USAInfo.append(
                            float(responseUSA['Items'][pos]['value']))
                        pos = pos + 1
                    else:
                        CANInfo.append(0)

                # queries Mexico table and adds values to output table
                MEXInfo = []
                responseMEX = tableMEX.query(KeyConditionExpression=Key('commodity').eq(
                    commodity) & Key('variable#year').begins_with(var['short']))
                pos = 0
                for year in YearInfo:
                    if responseMEX['Items'][pos]['year'] == year:
                        MEXInfo.append(
                            float(responseMEX['Items'][pos]['value']))
                        pos = pos + 1
                    else:
                        CANInfo.append(0)

                CANUSAInfo = []
                CANUSAMEXInfo = []
                DefInfo = []
                CANUSATally = 0
                CANUSAMEXTally = 0
                NeitherTally = 0
                for curr in range(len(CANInfo)):
                    # calculates totals
                    CANUSAInfo.append(
                        round(CANInfo[curr]+USAInfo[curr], 3))
                    CANUSAMEXInfo.append(
                        round(CANInfo[curr]+USAInfo[curr]+MEXInfo[curr], 3))
                for curr in range(len(NAInfo)):
                    # creates tally for what countries make up northamerica
                    if CANUSAInfo[curr] == NAInfo[curr]:
                        DefInfo.append("CAN+USA")
                        CANUSATally = CANUSATally + 1
                        OverallCANUSATally = OverallCANUSATally + 1
                    elif CANUSAMEXInfo[curr] == NAInfo[curr]:
                        DefInfo.append("CAN+USA+MEX")
                        CANUSAMEXTally = CANUSAMEXTally + 1
                        OverallCANUSAMEXTally = OverallCANUSAMEXTally + 1
                    else:
                        DefInfo.append("Neither")
                        NeitherTally = NeitherTally + 1
                        OverallNeitherTally = OverallNeitherTally + 1
                # print out findings for commodity
                print("Commodity: "+commodity)
                print("Variable: "+var['expanded'])
                print("{:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}".format(
                    "Year", "North America", "Canada", "USA", "Mexico", "CAN+USA", "CAN+USA+MEX", "NA Defn"))
                for curr in range(len(YearInfo)):
                    print("{:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}  {:<15}".format(YearInfo[curr], str(NAInfo[curr]), str(
                        CANInfo[curr]), str(USAInfo[curr]), str(MEXInfo[curr]), str(CANUSAInfo[curr]), str(CANUSAMEXInfo[curr]), DefInfo[curr]))
                print("North America Definition Results: " + str(CANUSATally) +
                      " CAN+USA, "+str(CANUSAMEXTally)+" CAN+USA+MEX, "+str(NeitherTally)+" Neither")
                if CANUSATally > CANUSAMEXTally and CANUSATally > NeitherTally:
                    print("Therefore we conclude North America = CAN+USA")
                elif CANUSAMEXTally > CANUSATally and CANUSAMEXTally > NeitherTally:
                    print("Therefore we conclude North America = CAN+USA+MEX")
                elif NeitherTally > CANUSATally and NeitherTally > CANUSAMEXTally:
                    print("Therefore we conclude North America = Neither")
                else:
                    print(
                        "Therefore we can not conclude the definition of North America\n")

        # prints out overall findings
        print("\nOverall North America Definition Results: " + str(OverallCANUSATally) +
              " CAN+USA, "+str(OverallCANUSAMEXTally)+" CAN+USA+MEX, "+str(OverallNeitherTally)+" Neither")
        if OverallCANUSATally > OverallCANUSAMEXTally and OverallCANUSATally > OverallNeitherTally:
            print("Therefore we conclude North America = CAN+USA")
        elif OverallCANUSAMEXTally > OverallCANUSATally and OverallCANUSAMEXTally > OverallNeitherTally:
            print("Therefore we conclude North America = CAN+USA+MEX")
        elif OverallNeitherTally > OverallCANUSATally and OverallNeitherTally > OverallCANUSAMEXTally:
            print("Therefore we conclude North America = Neither")
        else:
            print("Therefore we can not conclude the definition of North America\n")
    except Exception as e:
        print(e)


def main():
    print("To exit program enter 'exit'")

    while(True):
        print("Please enter the commodity or code for the commodity:")
        userInput = input().split(" ")
        if userInput[0] == "exit":
            print("BYE!")
            exit(1)
        elif len(userInput) == 1:
            queryTable(userInput[0])
        else:
            print("Invalid input.\nExample input: WT\nOr enter 'exit' to exit")


if __name__ == "__main__":
    main()
