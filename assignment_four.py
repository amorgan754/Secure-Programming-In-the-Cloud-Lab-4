"""
This application is to demonstrate final understanding of Cloud9 programming
"""

#imports
import sys
import math
import datetime
import logging
import random
import boto3
from botocore.exceptions import ClientError

#region
REGION = "us-east-1"

#s3 client
s3 =  boto3.client("s3", region_name = REGION)

#database resource
dynamodb = boto3.resource("dynamodb")

#functions

#create table
def create_table():
    """This function is to create the table"""
    table_creation = dynamodb.create_table(
        TableName="HighLowGames",
        KeySchema=[
            {
            "AttributeName": "GameName",
            "KeyType": "HASH"
            },

            {
            "AttributeName": "Number",
            "KeyType": "RANGE"
            }
        ],
        AttributeDefinitions=[
            {
            "AttributeName": "GameName",
            "AttributeType": "S"
            },
            {
            "AttributeName": "Number",
            "AttributeType": "N"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
            }
    )
table = dynamodb.Table("HighLowGames")

#function for the first time you run the program
def first_run():
    """This function is to run the first time you use the program"""
    #welcome letter to the application
    print()
    print("Hello and welcome to Assignmnet Four!")
    print("Before the menu is displayed, a s3 bucket and a table will be created.")
    print("Both of these are for input of information from a few of the choices below.")
    print("This application has a few choices to pick from, choices ranging from different games to"
    " password encryptions")
    print("When selecting an option, it will describe to you what it is and if it is a game,"
    " how to play.")
    print("Enjoy!")
    print("-Ashley Morgan")
    print()

    #create the bucket and table for first run
    create_bucket()
    create_table()


#function for other times running the program
def other_runs():
    """This function is if you are not running it the first time"""
    #see if user has both the bucket and table
    start_up = input("Do you have both the bucket and table created? \n")

    #if user does not have both bucket and table, sets up what they dont have
    if start_up.lower() == "no" or start_up.lower() == "n":
        bucket = input("Do you need a bucket created?\n")
        if bucket.lower() == "yes" or bucket.lower() == "y":
            create_bucket()
        table_needed = input("Do you need a table created?\n")
        if table_needed.lower() == "yes" or table_needed.lower() == "y":
            create_table()

    #welcome letter to the application
    print()
    print("Hello and welcome to Assignmnet Four!")
    print("Since this is not the first time running, you should have the s3 bucket "
    "and the table created.")
    print("Both of these are for input of information from a few of the choices below.")
    print("This application has a few choices to pick from, choices ranging from different games to"
    " password encryptions")
    print("When selecting an option, it will describe to you what it is and if it is a game,"
    " how to play.")
    print("Enjoy!")
    print("-Ashley Morgan")
    print()

#function to see if the bucket name exists
def already_bucket(bucket_name):
    """This function is to validate if there is already an existing bucket"""
    try:
        response = s3.head_bucket(Bucket = bucket_name)
    except ClientError as error:
        logging.debug(error)
        return False
    return response

#function to create bucket
def create_bucket():
    """This function is to create the s3 bucket"""
    #check to see if there is already a bucket with that name
    name = "assign4bucket"
    try:
        s3_client =  boto3.client("s3", region_name = REGION)
        s3_client.create_bucket(Bucket = name)
    except ClientError as error:
        logging.error(error)
        return False
    return True

#table inputs
def game_table_inputs(name, guessed_number):
    """This function is to input the data"""
    response = table.put_item(
        TableName = "HighLowGames",
            Item = {
                'GameName': name,
                'Number' : guessed_number
                }
            )
    return response

#function to validate number
def validate_number():
    """This function is to validate the input is a number"""
    #user inputs a number
    guess = input("Guess a number between 1-100: ")
    while not guess.isdigit():
        print("That is not a number.")
        print()
        guess = input("Guess a number between 1-100: ")
    return guess

#function to validate pennies inputted in an int
def validate_pennies(number):
    """This function is to validate the input of pennies is a number"""
    #user inputs a number
    cost = input("What is the " + number + " in pennies? ")
    while not cost.isdigit():
        print("That is not a number.")
        print()
        cost = input("What is the " + number + " in pennies? ")
    return cost

#function to place objects in s3 bucket
def insert_object(file_location):
    """This function is to put the files into a bucket"""
    #bucket name
    bucket_name = "assign4bucket"

    #moving file to the bucket
    try:
        s3.put_object(Bucket = bucket_name, Key = file_location)
        print(" ")
        print("File was successfully put into " + bucket_name)
        print(" ")
    except ClientError as error:
        logging.error(error)
        return False
    return True

#function of the menu
def main_menu():
    """This function is to define the main menu"""
    print("Option 1: Play the High Low Game Version One")
    print("Option 2: Play the High Low Game Version Two")
    print("Option 3: Convert pennies to bills and coins")
    print("Option 4: Encrypt and save a password to a s3 bucket")
    print("Option 5: Mad Libs")
    print("Option 6: Days Until")
    print("Option 0: Exit the program")

#function to exit the program
def exit_program():
    """This function is to exit the program"""
    print("\nThank you for using our program.")
    sys.exit(0)

#function for high low game v.one
def high_low_one():
    """This function is for the first version of high low game"""
    #instructions
    print("Welcome to the High Low Game Version One!")
    print("")
    print("In this game, you will think of a random number fromm 1-100")
    print("i will then try to guess the number")
    print("If the number I guess is too high, input h,")
    print("if the number I guess is too low, input l,")
    print("and if the number is correct, input c.")
    print("The correct number will then be inputted into a database table for later viewing")
    input("Press enter when you are ready to start! Good luck!")

    #set minimum and maximum numbers
    minnum = 0
    maxnum = 101

    #set guess based on 0 - 100 guess
    guess = random.randint(0,100)

    keepgoing = "true"
    #computer inputs guess
    while keepgoing == "true":
        print(" ")
        print("I guess " + str(guess))
        print(" ")
        response = input("Is it too (h)igh, (l)ow, or is it (c)orrect? ")

    #user responds to guess, application guesses again based on parameters
        if response.lower() == "h":
            maxnum = guess
            guess = guess - int((maxnum - minnum / 2))

        elif response.lower() == "l":
            minnum = guess
            guess = guess + int((maxnum-minnum)/2)

        elif response.lower() == "c":
            print("You won!")
            print(" ")
            #the correct number goes into the database
            game_table_inputs("High Low Version One", guess)
            keepgoing = "false"


#function for high low game v. two
def high_low_two():
    """This function is for the second version of high low game"""
    #instructions
    print("Welcome to the High Low Game Version Two!")
    print("")
    print("In this game, I will think of a random number fromm 1-100")
    print("you will then try to guess the number")
    print("If the number you guess is too high, I'll say it is too high and have you guess again.")
    print("If the number you guess is too low, I'll say it is too low and have you guess again,")
    print("and if the number is correct, I'll say correct!")
    print("The correct number will then be inputted into a database table for later viewing")
    input("Press enter when you are ready to start! Good luck!")

   #set number for guess
    number = random.randint(0,100)
    guess = validate_number()
    guess = int(guess)

    #user tries to guess number
    while number:
        if guess > number:
            print("The number is too high")
            print("Try again")
            print(" ")
            guess = validate_number()
            guess = int(guess)
        if guess < number:
            print("The number is too low")
            print("Try again")
            print(" ")
            guess = validate_number()
            guess = int(guess)
        if guess == number:
            print("The number is correct!")
            #the correct number goes into the database
            game_table_inputs("High Low Version Two", guess)
            break

#function for penny conversion
def penny_conversion():
    """This function is to convert a cost and change in pennies to bills and change"""
    #instructions
    print("Welcome to penny conversion!")
    print("This is to help you determine the amount of change that is given to you, or still owed,"
    " when inputted in pennies.")
    print("If the number is positive, it is how much is owed back to you."
    " If it is negative, it is how much you still owe.")
    print("Make sure to input both numbers as pennies.")
    input("Press enter to begin")

    #input cost and how much is given in pennies
    cost = validate_pennies("cost")
    cost = int(cost)
    money_given = validate_pennies("money given")
    money_given = int(money_given)

    #change given in pennies
    change = money_given - cost
    change = int(change)

    #how many twenties
    twenties = math.trunc(change / 2000)
    change = change - (twenties * 2000)

    #how many tens
    tens = math.trunc(change / 1000)
    change = change - (tens * 1000)

    #how many fives
    fives = math.trunc(change / 500)
    change = change - (fives * 500)

    #how many ones
    ones = math.trunc(change / 100)
    change = change - (ones * 100)

    #how much money is needed to be given to or given back
    dollars = (twenties * 20) + (tens * 10) + (fives * 5) + ones
    dollars = str(dollars)
    change = str(change)
    print()
    print("Your change is $" + dollars + "." + change)




#function for password encryption
def password_encryption_tool():
    """This function is to encrypt a password and store it in a file in a s3 bucket"""
    #instructions
    print("Welcome to a password encryption!")
    print("You will enter any password that you are wanting to encrypt")
    print("When you enter it, you will also give a file name that you are wanting"
    " to store it under")
    print("After giving both the password and the file name, it will be stored as an object"
    " in a s3 bucket for viewing")
    input("Press enter to continue")

    #input password and file name
    print()
    password = input("What is the password you are wanting to encrypt?: ")
    file_name = input("What is the name you want to call the file?: ")

    #file location given
    file_location = "protectedInformation/" + file_name + ".txt"

    #password encryption
    password_encryption = str(hash(password))

    #input for the file of the password unencrypted and encrypted
    file_input = "password hashed " + password_encryption

    #create new file
    with open(file_name, "w") as file:
        file.write(file_input)
        file.close()
    #put password and password encryption into file location

    #call for def insert_object(file_location): to put the file into the asign4bucket
    insert_object(file_location)

#function for mad libs
def mad_libs():
    """This function is for a mad libs story"""
    #instructions
    print("You will be asked for ten different verbs, nouns, adjectives, and adverbs.")
    print("These will be inputted into a mad libs story")
    print("The story will then be inputted into the asign4bucekt as a txt document")
    input("Press enter to begin\n")

    #user gives the file a name
    file_name = input("What would you like to call the file?\n")

    file_name = file_name + ".txt"

    #story put together and displayed
    story_line = story_input()
    print(story_line)

    #create new file
    with open(file_name, "w") as file:
        file.write(story_line)
        file.close()

    #putting the file into madlibs folder in the s3 bucket
    file_location = "madlibs/" + file_name

    insert_object(file_location)

#function for the story
def story_input():
    """This function is for user inputs and display of the story"""
    #user inputs for verbs, adj, nouns, and places
    adj_one = input("1. Input an adjective\n")
    noun_one = input("2. Input a single noun\n")
    verb_one = input("3. Input a verb \n")
    adj_two = input("4. Input an adjective\n")
    place_one = input("5. Input a place\n")
    verb_two = input("6. Input a verb \n")
    place_two = input("7. Input a place\n")
    verb_three = input("8. Input a past tense verb \n")
    noun_two = input("9. Input a single noun\n")
    verb_four = input("10. Input a verb \n")

    #user inputs put into the story
    story = "On a " + adj_one + " day, the " + noun_one + " and I decided to " + verb_one +\
    ". This was a " + adj_two + " way to spend the day in my opinion.\n When we got to " +\
    place_one + ", we decided to " + verb_two + " to the door "+\
    " so that we would be the first in line.\n What we didn't realize was that " +\
    place_two + " would be " + verb_three + " for the day. As a last second change, " +\
    noun_two + " and I decided to "  + verb_four + " instead."

    return story


#function for days until
def days_until():
    """This function is to show how many days are inbetween today and a given day"""
    #instructions
    print()
    print("Welcome!")
    print("If you wanted to know how many days are inbetween today and a future date,"
    " look no further.")
    print("All you need to do is input the month, day, and year of the event in question.")
    print("After you will see how many days are inbetween the event and today.")
    input("Press enter to begin.")
    print()

    #current day
    current_day = datetime.date.today()

    #user inputs the month, day, and year of the event
    month = input("What is the month of the event?\n")
    if month.lower() == "january" or month.lower() == "jan" or month == "1":
        month = 1
    elif month.lower() == "february" or month.lower() == "feb" or month == "2":
        month = 2
    elif month.lower() == "march" or month.lower() == "mar" or month == "3":
        month = 3
    elif month.lower() == "april" or month.lower() == "apr" or month == "4":
        month = 4
    elif month.lower() == "may" or month == "5":
        month = 5
    elif month.lower() == "june" or month.lower() == "jun" or month == "6":
        month = 6
    elif month.lower() == "july" or month.lower() == "jul" or month == "7":
        month = 7
    elif month.lower() == "august" or month.lower() == "aug" or month == "8":
        month = 8
    elif month.lower() == "september" or month.lower() == "sept" or month == "9":
        month = 9
    elif month.lower() == "october" or month.lower() == "oct" or month == "10":
        month = 10
    elif month.lower() == "november" or month.lower() == "nov" or month == "11":
        month = 11
    elif month.lower() == "december" or month.lower() == "dec" or month == "12":
        month = 12

    day = day_validation(month)
    day = int(day)
    year = input("What is the year of the event?\n")
    year = int(year)

    event_date = datetime.date(year, month, day)

    #find the difference in the days between current event and today
    difference_in_days = (event_date - current_day).days

    print()
    print("There is " + str(difference_in_days) + " days until the event!")
    print()

#function for day validation
def day_validation(month_given):
    """This fnction is to validate the day in the month"""
    #input of the date
    day = input("What is the day of the event?\n")

    #date validation in range of month
    while day:
        if month_given in (1, 3, 5, 7, 8, 10, 12):
            while day > "31":
                print("Invalid day for the month")
                day = input("What is the day of the event?\n")
        if month_given == 2:
            while day > "28":
                print("Invalid day for the month.")
                day = input("What is the day of the event?\n")
        if month_given in (4, 6, 9, 11):
            while day > "30":
                print("Invalid day for the month.")
                day = input("What is the day of the event?\n")
        return day

#running of the program
print("If this is your first time running the program, or you do not have a bucket"
" and table anymore, input yes")
print("If this is not your first time running and you have the bucket and table, or only need the"
" bucket or table created, input no")
print()
creation = input("Is this your first time running the program: \n")
if creation.lower() == "yes" or creation.lower() == "y":
    first_run()
    print()
else:
    other_runs()
    print()



#use while loop
CHOICE = None

#keeps running the while loop until selected to exit the program
while CHOICE != 0:
    main_menu()

    CHOICE = input("Please select a menu option number: \n")

    if CHOICE == "1":
        high_low_one()
    elif CHOICE == "2":
        high_low_two()
    elif CHOICE == "3":
        penny_conversion()
    elif CHOICE == "4":
        password_encryption_tool()
    elif CHOICE == "5":
        mad_libs()
    elif CHOICE == "6":
        days_until()
    elif CHOICE == "0":
        exit_program()
    else:
        print("\nPlease make a valid choice\n")
