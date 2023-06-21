import sqlite3
import bcrypt
from pysqlitecipher import sqlitewrapper

import GlobalConstants as GC

USERNAME_COLUMN_NUMBER = 1
PASSWORD_COLUMN_NUMBER = 2
SALT_COLUMN_NUMBER = 3

class HouseDatabase:

    def __init__(self):
        # Connect to the database (create if it doesn't exist)
        self.conn = sqlite3.connect('house.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UsersTable  (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS LightStateTable (id INTEGER PRIMARY KEY, words TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS NetworkStateTable (id INTEGER PRIMARY KEY, mermaidString TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DoorStateTable (id INTEGER PRIMARY KEY, words TEXT)''')
        #self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

    def commitChanges(self):
        self.conn.commit()


    def closeDatabase(self):
        self.conn.close()


    def queryDatabase(self, tableName):
        sqlStatement = f"SELECT * FROM {tableName}"
        self.cursor.execute(sqlStatement)
    
        result = self.cursor.fetchall()

        return result

    def insertIntoNetworkStateTable(self, currentNetworkState):
        """ Insert data into NetworkStateTable. When passing single variable into a row data must be followed by a comma, else (data1, data2, data3)

        Args:
            db (HouseDatabase Object): SQLite object store in a .db file
            currentNetworkState (String): Network node configuration as String in NiceGUI Meraid formatted https://mermaid.js.org
        """
        
        self.cursor.execute("INSERT INTO NetworkStateTable (mermaidString) VALUES (?)", (currentNetworkState,))

    def insertIntoUserTable(self, un, pw):
        """ Insert username, hashed password, and hash salt into the User Table if username is unqiue, otherwise ignore repeat user

        Args:
            un (String): Username to login, which can be either a 10 digit phone number or email address
            pw (String): Password to login, which is NEVER stored as plain text in any database or on a SSD (RAM only)
        """
        self.cursor.execute("SELECT * FROM UsersTable WHERE username LIKE ?", ('%' + un + '%',))
        results = self.cursor.fetchall()
        
        if len(results) > 0:
            pass #Ignore repeat username and DO NOTHING
        else:
            generatedSalt = bcrypt.gensalt()
            hashedPassword = bcrypt.hashpw(pw.encode('utf-8'), generatedSalt)
            
            self.cursor.execute("INSERT INTO UsersTable (username, password, salt) VALUES (?, ?, ?)", (un, hashedPassword, generatedSalt))

    def searchUsersTable(self, searchTerm):
        self.cursor.execute("SELECT * FROM UsersTable WHERE username LIKE ?", ('%' + searchTerm + '%',))
        results = self.cursor.fetchall()

        return results

if __name__ == "__main__":
    print("Creating new table")
    
    db = HouseDatabase()

    db.insertIntoNetworkStateTable(GC.STATIC_DEFAULT_NETWORK)
    db.insertIntoUserTable("blazes.mfc.us", "TestPassword")
    
    db.commitChanges()
    
    password =  "TestPassword"
    usersDatabaseList = db.queryDatabase("UsersTable")
    isUserFound = False
    for user in usersDatabaseList:
        if user[USERNAME_COLUMN_NUMBER] == "blaze.sanders@gentex.com":
            isUserFound = True
            print(user[PASSWORD_COLUMN_NUMBER])
            storedHashedPassword = user[PASSWORD_COLUMN_NUMBER]
            storedSalt = user[SALT_COLUMN_NUMBER]
            
            hashedPasssword = bcrypt.hashpw(password.encode('utf-8'), storedSalt)
    
            if hashedPasssword == storedHashedPassword:
                print("Password matches!")
            else:
                print("Invalid password.")
        else:
            isUserFound = isUserFound or False   
    print(isUserFound) 
    
    databaseSearch = db.searchUsersTable("blaze.s.d.a.sanders@gmail.com")
    print(databaseSearch)

    db.closeDatabase()
    