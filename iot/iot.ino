#include <ESP8266WiFi.h>
#include<WiFiClient.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);
void handleRoot(){
  server.send(200,"text/plain","working");
}
void handleLED(){
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  server.send(200,"text/plain","led toggled");
}
void setup(){
  Serial.begin(115200);
  pinMode(LED_BUILTIN,OUTPUT);
  WiFi.mode(WIFI_STA);
  WiFi.begin("I hate you all","n00dl3xyz");
  Serial.println("Connecting to wifi");
  while(WiFi.status() != WL_CONNECTED){
    delay(100);
    Serial.print(".");
  }
  Serial.println("Connected");
  Serial.println(WiFi.localIP());
  server.on("/",handleRoot);
  server.on("/led", handleLED);
  server.begin();
}
void loop(){
  server.handleClient();
}
