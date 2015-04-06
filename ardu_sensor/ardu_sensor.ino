#define temperaturePinA 0                                // analog pin from which retrieve the sensor value
#define temperaturePinB 1
#define B_RATE          9600                             // baud rate to initialize the serial port
#define SLEEP_TIME      6000                             // milliseconds to wait before the next sensor scan
#define CONVERSION      9.31                             // conversion factor due to internal analog ref.

float temperatureA;                                      // final temperature reading
float temperatureB; 
float temperature;
int analogTemperatureA;                                  // temperature retrieved from the sensor
int analogTemperatureB;

/* setup code to run once */
void setup() {
  Serial.begin(B_RATE);                                  // initializing the serial port
  analogReference(INTERNAL);                             // analogic reference to 1.1V for a better performance
}

/* main code to run repeatedly */
void loop() {
  analogTemperatureA = analogRead(temperaturePinA);
  analogTemperatureB = analogRead(temperaturePinB);
  
  temperatureA = analogTemperatureA / CONVERSION;
  temperatureB = analogTemperatureB / CONVERSION;
  
  temperature = (temperatureA + temperatureB) / 2;
  Serial.println(temperature);
  
  delay(SLEEP_TIME);
}
