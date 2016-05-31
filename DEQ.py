import sqlite3
from settings import Settings
import serial
import sys
import serial.tools.list_ports

db = sqlite3.connect('DEQ.sqlite')  # Conecta ao banco de dados
settingsObj = Settings()
valuesFromArduino = {}


def SaveToArduinoTable(dataToSave):
    cursor = db.cursor()
    sqlStringTemplate = ('''INSERT INTO'
        'arduino(variableID, value, modeID, fonte1, fonte2, solenoide)'
        'VALUES(?,?,?,?,?,?)''')

    for data in dataToSave:
        try:
            cursor.execute(sqlStringTemplate, data, settingsObj.modeID,
                           settingsObj.fonte1, settingsObj.fonte2, settingsObj.solenoide)
        except Exception as e:
            raise

    return true

# Função que setará o Arduino, escolhendo automaticamnte a porta em que
# ele está conectado e abrindo a sessão


def ArduinoSetup():

    int1 = 0
    str1 = ""
    str2 = ""

    # Find Live Ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:

        while int1 < 9:   # Loop checks "COM0" to "COM8" for Adruino Port Info.

            if "CH340" in p[1]:  # Looks for "CH340" in P[1].
                str2 = str(int1)  # Converts an Integer to a String, allowing:
                str1 = "COM" + str2  # add the strings together.

            if "CH340" in p[1] and str1 in p[1]:  # Looks for "CH340" and "COM#"
                # print "Found Arduino Uno on " + str1
                int1 = 9  # Causes loop to end.

            if int1 == 8:
                print ("Arduino not found!")
                sys.exit()  # Terminates Script.
                int1 = int1 + 1

    # Set Port
    # Put in your speed and timeout value.
    ser = serial.Serial(str1, 9600, timeout=10)

    # This begins the opening and printout of data from the Adruino.

    ser.close()  # In case the port is already open this closes it.
    ser.open()   # Reopen the port.

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
    settings.stateStartTime = timer.timer()
    if settingsObj.stateID == 1:
        settingsObj.stateID = 2
        serial.write(b'0,1,0')

    else:
        settingsObj.stateID = 1
        if settings.toggleSingle:
            serial.write(b'1,0,1')
        else:
            serial.write(b'1,0,0')


def shouldChangeStates(triggers):
    if 'timeAdsorption' in triggers:
        if settings.timeInCurrentState >= settings.timeAdsorption:
            return true

    if 'timeDesorption' in triggers:
        if settings.timeInCurrentState >= settings.timeDesorption:
            return true

    if 'minConductivityAdsorption' in triggers:
        if settings.minConductivityAdsorption > valuesFromArduino['condutividade']:
            return true

    if 'maxConductivityDesorption' in triggers:
        if settings.maxConductivityDesorption < valuesFromArduino['condutividade']:
            return true

    if 'cutPotentialAdsorption' in triggers:
        if settings.cutPotentialAdsorption > valuesFromArduino['potencialcelula']:
            return true

    if 'cutPotentialDesorption' in triggers:
        if settings.cutPotentialDesorption > valuesFromArduino['potencialcelula']:
            return true

    return false


def potenciostatico():
    triggers = ['timeAdsorption', 'timeDesorption',
                'minConductivityAdsorption', 'maxConductivityDesorption']


def GalvanoTempo():
    triggers = ['timeAdsorption', 'timeDesorption']


def GalvanoCond():
    triggers = ['minConductivityAdsorption', 'maxConductivityDesorption']


def GalvanoPot():
    triggers = ['cutPotentialAdsorption', 'cutPotentialDesorption']


def GalvanoGeral():
    triggers = ['timeAdsorption', 'timeDesorption', 'minConductivityAdsorption',
                'maxConductivityDesorption', 'cutPotentialAdsorption', 'cutPotentialDesorption']


def main():
    ser = ArduinoSetup()

    settings.solenoide = 0

    if settings.toggleAdsorption == True:
        settings.fonte1 = 1
        settings.fonte2 = 0
        settings.stateID = 1
        if settings.toggleSingle:
            settings.solenoide = 1
    else:
        settings.fonte1 = 0
        settings.fonte2 = 1
        settings.stateID = 2

    # Inicia o Arduino no estado correto
    ser.write(settings.fonte1, settings.fonte2, settings.solenoide)

    # Marca o tempo de início do primeiro estado
    settings.stateStartTime = time.time()

    if settingss.modeID == 1:  # Potenciostatico
        potenciostatico()

    if settingss.modeID == 2:  # Galvanostático - tempo
        GalvanoTempo()

    if settingss.modeID == 3:  # Galvanostático - condutividade
        GalvanoCond()

    if settingss.modeID == 4:  # galvanostático - potencialcelula
        GalvanoPot()

    if settingss.modeID == 5:  # galvanostático - geral
        GalvanoGeral()

    while settings.toggleOn and valuesFromArduino['nciclo'] < settings.numberCicles:

        time.sleep(1)
        leitura = ArduinoRead()

        if valuesFromArduino['condutividade'] > settings.maxConductivity:
            break  # NÃO FAZ NADA SE A CONDUTIVIDADE FOR MAIOR QUE A MÁXIMA

        if shouldChangeStates:
            changeState()

    ser.write(b'0,0,0')
