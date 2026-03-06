import time
import serial

PORT = "COM4"   # burayi kendi Arduino portuna gore degistir
BAUD = 9600

commands = [
    "LED_RED",
    "LED_GREEN",
    "LED_BLUE",
    "LED_OFF",
    "SERVO_ON",
    "SERVO_OFF"
]

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # Arduino reset icin bekleme

for cmd in commands:
    print(f"Gonderiliyor: {cmd}")
    ser.write((cmd + "\n").encode("utf-8"))
    time.sleep(1)

    response = ser.readline().decode("utf-8", errors="ignore").strip()
    if response:
        print("Arduino:", response)

ser.close()
print("Test tamamlandi.")