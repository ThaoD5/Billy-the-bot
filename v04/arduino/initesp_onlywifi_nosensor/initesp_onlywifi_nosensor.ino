#include <SoftwareSerial.h>
#include <ZumoMotors.h> 

SoftwareSerial ESP8266(3, 6);

String NomduReseauWifi = "WIFINAME"; // Garder les guillements
String MotDePasse      = "WIFIPWD"; // Garder les guillements
String a;
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

/****************************************************************/
/*                             INIT                             */
/****************************************************************/
void setup()
{
  ESP8266.begin(9600);
  Serial.begin(9600);
  initESP8266();
}
/****************************************************************/
/*                        BOUCLE INFINIE                        */
/****************************************************************/
void loop()
{
   while(ESP8266.available())
   {
    a= ESP8266.readString();// read the incoming data as string
    Serial.println(a);
    if(a.indexOf("front") > 0){
      moveFront();
    }
    else if(a.indexOf("right") > 0){
      moveRight();
    }
    else if(a.indexOf("left") > 0){
      moveLeft();
    }
    else if(a.indexOf("back") > 0){
      moveBack();

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
