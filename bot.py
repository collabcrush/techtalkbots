from flask import Flask, request
from webexteamssdk import WebexTeamsAPI
from brain import *
import os
import aiml


app = Flask(__name__)
api = WebexTeamsAPI()

####COPY START
BRAIN_FILE="brain.dump"

k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)
####COPY STOP

@app.route('/', methods=['POST'])
def simplebot():
    r = request.get_json()

    data_personId = r['data']['personId']
    data_roomId = r['data']['roomId']
    data_text = r['data']['text']

    me = api.people.me()
    if data_personId == me.id:
        return 'OK', 200
    else:
        msg=k.respond(data_text)
        api.messages.create(roomId=data_roomId, text=msg)
        return "Ok", 200


if __name__=='__main__':
    app.run(debug=True)