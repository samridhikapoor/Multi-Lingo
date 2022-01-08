#importingg required modules
from gtts import gTTS
import playsound
import os

#Converting text to speech
#Using gtts and playing it with playsound
def nischay(text,lang):
    ivu=gTTS(text=text ,lang=lang, slow= False)
    filename="voice.mp3"
    ivu.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
