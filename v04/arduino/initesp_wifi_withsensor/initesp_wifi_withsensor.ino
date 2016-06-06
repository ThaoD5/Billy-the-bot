#include <SoftwareSerial.h>
#include <ZumoMotors.h>
#include <QTRSensors.h>

#define NUM_SENSORS             6  // number of sensors used
#define NUM_SAMPLES_PER_SENSOR  4  // average 4 analog samples per sensor reading
#define EMITTER_PIN             2  // emitter is controlled by digital pin 2

QTRSensorsAnalog qtra((unsigned char[]) {0, 1, 2, 3, 4, 5}, 
  NUM_SENSORS, NUM_SAMPLES_PER_SENSOR, EMITTER_PIN);
unsigned int sensorValues[NUM_SENSORS];

SoftwareSerial ESP8266(3, 6);

String NomduReseauWifi = "WIFINAME"; // Garder les guillements
String MotDePasse      = "WIFIPWD"; // Garder les guillements
String a;
String movementsMade[3];

ZumoMotors motors;

void moveFront(){
      for (int speed = 0; speed <= 260; speed++)
      {
        motors.setLeftSpeed(speed);
        motors.setRightSpeed(speed);
        delay(2);
      }
    
      for (int speed = 200; speed >= 0; speed--)
      {
        motors.setLeftSpeed(speed);
        motors.setRightSpeed(speed);
        delay(2);
      }
}

void moveRight(){
      for (int speed = 0; speed <= 195; speed++)
      {
        motors.setLeftSpeed(speed);
        motors.setRightSpeed(-speed);
        delay(2);
      }
    
      for (int speed = 200; speed >= 0; speed--)
      {
        motors.setLeftSpeed(speed);
        motors.setRightSpeed(-speed);
        delay(2);
      }
}

void moveLeft(){
      for (int speed = 0; speed <= 195; speed++)
      {
        motors.setLeftSpeed(-speed);
        motors.setRightSpeed(speed);
        delay(2);
      }
    
      for (int speed = 200; speed >= 0; speed--)
      {
        motors.setLeftSpeed(-speed);
        motors.setRightSpeed(speed);
        delay(2);
      }
}

void moveBack(){
      for (int speed = 0; speed >= -260; speed--)
      {
        motors.setRightSpeed(speed);
        motors.setLeftSpeed(speed);
        delay(2);
      }
      
      for (int speed = -200; speed <= 0; speed++)
      {
        motors.setRightSpeed(speed);
        motors.setLeftSpeed(speed);
        delay(2);
      }
}

void movementsOfBilly(String ordersent)
{  
  if(movementsMade[0].length() == 0){
      Serial.println("position 0 empty");
      movementsMade[0] = ordersent;
      Serial.println(movementsMade[0]);
    }
    else if((movementsMade[0].length() != 0) && (movementsMade[1].length() == 0)){
        Serial.println("position 1 empty");
        movementsMade[1] = ordersent;
        Serial.println(movementsMade[0]);
        Serial.println(movementsMade[1]);
      }
    else if((movementsMade[0].length() != 0) && (movementsMade[1].length() != 0) && (movementsMade[2].length() == 0)){
        Serial.println("position 3 empty");
        movementsMade[2] = ordersent;
        Serial.println(movementsMade[0]);
        Serial.println(movementsMade[1]);
        Serial.println(movementsMade[2]);
      }
    else if((movementsMade[0].length() != 0) && (movementsMade[1].length() != 0) && (movementsMade[2].length() != 0)){
        movementsMade[0] = movementsMade[1];
        movementsMade[1] = movementsMade[2];
        movementsMade[2] = ordersent;
        Serial.println(movementsMade[0]);
        Serial.println(movementsMade[1]);
        Serial.println(movementsMade[2]);
      }
}

void calibrateSensors(){
      pinMode(13, OUTPUT);
      digitalWrite(13, HIGH);    // turn on Arduino's LED to indicate we are in calibration mode
      for (int i = 0; i < 400; i++)  // make the calibration take about 10 seconds
      {
        qtra.calibrate();       // reads all sensors 10 times at 2.5 ms per six sensors (i.e. ~25 ms per call)
      }
      digitalWrite(13, LOW);     // turn off Arduino's LED to indicate we are through with calibration
      Serial.begin(9600);
    
      for (int i = 0; i < NUM_SENSORS; i++)
      {
        Serial.print(qtra.calibratedMinimumOn[i]);
        Serial.print(' ');
      }
      Serial.println();
      
      // print the calibration maximum values measured when emitters were on
      for (int i = 0; i < NUM_SENSORS; i++)
      {
        Serial.print(qtra.calibratedMaximumOn[i]);
        Serial.print(' ');
      }
      Serial.println();
      Serial.println();
      delay(1000);
}

/****************************************************************/
/*                             INIT                             */
/****************************************************************/
void setup()
{
  calibrateSensors();
  ESP8266.begin(9600);
  initESP8266();
}

void loop()
{  
   while(ESP8266.available())
   {
    a= ESP8266.readString();// read the incoming data as string
    Serial.println(a);
    if(a.indexOf("front") > 0){
      moveFront();
      movementsOfBilly("front");
      checkTrap();
    }
    else if(a.indexOf("right") > 0){
      moveRight();
      movementsOfBilly("right");
      checkTrap();
    }
    else if(a.indexOf("left") > 0){
      moveLeft();
      movementsOfBilly("left");
      checkTrap();
      
    }
    else if(a.indexOf("back") > 0){
      moveBack();
      movementsOfBilly("back");
      checkTrap();
    }
  }
}

void checkTrap(){
  delay(500);
  unsigned int position = qtra.readLine(sensorValues);
  
    // print the sensor values as numbers from 0 to 1000, where 0 means maximum reflectance and
    // 1000 means minimum reflectance, followed by the line position
    for (unsigned char i = 0; i < NUM_SENSORS; i++)
    {
      Serial.print(sensorValues[i]);
      Serial.print('\t');
    }
    //Serial.println(); // uncomment this line if you are using raw values
    Serial.println(position); // comment this line out if you are using raw values
    
  Serial.println(position);
    Serial.println("TEEEEST");
    if(position >= 100){
      if(movementsMade[2] == "front"){
        moveBack();
      }
      else if(movementsMade[2] == "right"){
        moveLeft();
      }
      else if(movementsMade[2] == "left"){
        moveRight();
      }
      else if(movementsMade[2] == "back"){
        moveFront();
      }

      if(movementsMade[1] == "front"){
        moveBack();
      }
      else if(movementsMade[1] == "right"){
        moveLeft();
      }
      else if(movementsMade[1] == "left"){
        moveRight();
      }
      else if(movementsMade[1] == "back"){
        moveFront();
      }

      if(movementsMade[0] == "front"){
        moveBack();
      }
      else if(movementsMade[0] == "right"){
        moveLeft();
      }
      else if(movementsMade[0] == "left"){
        moveRight();
      }
      else if(movementsMade[0] == "back"){
        moveFront();
      }
    }
}

/****************************************************************/
/*                Fonction qui initialise l'ESP8266             */
/****************************************************************/
void initESP8266()
{  
  envoieAuESP8266("AT+RST");
  recoitDuESP8266(2000);
  envoieAuESP8266("AT+CWMODE=3");
  recoitDuESP8266(5000);
  envoieAuESP8266("AT+CWJAP=\""+ NomduReseauWifi + "\",\"" + MotDePasse +"\"");
  recoitDuESP8266(10000);
  envoieAuESP8266("AT+CIFSR");
  recoitDuESP8266(1000);
  envoieAuESP8266("AT+CIPMUX=1");   
  recoitDuESP8266(1000);
  envoieAuESP8266("AT+CIPSERVER=1,5555");
  recoitDuESP8266(1000);
  envoieAuESP8266("AT+CIFSR");
  Serial.println("wifi connected");
}

/****************************************************************/
/*        Fonction qui envoie une commande à l'ESP8266          */
/****************************************************************/
void envoieAuESP8266(String commande)
{  
  ESP8266.println(commande);
}
/****************************************************************/
/*Fonction qui lit et affiche les messages envoyés par l'ESP8266*/
/****************************************************************/
void recoitDuESP8266(const int timeout)
{
  String reponse = "";
  long int time = millis();
  while( (time+timeout) > millis())
  {
    while(ESP8266.available())
    {
      char c = ESP8266.read();
      reponse+=c;
    }
  }
}
