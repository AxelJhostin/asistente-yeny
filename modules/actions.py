import webbrowser
import datetime
import platform
import subprocess
from modules.speaker import talk
import screen_brightness_control as sbc
import wikipedia
import pyautogui

if platform.system() == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def open_browser(site="google.com"):
    """Abre el navegador web predeterminado en un sitio específico."""
    talk(f"Abriendo {site}")
    webbrowser.open(f"https://{site}")

def tell_time():
    """Dice la hora actual."""
    strTime = datetime.datetime.now().strftime("%I:%M %p")
    talk(f"Son las {strTime}")

def tell_date():
    """Dice la fecha actual."""
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
    """Ajusta el volumen del sistema."""
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
        # Lógica para macOS...
        pass
    else:
        talk("Lo siento, no puedo controlar el volumen en este sistema operativo.")

def open_brave():
    """Abre el navegador Brave."""
    talk("Abriendo Brave.")
    system = platform.system()
    if system == "Windows":
        path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        try:
            subprocess.Popen(path)
        except FileNotFoundError:
            talk("No encontré el navegador Brave en la ruta estándar.")
    elif system == "Darwin":
        try:
            subprocess.run(["open", "-a", "Brave Browser"])
        except FileNotFoundError:
            talk("No encontré el navegador Brave.")
    else:
        talk("No sé cómo abrir Brave en este sistema operativo.")

def set_brightness(level):
    """Ajusta el brillo de la pantalla a un porcentaje específico."""
    talk(f"Ajustando el brillo al {level} por ciento.")
    sbc.set_brightness(level)

def search_wikipedia(query):
    """Busca en Wikipedia y lee un resumen."""
    talk("Buscando en Wikipedia...")
    try:
        wikipedia.set_lang("es")
        summary = wikipedia.summary(query, sentences=2)
        talk("Según Wikipedia,")
        talk(summary)
    except wikipedia.exceptions.PageError:
        talk(f"Lo siento, no encontré la página para {query}.")
    except wikipedia.exceptions.DisambiguationError:
        talk(f"Hay demasiados resultados para {query}. Por favor, sé más específico.")
    except Exception as e:
        talk("Ocurrió un error al buscar en Wikipedia.")

def control_youtube(action):
    """Controla la reproducción de YouTube simulando atajos de teclado."""
    talk(f"Realizando acción: {action} en YouTube.")
    
    # Atajos de teclado de YouTube:
    # 'k' o 'space' -> play/pausa
    # 'j' -> retroceder 10 segundos
    # 'l' -> adelantar 10 segundos
    # 'm' -> mutear/desmutear
    # 'shift+n' -> siguiente video/canción
    # 'shift+p' -> video/canción anterior
    
    if action == 'siguiente':
        pyautogui.hotkey('shift', 'n')
    elif action == 'anterior':
        pyautogui.hotkey('shift', 'p')
    elif action == 'pausa':
        pyautogui.press('k')
    elif action == 'play':
        pyautogui.press('k')
    else:
        talk("No reconozco esa acción para YouTube.")
        