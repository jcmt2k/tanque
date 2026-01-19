import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100

def generate_tone(freq, duration, wave_type='square', duty_cycle=0.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    if wave_type == 'square':
        # Onda de pulso ajustable para textura de 8 bits
        audio = np.where((t * freq) % 1 < duty_cycle, 1, -1)
    elif wave_type == 'triangle':
        audio = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    
    # Envoltura ADSR simplificada (Linear Decay)
    decay = np.linspace(1, 0, len(t))
    return audio * decay

def generate_game_over_musical():
    """
    Genera una fanfarria de Game Over con acordes y arpegios.
    Progresión: Re menor -> La menor (Final trágico)
    """
    # Definición de notas (Hz)
    D3, F3, A3 = 146.83, 174.61, 220.00
    C3, E3, G3 = 130.81, 164.81, 196.00
    A2 = 110.00

    segments = []

    # 1. Acorde de entrada (Dm) - Impacto
    chord1 = (generate_tone(D3, 0.3) + generate_tone(F3, 0.3) + generate_tone(A3, 0.3)) / 3
    segments.append(chord1)

    # 2. Arpegio descendente rápido
    for f in [A3, F3, D3, C3]:
        segments.append(generate_tone(f, 0.15, 'square'))

    # 3. Acorde final sostenido (Am) con vibrato manual
    duration_final = 1.5
    t_final = np.linspace(0, duration_final, int(SAMPLE_RATE * duration_final))
    # Añadimos un pequeño vibrato de 6Hz a la frecuencia fundamental
    vibrato = 1 + 0.01 * np.sin(2 * np.pi * 6 * t_final)
    
    final_chord = (
        np.sin(2 * np.pi * A2 * vibrato * t_final) * 0.5 + 
        np.sin(2 * np.pi * (A2 * 1.5) * vibrato * t_final) * 0.3 # Quinta justa
    )
    # Envoltura de desvanecimiento largo
    envelope = np.exp(-2 * t_final)
    segments.append(final_chord * envelope)

    return np.concatenate(segments)

if __name__ == "__main__":
    audio_data = generate_game_over_musical()
    # Normalización para evitar clipping
    audio_data = audio_data / np.max(np.abs(audio_data))
    
    # Guardar archivo
    output = (audio_data * 32767).astype(np.int16)
    wavfile.write("fin_de_juego.wav", SAMPLE_RATE, output)
    print("Fin de juego musical generado como 'fin_de_juego.wav'")
