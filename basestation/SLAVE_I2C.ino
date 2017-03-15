#include <Wire.h>

/*
 * Commands sent from the master to the interrogator (slave)
 * 
 * Upon receiving MASTER_SEND_POSITION, the buggy will transmit 
 * its x, y and then orientation
 */
enum I2C_MASTER {MASTER_IDLE = 0, MASTER_MOVING = 1, MASTER_DOCKED = 2, MASTER_ADJUSTING = 3, MASTER_SEND_POSITION = 4};

/**
 *  Commands sent from the interrogator (slave) to the master
 */
enum I2C_SLAVE {SLAVE_IDLE = 0, SLAVE_BUSY = 1, SLAVE_DOCKED = 2};
enum orientation {NORTH = 0, EAST = 1, SOUTH = 2, WEST = 3};
enum wifiSendState {NA, AWAITING_X, AWAITING_Y, AWAITING_ORIENTATION}; 
/*
 * Used to track whether the buggy is awaiting an x, y or an orienation from the master
 */
wifiSendState currentWifiSendState = NA;

// Include the required Wire library for I2C<br>#include <Wire.h>
int recievedVal = 0;
void setup() {
  Serial.println("Slave setup");
  // Start the I2C Bus as Slave on address 9
  Wire.begin(44); 
  // Attach a function to trigger when something is received.
  Wire.onReceive(receiveEvent);
}

int x_coordinate = 0;
int y_coordinate = 0;
orientation currentOrientation = NORTH;

void receiveEvent(int bytes) {
  recievedVal = Wire.read();    // read one character from the I2C

  /*
   * Awaiting either the x, y or the orientation
   */
  if(currentWifiSendState != NA){
    switch(currentWifiSendState){
      case AWAITING_X:
        x_coordinate = recievedVal;
        Serial.print("Recieved x-coordinate: ");
        Serial.println(recievedVal);
        currentWifiSendState = AWAITING_Y;
        break;
      case AWAITING_Y:
        y_coordinate = recievedVal;
        Serial.print("Recieved y-coordinate: ");
        Serial.println(recievedVal);
        currentWifiSendState = AWAITING_ORIENTATION;
        break;
      case AWAITING_ORIENTATION:
        currentOrientation = recievedVal;
        Serial.print("Recieved orientation: ");
        Serial.println(orientationToString(recievedVal));
        currentWifiSendState = NA;
        break;
    }
  }
  
  /*
   * Perform based on the received command
   * If the command is not known, then it will be a value that is used dependning on the state
   */
  switch(recievedVal){
    case MASTER_SEND_POSITION:
      Serial.println("Recieved MASTER_SEND_POSITION");
      currentWifiSendState = AWAITING_X;
      break;
  }
}


void loop() {
  delay(100);
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

