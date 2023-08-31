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

# 3rd party libraries
import bcrypt
# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values 
    
# Internal modules
import GlobalConstants as GC

class HouseDatabase:
    """ Store non user identifable data in local salted hash SQLite database
    """
    USERNAME_COLUMN_NUMBER = 1
    PASSWORD_COLUMN_NUMBER = 2
    SALT_COLUMN_NUMBER = 3
    STATE_COLUMN_NUMBER = 1
    LEVEL_COLUMN_NUMBER = 1
    MERMAID_STRING_COLUMN_NUMBER = 1

    def __init__(self, dbName='House.db'):
        """ Constructor to initialize a HouseDatabase object
            Call db = HouseDatabase('Test.db') for testing
        
        Args:
            dbName (String): Filename of SQlite database, defaults to 'House.db'   
        """
        # Connect to the database
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()
        
        # Check if tables exist (using UserTable as placeholder for all tables) 
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='UsersTable'")
        if not self.cursor.fetchone():
            
            # Create four tables in House.db for user login and hardware state storage
            self.cursor.execute('''CREATE TABLE UsersTable (id INTEGER PRIMARY KEY, username TEXT, password TEXT, salt TEXT)''')
            self.cursor.execute('''CREATE TABLE LightStateTable (id INTEGER PRIMARY KEY, currentState INTEGER)''')
            self.cursor.execute('''CREATE TABLE LightLevelTable (id INTEGER PRIMARY KEY, currentLevel REAL)''')
            self.cursor.execute('''CREATE TABLE FanStateTable (id INTEGER PRIMARY KEY, currentState INTEGER)''')
            self.cursor.execute('''CREATE TABLE FanLevelTable (id INTEGER PRIMARY KEY, currentLevel REAL)''')
            self.cursor.execute('''CREATE TABLE DoorStateTable (id INTEGER PRIMARY KEY, currentState INTEGER)''')
            self.cursor.execute('''CREATE TABLE NetworkStateTable (id INTEGER PRIMARY KEY, mermaidString TEXT)''')

            self.init_tables()
        
            # Create debuging logg
            self.cursor.execute('''CREATE TABLE DebugLoggingTable (id INTEGER PRIMARY KEY, variable TEXT)''')
            
        self.commit_changes()
    
    
    def init_tables(self):
        """ Initialize database for the hardware installed  
        """
        config = dotenv_values()
        username = config['DATABASE_ADMIN_USERNAME']
        password = config['DATABASE_ADMIN_PASSWORD']
        self.insert_users_table(username, password)
        
        for id in range(GC.MAX_LIGHT_BIT_LENGTH):
            self.cursor.execute("INSERT INTO LightStateTable (currentState) VALUES (?)", (GC.ON_STATE,))
            self.cursor.execute("INSERT INTO LightLevelTable (currentLevel) VALUES (?)", (GC.OFF,))
            
        for id in range(GC.MAX_FAN_BIT_LENGTH):
            self.cursor.execute("INSERT INTO FanStateTable (currentState) VALUES (?)", (GC.OFF_STATE,))
            self.cursor.execute("INSERT INTO FanLevelTable (currentLevel) VALUES (?)", (GC.OFF,))           
            
        for id in range(GC.MAX_NUM_OF_DOORS):
            self.cursor.execute("INSERT INTO DoorStateTable (currentState) VALUES (?)", (GC.DOOR_UNLOCKED,))
            
        self.cursor.execute("INSERT INTO NetworkStateTable (mermaidString) VALUES (?)", (GC.STATIC_DEFAULT_NETWORK,))
        
        self.commit_changes()


    def commit_changes(self):
        """ Commit data inserted into a table to the .db database file 
        """
        self.conn.commit()


    def close_database(self):
        """ Close database to enable another sqlite3 instance to query this House.db database
        """
        self.conn.close()


    def query_table(self, tableName: str) -> tuple:
        """ Return every row of a table from a database

        Args:
            tableName (String): Name of table in database to query

        Returns:
            List: Tuples from a table, where each row in table is a tuple length n
        """
        sqlStatement = f"SELECT * FROM {tableName}"
        self.cursor.execute(sqlStatement)

        foundRow = True
        result = self.cursor.fetchall()
        if len(result) == 0:
            foundRow = False

        return result, foundRow


    def update_light_state_table(self, newLightState: int):
        """ Update every row of LightStateTable in database and backfill in ZERO's start at Most Significant Bit
            0  = 0b0000_0000 = All lights OFF
            15 = 0b0000_1111 = Four lights ON and one light OFF in house with 5 total lights
            30 = 0b0001_1110 = Four lights ON and one light OFF in house with 5 total lights
            
        Args:
            newLightState (Integer): New binary light state (on or off) of all lights in the house (e.g. 7 = 0b000_0111)
        """
        position = 0  
        if newLightState == 0 or newLightState >= 2**GC.MAX_LIGHT_BIT_LENGTH:
            self.cursor.execute("UPDATE LightStateTable SET currentState = 0")
        else:
            # Start with Least Significant Bit (LSB) and right shift currentLightState integer one bit until only zero bits are left
            shiftingLightState = newLightState
            while shiftingLightState:
                bit = shiftingLightState & 1
                position = position + 1
                self.cursor.execute("UPDATE LightStateTable SET currentState = ? WHERE id = ?", (bit, position))
                shiftingLightState >>= 1

            # Back fill in rest on database ID's with ZERO'S if currentLightState < 256 = 2^GC.MAX_LIGHT_BIT_LENGTH = 2^8
            if position < GC.MAX_LIGHT_BIT_LENGTH:
                for id in range(position+1, GC.MAX_LIGHT_BIT_LENGTH+1):
                    self.cursor.execute("UPDATE LightStateTable SET currentState = ? WHERE id = ?", (0, id))
            
        self.commit_changes()


    def update_light_level_table(self, id: int, newLightLevel: float):
        """ Update LightLevelTable in database using a GlobalConstants.py CONSTANT 
            
        Args:
            id (Integer): Primary key in LightLevelTable to update 
            newLightevel (Float): New light brightness level (OFF, LOW, MEDIUM, HIGH) for a single light
        """
        self.cursor.execute("UPDATE LightLevelTable SET currentLevel = ? WHERE id = ?", (newLightLevel, id))
        self.commit_changes()


    def update_fan_state_table(self, newwFanState: int):
        """ Update every row of FanStateTable in database and backfill in ZERO's start at Most Significant Bit
            0  = 0b0000_0000 = All fans OFF
            15 = 0b0000_1111 = Four lights ON and four light OFF in house with 8 total fans
            30 = 0b1111_1110 = Seven lights ON and one light OFF in house with 8 total fans
            
        Args:
            newLightState (Integer): New binary fan state (on or off) of all fans in the house (e.g. 8 = 0b000_1000)
        """
        position = 0  
        if newwFanState == 0 or newwFanState >= 2**GC.MAX_FAN_BIT_LENGTH:
            self.cursor.execute("UPDATE FanStateTable SET currentState = 0")
        else:
            # Start with Least Significant Bit (LSB) and right shift newwFanState integer one bit until only zero bits are left
            shiftingFanState = newwFanState
            while shiftingFanState:
                bit = shiftingFanState & 1
                position = position + 1
                self.cursor.execute("UPDATE FanStateTable SET currentState = ? WHERE id = ?", (bit, position))
                shiftingFanState >>= 1

            # Back fill in rest on database ID's with ZERO'S if currentLightState < 256 = 2^GC.MAX_LIGHT_BIT_LENGTH = 2^8
            if position < GC.MAX_FAN_BIT_LENGTH:
                for id in range(position+1, GC.MAX_FAN_BIT_LENGTH+1):
                    self.cursor.execute("UPDATE FanStateTable SET currentState = ? WHERE id = ?", (0, id))
            
        self.commit_changes()


    def update_fan_level_table(self, id: int, newFanLevel: float):    
        """ Update FanLevelTable in database using a GlobalConstants.py CONSTANT 
            
        Args:
            id (Integer): Primary key in FanLevelTable to update 
            newFanLevel (Float): New fan rotation speed (OFF, LOW, MED, HIGH) for a single fan
        """
        self.cursor.execute("UPDATE FanLevelTable SET currentLevel = ? WHERE id = ?", (newFanLevel, id))
        self.commit_changes()


    def update_door_state_table(self, id: int, newDoorState: bool):
        """ Update DoorStateTable in database using a GlobalConstants.py CONSTANT
            
        Args:
            newDoorState (Boolean): New door state (DOOR_UNLOCKED or DOOR_LOCKED) for a single door
        """
        self.cursor.execute("UPDATE DoorStateTable SET currentState = ? WHERE id = ?", (newDoorState, id))
        self.commit_changes()


    def insert_debug_logging_table(self, debugVariable: str):
        self.cursor.execute("INSERT INTO DebugLoggingTable (variable) VALUES (?)", (debugVariable,))
        self.commit_changes()
        
    
    def insert_network_state_table(self, newNetworkState: str):
        """ Insert data into NetworkStateTable of database

        Args:
            newNetworkState (String): Complete network node configuration in NiceGUI Meraid format https://mermaid.js.org
        """
        self.cursor.execute("INSERT INTO NetworkStateTable (mermaidString) VALUES (?)", (newNetworkState,))
        self.commit_changes()
        

    def insert_users_table(self, username: str, pw: str):
        """ Insert username, hashed password, and hash salt into the User Table if username is unqiue, otherwise update password

        Args:
            username (String): Username to login, which can be either a 10 digit phone number or email address
            pw (String): Password to login, which is NEVER stored as plain text in any database or on a SSD (RAM only)
        """
        results, foundUser = self.search_users_table(username)

        generatedSalt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(str(pw).encode('utf-8'), generatedSalt)

        if foundUser:
            idToUpdate = results[0][0]
            self.cursor.execute("UPDATE UsersTable SET username = ?, password = ?, salt = ? WHERE id = ?", (username, hashedPassword, generatedSalt, idToUpdate))
        else:
            self.cursor.execute("INSERT INTO UsersTable (username, password, salt) VALUES (?, ?, ?)", (username, hashedPassword, generatedSalt))

        self.commit_changes()


    def search_users_table(self, searchTerm: str) -> tuple:
        """ Search UsersTable table for every occurrence of a string

        Args:
            searchTerm (str): _description_

        Returns:
            List: Of Tuples from UsersTable, where each List item is a row in the table containing the exact search term
        """
        foundUser = False
        self.cursor.execute("SELECT * FROM UsersTable WHERE username LIKE ?", ('%' + searchTerm + '%',))
        results = self.cursor.fetchall()
        if len(results) > 0:
            foundUser = True
        
        return results, foundUser


    def verify_password(self, enteredUsername: str, enteredPassword: str) -> bool:
        """Vefify if username (phone number or email address) and password match 

        Args:
            enteredUsername (String): Santizied username input by a user into a GUI textbox
            enteredPassword (String): Raw password input by a user into a GUI textbox

        Returns:
            bool: True if salted hash password in database matches the password entered by the user, False otherwise
        """
        usersTableList, foundData =  self.query_table("UsersTable")
        isUserFound = False
        for user in usersTableList:
            if foundData:
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
    print("Testing HouseDatabase.py with asserts")

    db = HouseDatabase('Test.db')

    db.update_light_state_table(0b1100)
    db.update_light_level_table(4, GC.MEDIUM)
    db.update_fan_state_table(0b10111)
    db.update_fan_level_table(2, GC.LOW)
    db.update_door_state_table(1, GC.DOOR_LOCKED)
    db.insert_network_state_table(GC.STATIC_DEFAULT_NETWORK)
    db.insert_debug_logging_table("Testing debug logging")

    db.insert_users_table("blazes@mfc.us", "TestPassword")
    db.insert_users_table("blazes@mfc.us", "NewPassword")  # Test that duplicate usernames creates new password
    databaseSearch, foundUser = db.search_users_table("blazes@mfc.us")
    
    assert foundUser, "Search for know username in database failed"
    assert db.verify_password("blazes@mfc.us", "NewPassword"), "Password salted hashing failed"
    assert not db.verify_password("blazes@mfc.us", "BadPassword"), "Password salted hashing failed"

    db.close_database()
    