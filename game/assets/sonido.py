import numpy as np
from scipy.io import wavfile

# Configuración técnica
SAMPLE_RATE = 44100  # Frecuencia de muestreo estándar

def save_wav(filename, data):
    # Normalización a 16-bit PCM
    data = (data * 32767).astype(np.int16)
    wavfile.write(filename, SAMPLE_RATE, data)

def generate_laser_shoot(duration=0.2):
    """Genera un sonido de disparo tipo arcade usando un barrido de frecuencia."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Descenso de frecuencia: de 1000Hz a 100Hz
    freq = np.linspace(1000, 100, len(t))
    # Onda cuadrada para estilo retro
    audio = np.sign(np.sin(2 * np.pi * freq * t))
    # Envoltura de amplitud (fade out)
    envelope = np.exp(-10 * t)
    return audio * envelope

def generate_explosion(duration=0.5):
    """Genera una explosión usando ruido blanco y decaimiento."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    # Ruido blanco
    noise = np.random.uniform(-1, 1, len(t))
    # Envoltura para el impacto inicial y decaimiento
    envelope = np.exp(-5 * t)
    return noise * envelope

def generate_tank_bgm(duration=4.0):
    """Genera una base rítmica industrial/militar de 8-bits."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    audio = np.zeros_like(t)
    
    # Secuencia de notas simple (Frecuencias en Hz)
    sequence = [73.42, 73.42, 82.41, 65.41] # D2, D2, E2, F2
    note_duration = 0.5
    samples_per_note = int(SAMPLE_RATE * note_duration)
    
    for i, freq in enumerate(sequence * 2):
        start = i * samples_per_note
        end = start + samples_per_note
        if end > len(t): break
        
        t_note = np.linspace(0, note_duration, samples_per_note)
        # Onda de pulso (característica de chips de sonido antiguos)
        note = np.where(np.sin(2 * np.pi * freq * t_note) > 0, 0.5, -0.5)
        audio[start:end] = note
        
    return audio * 0.3 # Volumen más bajo para el fondo

# Ejecución y creación de archivos
if __name__ == "__main__":
    print("Generando assets de audio...")
    save_wav("disparo.wav", generate_laser_shoot())
    save_wav("explosion.wav", generate_explosion())
    save_wav("musica_fondo.wav", generate_tank_bgm())
    print("Archivos generados: disparo.wav, explosion.wav, musica_fondo.wav")
