import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando comando...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Reconociendo...")
        query = r.recognize_google(audio, language='es-ES')
        print(f"Tú: {query}\n")
        return query.lower()
    except Exception as e:
        print("No te he entendido bien.")
        return None