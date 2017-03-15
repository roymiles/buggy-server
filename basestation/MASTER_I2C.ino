#include <Wire.h>
#include "EasyTransferI2C.h"

// Create object
EasyTransferI2C ET;

struct SEND_DATA_STRUCTURE{
  // THIS MUST BE EXACTLY THE SAME ON THE OTHER ARDUINO
};

int val = 0;
void setup() {
  Serial.println("Master setup");
  // Start the I2C Bus as Master
  Wire.begin(); 

  //Let's make it more random
  //randomSeed(42);   
}
void loop() {
  /*
   * Master wants to transmit current buggy position
   */
  Wire.beginTransmission(44); // transmit to device #44 (0x2c)
                              // device address is specified in datasheet
  Serial.print("Transmitting: ");
  Serial.println(masterToString(MASTER_SEND_POSITION));                            
  Wire.write(MASTER_SEND_POSITION); // sends value byte  
  Wire.endTransmission();           // stop transmitting
  delay(500);

  /*
   * Send current x-coordinate
   */
  Wire.beginTransmission(44);
  Serial.print("Transmitting: ");
  //generate a random number
  randomNumber = 4;
  Serial.println(randomNumber);                            
  Wire.write(randomNumber); 
  Wire.endTransmission();
  delay(1000);
  
  /*
   * Send current y-coordinate
   */
  Wire.beginTransmission(44);
  Serial.print("Transmitting: ");
  //generate a random number
  randomNumber = 3;
  Serial.println(randomNumber);                            
  Wire.write(randomNumber); 
  Wire.endTransmission();
  delay(1000);
  
  /*
   * Send current orientation
   */
  Wire.beginTransmission(44);
  Serial.print("Transmitting: ");
  Serial.println(orientationToString(WEST));                            
  Wire.write(WEST); 
  Wire.endTransmission();
  delay(1000);
}
String orientationToString(orientation ornt){
  switch(ornt){
    case NORTH:
      return "NORTH";
      break;
    case EAST:
      return "EAST";
      break;
    case SOUTH:
      return "SOUTH";
      break;
    case WEST:
      return "WEST";
      break;
    default:
      return "UNKNOWN";
  }
}

String masterToString(I2C_MASTER mst){
  switch(mst){
    case MASTER_IDLE:
      return "MASTER_IDLE";
      break;
     case MASTER_MOVING:
      return "MASTER_MOVING";
      break;
     case MASTER_DOCKED:
      return "MASTER_DOCKED";
      break;
     case MASTER_ADJUSTING:
      return "MASTER_ADJUSTING";
      break;
     default:
      return "UNKNOWN";
  }
}
