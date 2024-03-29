#include <stdio.h>
#include <string.h>
#include <stdlib.h>

String input, inputteste;
int fonte1, fonte2, solenoide, contaQuebraLinhas, cicloAtual;
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
        // Formato da string de entrada: fonte1(0|1);fonte2(0|1);solenoide(0|1);
        if (Serial.available() > 0) {
                fonte1 = Serial.parseFloat();
                fonte2 = Serial.parseFloat();
                solenoide = Serial.parseFloat();
                cleanSerialBuffer();
                exec();
                Serial.println("r");
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
                                        float tempValor = valor.toFloat();
                                        if (valor.indexOf("m") >= 0) {
                                                tempValor *= 1000;
                                        }
                                        dtostrf(tempValor,7, 2, charBuffer);
                                        condutividade = "c" + String(charBuffer);
                                }
                                else if (variavel == "voltage") {
                                        dtostrf(valor.toFloat(),7, 2, charBuffer);
                                        voltagem = "v" + String(charBuffer);
                                }
                        }
                        int vpotencial = map( analogRead(A0), 0, 1024, 0, 5000);
                        dtostrf(vpotencial,7,0,charBuffer);
                        String sPotencial = "a" + String(charBuffer);
                        dtostrf(contaCiclos,7,0,charBuffer);
                        String sContaCiclos = "n" +  String(charBuffer);
                        String result = ph+temperatura+condutividade+voltagem+sContaCiclos+sPotencial;
                        result.replace(" ","0");
                        if (fonte1 || fonte2)
                                Serial.println(result);
                        input = "";
                }
        }
}
//_______________________________________________________
void exec() {
        if (solenoide) {
                digitalWrite( 47, LOW );
        }
        else {
                digitalWrite( 47, HIGH );
        }

        if (fonte1) {
                ads();
        }
        else if (fonte2) {
                des();
        }
        else {
                digitalWrite( 45, HIGH );
                digitalWrite( 46, HIGH );
                contaCiclos = 0;
        }
}
//_______________________________________________________
void des() {
        digitalWrite( 45, HIGH );
        digitalWrite( 46, LOW );
        if (!cicloAtual) {
                contaCiclos++;
        }
        cicloAtual = 1;
}
//_______________________________________________________
void ads() {
        digitalWrite( 45, LOW );
        digitalWrite( 46, HIGH );
        if (cicloAtual) {
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
