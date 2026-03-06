import os
from vosk import Model

MODEL_PATH = r"C:\mbux_project\models\vosk-tr"

print("Bulundugum klasor:", os.getcwd())
print("Model klasoru var mi:", os.path.exists(MODEL_PATH))
print("Model klasoru icerigi:", os.listdir(MODEL_PATH))

print("Model yukleniyor...")
model = Model(MODEL_PATH)
print("Model basariyla yuklendi.")