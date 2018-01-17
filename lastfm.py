#region Import Statements
import csv
import json
import numpy as np
import os
import requests
import sys
#endregion

# last fm client credentials
last_fm_cred = {
    "api_key" : "9534e4923a35c5b71b183107f1650395",
    "api_secret" : "d2bc0d321904c1a9b7c758cb1a7d0479" 
}

user_name = ''
song_list = []

# this lets me choose the mode on load
top_mode_array = ["7day", "1month", "3month", "6month", "12month", "overall"]
reccent_tracks = ["all_recent"]

#region Last FM Calls
def get_top_tracks(which_list, user_name, offset = 1):
    _url = "http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user="+user_name+"&api_key="+ last_fm_cred["api_key"]+"&period="+which_list+"&format=json&page=" + str(offset)
    
    # sending get request and saving the response as response object
    response = requests.get(url = _url)
    song_list.append(response.json()["toptracks"]["track"])
    
    #let's make sure we get all the pages
    current_page = response.json()["toptracks"]["@attr"]["page"]
    total_pages = response.json()["toptracks"]["@attr"]["totalPages"]
    print(current_page); print(total_pages)

    while (int(current_page) <= int(total_pages)):
        get_top_tracks(which_list, user_name, int(current_page) + 1)
        break
    else:
        return parse_top_songs(song_list, which_list, user_name)

def get_all_scrobbles(offset, which_list):
    """ This is the call for getting all scrobbles ever. 
        Depending on how long you'be been scrobbing this may take a minute or two.
        I've added print messages which should show your progress.
        There are also long messages if the call fails

        Args:
        offset (int): Since this call usually has multiple pages, this is a way to offset the call.
        which_list (string): Which mode should we go to.

    """
    _url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+user_name+"&api_key="+ last_fm_cred["api_key"]+"&limit=200&format=json&page=" + str(offset)
    
    # sending get request and saving the response as response object
    response = requests.get(url = _url)
    song_list.append(response.json()["recenttracks"]["track"])
    
    #let's make sure we get all the pages
    current_page = response.json()["recenttracks"]["@attr"]["page"]
    total_pages = response.json()["recenttracks"]["@attr"]["totalPages"]
    print(current_page); print(total_pages)

    while (int(current_page) <= int(total_pages)):
        get_all_scrobbles(int(current_page) + 1, which_list)
        break
    else:
        return parse_all_songs(song_list, which_list, user_name)

#endregion

#region Parsing Functions
def parse_all_songs(data, which_list, user_name):
    ret_list = []
    data = np.array(data)
    # NOTE data is the array of arrays here
    if len(data) > 0:
        for i in range(len(data)):
            for x in range(len(data[i])):
                song = data[i][x]
                #create in place dict
                s_dict = {
                "artist_name": song["artist"]["#text"],
                "artist_mbid": song["artist"]["mbid"],
                "track_name": song["name"],
                "track_mbid": song["mbid"],
                "date_uts": song["date"]["uts"],
                "date_text": song["date"]["#text"]
                }
                # add to the dictionary
                ret_list.append(s_dict)

    else:
        print("there was no data passed to: " + self)
    
    #now right the list to an excel file
    write_all_csv(ret_list, user_name, which_list)  

def parse_top_songs(data, which_list, user_name):
    ret_list = []
    data = np.array(data)
    # NOTE data is the array of arrays here
    if len(data) > 0:
        for i in range(len(data)):
            for x in range(len(data[i])):
                song = data[i][x]
                #create in place dict
                s_dict = {
                "artist_name": song["artist"]["name"],
                "play_count": song["playcount"],
                "track_name": song["name"]
                }
                # add to the dictionary
                ret_list.append(s_dict)

    else:
        print("there was no data passed to: " + self)  
    
    #now right the list to an excel file
    write_to_csv(ret_list, user_name, which_list)  
#endregion

#region CSV Methods
# Takes an array of dictionaries and writes them to a csv file
# Be sure to specify the name here
def write_to_csv(write_list, user_name, list_to_update):

    #if we don't have a directory yet make one
    if not os.path.exists("data/"+user_name+"/"):
        os.makedirs("data/"+user_name+"/")

    try:
        os.remove("data/"+user_name+"/"+list_to_update+".csv")
        print("File Removed!")
    except Exception:
        print("There was no file to delete")
    
    try:
        print("data/"+user_name+"/"+list_to_update+".csv")
        myFile = open("data/"+user_name+"/"+list_to_update+".csv", 'w', newline='', encoding='utf-8')  
        with myFile:  
            myFields = ["artist_name", "play_count", "track_name"]
            writer = csv.DictWriter(myFile, fieldnames=myFields) 
            writer.writeheader()
            writer.writerows(write_list)
    except Exception as ex:
        print(ex)

def write_all_csv(write_list, user_name, list_to_update):

    #if we don't have a directory yet make one
    if not os.path.exists("data/"+user_name+"/"):
        os.makedirs("data/"+user_name+"/")

    try:
        os.remove("data/"+user_name+"/"+list_to_update+".csv")
        print("File Removed!")
    except Exception:
        print("There was no file to delete")
    
    try:
        myFile = open("data/"+user_name+"/"+list_to_update+".csv", 'w', newline='', encoding='utf-8')  
        with myFile:  
            myFields = ["artist_name", "artist_mbid", "track_name", "track_mbid", "date_uts", "date_text"]
            writer = csv.DictWriter(myFile, fieldnames=myFields) 
            writer.writeheader()
            writer.writerows(write_list)
    except Exception as ex:
        print(ex)
#endregion

## Prettify and Dump Method
def prettify_response(data_to_parse):
    if data_to_parse:
        print(json.dumps(data_to_parse, sort_keys=True, indent=4, separators=(',', ': ')))

    else:
        print("There was no data passed in")

# Generic response for not being able to reach the last fm api
def last_fm_no_response():
    print("wasn't able to get a response from the last fm api")


def initialize(gather_songs = None):
    """ Initializes the application """

    #clears the song list so we can add more songs to it.
    song_list.clear()
    
    if not gather_songs:
        gather_songs = input("Should fetch songs? 1 for yes. 0 for no ")

    if int(gather_songs) == 1:
        user_name = input("")
        mode_to_get = input("Which mode should I get?")

        get_top_tracks(top_mode_array[int(mode_to_get)], user_name)

    else:
        return print("Goodbye!")

    initialize(1)

# initialize on app launch
initialize()

#get_all_scrobbles(1, reccent_tracks[0])
