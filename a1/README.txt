Name: Kaylee Bigelow
Date: October 03, 2020
Course: CIS*4010

Assignment 1

General:
	Python Modules:
		- boto3
		- csv

Part 1: awsS3Shell.py Program
	Basic Commands:
		- all basic commands and flags are implemented

	Extra Flags of Commands
		- all paths can be absolute or relative including .. or ~ anytime a path is given for an S3 object, including:
			- cd
			- cp
			- download
			- mkdir
			- mv
			- rm
			- redir
			- upload
		- rm -rf <S3 object name>: -rf is an optional flag that recurrively deletes everything in a folder
		- help: lists all available commands

	Error conditions
		- "Invalid command": returned if command does not match an available command
		- "Invalid arguments": returned if the user enters too many or not enough argguments for a command
		- "Please check you config file": returned by login if there is a problem parsing the config.ini file, then the program will exit
		- "Please login before executing a command": returned if the user trys to execute any command other than login or help before login is completed
		- "Invalid Path": returned when a path given is not found on awsS3Shell
		- "Bucket already exists": returned by mkbucket if a bucket that already exists tries to be created again
		- "Path already exists": returned by mkdir if the specified path already exists
		- "Directory must be empty": returned by rmdir if a specified folder to delete is not empty
		- "Invalid user": returned by login if the user specified does not exists in the config.ini file
		- Any except returned by boto3 will be printed out to the user and the program will continue

	Comments/Instructions
		- The config.ini file must contain session, refered to as "SessionKey" in the config.ini file provided
		
Part 2: DynamoDB
	loadTable.py Program
		- Keys: commodity variable#year
		- Names of fields:
			- commodity
			- variable#year
			- mfactor
			- units
			- value
			- year
		- Encoding.csv
			- this is not loaded with loadTable.py
			- this table is loaded with loadEncodings.py
			- to run: >python3 loadEncodings.py

	queryOECD.py Program
		- How to run:
			- input is recieved through stdin
			- user can enter commodity as abbribiation or full word (this is case sensitive)
		- Use of encodings table
			- uses encodings table to verify user input of commodity
			- uses encodings table to get all variables
	
	Error Conditions
		- "Invalid input.\nExample input: WT\nOr enter 'exit' to exit": is returned if the user enters nothing, just spaces, or an input that is greater than 1 word
		- "Invalid commodity": returned if the user enters a commodity that is not in the encodings table
		- "Invalid file type": returned if file is not .csv
		- If a year is missing from any table then 0 will be inputed and used for calculations
		- Any except returned by boto3 will be printed out to the user and the program will continue
	
	Comments/Instructions
		- loadEncodings.py must be run before you can query the DynamoDB (to run see "Encoding.csv" under "loadTable.py Program")
		- to exit loadTable.py or queryOECD.py programs enter 'exit' as listed at the start of the programs
		- the table displays the values the same way as they are displayed in the database