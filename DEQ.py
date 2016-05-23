import sqlite3
import time
inicio = timer()  #Marca o início da execução
db=sqlite3.connect('DEQ.sqlite') #Conecta ao banco de dados
cursor=db.cursor()

def InterfaceToPython(): #Salva os dados provenientes da interface (que estarão no banco de dados) em variáveis do Python

    cursor.execute('SELECT value FROM interface WHERE name=toggleSingle')
    toggleSingle = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=toggleOn')
    toggleOn = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=toggleAdsorption')
    toggleAdsorption = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=textDocument')
    textDocument = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=timeAdsorption')
    timeAdsorption = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=timeDesorption')
    timeDesorption = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=minConductivityAdsorption')
    minConductivityAdsorption = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=maxConductivityDesorption')
    maxConductivityDesorption = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=cutPotentialAdsorption')
    cutPotentialAdsorption = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=cutPotentialDesorption')
    cutPotentialDesorption = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=numberCicles')
    numberCicles = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=maxConductivity')
    maxConductivity = cursor.fetchone()
    cursor.execute('SELECT value FROM interface WHERE name=mode')
    mode = cursor.fetchone()

    return toggleSingle, toggleOn, toggleAdsorption, textDocument, timeAdsorption, timeDesorption, minConductivityAdsorption, maxConductivityDesorption,minConductivityAdsorption,cutPotentialAdsorption, cutPotentialDesorption,numberCicles,maxConductivity, mode

def ArduinoSetup(): ####Função que setará o Arduino, escolhendo automaticamnte a porta em que ele está conectado e abrindo a sessão
    #######Código roubado, testar!########
    #######O Arduino dele "chama" "CH340" é necessário verificar o "nome" da nossa e mudar no código"

    import pySerial
    import serial
    import sys
    #import time
    import serial.tools.list_ports

    #serPort = ""
    int1 = 0
    str1 = ""
    str2 = ""

    # Find Live Ports
    ports = list(serial.tools.list_ports.comports())
    #for p in ports:
        #print p # This causes each port's information to be printed out. Usar para achar o nome da nossa placa
           # To search this p data, use p[1].

    while int1 < 9:   # Loop checks "COM0" to "COM8" for Adruino Port Info.

        if "CH340" in p[1]:  # Looks for "CH340" in P[1].
            str2 = str(int1) # Converts an Integer to a String, allowing:
            str1 = "COM" + str2 # add the strings together.

        if "CH340" in p[1] and str1 in p[1]: # Looks for "CH340" and "COM#"
            #print "Found Arduino Uno on " + str1
            int1 = 9 # Causes loop to end.

        if int1 == 8:
            print ("Arduino not found!")
            sys.exit() # Terminates Script.

        int1 = int1 + 1

        #time.sleep(5)  # Gives user 5 seconds to view Port information -- can be   changed/removed.

    # Set Port
    ser = serial.Serial(str1, 9600, timeout=10) # Put in your speed and timeout value.

    # This begins the opening and printout of data from the Adruino.

    ser.close()  # In case the port is already open this closes it.
    ser.open()   # Reopen the port.

    return ser

def ArduinoRead(inicio): #Lê as informações vindas do arduino e salva no DB, o tempo de início da execução é o argumento

    entrada = ser.readline() #atribui à variável entrada uma linha vinda do Arduino

    for i in range(0,len(entrada)): #Procura pelos caractéres identificadores das variáveis na string do arduino
        if (entrada[i]=='c'):
            condutividade=int(entrada[i+1:i+8])
        if (entrada[i]=='p'):
            pH=int(entrada[i+1:i+8])
        if (entrada[i]=='a'):
            potencialcelula=int(entrada[i+1:i+8]) #Potencial de Célula
        if (entrada[i]=='n'):
            nciclo=int(entrada[i+1:i+8])
        if (entrada[i]=='t'):
            temperatura=int(entrada[i+1:i+8])

    agora = timer()
    tempo = inicio - agora

    dados = [('condutividade',condutividade, tempo),
             ('pH',pH, tempo),
             ('potencialcelula', potencialcelula, tempo),
             ('nciclo', nciclo, tempo),
             ('temperatura', temperatura, tempo)]

    cursor.executemany(''' INSERT INTO arduino(name, value, time) VALUES(?,?,?)''', dados) #Insere dados no banco de dados

    return condutividade, ph, potencialcelula, nciclo, temperatura

def potenciostatico():
    tempoestado=inicioestado-timer()
    if estado = 'Adsorção':
        if tempoestado>=timeAdsorption or condutividade<=minConductivityAdsorption:
            estado='Dessorção'
            inicioestado=timer()
            serial.write(b'0,1,0')
            cursor.execute(' INSERT INTO python(name, value) VALUES(estado,0)')
    if estado = 'Dessorção':
        if tempoestado>=timeDesorption or condutividade>=maxConductivityDesorption:
            estado='Adsorção'
            inicioestado=timer()
            if toggleSingle = True:
                serial.write(b'1,0,1')
            else:
                serial.write(b'1,0,0')
            cursor.execute(' INSERT INTO python(name, value) VALUES(estado,1)')
    return inicioestado, estado


def GalvanoTempo():
    tempoestado=inicioestado-timer()
    if estado = 'Adsorção':
        if condutividade<=minConductivityAdsorption:
            estado='Dessorção'
            inicioestado=timer()
            serial.write(b'0,1,0')
            cursor.execute(' INSERT INTO python(name, value) VALUES(estado,0)')
        if estado = 'Dessorção':
            if condutividade>=maxConductivityDesorption:
                estado='Adsorção'
                inicioestado=timer()
                if toggleSingle = True:
                    serial.write(b'1,0,1')
                else:
                    serial.write(b'1,0,0')
                cursor.execute(' INSERT INTO python(name, value) VALUES(estado,1)')
    return inicioestado, estado

def GalvanoCond():
    if estado = 'Adsorção':
        if tempoestado>=timeAdsorption:
            estado='Dessorção'
            serial.write(b'0,1,0')
            cursor.execute(' INSERT INTO python(name, value) VALUES(estado,0)')
        if estado = 'Dessorção':
            if tempoestado>=timeDesorption:
                estado='Adsorção'
                if toggleSingle = True:
                    serial.write(b'1,0,1')
                else:
                    serial.write(b'1,0,0')
                cursor.execute(' INSERT INTO python(name, value) VALUES(estado,1)')
        return inicioestado, estado

def GalvanoPot():
    if estado = 'Adsorção':
        if potencialcelula>=cutPotentialAdsorption:
            estado='Dessorção'
            serial.write(b'0,1,0')
            cursor.execute(' INSERT INTO python(name, value) VALUES(estado,0)')
        if estado = 'Dessorção':
            if potencialcelula>=cutPotentialDesorption:
                estado='Adsorção'
                if toggleSingle = True:
                    serial.write(b'1,0,1')
                else:
                    serial.write(b'1,0,0')
                cursor.execute(' INSERT INTO python(name, value) VALUES(estado,1)')
        return estado

def GalvanoGeral():
    tempoestado=inicioestado-timer()
    if estado = 'Adsorção':
        if tempoestado>=timeAdsorption or condutividade<=minConductivityAdsorption or potencialcelula>=cutPotentialAdsorption:
            estado='Dessorção'
            inicioestado=timer()
            serial.write(b'0,1,0')
            cursor.execute(' INSERT INTO python(name, value) VALUES(estado,0)')
    if estado = 'Dessorção':
        if tempoestado>=timeDesorption or condutividade>=maxConductivityDesorption or potencialcelula>=cutPotentialAdsorption:
            estado='Adsorção'
            inicioestado=timer()
            if toggleSingle = True:
                serial.write(b'1,0,1')
            else:
                serial.write(b'1,0,0')
            cursor.execute(' INSERT INTO python(name, value) VALUES(estado,1)')
    return inicioestado, estado




def main():
    ser = ArduinoSetup()
    interface = InterfaceToPython()
    #####Transforma as coisas retornadas pela função InterfaceToPython em variáveis "globais" de nome mais intuitivo.
    toggleSingle=interface[0]
    toggleOn=interface[1]
    toggleAdsorption=interface[2]
    textDocument=interface[3]
    timeAdsorption=interface[4]
    timeDesorption=interface[5]
    minConductivityAdsorption=interface[6]
    maxConductivityDesorption=interface[7]
    minConductivityAdsorption=interface[8]
    cutPotentialAdsorption=interface[9]
    cutPotentialDesorption=interface[10]
    numberCicles=interface[11]
    maxConductivity=interface[12]
    mode = interface[13]
    ########################################################################################
    if toggleAdsorption = True:
        fonte1 = 1
        fonte2= 0
        estado = 'Adsorção'
        cursor.execute(' INSERT INTO python(name, value) VALUES(estado,1)')
    else:
        fonte1=0
        fonte2=1
        estado='Dessorção'
        cursor.execute(' INSERT INTO python(name, value) VALUES(estado,0)')

    if toggleSingle = True:
        bobina = fonte1
    else:
        bobina=0
    ser.write(fonte1,fonte2,bobina) #Inicia o Arduino no estado correto

    inicioestado=timer()#Marca o tempo de início do primeiro estado
    nciclo = 0

    while toggleOn=true and nciclo<numberCicles:

        time.sleep(1)
        leitura=ArduinoRead(inicio)
        condutividade=leitura[0]
        ph = leitura[1]
        potencialcelula = leitura[2]
        nciclo = leitura[3]
        agora=timer()
        agora=inicio-agora
        dados=['tempo',agora]
        cursor.execute(' INSERT INTO python(name, value) VALUES(?,?)', dados)

        if condutividade<maxConductivity: #####NÃO FAZ NADA SE A CONDUTIVIDADE FOR MAIOR QUE A MÁXIMA - REVER
            if mode=1: #Potenciostatico
                aux=potenciostatico()
                inicioestado = aux[0]
                estado = aux[1]

            if mode=2: #Galvanostático - tempo
                estado=GalvanoTempo()

            if mode=3: #Galvanostático - condutividade
                estado=GalvanoCond()

            if mode=4: #galvanostático - potencialcelula
                estado = GalvanoPot()

            if mode=5: #galvanostático - geral
                aux=GalvanoGeral()
                inicioestado = aux[0]
                estado = aux[1]

    ser.write(b'0,0,0')

main()
