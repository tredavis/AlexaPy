import logging
import csv
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

#statment sends closes the application
#question asks a question

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# song dictionary 
top_songs = {
    "week" : [],
    "month" : [],
    "three_month" : [],
    "six_month" : [],
    "year" : [],
    "all_time" : [],
}

@ask.launch
def launch():
    welcome_msg = render_template('welcome')
    grab_top_songs()
    # Welcome the user and then ask them if they are ready to hear the top lists.   
    return question(welcome_msg).reprompt(welcome_msg)


#region Intent Answer Functions
@ask.intent("WeekIntent")
def week_answer():
    msg = "The top song is {0} By: {1} with {2} plays".format(top_songs["week"][1][2], top_songs["week"][1][0], top_songs["week"][1][1])
    return question(msg).reprompt(render_template('another_question'))

@ask.intent("MonthIntent")
def week_answer():
    msg = "The top song is {0} By: {1} with {2} plays".format(top_songs["month"][1][2], top_songs["month"][1][0], top_songs["month"][1][1])
    return question(msg).reprompt(render_template('another_question'))

@ask.intent("ThreeMonthIntent")
def week_answer():
    msg = "The top song is {0} By: {1} with {2} plays".format(top_songs["three_month"][1][2], top_songs["three_month"][1][0], top_songs["three_month"][1][1])
    return question(msg).reprompt(render_template('another_question'))

@ask.intent("SixMonthIntent")
def week_answer():
    msg = "The top song is {0} By: {1} with {2} plays".format(top_songs["six_month"][1][2], top_songs["six_month"][1][0], top_songs["six_month"][1][1])
    return question(msg).reprompt(render_template('another_question'))

@ask.intent("YearIntent")
def week_answer():
    msg = "The top song is {0} By: {1} with {2} plays".format(top_songs["year"][1][2], top_songs["year"][1][0], top_songs["year"][1][1])
    return question(msg).reprompt(render_template('another_question'))

@ask.intent("AllIntent")
def answer():
    pass
#endregion

# This is a function to grab the data at the beginning.
def grab_top_songs():
    read_top_week_csv()
    read_month_csv()
    read_three_month_csv()
    read_six_month_csv()
    read_year_csv()

#region Read CSV File Functions
def read_top_week_csv():
    try:
        with open('../../Pluralsight/MachineLearning/data/montredavis/7day.csv', newline='', encoding='utf-8') as myFile:  
            reader = csv.reader(myFile)
            
            #placeholder list 
            ph_list = []

            #hacking a loop that will only gather the top three songs
            #TODO: Learn more about the python csv reader
            counter = 0
            for row in reader:
                if counter != 4:
                    ph_list.append(row)
                    counter += 1
                else:
                    break

            top_songs["week"] = ph_list
    except:
        print("There was an error reading and/or parsing the file")

def read_month_csv():
    try:
        with open('../../Pluralsight/MachineLearning/data/montredavis/1month.csv', newline='', encoding='utf-8') as myFile:  
            reader = csv.reader(myFile)
            
            #placeholder list 
            ph_list = []

            #hacking a loop that will only gather the top three songs
            #TODO: Learn more about the python csv reader
            counter = 0
            for row in reader:
                if counter != 4:
                    ph_list.append(row)
                    counter += 1
                else:
                    break

            top_songs["month"] = ph_list
    except:
        print("There was an error reading and/or parsing the file")

def read_three_month_csv():
    try:
        with open('../../Pluralsight/MachineLearning/data/montredavis/3month.csv', newline='', encoding='utf-8') as myFile:  
            reader = csv.reader(myFile)
            
            #placeholder list 
            ph_list = []

            #hacking a loop that will only gather the top three songs
            #TODO: Learn more about the python csv reader
            counter = 0
            for row in reader:
                if counter != 4:
                    ph_list.append(row)
                    counter += 1
                else:
                    break

            top_songs["three_month"] = ph_list
    except:
        print("There was an error reading and/or parsing the file")

def read_six_month_csv():
    try:
        with open('../../Pluralsight/MachineLearning/data/montredavis/6month.csv', newline='', encoding='utf-8') as myFile:  
            reader = csv.reader(myFile)
            
            #placeholder list 
            ph_list = []

            #hacking a loop that will only gather the top three songs
            #TODO: Learn more about the python csv reader
            counter = 0
            for row in reader:
                if counter != 4:
                    ph_list.append(row)
                    counter += 1
                else:
                    break

            top_songs["six_month"] = ph_list
    except:
        print("There was an error reading and/or parsing the file")

def read_year_csv():
    try:
        with open('../../Pluralsight/MachineLearning/data/montredavis/12month.csv', newline='', encoding='utf-8') as myFile:  
            reader = csv.reader(myFile)
            
            #placeholder list 
            ph_list = []

            #hacking a loop that will only gather the top three songs
            #TODO: Learn more about the python csv reader
            counter = 0
            for row in reader:
                if counter != 4:
                    ph_list.append(row)
                    counter += 1
                else:
                    break

            top_songs["year"] = ph_list
    except:
        print("There was an error reading and/or parsing the file")

#endregion

if __name__ == '__main__':
    app.run(debug=True)
