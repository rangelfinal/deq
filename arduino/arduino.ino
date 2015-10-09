#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char inChar;
char *serialString;
float conductivity = 0;
float digitoVerificadorFinal = 0;
float digitoVerificadorInicial = 0;
float executar = 0;
float fonte1 = 0;
float fonte2 = 0;
float ph = 0;
float solenoide = 0;
float temperature = 0;
float tempo = 0;
float value = 0;
float voltage = 0;
int cicloAtual = 0;
int contaAds = 0;
int contaCiclos = 0;
int contaDes = 0;
int delimiter = 0;
int solen = 0;
int v1 = 0;
int v2 = 0;
int vai = 0;
int vPotencial = 0;
String propriety = "";
String respString = "";

//_______________________________________________________
void setup()
{
  Serial.begin(9600);
  Serial1.begin(2400);

  respString.reserve(260);

  pinMode( 44, OUTPUT);
  pinMode( 45, OUTPUT);
  pinMode( 46, OUTPUT);
  pinMode( 47, OUTPUT);
  pinMode( 48, OUTPUT);
  pinMode( 50, OUTPUT);
  pinMode( 52, OUTPUT);

  digitalWrite( 44, HIGH );
  digitalWrite( 45, HIGH );
  digitalWrite( 46, HIGH );
  digitalWrite( 47, HIGH );
  digitalWrite( 48, HIGH );
  digitalWrite( 50, HIGH );
  digitalWrite( 52, HIGH );
}
//_______________________________________________________
void loop() {
  serialEvent();
  serial1Send();
}
//_______________________________________________________
void serialEvent() {
  digitoVerificadorInicial = Serial.parseFloat(); // leitura da serial
  if (digitoVerificadorInicial == 8) { // teste básico(se o primeiro caractere (verificador) é igual a 8
    fonte1 = Serial.parseFloat();
    fonte2 = Serial.parseFloat();
    solenoide = Serial.parseFloat();
    executar = Serial.parseFloat();
    digitoVerificadorFinal = Serial.parseFloat();

    if (digitoVerificadorFinal == 922) { // verifica se o caractere verificador final foi recebido
      if(executar == 1) {
        roda();
      }
    }
    else{
      executar = 0;
    }
  }
}
//_______________________________________________________
void serial1Send() {
    char inChar = (char)Serial1.read();
    if (inChar == 10 || inChar == 13) { // Se for uma quebra de linha, gravar variável
      delimiter = respString.indexOf('=');
      if (delimiter != -1)  {
        propriety = respString.substring(0,delimiter-1);
        propriety.toLowerCase();
        propriety.trim();
        value = respString.substring(delimiter+1,respString.length()).toFloat();
        if (propriety == "ph") {
          ph = value;
        }
        else if (propriety == "temperature") {
          temperature = value;
        }
        else if (propriety == "conductivity") {
          conductivity = value;
        }
        else if (propriety == "voltage") {
          voltage = value;
        }
        propriety = "";
        value = -1;
        respString = "";
      }
    }
    if (inChar != 152) respString += inChar;
  sprintf(serialString, "p%04.2f;t%04.2f;c%04.2f;v%04.2f;n%07d", ph, temperature, conductivity, voltage, contaCiclos);
  Serial.println(serialString);
}
//_______________________________________________________
void roda(){
  if (solenoide == 1 ) {
    digitalWrite( 47, LOW );
  }
  else {
    digitalWrite( 47, HIGH );
  }
  if (fonte1 == 1 ) {
    ads();
  }
  else {
    if (fonte2 == 1) {
      des();
    }
    else {
      digitalWrite( 45, HIGH );
      digitalWrite( 46, HIGH );
    }
  }
}
//_______________________________________________________
void des()
{
  contaDes++;
  contaAds = 0;
  digitalWrite( 45, HIGH );
  digitalWrite( 46, LOW );
  if (cicloAtual == 0) {
    contaCiclos++;
  }
  cicloAtual = 1;
}
//_______________________________________________________
void ads()
{
  contaAds++;
  contaDes = 0;
  digitalWrite( 45, LOW );
  digitalWrite( 46, HIGH );
  if (cicloAtual == 1) {
    contaCiclos++;
  }
  cicloAtual = 0;
}

