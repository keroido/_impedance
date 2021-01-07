import processing.serial.*;
PrintWriter output;
Serial myPort;
boolean flg_start = false;
long time=0;
int now = 0;
String str1 = "S";
String str_format = "x";
//String port = "/dev/cu.wchusbserial1440";
String port = "/dev/cu.usbserial-AC008NHR";
void setup() {
  size(640, 480);
   myPort = new Serial(this, port, 115200);
}

void draw() {
  while ( myPort.available() > 0 ) {    
    String inBuffer = myPort.readString();
    String tmp = inBuffer;
    int r = tmp.indexOf(str1);
    if (r != -1){
      now++;
      println(now);
    }
    if ( inBuffer != null ) {
      if ( flg_start ) output.print(inBuffer);
    }
  }
}

void keyPressed() {
  if ( key == 's' ) {
    flg_start  = !flg_start;
    println(flg_start);
    if ( flg_start == false ) {
      // end of recording
      output.flush();
      output.close();
    } else if ( flg_start == true ) {
      // begining of recording
      String filename = nf(year(), 4) + nf(month(), 2) + nf(day(), 2) + nf(hour(), 2) + nf(minute(), 2) ;
      //String filename = "tmp3";
      output = createWriter( filename + ".csv"); 
      output.println( str_format );
    }
  }
}
