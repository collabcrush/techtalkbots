from flask import Flask, request
from webexteamssdk import WebexTeamsAPI
from brain import *
import re
import random


app = Flask(__name__)
api = WebexTeamsAPI()

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
        processed=re.sub('[^\w\s]','',data_text.lower())
        msg=brain.get(processed, random.choice(catchall))
        api.messages.create(roomId=data_roomId, text=msg)
        return "Ok", 200


if __name__=='__main__':
    app.run(debug=True)