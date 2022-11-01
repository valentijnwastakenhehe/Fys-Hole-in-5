import odroid_wiringpi as wpi
from gtts import gTTS

text_to_speech = "My life sucks"

language = "en"

myobj = gTTS(text=text_to_speech, lang=language, slow=False)

myobj.save("text_to_speech.mp3")
