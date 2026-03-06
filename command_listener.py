import json
import queue
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = "models/vosk-tr"
SAMPLE_RATE = 16000

GRAMMAR = json.dumps([
    "ambiyans",
    "mavi",
    "kırmızı",
    "kirmizi",
    "yeşil",
    "yesil",
    "kapat",
    "motor",
    "[unk]"
], ensure_ascii=False)

model = Model(MODEL_PATH)


def listen_for_command(timeout=5):
    q = queue.Queue()
    recognizer = KaldiRecognizer(model, SAMPLE_RATE, GRAMMAR)

    def callback(indata, frames, time_info, status):
        if status:
            print("Ses durumu:", status)
        q.put(bytes(indata))

    print("Komut dinleniyor...")

    start = time.time()

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while time.time() - start < timeout:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()
                if text:
                    print("Komut:", text)
                    return text

    final_result = json.loads(recognizer.FinalResult())
    text = final_result.get("text", "").lower().strip()
    if text:
        print("Komut:", text)
        return text

    return ""