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

        self.leftPanel = tkinter.Frame(self, relief=RAISED, borderwidth=1)

        self.config = {}

        self.DBConfig = Settings()

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

        self.toggleSingle = tkinter.Checkbutton(self.leftPanel, variable=self.config['toggleSingle'])
        self.toggleSingle.grid(column=1,row=1,stick='EW')
        self.toggleAdsorption = tkinter.Checkbutton(self.leftPanel, variable=self.config['toggleAdsorption'])
        self.toggleAdsorption.grid(column=1,row=2,stick='EW')
        self.textDocument = tkinter.Entry(self.leftPanel,textVariable=self.config['textDocument'])
        self.textDocument.grid(column=1,row=3,stick='EW')
        self.timeAdsorption = tkinter.Entry(self.leftPanel,textVariable=self.config['timeAdsorption'])
        self.timeAdsorption.grid(column=1,row=4,stick='EW')
        self.timeDesorption = tkinter.Entry(self.leftPanel,textVariable=self.config['timeDesorption'])
        self.timeDesorption.grid(column=1,row=5,stick='EW')
        self.minConductivityAdsorption = tkinter.Entry(self.leftPanel,textVariable=self.config['minConductivityAdsorption'])
        self.minConductivityAdsorption.grid(column=1,row=6,stick='EW')
        self.maxConductivityDesorption = tkinter.Entry(self.leftPanel,textVariable=self.config['maxConductivityDesorption'])
        self.maxConductivityDesorption.grid(column=1,row=7,stick='EW')
        self.cutPotentialAdsorption = tkinter.Entry(self.leftPanel,textVariable=self.config['cutPotentialAdsorption'])
        self.cutPotentialAdsorption.grid(column=1,row=8,stick='EW')
        self.cutPotentialDesorption = tkinter.Entry(self.leftPanel,textVariable=self.config['cutPotentialDesorption'])
        self.cutPotentialDesorption.grid(column=1,row=9,stick='EW')
        self.numberCicles = Tkinter.Entry(self.leftPanel,textVariable=self.config['numberCicles'])
        self.numberCicles.grid(column=1,row=10,stick='EW')
        self.maxConductivity = tkinter.Entry(self.leftPanel,textVariable=self.config['maxConductivity'])
        self.maxConductivity.grid(column=1,row=11,stick='EW')

        self.toggleOn = tkinter.Button(self,text="Ligar",command=self.saveConfig)
        self.toggleOn.grid(column=0,colspan=2,row=12,stick='EW')

    def saveConfig(self):
        configToSave = {}
        for key, value in self.config:
            configToSave[config] = value.get()

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Dessanilizador')
    app.mainloop()
