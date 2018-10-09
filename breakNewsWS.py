#!flask/bin/python
from flask import Flask, jsonify
import breakNewsLib

app = Flask(__name__)

@app.route('/')
def index():
    return "Not suppose to see this..."

@app.route('/startSpeech')
def startSpeech():
    reply = breakNewsLib.startSpeech()
    #return reply
    return jsonify({'result': reply})

if __name__ == '__main__':
    app.run(debug=True)