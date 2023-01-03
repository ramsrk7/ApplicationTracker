import utils
import database
import imaplib
import email
import os
import shutil
import tempfile
import html2text
from datetime import datetime
import re
from tqdm import tqdm
import sqlite3
from sqlite3 import Error

class ApplicationTracker:

    def __init__(self):
        print("Email ID:")
        self.LOGIN_EMAIL = input()
        print("Access Token:")
        self.LOGIN_PWD = input()
        self.SMTP_PORT = 993

        self.SMTP_SERVER = "imap.gmail.com"

        print("Logging in...")
        flag = self.login()

        if flag == 1:
            print("Login Success")
        else:
            print("Login Failed")
            self.__init__()

        self.DB = database.UserDatabase()


    def login(self):

        self.m = imaplib.IMAP4_SSL(self.SMTP_SERVER, self.SMTP_PORT)
        flag = self.m.login(self.LOGIN_EMAIL, self.LOGIN_PWD)

        if flag[0] == "OK":
            self.m.select('"inbox"')
            return 1
        else:
            return 0



    def read_email(self, mail_id):
        #returns dict

        email_data = {}
        _, data = self.m.fetch(mail_id.encode('utf-8'), '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        
        email_data['id'] = mail_id
        for header in ['subject','to','from','date']:
            #print("{}: {}".format(header, email_message[header]))
            email_data[header] =  email_message[header]
        
        for part in email_message.walk():
            #print(part.get_content_type())
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html'] = html_body
        
        return email_data


    def preprocess_email(self, email_data):
        
        ##only email body. Email html body will be added laterr
        
        #email_data['date'] = format_date(email_data['date']).date()
        
        
        if "body" in email_data:
            email_data['body'] = utils.clean_body(email_data['body'])
        if "html_body" in email_data:
            email_data['html'] = utils.clean_body(email_data['html'])
        
        return email_data

    def check_new_email(self):
        _, search_data = self.m.search(None, 'ALL')

        ## Get Checkpoint

        try:
            checkpoint = self.DB.curr.execute('SELECT mailbox_id FROM MAILBOX').fetchall()
        except:
            checkpoint = []


        search_data = search_data[0].decode().split()[::-1] 
        
        if checkpoint == None:
            curr = 0
        else:
            curr = len(checkpoint)
        
        ##check if the current id is in checkpoint
        print("Old emails:",curr)
        print("New emails:", len(search_data) - curr)
        #search_data = list(set(search_data) - set(checkpoint))
        #search_data = [i for i in search_data if i not in checkpoint]
        sqlite_select_query = """SELECT mailbox_id from MAILBOX where mailbox_id = ?"""
        print(search_data[:10])
        for i in tqdm(range(0,len(search_data))):
            id = search_data[i]
            

            if len(self.DB.curr.execute(sqlite_select_query,(id,)).fetchall()) == 0:
                email = self.read_email(id)
                email = self.preprocess_email(email)
                
                
                #update checkpoint and emails

                self.DB.update_mailbox(email)
                #return email
                #utils.update_json(email, "emails.txt")
                #checkpoint.append(i)
                #utils.update_json(i,"checkpoint.txt")
                #print(email['id'], email['date'])

    

def main():
    print("Welcome..")
    mail = ApplicationTracker()
    try:
        mail.check_new_email()
    except Error as e:
        print(e)
        mail.DB.curr.close()
        mail.DB.conn.close()

if __name__ == "__main__":
    main()
    

            
            