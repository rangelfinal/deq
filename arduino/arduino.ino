#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char inChar;
char *serialString;
float conductivity = -1;
float digitoVerificadorFinal = 0;
float digitoVerificadorInicial = 0;
float executar = 0;
float fonte1 = 0;
float fonte2 = 0;
float ph = -1;
float solenoide = 0;
float temperature = -1;
float tempo = 0;
float value = -1;
float voltage = -1;
int cicloAtual = 0;
int contaAds = 0;
int contaCiclos = 0;
int contaDes = 0;
int delimiter = 0;
int solen = 0;
int timeout = 5000;
int v1 = 0;
int v2 = 0;
int vai = 0;
int vPotencial = 0;
String propriety = "";
String respString = "";

//_______________________________________________________
void setup() {
  Serial.begin(250000);
  Serial1.begin(2400);

  while (!Serial && !Serial1) {} // Espera os seriais ficarem disponiveis
  respString.reserve(5000);

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
  delay(10);
  serial1Event();
}
//_______________________________________________________
void serialEvent() {
  // Formato da string de entrada: verificadorInicial(8);fonte1(0|1);fonte2(0|1);solenoide(0|1);executar(0|1);verificadorFinal(922)
  if (Serial.available() > 0) {
    digitoVerificadorInicial = Serial.parseFloat(); // leitura da serial
    if (digitoVerificadorInicial == 8) { // teste básico(se o primeiro caractere (verificador) é igual a 8
      fonte1 = Serial.parseFloat();
      fonte2 = Serial.parseFloat();
      solenoide = Serial.parseFloat();
      executar = Serial.parseFloat();
      digitoVerificadorFinal = Serial.parseFloat();
      cleanSerialBuffer();
      if (digitoVerificadorFinal == 922) { // verifica se o caractere verificador final foi recebido
        if (executar == 1) {
          roda();
        }
      }
      else {
        executar = 0;
      }
    }
  }
}
//_______________________________________________________
void serial1Event() {
  String line = "";
  if (Serial1.available()) {
    while (Serial1.available() > 0) {
      int readBit = Serial1.read();
      if (readBit != -1) {
        char inChar = (char)readBit;
        if (inChar != 152) respString += inChar;
      }
    }
    for(int aux = 0; aux < respString.length(); aux++) {
      int charValue = (int)respString[aux];
      line += respString[aux];
      if (charValue == 10 || charValue == 13) { // Se for uma quebra de linha, gravar variável
        delimiter = line.indexOf("=");
        if (delimiter != -1)  {
          propriety = line.substring(0, delimiter);
          propriety.toLowerCase();
          propriety.trim();
          value = line.substring(delimiter, line.length()).toFloat();
          if (propriety.indexOf("ph") != -1) {
            ph = value;
          }
          else if (propriety.indexOf("temperature") != -1) {
            temperature = value;
          }
          else if (propriety.indexOf("conductivity") != -1) {
            conductivity = value;
          }
          else if (propriety.indexOf("voltage") != -1) {
            voltage = value;
          }
          propriety = "";
          value = -1;
          line = "";
        }
      }
    }
    delay(50);
    serialSend();
  }
}
//_______________________________________________________
void serialSend() {
  sprintf(serialString, "p%04.2f;t%04.2f;c%04.2f;v%04.2f;n%07d", ph, temperature, conductivity, voltage, contaCiclos);
  delay(50);
  Serial.println("Serial send");
  Serial.println(serialString);
}
//_______________________________________________________
void roda() {
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
void des() {
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
void ads() {
  contaAds++;
  contaDes = 0;
  digitalWrite( 45, LOW );
  digitalWrite( 46, HIGH );
  if (cicloAtual == 1) {
    contaCiclos++;
  }
  cicloAtual = 0;
}
//_______________________________________________________
void cleanSerialBuffer() {
  while (Serial.available()) {
    char t = Serial.read();
  }
}
