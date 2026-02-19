int led1 = 8;
int led2 = 12;
int led3 = 13;
 
int buttonPin = 2;
 
int ledState = 0;      // 0 → LED1, 1 → LED2, 2 → LED3
int eventCount = 0;
 
bool lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
 
void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
 
  pinMode(buttonPin, INPUT_PULLUP);
 
  Serial.begin(9600);
}
 
void loop() {
  bool reading = digitalRead(buttonPin);
 
  // rilevazione cambiamento
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
 
 
  // pulsante premuto (da HIGH a LOW)
  if (reading == LOW && lastButtonState == HIGH) {
 
    eventCount++;
 
    // cambia LED
    ledState = (ledState + 1) % 3;
 
    digitalWrite(led1, ledState == 0);
    digitalWrite(led2, ledState == 1);
    digitalWrite(led3, ledState == 2);
 
    // invia SOLO i dati utili
    Serial.print(eventCount);
    Serial.print(",");
    Serial.println(ledState + 1);
  }
 
  lastButtonState = reading;
}
 
 