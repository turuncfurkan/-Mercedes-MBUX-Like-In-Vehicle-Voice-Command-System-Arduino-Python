import pyttsx3

engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
print("Bulunan sesler:")
for i, v in enumerate(voices):
    print(i, v.id, getattr(v, "name", ""))

if voices:
    engine.setProperty("voice", voices[0].id)

engine.say("Merhaba Furkan. Ses testi başarılı.")
engine.runAndWait()
print("Konuşma denemesi bitti.")