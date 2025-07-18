import struct
import pvporcupine
import pyaudio
from modules.speaker import talk
from modules.listener import listen
import modules.actions as actions
import re

def run_yeny():
    """Bucle principal que escucha la palabra de activación y luego los comandos."""

    ACCESS_KEY = "/XDnOtU4HxQ2opd2UQ5dlUytQC+9D+aEXk3BGIJiJgMhhcqhry/5CA=="
    
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=['wake-word/Maria_es_windows_v3_0_0.ppn'],
            model_path='wake-word/porcupine_params_es.pv'
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print("Esperando la palabra de activación ('Maria')...")
        talk("Sistema iniciado. Esperando activación.")

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Palabra de activación 'Maria' detectada.")
                talk("Sí, dígame.")
                
                command = listen()
                if command:
                    if 'adiós' in command or 'apágate' in command:
                        talk("Entendido. Desconectando.")
                        break 
                    
                    executed = False

                    # Comandos de búsqueda
                    if 'busca' in command or 'wikipedia' in command:
                        query = command.replace('busca en wikipedia sobre', '').replace('busca sobre', '').replace('busca', '').strip()
                        if query:
                            actions.search_wikipedia(query)
                        else:
                            talk("No entendí qué quieres buscar.")
                        executed = True

                    # Comandos de abrir aplicaciones/webs
                    elif 'abrir' in command:
                        if 'brave' in command:
                            actions.open_brave()
                        else:
                            match = re.search(r'abrir (\S+)', command)
                            site = match.group(1).replace('.com', '') + '.com' if match else "google.com"
                            actions.open_browser(site)
                        executed = True

                    # Comandos de control del sistema
                    elif 'volumen' in command:
                        if 'sube' in command: actions.set_volume("subir")
                        elif 'baja' in command: actions.set_volume("bajar")
                        elif 'silencio' in command: actions.set_volume("silencio")
                        executed = True
                    
                    elif 'brillo' in command:
                        match = re.search(r'(\d+)', command)
                        if match:
                            level = int(match.group(1))
                            actions.set_brightness(level)
                        else:
                            talk("No entendí a qué nivel ajustar el brillo.")
                        executed = True
                    
                    # Comandos de YouTube (CORREGIDO)
                    elif 'youtube' in command:
                        if 'siguiente' in command:
                            actions.control_youtube('siguiente')
                        elif 'anterior' in command:
                            actions.control_youtube('anterior')
                        elif 'pausa' in command:
                            actions.control_youtube('pausa')
                        elif 'ponle play' in command or 'reanudar' in command:
                            actions.control_youtube('play')
                        executed = True
                        
                    # Comandos de información
                    elif 'qué hora es' in command:
                        actions.tell_time()
                        executed = True
                    
                    elif 'qué día es hoy' in command:
                        actions.tell_date()
                        executed = True
                    
                    # Si ningún comando coincide
                    if not executed:
                        talk("No he entendido ese comando.")

                print("Esperando la palabra de activación ('Maria')...")

    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine is not None:
            porcupine.delete()
        talk("Recursos liberados. Adiós.")

if __name__ == '__main__':
    run_yeny()