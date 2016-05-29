db = sqlite3.connect('DEQ.sqlite')


class Settings:

    def __init__(self):
        updateFromDB()

    def updateFromDB():
        cursor = db.cursor().execute('SELECT * FROM settings')
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        self = dict(zip(columns, row))

    def updateDB(column=None, newValue=None):
        if column == None or newValue == None:
            for key, value in self:
                cursor = db.cursor().execute('UPDATE arduino SET ?=?', key, value)
        else:
            cursor = db.cursor().execute('UPDATE arduino SET ?=?', column, newValue)

    @property
    def toggleSingle(self):
        updateFromDB()
        return self._toggleSingle

    @toggleSingle.setter
    def toggleSingle(self, value):
        updateDB('toggleSingle', value)
        self._toggleSingle = value

    @property
    def toggleOn(self):
        updateFromDB()
        return self._toggleOn

    @toggleOn.setter
    def toggleOn(self, value):
        updateDB('toggleOn', value)
        self._toggleOn = value

    @property
    def toggleAdsorption(self):
        updateFromDB()
        return self._toggleAdsorption

    @toggleAdsorption.setter
    def toggleAdsorption(self, value):
        updateDB('toggleAdsorption', value)
        self._toggleAdsorption = value

    @property
    def textDocument(self):
        updateFromDB()
        return self._textDocument

    @textDocument.setter
    def textDocument(self, value):
        updateDB('textDocument', value)
        self._textDocument = value

    @property
    def timeAdsorption(self):
        updateFromDB()
        return self._timeAdsorption

    @timeAdsorption.setter
    def timeAdsorption(self, value):
        updateDB('timeAdsorption', value)
        self._timeAdsorption = value

    @property
    def timeDesorption(self):
        updateFromDB()
        return self._timeDesorption

    @timeDesorption.setter
    def timeDesorption(self, value):
        updateDB('timeDesorption', value)
        self._timeDesorption = value

    @property
    def minConductivityAdsorption(self):
        updateFromDB()
        return self._minConductivityAdsorption

    @minConductivityAdsorption.setter
    def minConductivityAdsorption(self, value):
        updateDB('minConductivityAdsorption', value)
        self._minConductivityAdsorption = value

    @property
    def maxConductivityDesorption(self):
        updateFromDB()
        return self._maxConductivityDesorption

    @maxConductivityDesorption.setter
    def maxConductivityDesorption(self, value):
        updateDB('maxConductivityDesorption', value)
        self._maxConductivityDesorption = value

    @property
    def cutPotentialAdsorption(self):
        updateFromDB()
        return self._cutPotentialAdsorption

    @cutPotentialAdsorption.setter
    def cutPotentialAdsorption(self, value):
        updateDB('cutPotentialAdsorption', value)
        self._cutPotentialAdsorption = value

    @property
    def cutPotentialDesorption(self):
        updateFromDB()
        return self._cutPotentialDesorption

    @cutPotentialDesorption.setter
    def cutPotentialDesorption(self, value):
        updateDB('cutPotentialDesorption', value)
        self._cutPotentialDesorption = value

    @property
    def numberCicles(self):
        updateFromDB()
        return self._numberCicles

    @numberCicles.setter
    def numberCicles(self, value):
        updateDB('numberCicles', value)
        self._numberCicles = value

    @property
    def maxConductivity(self):
        updateFromDB()
        return self._maxConductivity

    @maxConductivity.setter
    def maxConductivity(self, value):
        updateDB('maxConductivity', value)
        self._maxConductivity = value

    @property
    def modeID(self):
        updateFromDB()
        return self._modeID

    @modeID.setter
    def modeID(self, value):
        updateDB('modeID', value)
        self._modeID = value

    @property
    def fonte1(self):
        updateFromDB()
        return self._fonte1

    @fonte1.setter
    def fonte1(self, value):
        updateDB('fonte1', value)
        self._fonte1 = value

    @property
    def fonte2(self):
        updateFromDB()
        return self._fonte2

    @fonte2.setter
    def fonte2(self, value):
        updateDB('fonte2', value)
        self._fonte2 = value

    @property
    def solenoide(self):
        updateFromDB()
        return self._solenoide

    @solenoide.setter
    def solenoide(self, value):
        updateDB('solenoide', value)
        self._solenoide = value

    @property
    def stateID(self):
        updateFromDB()
        return self._stateID

    @stateID.setter
    def stateID(self, value):
        updateDB('stateID', value)
        self._stateID = value
