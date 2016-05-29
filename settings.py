import time
import sqlite3
db = sqlite3.connect('DEQ.sqlite')

class Settings:

    def updateFromDB(column=None):
        if column == None:
            cursor = db.cursor().execute('SELECT * FROM settings')
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            self = dict(zip(columns, row))
        else:
            cursor = db.cursor().execute('SELECT column FROM settings')
            row = cursor.fetchone()
            setattr(self, column, row['column'])

    def updateDB(column=None, newValue=None):
        if column == None or newValue == None:
            for key, value in self:
                cursor = db.cursor().execute('UPDATE arduino SET ?=?', key, value)
        else:
            cursor = db.cursor().execute('UPDATE arduino SET ?=?', column, newValue)

    def __init__(self):
        self.updateFromDB()

    @property
    def toggleSingle(self):
        self.updateFromDB('toggleSingle')
        return self._toggleSingle

    @toggleSingle.setter
    def toggleSingle(self, value):
        self.updateDB('toggleSingle', value)
        self._toggleSingle = value

    @property
    def toggleOn(self):
        self.updateFromDB('toggleOn')
        return self._toggleOn

    @toggleOn.setter
    def toggleOn(self, value):
        self.updateDB('toggleOn', value)
        self._toggleOn = value

    @property
    def toggleAdsorption(self):
        self.updateFromDB('toggleAdsorption')
        return self._toggleAdsorption

    @toggleAdsorption.setter
    def toggleAdsorption(self, value):
        self.updateDB('toggleAdsorption', value)
        self._toggleAdsorption = value

    @property
    def textDocument(self):
        self.updateFromDB('textDocument')
        return self._textDocument

    @textDocument.setter
    def textDocument(self, value):
        self.updateDB('textDocument', value)
        self._textDocument = value

    @property
    def timeAdsorption(self):
        self.updateFromDB('timeAdsorption')
        return self._timeAdsorption

    @timeAdsorption.setter
    def timeAdsorption(self, value):
        self.updateDB('timeAdsorption', value)
        self._timeAdsorption = value

    @property
    def timeDesorption(self):
        self.updateFromDB('timeDesorption')
        return self._timeDesorption

    @timeDesorption.setter
    def timeDesorption(self, value):
        self.updateDB('timeDesorption', value)
        self._timeDesorption = value

    @property
    def minConductivityAdsorption(self):
        self.updateFromDB('minConductivityAdsorption')
        return self._minConductivityAdsorption

    @minConductivityAdsorption.setter
    def minConductivityAdsorption(self, value):
        self.updateDB('minConductivityAdsorption', value)
        self._minConductivityAdsorption = value

    @property
    def maxConductivityDesorption(self):
        self.updateFromDB('maxConductivityDesorption')
        return self._maxConductivityDesorption

    @maxConductivityDesorption.setter
    def maxConductivityDesorption(self, value):
        self.updateDB('maxConductivityDesorption', value)
        self._maxConductivityDesorption = value

    @property
    def cutPotentialAdsorption(self):
        self.updateFromDB('cutPotentialAdsorption')
        return self._cutPotentialAdsorption

    @cutPotentialAdsorption.setter
    def cutPotentialAdsorption(self, value):
        self.updateDB('cutPotentialAdsorption', value)
        self._cutPotentialAdsorption = value

    @property
    def cutPotentialDesorption(self):
        self.updateFromDB('cutPotentialDesorption')
        return self._cutPotentialDesorption

    @cutPotentialDesorption.setter
    def cutPotentialDesorption(self, value):
        self.updateDB('cutPotentialDesorption', value)
        self._cutPotentialDesorption = value

    @property
    def numberCicles(self):
        self.updateFromDB('numberCicles')
        return self._numberCicles

    @numberCicles.setter
    def numberCicles(self, value):
        self.updateDB('numberCicles', value)
        self._numberCicles = value

    @property
    def maxConductivity(self):
        self.updateFromDB('maxConductivity')
        return self._maxConductivity

    @maxConductivity.setter
    def maxConductivity(self, value):
        self.updateDB('maxConductivity', value)
        self._maxConductivity = value

    @property
    def modeID(self):
        self.updateFromDB('modeID')
        return self._modeID

    @modeID.setter
    def modeID(self, value):
        self.updateDB('modeID', value)
        self._modeID = value

    @property
    def fonte1(self):
        self.updateFromDB('fonte1')
        return self._fonte1

    @fonte1.setter
    def fonte1(self, value):
        self.updateDB('fonte1', value)
        self._fonte1 = value

    @property
    def fonte2(self):
        self.updateFromDB('fonte2')
        return self._fonte2

    @fonte2.setter
    def fonte2(self, value):
        self.updateDB('fonte2', value)
        self._fonte2 = value

    @property
    def solenoide(self):
        self.updateFromDB('solenoide')
        return self._solenoide

    @solenoide.setter
    def solenoide(self, value):
        self.updateDB('solenoide', value)
        self._solenoide = value

    @property
    def stateID(self):
        self.updateFromDB('stateID')
        return self._stateID

    @stateID.setter
    def stateID(self, value):
        self.updateDB('stateID', value)
        self._stateID = value

    @property
    def stateStartTime(self):
        self.updateFromDB('stateStartTime')
        return self._stateStartTime

    @stateStartTime.setter
    def stateStartTime(self, value):
        self.updateDB('stateStartTime', value)
        self._stateStartTime = value

    def timeInCurrentState(self):
        return time.time() - self.stateStartTime
