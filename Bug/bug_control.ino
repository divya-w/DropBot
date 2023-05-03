#include <SPI.h>
#include <WiFi101.h>

const int motorEnableLeft = 9;   // Back Right motor
const int motorEnableRight = 21;  // Back Left motor
const int motorFrontEnableLeft = 6; // Front Left
const int motorFrontEnableRight = 2; //Front Right
const int motorForwardLeft = 10;
const int motorFrontForwardLeft = 7;
const int motorFrontBackwardLeft = 8;
const int motorFrontBackwardRight = 4;
const int motorFrontForwardRight= 3;
const int motorBackLeft = 11;
const int motorForwardRight = 0;
const int motorBackRight = 1;
const int wifiLed = 20;           // For indicating successful Wi-Fi connection
//const int collisionFrontLeft = 17;
//const int collisionFrontRight = 18;
//const int collisionFrontMiddle = 19;
const int linActuator = 16;
const int deploy = 15;
const int retract = 12;
const int leftMotorSpeed = 255;  //best at 160
const int rightMotorSpeed = 255;

int sensorValL = 0;
int sensorValM = 0;
int sensorValR = 0;
int deployer = 0;
int action = 0;


char ssid[] = "Rice Visitor";//char ssid[] = "Rice Visitor";  // Fill in your network SSID (name)
//char pass[] =  // Fill in your network password
int keyIndex = 0;  // Fill in your network key Index number (Optional - needed only for WEP)

int status = WL_IDLE_STATUS;
String readString;

WiFiServer server(80);  // Define the port of the server

void setup() {
  Serial.begin(9600);
  pinMode(motorEnableLeft, OUTPUT);
  pinMode(motorForwardLeft, OUTPUT);
  pinMode(motorBackLeft, OUTPUT);
  pinMode(motorEnableRight, OUTPUT);
  pinMode(motorForwardRight, OUTPUT);
  pinMode(motorBackRight, OUTPUT);
  pinMode(motorFrontForwardLeft, OUTPUT);
  pinMode(motorFrontBackwardRight, OUTPUT); 
  pinMode(motorFrontBackwardLeft, OUTPUT);  
  pinMode(motorFrontBackwardRight, OUTPUT);
  pinMode(motorFrontForwardRight, OUTPUT);
  pinMode(motorBackLeft, OUTPUT); 
  pinMode(motorForwardRight, OUTPUT); 
  pinMode(motorBackRight, OUTPUT);
  pinMode(deploy, OUTPUT);
  pinMode(linActuator, OUTPUT);
  pinMode(retract, OUTPUT);
  pinMode(wifiLed, OUTPUT);
  //pinMode(collisionFrontLeft, INPUT);
  //pinMode(collisionFrontMiddle, INPUT);
  //pinMode(collisionFrontRight, INPUT);

  // Attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    // For WEP network, replace with: status = WiFi.begin(ssid, keyIndex, pass);
    // For open network, replace with: status = WiFi.begin(ssid);
    status = WiFi.begin(ssid);
    // wait 10 seconds for connection:
    delay(10000);
  }

  // Begin the webserver
  server.begin();
  // Indicate that the server is running
  //digitalWrite(deploy, HIGH);
  printWifiStatus();
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");

  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
}

void loop() {
  action = 0;
  
  sensorValL = analogRead(A2);
  float vL = sensorValL * (5.0/1023.0);
  sensorValM = analogRead(A3);
  float vM = sensorValM * (5.0/1023.0);
  sensorValR = analogRead(A4);
  float vR = sensorValR * (5.0/1023.0);
  
  if (vL > 4.5){
     obstacleLeft();     
  }
  
  if (vM > 4.5){
    obstacleMiddle();   
  }

  if (vR > 4.5){
    obstacleRight();   
  }

  



  // Listen for incoming clients
  WiFiClient client = server.available();
  if (client) {
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {

        char c = client.read();
        // If you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply

        if (readString.length() < 100) {
          //store characters to string
          readString += c;
        }

        if ((c == '\n')) {
          // send a standard http response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          client.println("<head>");
          client.println("<style>");
          client.println("a.button {-webkit-appearance: button;");
          client.println("-moz-appearance: button;");
          client.println("appearance: button;");
          client.println("height:400px;");
          client.println("line-height:400px;");
          client.println("text-align:center;");
          client.println("text-decoration: none;");
          client.println("font-size: 100px;");
          client.println("color: initial;}");
          client.println("</style>");
          client.println("</head>");
          client.println("<body>");
          // Button for moving Forwards
          client.println("<a href=\"/?goForward\" class=\"button\" style=\"width:100%;\"\">goForward</a>");
          client.println("<br />");
          // Button for turning Left
          client.println("<a href=\"/?turnLeft\" class=\"button\" style=\"width:100%;\"\">turnLeft</a>");
          // Button for Stopping the car
          client.println("<a href=\"/?Stop\" class=\"button\" style=\"width:29%;\"\">STOP</a>");
          // Button for turning Right
          client.println("<a href=\"/?turnRight\" class=\"button\" style=\"width:100%;\"\">turnRight</a>");
          client.println("<br />");
          // Button for moving Backwards
          
          client.println("<a href=\"/?goBack\" class=\"button\" style=\"width:100%;\"\">goBack</a>");
          client.println("<br />");
          client.println("<a href=\"/?deployPackage\" class=\"button\" style=\"width:100%;\"\">deployPackage</a>");
          
          client.println("<br />");

          client.println("<a href=\"/?retractPackage\" class=\"button\" style=\"width:100%;\"\">retractPackage</a>");
          
          client.println("<br />");

          client.println("<a href=\"/?stopDeploy\" class=\"button\" style=\"width:100%;\"\">stopDeploy</a>");
          
          client.println("<br />");

          client.println("<br />");

          client.println("</body>");
          client.println("</html>");
          break;
        }
        if (action == 0){
          
          if ((readString.indexOf("?goForward") > 0)) {
           goForward();         
           Serial.print("forward");
           Serial.println();
           // Clear the readString to be able to get the next command
           readString = "";
          }
          if (readString.indexOf("?goBack") > 0) {
            goBack();
            Serial.print("back");
            Serial.println();
            // Clear the readString to be able to get the next command
            readString = "";
          }
          if (readString.indexOf("?turnLeft") > 0) {
            turnLeft();
            Serial.print("left");
            Serial.println();

          // Clear the readString to be able to get the next command
          readString = "";
        }
        if (readString.indexOf("?turnRight") > 0) {
          turnRight();
          Serial.print("right");
          Serial.println();

          // Clear the readString to be able to get the next command
          readString = "";
        }
        if ((readString.indexOf("?Stop") > 0)) {
          stopCar();
          Serial.print("stop");
          Serial.println();
          // Clear the readString to be able to get the next command
          readString = "";
        }

        if ((readString.indexOf("?deployPackage") > 0)) {
          digitalWrite(16, HIGH);
          digitalWrite(15, LOW);
          //digitalWrite(12, HIGH);
          Serial.print("deploy");
          Serial.println();
          // Clear the readString to be able to get the next command
          readString = "";
                   
        }

        if ((readString.indexOf("?retractPackage") > 0)) {
          digitalWrite(16, LOW);
          digitalWrite(15, HIGH);
          //digitalWrite(12, HIGH);
          Serial.print("retract");
          Serial.println();
          // Clear the readString to be able to get the next command
          readString = "";
                   
        }
        if ((readString.indexOf("?stopDeploy") > 0)) {
          
          digitalWrite(16, LOW);
          digitalWrite(15, LOW);
          //digitalWrite(12, LOW);
          Serial.print("deployStopped");
          Serial.println();
          // Clear the readString to be able to get the next command
          readString = "";
                   
        }

        }
       

          
        
        
        
      }
    }
    // Give the web browser time to receive the data
    delay(1);
    // Close the connection:
    client.stop();
  }
}

void stopCar() {
  digitalWrite(motorForwardLeft, LOW);
  digitalWrite(motorBackLeft, LOW);
  digitalWrite(motorForwardRight, LOW);
  digitalWrite(motorBackRight, LOW);
  digitalWrite(motorEnableLeft, LOW);
  digitalWrite(motorEnableRight, LOW);

  digitalWrite(motorFrontForwardLeft, LOW);
  digitalWrite(motorFrontBackwardLeft, LOW);
  digitalWrite(motorFrontForwardRight, LOW);
  digitalWrite(motorFrontBackwardRight, LOW);
  digitalWrite(motorFrontEnableLeft, LOW);
  digitalWrite(motorFrontEnableRight, LOW);
}

void goForward() {
  digitalWrite(motorForwardLeft, LOW);
  digitalWrite(motorBackLeft, HIGH);
  digitalWrite(motorForwardRight, HIGH);
  digitalWrite(motorBackRight, LOW);
  digitalWrite(motorEnableLeft, HIGH);
  digitalWrite(motorEnableRight, HIGH);

  digitalWrite(motorFrontForwardLeft, LOW);
  digitalWrite(motorFrontBackwardLeft, HIGH);
  digitalWrite(motorFrontForwardRight, HIGH);
  digitalWrite(motorFrontBackwardRight, LOW);
  digitalWrite(motorFrontEnableLeft, HIGH);
  digitalWrite(motorFrontEnableRight, HIGH);
}

void goRight() {

}

void turnRight() {
  digitalWrite(motorForwardLeft, LOW);
  digitalWrite(motorBackLeft, HIGH);
  digitalWrite(motorForwardRight, LOW);
  digitalWrite(motorBackRight, HIGH);
  digitalWrite(motorEnableLeft, HIGH);
  digitalWrite(motorEnableRight, HIGH);

  digitalWrite(motorFrontForwardLeft, LOW);
  digitalWrite(motorFrontBackwardLeft, HIGH);
  digitalWrite(motorFrontForwardRight, LOW);
  digitalWrite(motorFrontBackwardRight, HIGH);
  digitalWrite(motorFrontEnableLeft, HIGH);
  digitalWrite(motorFrontEnableRight, LOW);
}

void goLeft() {

}

void turnLeft() {
  digitalWrite(motorForwardLeft, HIGH);
  digitalWrite(motorBackLeft, LOW);
  digitalWrite(motorForwardRight, HIGH);
  digitalWrite(motorBackRight, LOW);
  digitalWrite(motorEnableLeft, HIGH);
  digitalWrite(motorEnableRight, HIGH);

  digitalWrite(motorFrontForwardLeft, HIGH);
  digitalWrite(motorFrontBackwardLeft, LOW);
  digitalWrite(motorFrontForwardRight, HIGH);
  digitalWrite(motorFrontBackwardRight, LOW);
  digitalWrite(motorFrontEnableLeft, HIGH);
  digitalWrite(motorFrontEnableRight, HIGH);
}


void goBack() {
  digitalWrite(motorForwardLeft, HIGH);
  digitalWrite(motorBackLeft, LOW);
  digitalWrite(motorForwardRight, LOW);
  digitalWrite(motorBackRight, HIGH);
  digitalWrite(motorEnableLeft, HIGH);
  digitalWrite(motorEnableRight, HIGH);

  digitalWrite(motorFrontForwardLeft, HIGH);
  digitalWrite(motorFrontBackwardLeft, LOW);
  digitalWrite(motorFrontForwardRight, LOW);
  digitalWrite(motorFrontBackwardRight, HIGH);
  digitalWrite(motorFrontEnableLeft, HIGH);
  digitalWrite(motorFrontEnableRight, HIGH);
}

void obstacleLeft() {
  action = 1;
  Serial.print("obstacle left!");
  Serial.println();
  stopCar();
  Serial.print("stop1");
  Serial.println();        
  delay(1500);
  goBack();
  Serial.print("reverse");
  Serial.println();
  delay(1500);
  stopCar();
  delay(1500);
  turnRight();
  delay(500);
  stopCar();
  Serial.print("stop2");
  Serial.println();
}

void obstacleRight() {
  action = 1;
  Serial.print("obstacle Right!");
  Serial.println();
  stopCar();
  Serial.print("stop1");
  Serial.println();        
  delay(1500);
  goBack();
  Serial.print("reverse");
  Serial.println();
  delay(1500);
  stopCar();
  delay(1500);
  turnLeft();
  delay(500);
  stopCar();
  Serial.print("stop2");
  Serial.println();
}

void obstacleMiddle() {
  action = 1;
  Serial.print("obstacle Middle!");
  Serial.println();
  stopCar();
  Serial.print("stop1");
  Serial.println();        
  delay(1500);
  goBack();
  Serial.print("reverse");
  Serial.println();
  delay(1500);
  //turnLeft();
  //delay(500);
  stopCar();
  Serial.print("stop2");
  Serial.println();
}
