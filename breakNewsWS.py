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
	if not request.args.get('sessionId'):
		reply = breakNewsLib.startSpeech()
	else:
		reply = breakNewsLib.startSpeech(request.args.get('sessionId'))
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

@app.route('/sendBot')
def sendBot():
	logging.debug(request.args)
	reply = breakNewsLib.sendBot(request.args.get('text'))
	#return jsonify({'result': reply})
	return jsonify(reply)

if __name__ == '__main__':
	app.run(debug=True)