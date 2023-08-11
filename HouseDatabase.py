#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.1.0"
"""

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=line-too-long
# pylint: disable=invalid-name

# Standard Python libraries
import sqlite3

# 3rd paarty libraries
import bcrypt

# Internal modules
import GlobalConstants as GC



class HouseDatabase:
    """ Store non user identifable data in local salted hash SQLite database
    """

    USERNAME_COLUMN_NUMBER = 1
    PASSWORD_COLUMN_NUMBER = 2
    SALT_COLUMN_NUMBER = 3
    FIRST_ROW_ID = 1
    BINARY_STATE_COLUMN_NUMBER = 1
    MERMAID_STRING_COLUMN_NUMBER = 1

    def __init__(self):
        """ Constructor to initialize an HouseDatabase object
        """
        # Connect to the database (create if it doesn't exist)
        self.conn = sqlite3.connect('House.db')
        self.cursor = self.conn.cursor()

        # Create four tables in House.db for user login and hardware state data storage
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UsersTable (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS LightStateTable (id INTEGER PRIMARY KEY, binaryState INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS NetworkStateTable (id INTEGER PRIMARY KEY, mermaidString TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DoorStateTable (id INTEGER PRIMARY KEY, binaryState INTEGER)''')
        
        # Create debuging logg
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DebugLoggingTable (id INTEGER PRIMARY KEY, variable TEXT)''')
        
        # Initialize hardware states
        self.cursor.execute("INSERT INTO LightStateTable (binaryState) VALUES (?)", (0,))
        self.cursor.execute("INSERT INTO NetworkStateTable (mermaidString) VALUES (?)", (GC.STATIC_DEFAULT_NETWORK,))
        self.cursor.execute("INSERT INTO DoorStateTable (binaryState) VALUES (?)", (0,))
        
        self.conn.commit()


    def commit_changes(self):
        """ Commit data inserted into a table to the .db database file 
        """
        self.conn.commit()


    def close_database(self):
        """ Close database to enable another sqlite3 instance to query this House.db database
        """
        self.conn.close()


    def query_table(self, tableName: str):
        """ Return every row of a table from a database

        Args:
            tableName (String): Name of table in database to query

        Returns:
            List: Tuples from a table, where each row in table is a tuple length n
        """
        sqlStatement = f"SELECT * FROM {tableName}"
        self.cursor.execute(sqlStatement)

        result = self.cursor.fetchall()

        return result


    def insert_network_state_table(self, currentNetworkState: str):
        """ Insert data into NetworkStateTable of database

        Args:
            currentNetworkState (String): Complete network node configuration in NiceGUI Meraid format https://mermaid.js.org
        """
        self.cursor.execute("INSERT INTO NetworkStateTable (mermaidString) VALUES (?)", (currentNetworkState,))
        self.commit_changes()


    def update_light_state_table(self, currentLightState: int):
        """ Updates the first row of the LightStateTable in database and delete new row created everytime HouseDatabase.py is run
            0 = 0b0 = All lights OFF
            15 = 0b1111 = Four lights ON
            30 = 0b11110 = Four lights ON and one light OFF
            
        Args:
            currentLightState (Integer): Current binary light state (on or off) of all lights in the house but stored as Integer
        """
        self.cursor.execute("UPDATE LightStateTable SET binaryState = ? WHERE id = ?", (currentLightState, HouseDatabase.FIRST_ROW_ID))
        self.commit_changes()


    def update_door_state_table(self, currentDoorState: int):
        """ Updates the first row of the DoorStateTable in database and delete new row created everytime HouseDatabase.py is run
            0 = 0b0 = All doors LOCKED
            1 = 0b1 = One door LOCKED lights ON
            2 = 0b10 = One door LOCKED and one door UNLOCKED
            
        Args:
            currentDoorState (Integer): Current binary door state (LOCKED or UNLOCKED) of all doors in the house but stored as Integer
        """
        self.cursor.execute("UPDATE DoorStateTable SET binaryState = ? WHERE id = ?", (currentDoorState, HouseDatabase.FIRST_ROW_ID))
        self.commit_changes()


    def insert_debug_logging_table(self, debugVariable: str):
        self.cursor.execute("INSERT INTO DebugLoggingTable (variable) VALUES (?)", (debugVariable,))
        self.commit_changes()
        

    def insert_users_table(self, username: str, pw: str):
        """ Insert username, hashed password, and hash salt into the User Table if username is unqiue, otherwise update password

        Args:
            username (String): Username to login, which can be either a 10 digit phone number or email address
            pw (String): Password to login, which is NEVER stored as plain text in any database or on a SSD (RAM only)
        """
        results = self.search_users_table(username)

        generatedSalt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(str(pw).encode('utf-8'), generatedSalt)

        if len(results) > 0:
            idToUpdate = results[0][0]
            self.cursor.execute("UPDATE UsersTable SET username = ?, password = ?, salt = ? WHERE id = ?", (username, hashedPassword, generatedSalt, idToUpdate))
        else:
            self.cursor.execute("INSERT INTO UsersTable (username, password, salt) VALUES (?, ?, ?)", (username, hashedPassword, generatedSalt))

        self.commit_changes()


    def search_users_table(self, searchTerm: str):
        """ Search UsersTable table for every occurrence of a string

        Args:
            searchTerm (str): _description_

        Returns:
            List: Of Tuples from a UsersTable, where each List item is a row in the table containing the exact search term
        """
        self.cursor.execute("SELECT * FROM UsersTable WHERE username LIKE ?", ('%' + searchTerm + '%',))
        results = self.cursor.fetchall()

        return results


    def verify_password(self, enteredUsername: str, enteredPassword: str) -> bool:
        """Vefify if username (phone number or email address) and password match 

        Args:
            enteredUsername (String): Santizied username input by a user into a GUI textbox
            enteredPassword (String): Raw password input by a user into a GUI textbox

        Returns:
            bool: True if salted hash password in database matches the password entered by the user, False otherwise
        """
        usersTableList =  self.query_table("UsersTable")
        isUserFound = False
        for user in usersTableList:
            if user[HouseDatabase.USERNAME_COLUMN_NUMBER] == enteredUsername:
                isUserFound = True

                storedHashedPassword = user[HouseDatabase.PASSWORD_COLUMN_NUMBER]
                storedSalt = user[HouseDatabase.SALT_COLUMN_NUMBER]
                hashedPasssword = bcrypt.hashpw(enteredPassword.encode('utf-8'), storedSalt)

                if hashedPasssword == storedHashedPassword:
                    return True
                else:
                    return False
            else:
                isUserFound = isUserFound or False


if __name__ == "__main__":
    print("Testing HouseDatabase.py")

    db = HouseDatabase()

    db.update_light_state_table(4)
    db.update_door_state_table(2)
    db.insert_network_state_table(GC.STATIC_DEFAULT_NETWORK)

    db.insert_users_table("blazes@mfc.us", "TestPassword")
    db.insert_users_table("blazes@mfc.us", "NewPassword")  # Test that duplicate usernames creates new password

    if db.verify_password("blazes@mfc.us", "NewPassword"):
        print("Salted hash password matches username")

    if not db.verify_password("blazes@mfc.us", "Bad"):
        print("As expected the password did NOT match username")

    databaseSearch = db.search_users_table("blazes@mfc.us")
    if len(databaseSearch) > 0:
        print("Found username in database")


    db.close_database()
    