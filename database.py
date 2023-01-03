import sqlite3
from sqlite3 import Error
import re


class UserDatabase:

    def __init__(self):

        self.conn = self.create_connection("/Users/ram/Desktop/ApplicationTracker/database.db")
        self.curr = self.conn.cursor()
        print('Checking if table mailbox exists:')
        listOfTables = self.curr.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
        AND name='MAILBOX'; """).fetchall()
        
        if listOfTables == []:
            print('Table not found!')
            sql_create_MAILBOX = """CREATE TABLE IF NOT EXISTS MAILBOX (
                                    id integer PRIMARY KEY,
                                    mailbox_id text,
                                    name text NOT NULL,
                                    email text NOT NULL,
                                    subject text,
                                    date text,
                                    body text,
                                    html text
                                );"""

            self.create_table(sql_create_MAILBOX)
        else:
            print('Table found!')
        


    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                print("Connection Successful")
                return conn

    def create_table(self, create_table_sql):
   
        try:
            #c = self.conn.cursor()
            self.curr.execute(create_table_sql)
            print("Table Created")
            self.conn.commit()
        except Error as e:
            print(e, "Table not created.")

    def update_mailbox(self, data):

        #Add code to validate input
        for i in ['id','from','subject','date','body','html']:
            if i in data:
                if i == "from":
                    
                    email = re.findall('\S+@\S+', data['from'])
                    email[0] = email[0][1:-1]
                    regex = "\<(.+?)\>"
                    name = re.sub(regex, "", data['from'])
                continue
            else:
                data[i] = None

        try:
    
            sqlite_insert_with_param = """INSERT INTO MAILBOX
                            (mailbox_id, name, email, subject, date, body, html) 
                            VALUES (?, ?, ?, ?, ?, ?, ?);"""

            #for i in ['id','from']:
            #    print(i, data[i], type(data[i]))
            #    print("#########################")
            #    print("###") 
            #print(name, email[0])
            data_tuple = (data["id"], name, email[0], data["subject"], data["date"], data["body"], data["html"])
            self.curr.execute(sqlite_insert_with_param, data_tuple)
            self.conn.commit()
            #print("Python Variables inserted successfully into SqliteDb_developers table")


        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)


    