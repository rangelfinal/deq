#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int vai;
int v1;
int run;
int vpotencial;
float correntecorrigida;
float corr;
int ciclosads;
int contades;
int rpmbomba;
int cicloatual;
int C;
int totaldeciclos;
int v2;
int ciclosdes;
int A;
int D;
int tempototal;
int contaads;
int timebase;
int B;
int contaciclos;
char y;
String x;
int solen;
String inputString="";
boolean stringComplete=false;
char inChar;
int la;
int lb;
int w;

float fa;
float ga;
float ha;
float ia;
float ja;
float ka;

unsigned long int tempo;

//_______________________________________________________
void setup()
{

cicloatual = 0;
vai = 0;
Serial.begin(9600);
Serial1.begin(2400);

inputString.reserve(260);

contaads = 0;
ciclosads = 0;
contades = 0;
vpotencial = 0;
contaciclos = 0;
ciclosdes = 0;
v2 = 0;
v1 = 0;

pinMode( 22 , INPUT);
run = 0;
pinMode( 50 , OUTPUT);
A = 0;
pinMode( 47 , OUTPUT);
pinMode( 44 , OUTPUT);
tempototal = 0;
totaldeciclos = 0;
D = 0;
pinMode( 48 , OUTPUT);
rpmbomba = 0;
pinMode( 52 , OUTPUT);
pinMode( 46 , OUTPUT);
C = 0;
correntecorrigida = 0;
pinMode( 45 , OUTPUT);

digitalWrite( 44 , HIGH );
digitalWrite( 45 , HIGH );
digitalWrite( 46 , HIGH );
digitalWrite( 47 , HIGH );
digitalWrite( 48 , LOW );
digitalWrite( 50 , LOW );
digitalWrite( 52 , LOW );

cicloatual = 0 ;
contaads = 0 ;
contades = 0 ;
contaciclos = 0 ;
la=0;
lb=0;

}

//______________________________________________
void loop()
{
run = 0 ;
teste();
}

//__________________________________________________
void teste()  // lendo os dados envados pelo Matlab
{
fa=Serial.parseFloat(); // leitura da serial
 if (fa==8) {  // teste básico(se o primeiro caractere (verificador) é igual a 8
  ga=Serial.parseFloat();
  ha=Serial.parseFloat();
  ia=Serial.parseFloat();
  ja=Serial.parseFloat();
  ka=Serial.parseFloat();
  
  if (ka==922) {  // verifica se o caractere verificador final foi recebido
    Serial.println(933); // caso sim, envia a confirmação
        if(ja == 1){
        vai = 1;
        start();
        }
          else{
          run = 0 ;
          vai=0;
          teste();
          }
  }   
else
{
run = 0 ;
vai=0;
teste();
}
}
else{
  teste();
}
}

//________________________________________
void start()
{
if (( ( vai ) == ( 1 ) ))
{
if (( ( run ) == ( 1 ) ))
{
roda();
}
else
{
preset();
}
}
else
{
teste();
}
}
//______________________________________________-

void preset()
{
digitalWrite( 48 , HIGH );
digitalWrite( 50 , HIGH );
digitalWrite( 52 , HIGH );
run = 1 ;
start();
}

//_________________________________________________________
void roda(){
contaciclos = ( contaciclos + 1 ) ;

if (ia == 1 ){
digitalWrite( 47 , LOW );
solen=0;
}
else{
digitalWrite( 47 , HIGH );
solen=1;
}

if (ga == 1 ) {
ads();
}
else {
  if (ha == 1){
      des();
      }
      else{
        digitalWrite( 45 , HIGH );
        digitalWrite( 46 , HIGH );
        }
}
}

//_____________________________________________________________-
void des()
{
contades = ( contades + 1 ) ;
contaads = 0 ;
digitalWrite( 45 , HIGH );
digitalWrite( 46 , LOW );
cicloatual =1 ;
manda();
}


void ads()
{
contaads = ( contaads + 1 ) ;
contades = 0 ;
digitalWrite( 45 , LOW );
digitalWrite( 46 , HIGH );
cicloatual = 0 ;
manda();
}

//_____________________________________________________

//    ____________________________________
void manda(){
tempo = millis();
tempo/= 1000;
v1 = map( analogRead(A0) , 0, 1024, 0, 5000) ;
v2 = map( analogRead(A1) , 0, 1024, 0, 5000) ;
vpotencial = map( analogRead(A2) , 0, 1024, 0, 5000) ;


if (ha==1){
v1= (v1 * (-1));
v2= (v2 * (-1));
}

Serial.print( v1);
Serial.print(";");
Serial.print( v2 );
Serial.print(";");
Serial.print( vpotencial );
Serial.print(";");
Serial.print(vai);
Serial.print(";");
Serial.print(run);
Serial.print(";");
Serial.print(contaads);
Serial.print(";");
Serial.print(contades);
Serial.print(";");
Serial.print(contaciclos);
Serial.print(";");
Serial.print(cicloatual);
Serial.print(";");
Serial.print(tempo);
Serial.print(";");
Serial.print(solen);
Serial.println(";");
w=0;
serialEvent();
}

void serialEvent(){
  for(w=0; w<2800;w++){
        char inChar= (char)Serial1.read();
        Serial.print(inChar);
  }
   w=0;     
   teste();
}



