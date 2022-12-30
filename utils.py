import json
from bs4 import BeautifulSoup
from datetime import datetime

def load_json(filename, default = ["-1"]):
    
    try:
        with open(filename,'r') as json_file:
            data = json.loads(json_file.read())
            return data
    except FileNotFoundError:
        
        print("{} not found. Creating a new {}".format(filename,filename))
        save_json(default,filename)
        load_json(filename)
        

def save_json(data, filename):

    try:
        with open(filename,'w') as fp:
            fp.write(json.dumps(data))
    except:
        print(data)
        
def update_json(data, filename):
    
    try:
        with open(filename,'r') as json_file:
            old_data = json.loads(json_file.read())
            old_data.append(data)
            save_json(old_data,filename)
    except FileNotFoundError as FE:
        
        print("{} not found. Creating a new {}".format(filename,filename))
        save_json([data],filename)
    
    except JSONDecodeError as JE:
        print("Unable to read and save file.")

    

           
    
def decode_bits(body, encoding = 'utf-8'):
    
    try:
        return 1, body.decode(encoding)
    except:
        return 0, None
    


def clean_body(html):
    
    text = ""
    for encoding in ['utf-8','utf-16','utf-32']:
        flag, text = decode_bits(html, encoding)
        
        if flag == 1 and text != None:
            break
    try:

        text = BeautifulSoup(text, 'html.parser')
        #text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http+?", " ", text.text)
        text = text.text
        text = " ".join(text.split())
    except: 
        return str(html)[2:-1]
    
    return text

def format_date(date):
    
    if date[:3].isalpha():
        return datetime.strptime(date[:25], '%a, %d %b %Y %H:%M:%S')
    
    else:
        return datetime.strptime(date[:20], '%d %b %Y %H:%M:%S')
    
    
    
        
