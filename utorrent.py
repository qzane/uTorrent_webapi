import requests
import json

'''
test with uTorrent 1.8.5 and python 3.4
utorrent API according to:
http://help.utorrent.com/customer/en/portal/topics/664593-web-api/articles?b_id=3883
'''

def init():
    global OPENER
    global IP,PORT,USERNAME,PASSWD,HASH
    global URL_LIST
    global URL_ADD_FILE
    global URL_START
    
    OPENER = requests.session()
    
    #these info below should be changed 
    IP='127.0.0.1'
    PORT='8080'
    USERNAME='username'
    PASSWD='passwd'
    #these info above should be changed 
    
    HASH='' #none
    
    #cmd list:
    
    URL_LIST = r"http://[IP]:[PORT]/gui/?list=1"
    #To get the list of all torrents
    
    URL_ADD_FILE = r"HTTP://[IP]:[PORT]/GUI/?ACTION=ADD-FILE"
    # This action is different from the other actions in that it uses HTTP POST 
    # instead of HTTP GET to submit data to BitTorrent. The HTTP form must use 
    # an enctype of "multipart/form-data" and have an input field of type "file" 
    # with name "torrent_file" that stores the local path to the file to upload to BitTorrent.

    URL_START = r"HTTP://[IP]:[PORT]/GUI/?ACTION=START&HASH=[TORRENT HASH]"
    #This action tells BitTorrent to start the specified torrent job(s). 
    #Multiple hashes may be specified to act on multiple torrent jobs.
 
init() 

def set_info(ip,username,passwd,port='8080'):
    global IP,PORT,USERNAME,PASSWD
    IP=str(ip)
    PORT=str(port)
    USERNAME=str(username)
    PASSWD=str(passwd)    
    
def get_cmd(cmd):
    return cmd.replace(r'[IP]',IP).replace(r'[PORT]',PORT).replace(r'[TORRENT HASH]',HASH).lower()
    
def send_cmd(cmd):
    return OPENER.get(get_cmd(cmd),auth=(USERNAME,PASSWD))
    
def add_torrent(bfile):
    '''bfile:binary torrent_file'''
    url = get_cmd(URL_ADD_FILE)
    res = OPENER.post(url,auth=(USERNAME,PASSWD),files={'torrent_file':bfile})
    if res.text.find('error')==-1:
        return 0
    else:
        print(res.text)
        return 1
        
def add_and_start(bfile):
    '''bfile:binary torrent_file'''
    global HASH
    ulist = send_cmd(URL_LIST)
    data = json.loads(ulist.content.decode('utf-8'))   
    old = set(map(lambda x:str(x[0]),data['torrents']))
    
    if add_torrent(bfile) !=0:
        print('add file failed')
        return 1
    
    
    ulist = send_cmd(URL_LIST)
    data = json.loads(ulist.content.decode('utf-8'))   
    new = set(map(lambda x:str(x[0]),data['torrents']))
    
    HASH = list(new.difference(old))[0]
    
    res = send_cmd(URL_START)
    
    return 0
    
