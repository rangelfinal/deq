#include <stdio.h>
#include <string.h>
#include <stdlib.h>

String input, inputteste;
int fonte1, fonte2, solenoide, executar, contaQuebraLinhas, contaDes, contaAds, cicloAtual;
int contaCiclos = 0;
//_______________________________________________________
void setup() {
  Serial.begin(9600);
  Serial1.begin(2400);

  while (!Serial && !Serial1) {} // Espera os seriais ficarem disponiveis
  input = "";
  contaQuebraLinhas = 0;

  pinMode( 22, INPUT);
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
  serialRead();
  serial1Read();
}
//_______________________________________________________
void serialRead() {
  // Formato da string de entrada: verificadorInicial(8);fonte1(0|1);fonte2(0|1);solenoide(0|1);executar(0|1);verificadorFinal(922)
  if (Serial.available() > 0) {
    float digitoVerificadorInicial = Serial.parseFloat(); // leitura da serial
    if (digitoVerificadorInicial == 8) { // teste básico(se o primeiro caractere (verificador) é igual a 8
      fonte1 = Serial.parseFloat();
      fonte2 = Serial.parseFloat();
      solenoide = Serial.parseFloat();
      executar = Serial.parseFloat();
      float digitoVerificadorFinal = Serial.parseFloat();
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
String ph = "p0000.00";
String temperatura = "t0000.00";
String condutividade = "c0000.00";
String voltagem = "v0000.00";
void serial1Read() {
  if (Serial1.available() > 0) {
    char charRead = Serial1.read();
    int intRead = (int) charRead;
    if (intRead != -1 && intRead != 10 && intRead != 13) {
      input += charRead;
    }
    if (intRead == 10 || intRead == 13) {
      input += ';';
      contaQuebraLinhas++;
    }
    else {
      contaQuebraLinhas = 0;
    }
    if (contaQuebraLinhas == 4) {
      int aux = 0;
      contaQuebraLinhas = 0;
      char charBuffer[7];
      while (aux != -1) {
        aux = input.indexOf('=', aux+1);
        String variavel = input.substring(input.lastIndexOf(';', aux-1)+1, aux);
        variavel.trim();
        variavel.toLowerCase();
        String valor = input.substring(aux + 1, input.indexOf(';', aux + 1));
        valor.trim();
        valor.toLowerCase();
        if (variavel == "ph") {
          dtostrf(valor.toFloat(),7, 2, charBuffer);
          ph = "p" + String(charBuffer);
        } 
        else if (variavel == "temperature") {
          dtostrf(valor.toFloat(),7, 2, charBuffer);
          temperatura = "t" + String(charBuffer);
        }
        else if (variavel == "conductivity") {
          dtostrf(valor.toFloat(),7, 2, charBuffer);
          condutividade = "c" + String(charBuffer);
        }
        else if (variavel == "voltage") {
          dtostrf(valor.toFloat(),7, 2, charBuffer);
          voltagem = "v" + String(charBuffer);
        }
      }
      dtostrf(contaCiclos,7,0,charBuffer);
      String contaCiclos = "n" +  String(charBuffer);
      String result = ph+temperatura+condutividade+voltagem+contaCiclos;
      result.replace(" ","0");
      Serial.println(ph+temperatura+condutividade+voltagem+contaCiclos);
      input = "";
    }
  }
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
