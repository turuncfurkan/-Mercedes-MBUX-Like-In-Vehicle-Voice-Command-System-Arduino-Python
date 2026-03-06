import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = "models/vosk-tr"
SAMPLE_RATE = 16000

WAKE_PHRASES = [
    "mercedes",
    "hey mercedes"
]

model = Model(MODEL_PATH)


def listen_for_wake_word():
    q = queue.Queue()
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    def callback(indata, frames, time_info, status):
        if status:
            print("Ses durumu:", status)
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()

                if text:
                    print("Duyulan:", text)

                for phrase in WAKE_PHRASES:
                    if phrase in text:
                        return phrase