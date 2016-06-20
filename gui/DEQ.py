import sqlite3
import sys
import time

import serial
import serial.tools.list_ports

from settings import Settings

db = sqlite3.connect('DEQ.sqlite')  # Conecta ao banco de dados
settingsObj = Settings() # Cria um novo objeto para armazenar configurações
valuesFromArduino = {}


def SaveToArduinoTable(dataToSave):
    cursor = db.cursor()
    sqlStringTemplate = ('''INSERT INTO'
        'arduino(variableID, value, modeID, fonte1, fonte2, solenoide, currentUUID)'
        'VALUES(?,?,?,?,?,?,?)''')

    for data in dataToSave:
        try:
            cursor.execute(sqlStringTemplate, data, settingsObj.modeID,
                           settingsObj.fonte1, settingsObj.fonte2, settingsObj.solenoide, settingsObj.currentUUID)
        except Exception as e:
            raise

    return true

# Função que setará o Arduino, escolhendo automaticamnte a porta em que
# ele está conectado e abrindo a sessão


def ArduinoSetup():

    ports = list(serial.tools.list_ports.comports())
    COMstr = ""

    for p in ports:

        if "HL-340" in p[1] or "Arduino" in p[1] or "Serial" in p[1]:
            COMstr = p[0]

    if COMstr == "":
        print("Arduino não encontrado!")
        sys.exit()

    ser = serial.Serial(COMstr, 9600, timeout=10)


    ser.close()
    ser.open()

    return ser

# Lê as informações vindas do arduino e salva no DB, o tempo de início da
# execução é o argumento


def ArduinoRead():

    entrada = ser.readline()  # atribui à variável entrada uma linha vinda do Arduino

    # Procura pelos caractéres identificadores das variáveis na string do
    # arduino
    for i in range(0, len(entrada)):
        if (entrada[i] == 'c'):
            valuesFromArduino['condutividade'] = int(entrada[i + 1:i + 8])
        if (entrada[i] == 'p'):
            valuesFromArduino['pH'] = int(entrada[i + 1:i + 8])
        if (entrada[i] == 'a'):
            valuesFromArduino['potencialcelula'] = int(
                entrada[i + 1:i + 8])  # Potencial de Célula
        if (entrada[i] == 'n'):
            valuesFromArduino['nciclo'] = int(entrada[i + 1:i + 8])
        if (entrada[i] == 't'):
            valuesFromArduino['temperatura'] = int(entrada[i + 1:i + 8])

    data = [(1, valuesFromArduino['condutividade']),
            (2, valuesFromArduino['pH']),
            (3, valuesFromArduino['potencialcelula']),
            (4, valuesFromArduino['nciclo']),
            (5, valuesFromArduino['temperatura'])]

    SaveToArduinoTable(data)

    return condutividade, ph, potencialcelula, nciclo, temperatura


def changeState():
    settingsObj.stateStartTime = timer.timer()
    if settingsObj.stateID == 1:
        settingsObj.stateID = 2
        serial.write(b'0,1,0')

    else:
        settingsObj.stateID = 1
        if settingsObj.toggleSingle:
            serial.write(b'1,0,1')
        else:
            serial.write(b'1,0,0')


def shouldChangeStates(triggers):
    if 'timeAdsorption' in triggers:
        if settingsObj.timeInCurrentState >= settingsObj.timeAdsorption:
            return true

    if 'timeDesorption' in triggers:
        if settingsObj.timeInCurrentState >= settingsObj.timeDesorption:
            return true

    if 'minConductivityAdsorption' in triggers:
        if settingsObj.minConductivityAdsorption > valuesFromArduino['condutividade']:
            return true

    if 'maxConductivityDesorption' in triggers:
        if settingsObj.maxConductivityDesorption < valuesFromArduino['condutividade']:
            return true

    if 'cutPotentialAdsorption' in triggers:
        if settingsObj.cutPotentialAdsorption > valuesFromArduino['potencialcelula']:
            return true

    if 'cutPotentialDesorption' in triggers:
        if settingsObj.cutPotentialDesorption > valuesFromArduino['potencialcelula']:
            return true

    return false


def main():
    ser = ArduinoSetup()

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
    arduinoStr = str(settingsObj.fonte1) + ";" + \
        str(settingsObj.fonte2) + ";" + str(settingsObj.solenoide)
    print(arduinoStr)
    ser.write(arduinoStr.encode('utf-8'))

    # Marca o tempo de início do primeiro estado
    settingsObj.stateStartTime = time.time()

    print(settingsObj.modeID)

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

    while settingsObj.toggleOn and valuesFromArduino['nciclo'] < settingsObj.numberCicles:

        time.sleep(1)
        leitura = ArduinoRead()

        if valuesFromArduino['condutividade'] > settingsObj.maxConductivity:
            break  # NÃO FAZ NADA SE A CONDUTIVIDADE FOR MAIOR QUE A MÁXIMA

        if shouldChangeStates:
            changeState()

    ser.write(b'0,0,0')
