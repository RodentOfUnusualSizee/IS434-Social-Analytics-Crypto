from ast import Try
from tempfile import TemporaryFile
from flask import Flask, request, jsonify
import os
app = Flask(__name__)


@app.route("/test", methods=['GET'])
def test():
    try:
        stream = os.popen('cd')
        output = stream.read()
        return output
    except:
        None

@app.route("/getNewDiscordData", methods=['GET'])
def getNewDiscordData():
    try:
        stream = os.popen('python ./scriptsToPullData/discord.py')
        output = stream.read()
        return output
    except:
        None


@app.route("/getNewDiscordSentiment", methods=['GET'])
def getNewDiscordSentiment():
    try:
        stream = os.popen('python ./SentimentScript/discord.py')
        output = stream.read()
        return output
    except:
        None



if __name__ == '__main__':
    # app.run(port=5001, debug=True)
    app.run(host='0.0.0.0', port=5002, debug=True)
