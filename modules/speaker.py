import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) 

def talk(text):
    print(f"Yeny: {text}")
    engine.say(text)
    engine.runAndWait()