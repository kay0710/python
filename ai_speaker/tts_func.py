# TTS (Text to Speech)
import sys
sys.path.append("C:\\ProgramData\\Anaconda3\\envs\\ai\\Lib")
sys.path.append("C:\\ProgramData\\Anaconda3\\envs\\ai\\Lib\\site-packages")

import os
import stt_func
from gtts import gTTS
from playsound import playsound

# choose answer
def answer(input_text):
    answer_text = ''
    if '안녕' in input_text:
        answer_text = '안녕하세요? 반가워요.'
    elif '날씨' in input_text:
        answer_text = '오늘은 날이 춥네요.'
    elif '환율' in input_text:
        answer_text = '원 달러 환율은 1380원 입니다.'
    elif '고마워' in input_text:
        answer_text = '별 말씀을요.'
    elif '종료' in input_text:
        answer_text = '다음에 또 만나요.'
        stt_func.stop_listening(wait_for_stop=False) # stop listen
    else:
        answer_text = '다시 한 번 말씀해주세요.'
    speak(answer_text)

# speak (TTS)
def speak(text):
    print('[AI Speaker] ' + text)
    file_name = 'ai_speaker\\voice.mp3'
    tts = gTTS(text=text, lang='ko')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)

# file_name = 'ai_speaker\\sample.mp3'

# # English
# # sample_text = "Kay likes AI"
# # tts_en = gTTS(text=sample_text, lang='en')
# # tts_en.save(file_name)
# # playsound(file_name)

# # Korean
# # sample_text = "소린아 사랑해"
# # tts_ko = gTTS(text=sample_text, lang='ko')
# # tts_ko.save(file_name)
# # playsound(file_name)

# # long str
# with open('ai_speaker\\sample.txt', 'r', encoding='utf8') as f:
#     sample_text = f.read()

# tts_ko = gTTS(text=sample_text, lang='ko')
# tts_ko.save(file_name)
# playsound(file_name)