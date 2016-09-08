# -*- coding: utf-8 -*-

import sqlite3
import sys
import time
import serial
import serial.tools.list_ports

from settings import Settings


db = sqlite3.connect('DEQ.sqlite')  # Conecta ao banco de dados
settingsObj = Settings()  # Cria um novo objeto para armazenar configurações
valuesFromArduino = {}
valuesFromArduino['condutividade'] = 0
valuesFromArduino['pH'] = 0
valuesFromArduino['potencialcelula'] = 0
valuesFromArduino['nciclo'] = 0
valuesFromArduino['temperatura'] = 0

# Função que setará o Arduino, escolhendo automaticamnte a porta em que
# ele está conectado e abrindo a sessão
def ArduinoSetup():

    ports = list(serial.tools.list_ports.comports())
    COMstr = ""

    for p in ports:

        if "HL-340" in p[1] or "Arduino" in p[1] or "Serial" or "CH340" in p[1]:
            COMstr = p[0]

    if COMstr == "":
        print("Arduino não encontrado!")
        #tkinter.messagebox.showerror("Erro", "Arduino não encontrado!")
        settingsObj.toggleOn = 0
        return False

    else:
        try:
            ser = serial.Serial(COMstr, 9600, timeout=10)

            ser.close()
            ser.open()
        except:
            print("Erro ao conectar com o Arduino!")
            #tkinter.messagebox.showerror("Erro", "Erro ao conectar com o Arduino!")
            settingsObj.toggleOn = 0
            return False

        return ser

# Lê as informações vindas do arduino e salva no DB, o tempo de início da
# execução é o argumento
def ArduinoRead(ser):

    entrada = ser.readline()  # atribui à variável entrada uma linha vinda do Arduino

    # Procura pelos caractéres identificadores das variáveis na string do
    # arduino
    for i in range(0, len(entrada)):
        if (entrada[i] == 99):  # 99 = c
            valuesFromArduino['condutividade'] = float(entrada[i + 1:i + 8])
            print("condutividade = " + str(valuesFromArduino['condutividade']))
        if (entrada[i] == 112):  # 112 = p
            valuesFromArduino['pH'] = float(entrada[i + 1:i + 8])
            print("pH = " + str(valuesFromArduino['pH']))
        if (entrada[i] == 97):  # 97 = a
            valuesFromArduino['potencialcelula'] = float(
                entrada[i + 1:i + 8])  # Potencial de Célula
            print("potencialcelula = " +
                  str(valuesFromArduino['potencialcelula']))
        if (entrada[i] == 110):  # 110 = n
            valuesFromArduino['nciclo'] = float(entrada[i + 1:i + 8])
            print("nciclo = " + str(valuesFromArduino['nciclo']))
        if (entrada[i] == 116):  # 116 = t
            valuesFromArduino['temperatura'] = float(entrada[i + 1:i + 8])
            print("temperatura = " + str(valuesFromArduino['temperatura']))

    data = [(1, valuesFromArduino['condutividade']),
            (2, valuesFromArduino['pH']),
            (3, valuesFromArduino['potencialcelula']),
            (4, valuesFromArduino['nciclo']),
            (5, valuesFromArduino['temperatura'])]

    SaveToArduinoTable(data)


def SaveToArduinoTable(dataToSave):
    cursor = db.cursor()
    sqlStringTemplate = (
        '''INSERT INTO arduino(variableID, value, modeID, fonte1, fonte2, solenoide, currentUUID, timeInCurrentState, totalTime) VALUES(?,?,?,?,?,?,?,?,?)''')

    for data in dataToSave:
        try:
            cursor.execute(sqlStringTemplate, (data[0], data[1], settingsObj.modeID, settingsObj.fonte1,
                                               settingsObj.fonte2, settingsObj.solenoide, settingsObj.currentUUID, settingsObj.timeInCurrentState(), settingsObj.totalTime()))
            db.commit()
        except Exception as e:
            raise

    return True


def changeState(ser):
    settingsObj.stateStartTime = time.time()

    if settingsObj.stateID == 1:
        settingsObj.stateID = 2
        settingsObj.fonte1 = 0
        settingsObj.fonte2 = 1
        settingsObj.solenoide = 0
        ser.write(b'0,1,0')
        print("De adsorção para dessorção")

    else:
        settingsObj.stateID = 1
        if settingsObj.toggleSingle:
            settingsObj.fonte1 = 1
            settingsObj.fonte2 = 0
            settingsObj.solenoide = 1
            ser.write(b'1,0,1')
        else:
            ser.write(b'1,0,0')
            settingsObj.fonte1 = 1
            settingsObj.fonte2 = 0
            settingsObj.solenoide = 0
        print("De dessorção para adsorção")


def shouldChangeStates(triggers):
    if 'timeAdsorption' in triggers:
        if settingsObj.timeInCurrentState() >= settingsObj.timeAdsorption:
            print("timeAdsorption")
            return True

    if 'timeDesorption' in triggers:
        if settingsObj.timeInCurrentState() >= settingsObj.timeDesorption:
            print("timeDesorption")
            return True

    if 'minConductivityAdsorption' in triggers:
        if settingsObj.minConductivityAdsorption > valuesFromArduino['condutividade']:
            print("minConductivityAdsorption")
            return True

    if 'maxConductivityDesorption' in triggers:
        if settingsObj.maxConductivityDesorption < valuesFromArduino['condutividade']:
            print("maxConductivityDesorption")
            return True

    if 'cutPotentialAdsorption' in triggers:
        if settingsObj.cutPotentialAdsorption > valuesFromArduino['potencialcelula']:
            print("cutPotentialAdsorption")
            return True

    if 'cutPotentialDesorption' in triggers:
        if settingsObj.cutPotentialDesorption > valuesFromArduino['potencialcelula']:
            print("cutPotentialDesorption")
            return True

    return False


def main():
    ser = ArduinoSetup()

    if ser == False:
        return

    settingsObj.solenoide = 0

    if settingsObj.toggleAdsorption == True:
        settingsObj.fonte1 = 1
        settingsObj.fonte2 = 0
        settingsObj.stateID = 1
        if settingsObj.toggleSingle:
            settingsObj.solenoide = 1
    else:
        settingsObj.fonte1 = 0
        settingsObj.fonte2 = 1
        settingsObj.stateID = 2

    # Inicia o Arduino no estado correto
    print('%d;%d;%d' % (settingsObj.fonte1,
                        settingsObj.fonte2, settingsObj.solenoide))
    ser.write(b'0,0,0')
    time.sleep(5)
    ser.write(b'%d;%d;%d' % (settingsObj.fonte1,
                             settingsObj.fonte2, settingsObj.solenoide))
    time.sleep(5)
    ser.write(b'%d;%d;%d' % (settingsObj.fonte1,
                             settingsObj.fonte2, settingsObj.solenoide))
    print("Inicializando Arduino")

    # Marca o tempo de início do primeiro estado
    settingsObj.stateStartTime = time.time()

    if settingsObj.modeID == 1:  # Potenciostatico
        triggers = ['timeAdsorption', 'timeDesorption',
                    'minConductivityAdsorption', 'maxConductivityDesorption']

    if settingsObj.modeID == 2:  # Galvanostático - tempo
        triggers = ['timeAdsorption', 'timeDesorption']

    if settingsObj.modeID == 3:  # Galvanostático - condutividade
        triggers = ['minConductivityAdsorption', 'maxConductivityDesorption']

    if settingsObj.modeID == 4:  # galvanostático - potencialcelula
        triggers = ['cutPotentialAdsorption', 'cutPotentialDesorption']

    if settingsObj.modeID == 5:  # galvanostático - geral
        triggers = ['timeAdsorption', 'timeDesorption', 'minConductivityAdsorption',
                    'maxConductivityDesorption', 'cutPotentialAdsorption', 'cutPotentialDesorption']

    print(triggers)
    print(settingsObj.modeID)

    ArduinoRead(ser)

    print("ligado:" + str(settingsObj.toggleOn))
    print("ciclo:" +
          str(valuesFromArduino['nciclo']) + "/" + str(settingsObj.numberCicles))

    while settingsObj.toggleOn and valuesFromArduino['nciclo'] < settingsObj.numberCicles:

        print("ligado:" + str(settingsObj.toggleOn))
        print(
            "ciclo:" + str(valuesFromArduino['nciclo']) + "/" + str(settingsObj.numberCicles))

        time.sleep(1)  # Aguarda 1 segundo
        ArduinoRead(ser)

        if valuesFromArduino['condutividade'] > settingsObj.maxConductivity:
            break  # NÃO FAZ NADA SE A CONDUTIVIDADE FOR MAIOR QUE A MÁXIMA

        if shouldChangeStates(triggers):
            print("Trocando de estado")
            changeState(ser)

    settingsObj.toggleOn = 0
    ser.write(b'0,0,0')
    print("Fim da execução")

    return
