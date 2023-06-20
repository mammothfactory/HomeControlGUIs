import sqlite3


class HouseDatabase:

    def __init__(self):
        # Connect to the database (create if it doesn't exist)
        self.conn = sqlite3.connect('house.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS LightStateTable (id INTEGER PRIMARY KEY, words TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS NetworkStateTable (id INTEGER PRIMARY KEY, words TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DoorStateTable (id INTEGER PRIMARY KEY, words TEXT)''')
        #self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

    def commitChanges(self):
        self.conn.commit()


    def closeDatabase(self):
        self.conn.close()


    def queryDatabase(self, tableName):
        self.cursor.execute("SELECT * FROM CountableNounsTable")
        result = self.cursor.fetchall()

        return result 

    def insertIntoCountableNounsTable(self, newWord):
        """ Insert data into CountableNounsTable. When passing single variable into a row data must be followed by a comma, else (data1, data2, data3)

        Args:
            db (WordListDatabase Object): _description_
            newWord (String): Single word variable
        """
        
        self.cursor.execute("INSERT INTO CountableNounsTable (words) VALUES (?)", (newWord,))

    def insertIntoNetworkStateTable(self, currentNetworkState):
        """ Insert data into NetworkStateTable. When passing single variable into a row data must be followed by a comma, else (data1, data2, data3)

        Args:
            db (HouseDatabase Object): SQLite object store in a .db file
            currentNetworkState (String): Network node configuration as String in NiceGUI Meraid formatted https://mermaid.js.org
        """
        
        self.cursor.execute("INSERT INTO NetworkStateTable (mermaidString) VALUES (?)", (currentNetworkState,))

    def insertIntoUserTable(self, un, pw):
        """ Insert data into NetworkStateTable. When passing single variable into a row data must be followed by a comma, else (data1, data2, data3)

        Args:
            db (HouseDatabase Object): SQLite object store in a .db file
            currentNetworkState (String): Network node configuration as String in NiceGUI Meraid formatted https://mermaid.js.org
        """
        generatedSalt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(pw.encode('utf-8'), generatedSalt)
        
        self.cursor.execute("INSERT INTO UsersTable (username, password, salt) VALUES (?, ?, ?)", (un, hashedPassword, generatedSalt))

    def searchCountableNounsTable(self, searchTerm):
        self.cursor.execute("SELECT * FROM CountableNounsTable WHERE words LIKE ?", ('%' + searchTerm + '%',))
        results = self.cursor.fetchall()

        return results

if __name__ == "__main__":
    print("Creating new table")
    
    db = HouseDatabase()

    db.insertIntoCountableNounsTable("House")
    db.insertIntoCountableNounsTable("Dog")
    db.insertIntoUserTable("blazes.mfc.us", "TestPassword")
    
    db.commitChanges()

    databaseList = db.queryDatabase("CountableNounsTable")
    
    print(databaseList)
    password =  "TestPassword"
    usersDatabaseList = db.queryDatabase("UsersTable")
    usernameColumnNumber = 1
    passwordColumnNumber = 2
    for user in usersDatabaseList:
        if user[usernameColumnNumber] == "blaze.sanders@gentex.com":
            print(user[passwordColumnNumber])
    
    if bcrypt.checkpw(password.encode('utf-8'), usersDatabaseList[0][2]):
        print("Password matches!")
    else:
        print("Invalid password.")
    
    
    databaseSearch = db.searchCountableNounsTable("Dog")
    print(databaseSearch)

    db.closeDatabase()