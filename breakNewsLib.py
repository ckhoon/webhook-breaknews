# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import sys
import codecs, json
import random
import time
import logging
import win32com.client as wincl
import pyttsx3
import speech_recognition as sr
import pyaudio  
import wave
import pythoncom

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
CLIENT_ACCESS_TOKEN = 'f9ccddaf4b7b47c09beb62dcb5868a35'
emotionMapping = {
    "happy" : "1",
    "shocked" : "2",
    "worried" : "3",
    "confuse" : "4"
}



def play_sound():
    #define stream chunk   
    chunk = 1024  

    #open a wav format music  
    f = wave.open(r"titi.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        logging.debug("adjusting ambient noise")
        recognizer.adjust_for_ambient_noise(source)
        play_sound()
        logging.debug("listening now")
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    logging.debug("sending to google.")
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response



def talk(text):
    logging.debug("Text to speech -> " + text)
    pythoncom.CoInitialize()
    speak = pyttsx3.init()
    speak.setProperty('rate', 150)
    voices = speak.getProperty('voices')
    speak.setProperty('voice', voices[1].id)
    speak.say(text)
    speak.runAndWait()
    speak.stop()
    return 

def startSpeech(session_id="001"):
    pythoncom.CoInitialize()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = session_id
    #speak = pyttsx3.init()
    #speak.setProperty('rate', 150)
    #voices = speak.getProperty('voices')
    #speak.setProperty('voice', voices[1].id)


    textFromSpeech = recognize_speech_from_mic(recognizer, microphone)
    play_sound()
    logging.debug("You said: {}".format(textFromSpeech["transcription"]))

    if not textFromSpeech["transcription"]:
        logging.debug("mic did not pick up anything") 
        return "mic did not pick up anything ;0;0"

    request.query = textFromSpeech["transcription"]
    logging.debug("sending to bot")
    response = request.getresponse()
    reader = codecs.getdecoder("utf-8")
    obj = json.load(response)

    replied_text = ' '
    replied_expression = '0'
    replied_value = '0'
    #logging.debug("full reply is {}".format(obj))
    logging.debug("Bot said: {}".format(obj['result']['fulfillment']['speech']))
    try:
        replied_text = obj['result']['fulfillment']['speech']
        #replied_expression = obj['result']['fulfillment']['source']
        #logging.debug("message = {}".format(obj['result']['fulfillment']['messages'][0]))
        #logging.debug("meassage 1 = {}".format(obj['result']['fulfillment']['messages'][1]['payload']['emotion']))
        replied_expression = emotionMapping.get(obj['result']['fulfillment']['messages'][1]['payload']['emotion'], "0")
        replied_value = obj['result']['fulfillment']['messages'][1]['payload']['value']
        #logging.debug("Bot source: {}".format(obj['result']['fulfillment']['source']))
    except KeyError:
        logging.debug("no source")
    except :
        return replied_text + ":" + "0" + ";" + "0" 
    
    #logging.debug("Bot show all: {}".format(obj['result']['fulfillment']))
    #speak.say(obj['result']['fulfillment']['speech'])
    #speak.runAndWait()
    #speak.stop()
    #return obj['result']['fulfillment']['speech']
    return replied_text + ":" + replied_expression + ";" + replied_value


if __name__ == '__main__':
    startSpeech()