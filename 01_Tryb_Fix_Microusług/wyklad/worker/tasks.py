from celery import Celery, current_task, signals
from transformers import pipeline
import os
import numpy as np
from scipy.io.wavfile import write

celery = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

# Globalne zmienne dla modeli (zainicjalizowane w worker_process_init)
translator = None
text_to_speech = None

@signals.worker_process_init.connect
def init_models(**kwargs):
    """Inicjalizacja modeli w każdym procesie workera"""
    global translator, text_to_speech
    translator = pipeline("translation_en_to_de")
    text_to_speech = pipeline("text-to-speech", model="suno/bark-small")

@celery.task(name="tasks.translate_text")
def translate_text(text: str):
    global translator
    if translator is None:
        translator = pipeline("translation_en_to_de")
    result = translator(text)
    return result[0]["translation_text"]

@celery.task(name="tasks.generate_audio")
def generate_audio(text: str):
    global text_to_speech
    if text_to_speech is None:
        text_to_speech = pipeline("text-to-speech", model="suno/bark-small")
    
    # Generowanie audio z tekstu
    audio_data = text_to_speech(text)
    
    # Pobranie audio array i sample rate
    audio_array = audio_data["audio"]
    sample_rate = audio_data["sampling_rate"]
    
    # Tworzenie katalogu /data/audio jeśli nie istnieje
    audio_dir = "/data/audio"
    os.makedirs(audio_dir, exist_ok=True)
    
    # Generowanie unikalnej nazwy pliku używając ID zadania
    task_id = current_task.request.id.replace("-", "")
    filename = f"audio_{task_id}.wav"
    filepath = os.path.join(audio_dir, filename)
    
    # Korygowanie kształtu tablicy audio
    # scipy.io.wavfile.write expects (samples,) for mono or (samples, channels) for multi-channel
    # Transformers pipeline może zwracać (channels, samples) lub (1, samples)
    if audio_array.ndim == 2:
        if audio_array.shape[0] == 1:
            # Mono: (1, samples) -> (samples,)
            audio_array = audio_array.squeeze()
        else:
            # Multi-channel: (channels, samples) -> (samples, channels)
            audio_array = audio_array.T
    
    # Zapisywanie pliku WAV
    # Konwersja do int16 - audio jest w zakresie [-1, 1]
    if audio_array.dtype != np.int16:
        # Normalizacja: [-1, 1] -> int16 range [-32768, 32767]
        audio_array = np.clip(audio_array * 32767, -32768, 32767).astype(np.int16)
    
    # Upewnij się, że sample_rate jest int
    sample_rate = int(sample_rate)
    write(filepath, sample_rate, audio_array)
    
    return filename
