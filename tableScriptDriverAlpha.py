#Sean Vassi TableScript Driver Alhpa 2023 BestProjectEver
import random

import connectionUtility as connUtility
import requests
import json

boredAPIUrl = 'https://www.boredapi.com/api/activity'
shibuInuURL = 'https://shibe.online/api/shibes?count=10'
iTunesUrl = "https://itunes.apple.com/search"
trviaURL = "https://opentdb.com/api.php?amount=1"


def boredAPIGenerateNewRow():
    response = requests.get(boredAPIUrl)
    data = response.json()
    data_values = (data['key'], data['activity'], data['type'], data['participants'], data['accessibility'])
    insert_query ='''INSERT INTO funactivities
    VALUES (%s, %s, %s, %s, %s)'''
    try:
        connUtility.insertData(insert_query,data_values)
    except connUtility.connector.Error as err:
        if err.errno == 1062:
            print("Duplicate primary key, generating new activity...")
            boredAPIGenerateNewRow()
        else:
            print("SQL Error in bored APIGenerateNewRow")
            print(err)
    except Exception as error:
            print("Error in boredAPIGenerateNewRow")
            print(error)

def boredAPITable():
    return connUtility.executeQuerySeeTable("funactivities")
def boredAPITest():
    boredAPIGenerateNewRow()
    return boredAPITable()

def returnMealRecipiesAPI():
 return connUtility.executeQuerySeeTable('mealsrecipes')

def returnMealRecipiesByDiff():
    query = """
        SELECT id, title FROM mealsrecipes
        ORDER BY
            CASE
                WHEN type = 'easy' THEN 1
                WHEN type = 'medium' THEN 2
                WHEN type = 'hard' THEN 3
                ELSE 4
            END
    """
    return connUtility.executeQuery(query)

def returnShibuAPI():
    return requests.get(shibuInuURL)
def iTunesSearchAPI(searchQuery):
    params = {
        "term": searchQuery,
        "media": "music",
        "limit": 10
    }
    try:
        response = requests.get(iTunesUrl, params=params)
    except Exception as exception:
        return "Error or No Data Found"
    data = response.json()
    importantData = []
    for result in data['results']:
        selected_entry = {
            "trackName": result.get('trackName', 'Unknown Track'),
            "artistName": result.get('artistName', 'Unknown Artist'),
            "collectionName": result.get('collectionName', 'Unknown Album')
        }
        importantData.append(selected_entry)

    return importantData
def exercisePLaylistInsert(songData):

    data_values = (songData['artistName'], songData['collectionName'], songData['trackName'])
    insert_query ='''INSERT INTO exercisePlaylist (Artist, Album, TrackName)
    VALUES (%s, %s, %s)'''
    try:
        connUtility.insertData(insert_query,data_values)
    except connUtility.connector.Error as err:
        if err.errno == 1062:
            print("Duplicate primary key, generating new activity...")
            boredAPIGenerateNewRow()
        else:
            print("SQL Error in bored APIGenerateNewRow")
            print(err)
    except Exception as error:
            print("Error in boredAPIGenerateNewRow")
            print(error)

def exercisePlaylistView():
    return connUtility.executeQuerySeeTable("exercisePlaylist")
def triviaDataView():
    return connUtility.executeQuerySeeTable("triviaData")

def getTriviaQuestion():
    response = requests.get(trviaURL)
    data = response.json()
    correct_answer = data["results"][0]["correct_answer"]
    triviaGame.set_correct_answer(correct_answer)
    formattedData = []
    for question in data['results']:
        incorrect_answers = question['incorrect_answers']
        incorrect_answers.append(question['correct_answer'])
        random.shuffle(incorrect_answers)  # Shuffle the answers

        formatted_question = {
            "category": question['category'],
            "difficulty": question['difficulty'],
            "question": question['question']
        }
        formattedData.append(formatted_question)

    triviaGame.setAnswers(incorrect_answers)
    return formattedData

def getTriviaAnswers():
    return triviaGame.allAnswers

def getTriviaValidation(answer):
    if triviaGame.checkAnswer(answer):
        print("Correct")
        return ["Correct!", True]  # Return a list with the message and a True flag
    else:
        print("Incorrect, Correct Answer " + triviaGame.correctAnswer)
        return ["Incorrect! The correct answer was " + triviaGame.correctAnswer, False]  # Return a list with the message and a False flag

def insertTriviaData(data):

    data_values = (data['question'], data['catagory'], data['difficulty'], data['correct_answer'])
    insert_query ='''INSERT INTO triviaData (Catagory, Difficulty, Question, correct_answer)
    VALUES (%s, %s, %s, %s)'''
    try:
        connUtility.insertData(insert_query,data_values)
    except connUtility.connector.Error as err:
        if err.errno == 1062:
            print("Duplicate primary key, generating new activity...")
            boredAPIGenerateNewRow()
        else:
            print("SQL Error in bored APIGenerateNewRow")
            print(err)
    except Exception as error:
            print("Error in boredAPIGenerateNewRow")
            print(error)

def getTriviaValidationBeta(answer):
    print(answer)
    if triviaGame.checkAnswer(answer):
        returnString = "Correct!"
        print("Correct")
        triviaGame.resetGame()
        return returnString
    else:
        returnString =  "False! the correct answer was " + triviaGame.correctAnswer
        print("Incorrect, Correct Answer " + triviaGame.correctAnswer)
        triviaGame.resetGame()
        return returnString



class triviaGame:
    correctAnswer = None
    allAnswers = []

    @classmethod
    def set_correct_answer(cls, answer):
        cls.correctAnswer = answer

    @classmethod
    def setAnswers(cls, array):
        cls.allAnswers = array

    @classmethod
    def checkAnswer(cls, answer):
        if answer == cls.correctAnswer:
            return True
        else:
            return False

    @classmethod
    def resetGame(cls):
        cls.correctAnswer = None
        cls.allAnswers = []





def main():
    boredAPITest()

#main()