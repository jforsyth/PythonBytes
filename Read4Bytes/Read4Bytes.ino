void setup()
{

  Serial.begin(9600);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

const int numBytes = 4;

void loop() {

  // put your main code here, to run repeatedly:
  byte array[numBytes];

  // spam the PC to indicate we're ready for data
  while (Serial.available() == 0)
  {
    //send '!' up the chain
    Serial.println('!');

    //spam the host until they respond :)
    delay(10);
  }

  // turn on the LED to indicate we're waiting on data
  digitalWrite(LED_BUILTIN, HIGH);

  // wait until we have enough bytes
  while (Serial.available() < numBytes) {}

  for (int i = 0; i < numBytes; i++)
  {
    array[i] = (uint8_t)Serial.read();
  }

  // print out what we received to just double check
  Serial.print("Byte array received was: 0x");
  for (int i = 0; i < numBytes; i++)
  {
    Serial.print(array[i], HEX);
  }
  Serial.println("");

  // now cast the 32 bits into something we want...
  int32_t value = *((int32_t*)array);

  // print out received value
  Serial.print("Value on my system is: ");
  Serial.println(value);

  // delay so the light stays on
  delay(5000);

  digitalWrite(LED_BUILTIN, LOW);

}
