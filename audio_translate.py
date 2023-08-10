from vosk import Model, KaldiRecognizer, SetLogLevel
import pyaudio
import wave
import json
from googletrans import Translator #had to pip install googletrans==4.0.0-rc1 for translation to work 

RATE= 16000
CHUNK = 4096

model= Model(r"/Users/azhou924/Downloads/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, RATE)
recognizer.SetWords(True)

def translate(text):
        translator = Translator()
        outputs = translator.translate(text, src="en", dest="ko")
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
        if len(r) != 1:
            if len(r['text']) != 1:
                out = out + [' '] + [r['text']]
print(out)


#Using classes 
# class TransformAudio():
#     def __init__(self, transcribe_path):
#         self.classifier = Model(transcribe_path)
#         self.recognizer = KaldiRecognizer(self.classifier, RATE)
#         #self.translate_models = TFMarianMTModel.from_pretrained(translate_path)
#         #self.translate_tok = MarianTokenizer.from_pretrained(translate_path)
#         self.translator = Translator() 

#     def translate(self,text):
#         #batch = self.translate_tok(text, return_tensors="tf")
#         #gen = self.translate_models.generate(**batch)
#         #outputs= self.translate_tok.batch_decode(gen, skip_special_tokens=True)
#         outputs = self.translator.translate(text, src="en", dest="en")
#         return outputs

# audio_translator = TransformAudio(r"/Users/azhou924/Downloads/vosk-model-small-en-us-0.15")