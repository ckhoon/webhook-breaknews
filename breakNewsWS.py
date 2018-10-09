#!flask/bin/python
from flask import Flask, redirect, url_for, request, jsonify
import logging
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

@app.route('/talk/<text>')
def talk(text):
		breakNewsLib.talk(text)
		return jsonify({'result': 'true'})
@app.route('/speak')
def speak():
		logging.debug(request.args)
		breakNewsLib.talk(request.args.get('text'))
		return jsonify({'result': 'true'})

if __name__ == '__main__':
    app.run(debug=True)