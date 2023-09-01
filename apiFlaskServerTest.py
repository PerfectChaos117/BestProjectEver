from flask import Flask, request, render_template, jsonify

import tableScriptDriverAlpha
#import tableScript as script
import tableScriptDriverAlpha as scriptAlpha

#from tableScript import returnMealRecipiesAPI, testStringAPI

app = Flask(__name__)

@app.route('/api/recipies', methods=['GET'])
def recipiesTable():
  data = scriptAlpha.returnMealRecipiesAPI()
  return data

@app.route('/api/recipiesByDiff', methods=['GET'])
def recipiesTableByDiff():
  data = scriptAlpha.returnMealRecipiesByDiff()
  return data



@app.route('/api/funactivitiesGenerate', methods=['GET'])
def funactivitiesGenerate():
  data = scriptAlpha.boredAPITest()
  return jsonify(data)
  #return data

@app.route('/api/funactivitiesView', methods=['GET'])
def funactivitiesView():
  data = scriptAlpha.boredAPITable()
  return data


@app.route('/api/shibuInuGenerator', methods=['GET'])
def shibuInuGenerator():
  return jsonify(scriptAlpha.returnShibuAPI().json())

@app.route('/api/iTunesSearch', methods=['GET'])
def iTunesSearch():
  search_query = request.args.get('query')
  print(search_query)
  return tableScriptDriverAlpha.iTunesSearchAPI(search_query)

@app.route('/api/exercisePlaylistView', methods=['GET'])
def loadPlaylist():
  return scriptAlpha.exercisePlaylistView()

@app.route('/api/addToPlaylist', methods=['POST'])
def addToPlaylist():
   data = request.get_json()
   tableScriptDriverAlpha.exercisePLaylistInsert(data)
   return loadPlaylist()

@app.route('/api/triviaRecord', methods=['GET'])
def getTriviaRecord():
  return scriptAlpha.triviaDataView()

@app.route('/api/triviaGameQuestion', methods=['GET'])
def triviaQuestion():
   return scriptAlpha.getTriviaQuestion()

@app.route('/api/triviaGameAnswers', methods=['GET'])
def triviaQuestionAnswers():
   return jsonify(scriptAlpha.getTriviaAnswers())

@app.route('/api/insertTriviaData', methods=['POST'])
def insertTriviaQuestion():
    data = request.get_json()
    scriptAlpha.insertTriviaData(data)
    return getTriviaRecord()



@app.route('/api/sendTriviaAnswer', methods=['POST'])
def sendTriviaAnswer():
   data = request.get_json()
   return validateTriviaAnswer(data['answer'])

@app.route('/api/validateTriviaAnswer', methods=['GET'])
def validateTriviaAnswer(data):
  print(data)
  return scriptAlpha.getTriviaValidation(data)



@app.route('/api/indexBestProjectEver', methods=['GET'])
def indexPage():
  return render_template('indexBestProjectEver.html')

if __name__ == '__main__':
    app.run(debug=True)
