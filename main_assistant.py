import time
import serial
import win32com.client

from wake_word import listen_for_wake_word
from command_listener import listen_for_command

PORT = "COM4"
BAUD = 9600

speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 1
speaker.Volume = 100


def speak(text):
    print("Asistan:", text)
    speaker.Speak(text)
    time.sleep(0.2)


def map_command(text):
    text = text.lower().strip()

    if text == "mavi":
        return "LED_BLUE"
    elif text == "kırmızı" or text == "kirmizi":
        return "LED_RED"
    elif text == "yeşil" or text == "yesil":
        return "LED_GREEN"
    elif text == "kapat":
        return "ALL_OFF"
    elif text == "motor":
        return "SERVO_ON"
    elif text == "ambiyans":
        return "AMBIANCE_ONLY"

    return None


def send_to_arduino(ser, command):
    if command == "ALL_OFF":
        ser.write(("LED_OFF\n").encode("utf-8"))
        time.sleep(0.3)
        ser.write(("SERVO_OFF\n").encode("utf-8"))
        time.sleep(0.3)
    else:
        ser.write((command + "\n").encode("utf-8"))
        time.sleep(0.5)

    while ser.in_waiting:
        response = ser.readline().decode("utf-8", errors="ignore").strip()
        if response:
            print("Arduino:", response)


def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)

    print("Sistem hazir.")

    while True:
        try:
            print("\nWake word bekleniyor...")
            wake = listen_for_wake_word()
            print("Wake word algilandi:", wake)

            speak("Sizin için ne yapabilirim Furkan?")

            user_command = listen_for_command(timeout=5)

            if not user_command:
                speak("Komut duyamadım.")
                continue

            print("Algilanan komut:", user_command)
            arduino_command = map_command(user_command)

            if arduino_command == "AMBIANCE_ONLY":
                speak("Ambiyans için bir renk söyleyin.")

            elif arduino_command:
                print("Arduino komutu:", arduino_command)
                send_to_arduino(ser, arduino_command)
                speak("Tamam.")

            else:
                speak("Bu komutu anlayamadım.")

            time.sleep(0.3)

        except KeyboardInterrupt:
            print("Program durduruldu.")
            break

        except Exception as e:
            print("Hata:", e)
            time.sleep(1)

    ser.close()


if __name__ == "__main__":
    main()