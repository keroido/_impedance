#include <EF_AD9850.h>
//BitData - D8, CLK - D9, FQUP - D10, REST - D11
EF_AD9850 AD9850(9, 10, 11, 8);

#define hi 2
#define mi 3
#define lo 4

long i,n,frq;
int c=0,g,s,d,sum;
float val[10];
float avg[300];

void setup() {
  Serial.begin(115200);
  pinMode(2,OUTPUT);
}

void loop() {
 d=0;
 i=1000000;
 for(int p=0; p<10; p++){
  val[p] = 0;
 }
 for(int u=0; u<300; u++){
  avg[u] = 0;
 }
  do{
   if(i<=1000000 && i>100000){
    n = 10000;
    c = 0;
   } else if(i<=100000 && i>10000){
    n = 1000;
    c = 1;
   } else if(i<=10000 && i>=1000){
    n = 100;
    c = 2;
   }
    AD9850.init();
    AD9850.reset();
    AD9850.wr_serial(0x01, i);
     delay(5); 
    digitalWrite(2,HIGH); 
   for(int m=0; m<10; m++){
    switch(c){
      case 0:
       val[m] = analogRead(hi);
       break;
      case 1:
       val[m] = analogRead(mi);
       break;
      case 2:
       val[m] = analogRead(lo);
       break;
    }
    if(val[m]<100){
      val[m] = 0;
    }
    delay(1);
   }
   digitalWrite(2,LOW);
   for(int f=0; f<10; f++){
    sum+=val[f];
   }
   avg[d]=sum/10;
   sum=0;
   d++;
   i = i-n;
 } while(i>=1000);
 g = 0;
 for(int t=0; t<300; t++){
    if(0 == avg[t]){
      g--;
    } else{
      g++;;
    }
    
 }
// g = 1;
 if(g>0){
  frq = 1000000;
   for(d=0; d<=270; d++){
//     Serial.print("frq =");
//     Serial.println("start");
//     Serial.print(frq);
//     Serial.print(",");
//     Serial.print("amp =");
     Serial.println(avg[d]);
//     Serial.println("end");

      if(frq<=1000000 && frq>100000){
    n = 10000;
   } else if(frq<=100000 && frq>10000){
    n = 1000;
   } else if(frq<=10000 && frq>=1000){
    n = 100;
   }
   frq = frq-n;
     
   }
 }
 delay(2000);
}
