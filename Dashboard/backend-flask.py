from ast import Try
from tempfile import TemporaryFile
from flask import Flask, request, jsonify,render_template
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/data")
def data():
    return render_template("dataETL.html")
    
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

@app.route("/getNewTwitterData", methods=['GET'])
def getNewTwitterData():
    try:
        stream = os.popen('python ./scriptsToPullData/twitter.py')
        output = stream.read()
        return output
    except:
        None


@app.route("/getNewTwitterSentiment", methods=['GET'])
def getNewTwitterSentiment():
    try:
        stream = os.popen('python ./SentimentScript/twitter.py')
        output = stream.read()
        return output
    except:
        None

@app.route("/getNewCryptoPriceData", methods=['GET'])
def getNewCryptoPriceData():
    try:
        stream = os.popen('python ./Dashboard/scriptsToPullData/python.py')
        output = stream.read()
        return output
    except:
        None




if __name__ == '__main__':
    # app.run(port=5001, debug=True)
    app.run(port=5002, debug=True)
    # app.run(host='0.0.0.0', port=5002, debug=True)
