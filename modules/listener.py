import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando comando...")
        # Aumentamos el umbral de energía para filtrar ruido.
        # 300 es un buen punto de partida, puedes subirlo si hay mucho ruido.
        r.energy_threshold = 300
        
        r.pause_threshold = 1
        # Comentamos esta línea porque ya fijamos el umbral manualmente
        # r.adjust_for_ambient_noise(source, duration=1) 
        audio = r.listen(source)
    try:
        print("Reconociendo...")
        query = r.recognize_google(audio, language='es-ES')
        print(f"Tú: {query}\n")
        return query.lower()
    except Exception as e:
        print("No te he entendido bien.")
        return None