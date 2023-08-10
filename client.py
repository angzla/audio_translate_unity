from vosk import Model, KaldiRecognizer, SetLogLevel
import pyaudio
import wave
import json
from googletrans import Translator #had to pip install googletrans==4.0.0-rc1 for translation to work 
import socket

RATE= 16000
CHUNK = 4096

model= Model(r"/Users/azhou924/Downloads/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, RATE)
recognizer.SetWords(True)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        
sock.connect(('127.0.0.1', 65432))

def translate(text):
        translator = Translator()
        outputs = translator.translate(text, src="en", dest="en")
        return outputs

#USING MIC
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
stream.start_stream()

out=[]
muteTimes = []
data = stream.read(CHUNK)
while len(data):
    print(muteTimes)
    data = stream.read(CHUNK)
    if recognizer.AcceptWaveform(data):
        r = json.loads(recognizer.Result())
        print (r)
        print(r['text'])
        translatedText= translate(r['text'])
        print(translatedText.text)
        caption = translatedText.text
        caption_bytes = caption.encode('utf-8')       
        sock.sendall(caption_bytes)
        if len(r) != 1:
            if len(r['text']) != 1:
                out = out + [' '] + [r['text']]
print(out)