import matplotlib
matplotlib.use('TkAgg')

import time
import os
import uuid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import DEQ
import sched
from settings import Settings

try:
    import tkinter
except ImportError:
    print("tkinter não foi encontrado no sistema!")


s = sched.scheduler(time.time, time.sleep)
# except ImportError:
#print("matplotlib não foi encontrado no sistema!")

def updateGraph(self):
    for variableID in [1, 2, 3]:
        cursor = db.cursor().execute('SELECT value FROM arduino WHERE currentUUID=? AND variableID=?  ORDER BY ID LIMIT 30',
                                     self.DBConfig.currentUUID, variableID)
        result = cursor.fetchall()
        if variableID == 1:
            conductivityGraph['subplot'].clear()
            self.conductivityGraph['subplot'].plot(result)
            self.conductivityGraph['subplot'].draw()
        if variableID == 2:
            pHGraph['subplot'].clear()
            self.pHGraph['subplot'].plot(result)
            self.pHGraph['subplot'].draw()
        if variableID == 3:
            potentialGraph['subplot'].clear()
            self.potentialGraph['subplot'].plot(result)
            self.potentialGraph['subplot'].draw()

    s.enter(1, 1, updateGraph)

class simpleapp_tk(tkinter.Tk):

    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        filename = os.path.join(os.getcwd(), 'DEQ.sqlite')
        print(filename)
        if not os.path.isfile(filename):
            import createDB
            createDB.createDB()

        self.grid()

        self.config = {}

        self.DBConfig = Settings()

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
        self.config['toggleOn'] = tkinter.BooleanVar()
        self.config['toggleOn'].set(self.DBConfig.toggleOn)

        self.modeRadio1 = tkinter.Radiobutton(self, text="Potenciostático", variable=self.config[
            'modeID'], value=1, command=self.changeMode, indicatoron=0)
        self.modeRadio2 = tkinter.Radiobutton(self, text="Galvanostático por Tempo", variable=self.config[
            'modeID'], value=2, command=self.changeMode, indicatoron=0)
        self.modeRadio3 = tkinter.Radiobutton(self, text="Galvanostático por Condutividade", variable=self.config[
            'modeID'], value=3, command=self.changeMode, indicatoron=0)
        self.modeRadio4 = tkinter.Radiobutton(self, text="Galvanostático por Potencial", variable=self.config[
            'modeID'], value=4, command=self.changeMode, indicatoron=0)
        self.modeRadio5 = tkinter.Radiobutton(self, text="Galvanostático Geral", variable=self.config[
            'modeID'], value=5, command=self.changeMode, indicatoron=0)
        self.modeRadio1.grid(column=0, row=0, stick='EW')
        self.modeRadio2.grid(column=0, row=1, stick='EW')
        self.modeRadio3.grid(column=0, row=2, stick='EW')
        self.modeRadio4.grid(column=0, row=3, stick='EW')
        self.modeRadio5.grid(column=0, row=4, stick='EW')

        self.leftPanel = tkinter.Frame(self, relief='raised', borderwidth=1)
        self.leftPanel.grid(column=0, row=5)

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

        self.textDocumentLabel = tkinter.Label(
            self.leftPanel, text="Documento de texto")
        self.textDocumentLabel.grid(column=0, row=3)
        self.textDocument = tkinter.Entry(
            self.leftPanel, textvariable=self.config['textDocument'])
        self.textDocument.grid(column=1, row=3, stick='EW')

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
            self.leftPanel, textvariable=self.config['numberCicles'], state="disabled")
        self.numberCicles.grid(column=1, row=10, stick='EW')

        self.maxConductivityLabel = tkinter.Label(
            self.leftPanel, text="Conductividade Máxima")
        self.maxConductivityLabel.grid(column=0, row=11)
        self.maxConductivity = tkinter.Entry(
            self.leftPanel, textvariable=self.config['maxConductivity'], state="disabled")
        self.maxConductivity.grid(column=1, row=11, stick='EW')

        self.toggleOn = tkinter.Button(
            self, text="Ligar", command=self.saveConfig)
        self.toggleOn.grid(column=0, columnspan=2, row=12, stick='EW')

        # Gráficos

        self.graphPanel = tkinter.Frame(self)
        self.graphPanel.grid(column=1, row=0, columnspan=5)

        self.conductivityGraph = {}
        self.conductivityGraph['frame'] = tkinter.Frame(self.graphPanel)
        self.conductivityGraph['frame'].grid(column=0, row=0, rowspan=2)
        self.conductivityGraph['figure'] = Figure()
        self.conductivityGraph['subplot'] = self.conductivityGraph[
            'figure'].add_subplot(111)
        self.conductivityGraph['canvas'] = FigureCanvasTkAgg(
            self.conductivityGraph['figure'], master=self.conductivityGraph['frame'])
        self.conductivityGraph['canvas'].show()

        self.pHGraph = {}
        self.pHGraph['frame'] = tkinter.Frame(self.graphPanel)
        self.pHGraph['frame'].grid(column=1, row=0)
        self.pHGraph['figure'] = Figure()
        self.pHGraph['subplot'] = self.pHGraph['figure'].add_subplot(111)
        self.pHGraph['canvas'] = FigureCanvasTkAgg(
            self.pHGraph['figure'], master=self.pHGraph['frame'])
        self.pHGraph['canvas'].show()

        self.potentialGraph = {}
        self.potentialGraph['frame'] = tkinter.Frame(self.graphPanel)
        self.potentialGraph['frame'].grid(column=1, row=1)
        self.potentialGraph['figure'] = Figure()
        self.potentialGraph['subplot'] = self.potentialGraph[
            'figure'].add_subplot(111)
        self.potentialGraph['canvas'] = FigureCanvasTkAgg(
            self.potentialGraph['figure'], master=self.potentialGraph['frame'])
        self.potentialGraph['canvas'].show()

        s.enter(1, 1, updateGraph)

    def saveConfig(self):
        configToSave = {}
        for key, value in self.config.items():
            configToSave[key] = value.get()
        DEQ.main()

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

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Dessanilizador')
    app.mainloop()
