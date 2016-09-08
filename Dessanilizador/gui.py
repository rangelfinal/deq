# -*- coding: utf-8 -*-

import os
import sqlite3
import threading
import time
import uuid
from multiprocessing import Process

import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import DEQ
from settings import Settings

matplotlib.use('TkAgg')

import tkinter

p = Process(target=DEQ.main)

db = sqlite3.connect('DEQ.sqlite', check_same_thread=False)


class simpleapp_tk(tkinter.Tk):

    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.attributes('-fullscreen', True)

        filename = os.path.join(os.getcwd(), 'DEQ.sqlite')
        print(filename)
        if not os.path.isfile(filename):
            import createDB
            createDB.createDB()

        self.grid()

        self.config = {}

        self.DBConfig = Settings()
        self.DBConfig.toggleOn = 0

        self.DBConfig.currentUUID = uuid.uuid4().hex

        self.config['modeID'] = tkinter.IntVar()
        self.config['toggleSingle'] = tkinter.BooleanVar()
        self.config['toggleSingle'].set(self.DBConfig.toggleSingle)
        self.config['toggleAdsorption'] = tkinter.BooleanVar()
        self.config['toggleAdsorption'].set(self.DBConfig.toggleAdsorption)
        self.config['textDocument'] = tkinter.StringVar()
        self.config['textDocument'].set(self.DBConfig.textDocument)
        self.config['timeAdsorption'] = tkinter.DoubleVar()
        self.config['timeAdsorption'].set(self.DBConfig.timeAdsorption)
        self.config['timeDesorption'] = tkinter.DoubleVar()
        self.config['timeDesorption'].set(self.DBConfig.timeDesorption)
        self.config['minConductivityAdsorption'] = tkinter.DoubleVar()
        self.config['minConductivityAdsorption'].set(
            self.DBConfig.minConductivityAdsorption)
        self.config['maxConductivityDesorption'] = tkinter.DoubleVar()
        self.config['maxConductivityDesorption'].set(
            self.DBConfig.maxConductivityDesorption)
        self.config['cutPotentialAdsorption'] = tkinter.DoubleVar()
        self.config['cutPotentialAdsorption'].set(
            self.DBConfig.cutPotentialAdsorption)
        self.config['cutPotentialDesorption'] = tkinter.DoubleVar()
        self.config['cutPotentialDesorption'].set(
            self.DBConfig.cutPotentialDesorption)
        self.config['numberCicles'] = tkinter.IntVar()
        self.config['numberCicles'].set(self.DBConfig.numberCicles)
        self.config['maxConductivity'] = tkinter.DoubleVar()
        self.config['maxConductivity'].set(self.DBConfig.maxConductivity)
        self.config['timeInCurrentState'] = tkinter.IntVar()
        self.config['timeInCurrentState'].set(0)
        self.config['currentConductivity'] = tkinter.DoubleVar()
        self.config['currentConductivity'].set(0)
        self.config['currentpH'] = tkinter.DoubleVar()
        self.config['currentpH'].set(0)
        self.config['currentPotential'] = tkinter.DoubleVar()
        self.config['currentPotential'].set(0)
        self.config['showLast30Points'] = tkinter.BooleanVar()
        self.config['showLast30Points'].set(0)

        self.radioPanel = tkinter.Frame(self, relief='raised', borderwidth=1)
        self.radioPanel.grid(column=0, row=0, stick='WE')

        self.modeRadio1 = tkinter.Radiobutton(self.radioPanel, text="Potenciostático", variable=self.config[
            'modeID'], value=1, command=self.changeMode, indicatoron=0)
        self.modeRadio2 = tkinter.Radiobutton(self.radioPanel, text="Galvanostático por Tempo", variable=self.config[
            'modeID'], value=2, command=self.changeMode, indicatoron=0)
        self.modeRadio3 = tkinter.Radiobutton(self.radioPanel, text="Galvanostático por Condutividade", variable=self.config[
            'modeID'], value=3, command=self.changeMode, indicatoron=0)
        self.modeRadio4 = tkinter.Radiobutton(self.radioPanel, text="Galvanostático por Potencial", variable=self.config[
            'modeID'], value=4, command=self.changeMode, indicatoron=0)
        self.modeRadio5 = tkinter.Radiobutton(self.radioPanel, text="Galvanostático Geral", variable=self.config[
            'modeID'], value=5, command=self.changeMode, indicatoron=0)
        self.modeRadio1.grid(column=0, columnspan=2, row=0, stick='WENS')
        self.modeRadio2.grid(column=0, row=1, stick='WENS')
        self.modeRadio3.grid(column=0, row=2, stick='WENS')
        self.modeRadio4.grid(column=0, row=3, stick='WENS')
        self.modeRadio5.grid(column=0, row=4, stick='WENS')

        # Painel esquerdo

        self.leftPanel = tkinter.Frame(self, relief='raised', borderwidth=1)
        self.leftPanel.grid(column=0, row=1, stick='WENS')

        self.toggleSingleLabel = tkinter.Label(
            self.leftPanel, text="Single-Pass")
        self.toggleSingleLabel.grid(column=0, row=1)
        self.toggleSingle = tkinter.Checkbutton(
            self.leftPanel, variable=self.config['toggleSingle'])
        self.toggleSingle.grid(column=1, row=1, stick='EW')

        self.toggleAdsorptionLabel = tkinter.Label(
            self.leftPanel, text="Iniciar com Adsorção")
        self.toggleAdsorptionLabel.grid(column=0, row=2)
        self.toggleAdsorption = tkinter.Checkbutton(
            self.leftPanel, variable=self.config['toggleAdsorption'])
        self.toggleAdsorption.grid(column=1, row=2, stick='EW')

        self.timeOptions = {}

        self.timeAdsorptionLabel = tkinter.Label(
            self.leftPanel, text="Tempo - Adsorção")
        self.timeAdsorptionLabel.grid(column=0, row=4)
        self.timeOptions['timeAdsorption'] = tkinter.Entry(
            self.leftPanel, textvariable=self.config['timeAdsorption'], state="disabled")
        self.timeOptions['timeAdsorption'].grid(column=1, row=4, stick='EW')

        self.timeDesorptionLabel = tkinter.Label(
            self.leftPanel, text="Tempo - Dessorção")
        self.timeDesorptionLabel.grid(column=0, row=5)
        self.timeOptions['timeDesorption'] = tkinter.Entry(
            self.leftPanel, textvariable=self.config['timeDesorption'], state="disabled")
        self.timeOptions['timeDesorption'].grid(column=1, row=5, stick='EW')

        self.conductivityOptions = {}

        self.minConductivityAdsorptionLabel = tkinter.Label(
            self.leftPanel, text="Condutividade Minima - Adsorção")
        self.minConductivityAdsorptionLabel.grid(column=0, row=6)
        self.conductivityOptions['minConductivityAdsorption'] = tkinter.Entry(
            self.leftPanel, textvariable=self.config['minConductivityAdsorption'], state="disabled")
        self.conductivityOptions['minConductivityAdsorption'].grid(
            column=1, row=6, stick='EW')

        self.maxConductivityDesorptionLabel = tkinter.Label(
            self.leftPanel, text="Condutividade Máxima - Dessorção")
        self.maxConductivityDesorptionLabel.grid(column=0, row=7)
        self.conductivityOptions['maxConductivityDesorption'] = tkinter.Entry(
            self.leftPanel, textvariable=self.config['maxConductivityDesorption'], state="disabled")
        self.conductivityOptions['maxConductivityDesorption'].grid(
            column=1, row=7, stick='EW')

        self.potentialOptions = {}

        self.cutPotentialAdsorptionLabel = tkinter.Label(
            self.leftPanel, text="Potencial de corte - Adsorção")
        self.cutPotentialAdsorptionLabel.grid(column=0, row=8)
        self.potentialOptions['cutPotentialAdsorption'] = tkinter.Entry(
            self.leftPanel, textvariable=self.config['cutPotentialAdsorption'], state="disabled")
        self.potentialOptions['cutPotentialAdsorption'].grid(
            column=1, row=8, stick='EW')

        self.cutPotentialDesorptionLabel = tkinter.Label(
            self.leftPanel, text="Potencial de corte - Dessorção")
        self.cutPotentialDesorptionLabel.grid(column=0, row=9)
        self.potentialOptions['cutPotentialDesorption'] = tkinter.Entry(
            self.leftPanel, textvariable=self.config['cutPotentialDesorption'], state="disabled")
        self.potentialOptions['cutPotentialDesorption'].grid(
            column=1, row=9, stick='EW')

        self.numberCiclesLabel = tkinter.Label(
            self.leftPanel, text="Numero de Ciclos")
        self.numberCiclesLabel.grid(column=0, row=10)
        self.numberCicles = tkinter.Entry(
            self.leftPanel, textvariable=self.config['numberCicles'])
        self.numberCicles.grid(column=1, row=10, stick='EW')

        self.maxConductivityLabel = tkinter.Label(
            self.leftPanel, text="Conductividade Máxima")
        self.maxConductivityLabel.grid(column=0, row=11)
        self.maxConductivity = tkinter.Entry(
            self.leftPanel, textvariable=self.config['maxConductivity'])
        self.maxConductivity.grid(column=1, row=11, stick='EW')

        self.ShowLast30PointsLabel = tkinter.Label(
            self.leftPanel, text="Exibir ultimos 30 pontos")
        self.ShowLast30PointsLabel.grid(column=0, row=12)
        self.ShowLast30Points = tkinter.Checkbutton(
            self.leftPanel, variable=self.config['showLast30Points'])
        self.ShowLast30Points.grid(column=1, row=12, stick='EW')

        self.toggleOn = tkinter.Button(
            self, text="Ligar", command=self.toggleOnClick)
        self.toggleOn.grid(column=0, row=2, stick='EW')

        self.exitButton = tkinter.Button(
            self, text="Sair", command=self.exitButtonClick)
        self.exitButton.grid(column=0, row=3, stick='EW')

        # Gráficos

        self.graphPanel = tkinter.Frame(self, bd=1, relief='sunken')
        self.graphPanel.grid(column=1, row=0, rowspan=4)

        self.figure = Figure(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graphPanel)
        self.gridspec = gridspec.GridSpec(5, 2)
        self.gridspec.update(hspace=0.3, wspace=0.3)

        self.conductivityGraph = {}
        self.conductivityGraph['subplot'] = self.figure.add_subplot(self.gridspec[
                                                                    :-2, :])
        self.conductivityGraph['subplot'].set_title("Condutividade")
        self.conductivityGraph['subplot'].tick_params(
            direction='inout', length=6, width=2, colors='b')
        self.conductivityGraph['subplot'].grid(True)
        self.conductivityGraph['subplot'].set_xlabel("Tempo (s)")
        self.conductivityGraph['subplot'].set_xbound(lower=0)

        self.pHGraph = {}
        self.pHGraph['subplot'] = self.figure.add_subplot(self.gridspec[3:, 0])
        self.pHGraph['subplot'].set_title("pH")
        self.pHGraph['subplot'].tick_params(
            direction='inout', length=6, width=2, colors='b')
        self.pHGraph['subplot'].grid(True)
        self.pHGraph['subplot'].set_xlabel("Tempo (s)")
        self.pHGraph['subplot'].set_xbound(lower=0)

        self.potentialGraph = {}
        self.potentialGraph['subplot'] = self.figure.add_subplot(self.gridspec[
                                                                 3:, 1])
        self.potentialGraph['subplot'].set_title("Potencial")
        self.potentialGraph['subplot'].tick_params(
            direction='inout', length=6, width=2, colors='b')
        self.potentialGraph['subplot'].grid(True)
        self.potentialGraph['subplot'].set_xlabel("Tempo (s)")
        self.potentialGraph['subplot'].set_xbound(lower=0)

        self.canvas.get_tk_widget().grid(column=0, row=0)
        self.canvas.show()

        # Painel direito

        self.rightPanel = tkinter.Frame(self, relief='raised', borderwidth=1)
        self.rightPanel.grid(column=2, row=0)

        self.timeInCurrentStateLabel = tkinter.Label(
            self.rightPanel, text="Tempo no estado atual:")
        self.timeInCurrentStateLabel.grid(column=0, row=0)
        self.timeInCurrentState = tkinter.Entry(
            self.rightPanel, textvariable=self.config['timeInCurrentState'], state='readonly')
        self.timeInCurrentState.grid(column=0, row=1)

        self.currentConductivityLabel = tkinter.Label(
            self.rightPanel, text="Condutividade atual:")
        self.currentConductivityLabel.grid(column=0, row=2)
        self.currentConductivity = tkinter.Entry(
            self.rightPanel, textvariable=self.config['currentConductivity'], state='readonly')
        self.currentConductivity.grid(column=0, row=3)

        self.currentpHLabel = tkinter.Label(self.rightPanel, text="pH atual:")
        self.currentpHLabel.grid(column=0, row=4)
        self.currentpH = tkinter.Entry(
            self.rightPanel, textvariable=self.config['currentpH'], state='readonly')
        self.currentpH.grid(column=0, row=5)

        self.currentPotentialLabel = tkinter.Label(
            self.rightPanel, text="Condutividade atual:")
        self.currentPotentialLabel.grid(column=0, row=6)
        self.currentPotential = tkinter.Entry(
            self.rightPanel, textvariable=self.config['currentPotential'], state='readonly')
        self.currentPotential.grid(column=0, row=7)

        tkinter.Tk.update(self)

    def turnOn(self):
        if self.DBConfig.toggleOn == 0:
            self.DBConfig.toggleOn = 1

        self.toggleOn.config(text="Desligar")
        print("Ligando")
        self.DBConfig.currentUUID = uuid.uuid4().hex
        self.DBConfig.currentExecutionStartTime = time.time()
        self.saveConfigToDb()
        global p
        if p.is_alive():
            p.join()

        # Reseta o processo para que esse possa ser lançado novamente

        p = None
        p = Process(target=DEQ.main)

        p.start()

        t = threading.Timer(1, self.updateGraph)
        t.daemon = True
        t.start()

    def turnOff(self):
        if self.DBConfig.toggleOn == 1:
            self.DBConfig.toggleOn = 0

        if p.is_alive():
            p.join()

        self.toggleOn.config(text="Ligar")
        self.saveConfigToDb()
        print("Desligando")

    def updateGraph(self):
        for variableID in [1, 2, 3]:
            SQLString = 'SELECT value, totalTime FROM (SELECT ID, value, totalTime FROM arduino WHERE currentUUID=''?'' AND variableID=? ORDER BY timeInCurrentState DESC'
            if self.config['showLast30Points'].get():
                SQLString += ' LIMIT 30'
            SQLString += ') ORDER BY ID'
            cursor = db.cursor().execute(SQLString, (self.DBConfig.currentUUID, variableID))
            result = cursor.fetchall()

            if result != None and result != []:
                breaks = [i for i in range(1, len(result)) if result[
                    i][0] < result[i - 1][0]]
                splitedResult = [result[x:y]
                                 for x, y in zip([0] + breaks, breaks + [None])]

                if variableID == 1:
                    if breaks:
                        for result in splitedResult:
                            self.conductivityGraph['subplot'].plot([item[1] for item in result], [
                                                                   item[0] for item in result], 'go-')
                        try:
                            self.config['currentConductivity'].set(
                                result[-1][-1][0])
                        except:
                            try:
                                self.config['currentConductivity'].set(
                                    result[-1][0])
                            except:
                                pass
                    else:
                        self.conductivityGraph['subplot'].plot([item[1] for item in result], [
                                                               item[0] for item in result], 'go-')

                        self.config['currentConductivity'].set(result[-1][0])

                if variableID == 2:
                    if breaks:
                        for result in splitedResult:
                            self.pHGraph['subplot'].plot([item[1] for item in result], [
                                                         item[0] for item in result], 'go-')
                        try:
                            self.config['currentpH'].set(result[-1][-1][0])
                        except:
                            try:
                                self.config['currentpH'].set(result[-1][0])
                            except:
                                pass

                    else:
                        self.pHGraph['subplot'].plot([item[1] for item in result], [
                                                     item[0] for item in result], 'go-')
                        self.config['currentpH'].set(result[-1][0])

                if variableID == 3:
                    if breaks:
                        for result in splitedResult:
                            self.potentialGraph['subplot'].plot([item[1] for item in result], [
                                                                item[0] for item in result], 'go-')
                        try:
                            self.config['currentPotential'].set(result[-1][-1][0])
                        except:
                            try:
                                self.config['currentPotential'].set(result[-1][0])
                            except:
                                pass
                    else:
                        self.potentialGraph['subplot'].plot([item[1] for item in result], [
                                                            item[0] for item in result], 'go-')
                        self.config['currentPotential'].set(result[-1][0])

        if(self.DBConfig.toggleOn == 0):
            self.toggleOn.config(text="Ligar")

        if (self.DBConfig.toggleOn == 1 and not p.is_alive()) or (self.DBConfig.toggleOn == 0 and p.is_alive()):
            self.turnOff()

        self.config['timeInCurrentState'].set(
            int(self.DBConfig.timeInCurrentState()))

        self.canvas.draw()

        if (self.DBConfig.toggleOn == 1):
            t = threading.Timer(1, self.updateGraph)
            t.daemon = True
            t.start()

    def saveConfigToDb(self):
        self.DBConfig.toggleSingle = self.config['toggleSingle'].get()
        self.DBConfig.toggleAdsorption = self.config['toggleAdsorption'].get()
        self.DBConfig.textDocument = self.config['textDocument'].get()
        self.DBConfig.timeAdsorption = self.config['timeAdsorption'].get()
        self.DBConfig.timeDesorption = self.config['timeDesorption'].get()
        self.DBConfig.minConductivityAdsorption = self.config[
            'minConductivityAdsorption'].get()
        self.DBConfig.maxConductivityDesorption = self.config[
            'maxConductivityDesorption'].get()
        self.DBConfig.cutPotentialAdsorption = self.config[
            'cutPotentialAdsorption'].get()
        self.DBConfig.cutPotentialDesorption = self.config[
            'cutPotentialDesorption'].get()
        self.DBConfig.numberCicles = self.config['numberCicles'].get()
        self.DBConfig.maxConductivity = self.config['maxConductivity'].get()

    def toggleOnClick(self):
        if self.DBConfig.toggleOn == 0:
            self.turnOn()

        elif self.DBConfig.toggleOn == 1:
            self.turnOff()

    def exitButtonClick(self):
        self.turnOff()
        self.quit()

    def changeMode(self):
        if self.config['modeID'].get() == 1:
            for key, opt in self.timeOptions.items():
                opt.config(state='normal')
            for key, opt in self.conductivityOptions.items():
                opt.config(state='normal')
            for key, opt in self.potentialOptions.items():
                opt.config(state='disabled')
        elif self.config['modeID'].get() == 2:
            for key, opt in self.timeOptions.items():
                opt.config(state='normal')
            for key, opt in self.conductivityOptions.items():
                opt.config(state='disabled')
            for key, opt in self.potentialOptions.items():
                opt.config(state='disabled')
        elif self.config['modeID'].get() == 3:
            for key, opt in self.timeOptions.items():
                opt.config(state='disabled')
            for key, opt in self.conductivityOptions.items():
                opt.config(state='normal')
            for key, opt in self.potentialOptions.items():
                opt.config(state='disabled')
        elif self.config['modeID'].get() == 4:
            for key, opt in self.timeOptions.items():
                opt.config(state='disabled')
            for key, opt in self.conductivityOptions.items():
                opt.config(state='disabled')
            for key, opt in self.potentialOptions.items():
                opt.config(state='normal')
        elif self.config['modeID'].get() == 5:
            for key, opt in self.timeOptions.items():
                opt.config(state='normal')
            for key, opt in self.conductivityOptions.items():
                opt.config(state='normal')
            for key, opt in self.potentialOptions.items():
                opt.config(state='normal')

        self.DBConfig.modeID = self.config['modeID'].get()

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Dessanilizador')
    app.mainloop()
