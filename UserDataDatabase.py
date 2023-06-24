import sqlite3
from pysqlitecipher import sqlitewrapper
from dotenv import dotenv_values    # Load environment variables for things usernames, passwords, and API keys

import bcrypt

import GlobalConstants as GC

STATIC_DEFAULT_NETWORK = '''
                graph LR;
                    A[UniFi PoE Switch] --> B[ROOM: Master Bedroom];
                    A[UniFi PoE Switch] --> F[ZimaBoard Server];
                    F[CPU: ZimaBoard Server] --> E[DISPLAY: Main Central Control];
                    B[ROOM: Master Bedroom] --> C[LIGHT: Master Bedroom]; 
                    B[ROOM: Master Bedroom] --> D[DISPLAY: Master Bedroom];
                    A[UniFi PoE Switch] --> G[LIGHT-Kitchen];
                    
                    style A color:#000000, fill:#03C04A, stroke:#000000;
                    style B color:#000000, fill:#03COFF, stroke:#000000;
                    style C color:#000000, fill:#FFC04A, stroke:#000000;
                    style D color:#FFFFFF, fill:#1F1F1F, stroke:#000000;
                    style E color:#FFFFFF, fill:#1F1F1F, stroke:#000000;
                    style F color:#000000, fill:#B8191D, stroke:#000000;
                    style G color:#000000, fill:#FFC04A, stroke:#000000;
                '''


class UserDataDatabase:

    def __init__(self):
        # Connect to the database (create if it doesn't exist)
        self.conn = sqlite3.connect('UserData.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS CountableNounsTable (id INTEGER PRIMARY KEY, words TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UsersTable  (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS NetworkStateTable (id INTEGER PRIMARY KEY, mermaidString TEXT)''')

        # https://medium.com/@harshnative/encrypting-sqlite-database-in-python-using-pysqlitecipher-module-23b80129fda0
        sqliteWrapperEnvironmentVariables = dotenv_values()
        sqliteWrapperPassword = sqliteWrapperEnvironmentVariables['SQLITE_WRAPPER_PASSWORD']
        
        self.obj = sqlitewrapper.SqliteCipher(dataBasePath="UserData.db", checkSameThread=False, password=sqliteWrapperPassword)
        
        try:
            self.obj.createTable("encrytedUsersTable" , ["username", "password", "salt"], makeSecure=True , commit=True)
            #self.obj.createTable("unencrytedUsersTable", ["username", "password", "salt"], makeSecure=False , commit=True)
        except ValueError:
            pass
            print("DO NOTHING encryted table already exists")
            
            
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
        #self.cursor.execute("SELECT * FROM UsersTable WHERE username LIKE ?", ('%' + un + '%',))
        #results = self.cursor.fetchall()
        
        colList, results  = db.obj.getDataFromTable("encrytedUsersTable" , raiseConversionError = True , omitID = False)
        print(results)
        
        isUserFound = False
        for user in usersDatabaseList:
            if user[GC] == "b.sandersnv@gmail.com":
                isUserFound = True
                print(user[passwordColumnNumber])
                storedHashedPassword = user[passwordColumnNumber]
                storedSalt = user[saltColumnNumber]

                #try:
                hashedPasssword = bcrypt.hashpw(password.encode('utf-8'), storedSalt)
                
                if hashedPasssword == storedHashedPassword:
                    print("Password matches!")
                else:
                    print("Invalid password.")
            else:
                isUserFound = isUserFound or False

        print(isUserFound)
        
        
        
        if len(results) > 0:
            pass #Ignore repeat username and DO NOTHING
        else:
            generatedSalt = bcrypt.gensalt()
            hashedPassword = bcrypt.hashpw(pw.encode('utf-8'), generatedSalt)
            
            #self.cursor.execute("INSERT INTO UsersTable (username, password, salt) VALUES (?, ?, ?)", (un, hashedPassword, generatedSalt))
            self.obj.insertIntoTable("encrytedUsersTable" , [un, hashedPassword, generatedSalt], commit = True)

    def searchCountableNounsTable(self, searchTerm):
        self.cursor.execute("SELECT * FROM CountableNounsTable WHERE words LIKE ?", ('%' + searchTerm + '%',))
        results = self.cursor.fetchall()

        return results

if __name__ == "__main__":
    print("Creating new table")
    
    db = HomeDatabase()

    #db.insertIntoNetworkStateTable(STATIC_DEFAULT_NETWORK)
    #db.closeDatabase()
    db.insertIntoUserTable("blaze.sanders@gentex.com", "GentexPassword")
    db.insertIntoUserTable("blazes.d.a.sanders@gmail.com", "TestPassword")
    db.insertIntoUserTable("b.sanders.nv@gmail.com", "BadPassword")
    
    db.commitChanges()
    
    password =  "BadPassword"
    usernameColumnNumber = 1
    passwordColumnNumber = 2
    saltColumnNumber = 3
       
    #databaseSearch = db.searchCountableNounsTable("Dog")
    #print(databaseSearch)
    #db.obj.insertIntoTable("unencrytedUsersTable" , ["blaze.d.a.sanders@gmail.com", "Password", "Salt"], commit = True)
    db.obj.insertIntoTable("encrytedUsersTable" , ["blaze.d.a.sanders@gmail.com", "12345678", "wl2k45!"], commit = True)
    
    
    blazeUser = db.obj.getDataFromTable("encrytedUsersTable" , raiseConversionError = True , omitID = False)
    #blazeUser = db.obj.getDataFromTable("unencrytedUsersTable" , raiseConversionError = True , omitID = False)
    print(blazeUser)

    db.closeDatabase()