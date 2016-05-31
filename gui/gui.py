import ../settings

try:
    import tkinter
except ImportError:
    print("tkinter não foi encontrado no sistema!")

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.config = {}

        self.DBConfig = Settings()

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
        self.config['minConductivityAdsorption'].set(self.DBConfig.minConductivityAdsorption)
        self.config['maxConductivityDesorption'] = tkinter.DoubleVar()
        self.config['maxConductivityDesorption'].set(self.DBConfig.maxConductivityDesorption)
        self.config['cutPotentialAdsorption'] = tkinter.DoubleVar()
        self.config['cutPotentialAdsorption'].set(self.DBConfig.cutPotentialAdsorption)
        self.config['cutPotentialDesorption'] = tkinter.DoubleVar()
        self.config['cutPotentialDesorption'].set(self.DBConfig.cutPotentialDesorption)
        self.config['numberCicles'] = tkinter.IntVar()
        self.config['numberCicles'].set(self.DBConfig.numberCicles)
        self.config['maxConductivity'] = tkinter.DoubleVar()
        self.config['maxConductivity'].set(self.DBConfig.maxConductivity)
        self.config['toggleOn'] = tkinter.BooleanVar()
        self.config['toggleOn'].set(self.DBConfig.toggleOn)

        self.modeRadio = tkinter.Radiobutton(self, text="Potenciostático", variable = self.config['modeID'], value=1, command=self.changeMode)
        self.modeRadio = tkinter.Radiobutton(self, text="Galvanostático por Tempo", variable = self.config['modeID'], value=2, command=self.changeMode)
        self.modeRadio = tkinter.Radiobutton(self, text="Galvanostático por Condutividade", variable = self.config['modeID'], value=3, command=self.changeMode)
        self.modeRadio = tkinter.Radiobutton(self, text="Galvanostático por Potencial", variable = self.config['modeID'], value=4, command=self.changeMode)
        self.modeRadio = tkinter.Radiobutton(self, text="Galvanostático Geral", variable = self.config['modeID'], value=5, command=self.changeMode)

        self.leftPanel = tkinter.Frame(self, relief=RAISED, borderwidth=1)

        self.toggleSingleLabel = tkinter.Label(self.leftPanel, text="Single-Pass")
        self.toggleSingleLabel.grid(column=0,row=1)
        self.toggleSingle = tkinter.Checkbutton(self.leftPanel, variable=self.config['toggleSingle'])
        self.toggleSingle.grid(column=1,row=1,stick='EW')

        self.toggleAdsorptionLabel = tkinter.Label(self.leftPanel, text="Iniciar com Adsorção")
        self.toggleAdsorptionLabel.grid(column=0,row=2)
        self.toggleAdsorption = tkinter.Checkbutton(self.leftPanel, variable=self.config['toggleAdsorption'])
        self.toggleAdsorption.grid(column=1,row=2,stick='EW')

        self.textDocumentLabel = tkinter.Label(self.leftPanel, text="Documento de texto")
        self.textDocumentLabel.grid(column=0,row=3)
        self.textDocument = tkinter.Entry(self.leftPanel,textVariable=self.config['textDocument'])
        self.textDocument.grid(column=1,row=3,stick='EW')

        self.timeOptions = {}

        self.timeOptions['timeAdsorptionLabel'] = tkinter.Label(self.leftPanel, text="timeAdsorption")
        self.timeOptions['timeAdsorptionLabel'].grid(column=0,row=4)
        self.timeOptions['timeAdsorption'] = tkinter.Entry(self.leftPanel,textVariable=self.config['timeAdsorption'])
        self.timeOptions['timeAdsorption'].grid(column=1,row=4,stick='EW')

        self.timeOptions['timeDesorptionLabel'] = tkinter.Label(self.leftPanel, text="timeDesorption")
        self.timeOptions['timeDesorptionLabel'].grid(column=0,row=5)
        self.timeOptions['timeDesorption'] = tkinter.Entry(self.leftPanel,textVariable=self.config['timeDesorption'])
        self.timeOptions['timeDesorption'].grid(column=1,row=5,stick='EW')

        self.conductivityOptions = {}

        self.conductivityOptions['minConductivityAdsorptionLabel'] = tkinter.Label(self.leftPanel, text="minConductivityAdsorption")
        self.conductivityOptions['minConductivityAdsorptionLabel'].grid(column=0,row=6)
        self.conductivityOptions['minConductivityAdsorption'] = tkinter.Entry(self.leftPanel,textVariable=self.config['minConductivityAdsorption'])
        self.conductivityOptions['minConductivityAdsorption'].grid(column=1,row=6,stick='EW')

        self.conductivityOptions['maxConductivityDesorptionLabel'] = tkinter.Label(self.leftPanel, text="maxConductivityDesorption")
        self.conductivityOptions['maxConductivityDesorptionLabel'].grid(column=0,row=7)
        self.conductivityOptions['maxConductivityDesorption'] = tkinter.Entry(self.leftPanel,textVariable=self.config['maxConductivityDesorption'])
        self.conductivityOptions['maxConductivityDesorption'].grid(column=1,row=7,stick='EW')

        self.potentialOptions = {}

        self.potentialOptions['cutPotentialAdsorptionLabel'] = tkinter.Label(self.leftPanel, text="cutPotentialAdsorption")
        self.potentialOptions['cutPotentialAdsorptionLabel'].grid(column=0,row=8)
        self.potentialOptions['cutPotentialAdsorption'] = tkinter.Entry(self.leftPanel,textVariable=self.config['cutPotentialAdsorption'])
        self.potentialOptions['cutPotentialAdsorption'].grid(column=1,row=8,stick='EW')

        self.potentialOptions['cutPotentialDesorptionLabel'] = tkinter.Label(self.leftPanel, text="cutPotentialDesorption")
        self.potentialOptions['cutPotentialDesorptionLabel'].grid(column=0,row=9)
        self.potentialOptions['cutPotentialDesorption'] = tkinter.Entry(self.leftPanel,textVariable=self.config['cutPotentialDesorption'])
        self.potentialOptions['cutPotentialDesorption'].grid(column=1,row=9,stick='EW')

        self.numberCiclesLabel = tkinter.Label(self.leftPanel, text="numberCicles")
        self.numberCiclesLabel.grid(column=0,row=10)
        self.numberCicles = Tkinter.Entry(self.leftPanel,textVariable=self.config['numberCicles'])
        self.numberCicles.grid(column=1,row=10,stick='EW')

        self.maxConductivityLabel = tkinter.Label(self.leftPanel, text="maxConductivity")
        self.maxConductivityLabel.grid(column=0,row=11)
        self.maxConductivity = tkinter.Entry(self.leftPanel,textVariable=self.config['maxConductivity'])
        self.maxConductivity.grid(column=1,row=11,stick='EW')


        self.toggleOn = tkinter.Button(self,text="Ligar",command=self.saveConfig)
        self.toggleOn.grid(column=0,colspan=2,row=12,stick='EW')


    def saveConfig(self):
        configToSave = {}
        for key, value in self.config:
            configToSave[config] = value.get()

    def changeMode(self):
        if self.config['modeID'] = 1:
            for opt in self.timeOptions:
                opt['state'] = 'normal'
            for opt in self.conductivityOptions:
                opt['state'] = 'normal'
            for opt in self.potentialOptions:
                opt['state'] = 'disabled'
        elif self.config['modeID'] = 2:
            for opt in self.timeOptions:
                opt['state'] = 'normal'
            for opt in self.conductivityOptions:
                opt['state'] = 'disabled'
            for opt in self.potentialOptions:
                opt['state'] = 'disabled'
        elif self.config['modeID'] = 3:
            for opt in self.timeOptions:
                opt['state'] = 'disabled'
            for opt in self.conductivityOptions:
                opt['state'] = 'normal'
            for opt in self.potentialOptions:
                opt['state'] = 'disabled'
        elif self.config['modeID'] = 4:
            for opt in self.timeOptions:
                opt['state'] = 'disabled'
            for opt in self.conductivityOptions:
                opt['state'] = 'disabled'
            for opt in self.potentialOptions:
                opt['state'] = 'normal'
        elif self.config['modeID'] = 5:
            for opt in self.timeOptions:
                opt['state'] = 'normal'
            for opt in self.conductivityOptions:
                opt['state'] = 'normal'
            for opt in self.potentialOptions:
                opt['state'] = 'normal'

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Dessanilizador')
    app.mainloop()
