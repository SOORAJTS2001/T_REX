/*int x;
#include <Servo.h>
Servo servo;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 servo.write(x);
 delay(500);
 servo.write(0);
 delay(500);
}*/
int data[10];
int data_pos =0;
int prev__base = 90;
String rec_data="";
#include <Servo.h>
Servo base_servo;
Servo arm1_servo;
void setup()
{
 Serial.begin(9600);
 Serial.setTimeout(1);
 base_servo.attach(9);
 base_servo.write(90);
 arm1_servo.write(90);
}
void move(int prevPos,int currPos,Servo name)
{
  if(prevPos>currPos)
  {
    for(int i = prevPos;i>=currPos;i--)
    {
      name.write(i);
      delay(15);
    }
  }
  else if(prevPos<currPos)
  {
    for(int i = prevPos;i<=currPos;i++)
    {
      name.write(i);
      delay(15);
    }
  }
  delay(10000);
}
void loop()
{
if(Serial.available()>0){
 String x = Serial.readString();
 for(int i =0;i<x.length();i++)
 {
   if(x[i]!='/')
   {
         rec_data+=x[i];
   }
   else{
     int ans = rec_data.toInt();
     rec_data = " ";
     data[data_pos] = ans;
     data_pos++;

   }
 }
 data_pos=0;
 move(prev__base,data[0],base_servo);
 Serial.print(rec_data);
 prev__base = data[0]; 
}
}
