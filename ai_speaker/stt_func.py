# STT (Speech to Text)
import sys
sys.path.append("C:\\ProgramData\\Anaconda3\\envs\\ai\\Lib")
sys.path.append("C:\\ProgramData\\Anaconda3\\envs\\ai\\Lib\\site-packages")

import tts_func
import speech_recognition as sr

def listen(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language='ko')
        print('[Me] ' + text)
        tts_func.answer(text)
    except sr.UnknownValueError:
        print("Recognition Error")
    except sr.RequestError as e:
        print("Request Error: {0}".format(e)) # API key Error // Network Error

r = sr.Recognizer()
m = sr.Microphone()

stop_listening = r.listen_in_background(m, listen)

# # Audio from Microphone
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print('I am listening now.')
#     audio = r.listen(source)

# # Audio from file (wav, aiff, flac) // mp3 - impossible
# # r = sr.Recognizer()
# # with sr.AudioFile('sample.wav') as source:
# #     audio = r.record(source)

# # try & exception
# try:
#     # Google API - 50 times/day is allowed
#     # English
#     # text = r.recognize_google(audio, language='en-US')
#     # print(text)

#     # Korean
#     text = r.recognize_google(audio, language='ko')
#     print(text)

# except sr.UnknownValueError:
#     print("Recogition Error")
# except sr.RequestError as e:
#     print("Request Error: {0}".format(e)) # API key Error // Network Error

