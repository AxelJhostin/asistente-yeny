import webbrowser
import datetime
import platform
import subprocess
from modules.speaker import talk

if platform.system() == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def open_browser(site="google.com"):
    talk(f"Abriendo {site}")
    webbrowser.open(f"https://{site}")

def tell_time():
    strTime = datetime.datetime.now().strftime("%I:%M %p")
    talk(f"Son las {strTime}")

def tell_date():
    now = datetime.datetime.now()
    date_str = now.strftime("hoy es %A, %d de %B del %Y")
    translations = {
        "Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles", 
        "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo",
        "January": "enero", "February": "febrero", "March": "marzo", "April": "abril",
        "May": "mayo", "June": "junio", "July": "julio", "August": "agosto",
        "September": "septiembre", "October": "octubre", "November": "noviembre", "December": "diciembre"
    }
    for eng, esp in translations.items():
        date_str = date_str.replace(eng, esp)
    talk(date_str)

def set_volume(level):
    system = platform.system()
    if system == "Windows":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_vol_scalar = volume.GetMasterVolumeLevelScalar()
        
        if level == "subir":
            new_vol = min(1.0, current_vol_scalar + 0.1)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            talk(f"Volumen subido al {int(new_vol * 100)}%")
        elif level == "bajar":
            new_vol = max(0.0, current_vol_scalar - 0.1)
            volume.SetMasterVolumeLevelScalar(new_vol, None)
            talk(f"Volumen bajado al {int(new_vol * 100)}%")
        elif level == "silencio":
            volume.SetMute(1, None)
            talk("Silencio activado.")
    elif system == "Darwin":
        if level == "subir":
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
            talk("Volumen subido.")
        elif level == "bajar":
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
            talk("Volumen bajado.")
        elif level == "silencio":
            subprocess.run(["osascript", "-e", "set volume output muted true"])
            talk("Silencio activado.")
    else:
        talk("Lo siento, no puedo controlar el volumen en este sistema operativo.")