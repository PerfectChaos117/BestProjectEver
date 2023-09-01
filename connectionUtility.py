#Sean Vassi 2023 Connection Utility Class for GreatestProjectEver
import atexit
import os

import mysql.connector

#Will instantiate the connection to the SQL server
connectionInstance = mysql.connector.connect(
    host=os.environ.get('fitnessDatabaseHostname'),
    user=os.environ.get('fitnessDatabaseUsername'),
    password=os.environ.get('fitnessDatabaseSeanPassword'),
    database=os.environ.get('fitnessDatabaseAPPTEST_DB')
)
print("SQL Connection Established")

#Will get called when the program exits to insure proper procedure
def connectionCleanup():
    try:
        connectionInstance.close
        print("Connection closed succesfully")
    except Exception as error:
        print("Error in connection closure, see connectionCleanup method in ConnectionUtility.py")
        print(error)


atexit.register(connectionCleanup)

#WIll return the connection instance
def getConnection():
    return connectionInstance
#Will return a cursor from the connnection instance
def cursorControl():
    return getConnection().cursor()
#will execute the given query and return with its repsonse
def executeQuery(query):
    cursor = cursorControl()
    data = None
    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as error:
        print("Error in execute Query Method in connectionUtil.py")
        print("Query:" + query)
        print(error)
    cursor.close()
    return data
#Will attempt to veiw 100 lines of data from a given table name. Mostly for testing purposes
def executeQuerySeeTable(tableName):
    return executeQuery(f"SELECT * FROM " + tableName + " LIMIT 100")


#Takes in an array and attempts to insert Data into a table
def insertData(query, dataArray):
    cursor = cursorControl()
    try:
        cursor.execute(query,dataArray)
        getConnection().commit()
    except Exception as error:
        print("Error in insertData Method")
        print("Query: " + query)
        print("Array: ")
        print(dataArray)
        print(error)
    cursor.close()





