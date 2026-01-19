import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100

def save_wav(filename, data):
    data = (data * 32767).astype(np.int16)
    wavfile.write(filename, SAMPLE_RATE, data)

def generate_bounce(duration=0.15):
    """
    Genera un sonido de rebote (ricochet) metálico.
    Usa un barrido de frecuencia ascendente rápido.
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    
    # Frecuencia que sube rápidamente de 800Hz a 2500Hz
    # El efecto ascendente da la sensación de 'rebote'
    freq = np.logspace(np.log10(800), np.log10(2500), len(t))
    
    # Onda triangular para un tono más 'metálico' que la sinusoidal
    # pero menos agresivo que la cuadrada
    audio = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    
    # Envoltura con decaimiento muy rápido
    envelope = np.exp(-15 * t)
    
    return audio * envelope

# Generar el nuevo asset
if __name__ == "__main__":
    bounce_effect = generate_bounce()
    save_wav("rebote.wav", bounce_effect)
    print("Archivo 'rebote.wav' generado exitosamente.")
