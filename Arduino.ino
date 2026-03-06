#include <Servo.h>

Servo myServo;

const int RED_PIN = 3;
const int GREEN_PIN = 5;
const int BLUE_PIN = 6;
const int SERVO_PIN = 9;

// RGB LED ortak katot ise false bırak.
// Ortak anot ise true yap.
bool COMMON_ANODE = false;

String incomingCommand = "";

void setColor(int r, int g, int b) {
  if (COMMON_ANODE) {
    analogWrite(RED_PIN, 255 - r);
    analogWrite(GREEN_PIN, 255 - g);
    analogWrite(BLUE_PIN, 255 - b);
  } else {
    analogWrite(RED_PIN, r);
    analogWrite(GREEN_PIN, g);
    analogWrite(BLUE_PIN, b);
  }
}

void executeCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();

  if (cmd == "LED_RED") {
    setColor(255, 0, 0);
    Serial.println("OK: LED RED");
  }
  else if (cmd == "LED_GREEN") {
    setColor(0, 255, 0);
    Serial.println("OK: LED GREEN");
  }
  else if (cmd == "LED_BLUE") {
    setColor(0, 0, 255);
    Serial.println("OK: LED BLUE");
  }
  else if (cmd == "LED_OFF") {
    setColor(0, 0, 0);
    Serial.println("OK: LED OFF");
  }
  else if (cmd == "SERVO_ON") {
    myServo.write(90);
    Serial.println("OK: SERVO ON");
  }
  else if (cmd == "SERVO_OFF") {
    myServo.write(0);
    Serial.println("OK: SERVO OFF");
  }
  else {
    Serial.print("ERR: UNKNOWN CMD -> ");
    Serial.println(cmd);
  }
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  myServo.attach(SERVO_PIN);
  myServo.write(0);

  Serial.begin(9600);

  setColor(0, 0, 0);

  Serial.println("SYSTEM READY");
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n') {
      executeCommand(incomingCommand);
      incomingCommand = "";
    } else {
      incomingCommand += c;
    }
  }
}void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
