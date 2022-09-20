import requests
import json
from JDatabase import JsonDatabase

jdb = JsonDatabase('database')
jdb.check_create()
jdb.load()

def parse(urls, username):
    getUser = jdb.get_user(username)
    link = urls
    channelId = getUser['channelid']
    if getUser['xdlink'] == 1:
        if getUser['channelid'] == 0:
            requrl = 'https://xd-core-api.onrender.com/xdlinks/encode'
            jsondata = {"channelId":"","urls":link}
            headers = {"Content-type":"application/json"}
            resp = requests.post(requrl,data=json.dumps(jsondata),headers=headers)
            return parsejson(resp.text)
        else:
            requrl = 'https://xd-core-api.onrender.com/xdlinks/encode'
            jsondata = {"channelId":channelIdd,"urls":link}
            headers = {"Content-type":"application/json"}
            resp = requests.post(requrl,data=json.dumps(jsondata),headers=headers)
            return parsejson(resp.text, username)
    elif getUser['xdlink'] == 0:
        pass

def parsejson(json, username):
    getUser = jdb.get_user(username)
    data = {}
    tokens = str(json).replace('{','').replace('}','').split(',')
    for t in tokens:
        split = str(t).split(':',1)
        data[str(split[0]).replace('"','')] = str(split[1]).replace('"','')
    return data['data']