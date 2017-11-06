int ledpin = 11;

void setup() {
	pinMode(ledpin, OUTPUT);
	analogWrite(ledpin, 60);
	delay(100);
	analogWrite(ledpin, 255);

	pinMode(13, OUTPUT);
	digitalWrite(13, HIGH);

	Serial.begin(9600);
}

void loop() {
	// delay(500);
	// digitalWrite(13, LOW);
	// delay(500);
	// digitalWrite(13, HIGH);

	if (Serial.available() > 0) {
		int val = Serial.parseInt();
		if (val >= 0 && val <= 255)
			analogWrite(ledpin, 255 - val);
		while (Serial.read() != '\n') {}
	}
}
