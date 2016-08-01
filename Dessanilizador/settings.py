import sqlite3
import time

db = sqlite3.connect('DEQ.sqlite', check_same_thread=False)


class Settings:

    def updateFromDB(self, column=None):
        if column == None:
            cursor = db.cursor().execute('SELECT * FROM settings')
            columns = []
            for c in cursor.description:
                columns.append(c[0])
            row = cursor.fetchone()
            self = dict(zip(columns, row))
        else:
            cursor = db.cursor().execute('SELECT ' + column + ' FROM settings')
            return cursor.fetchone()[0]

    def updateDB(self, column=None, newValue=None):
        if column == None or newValue == None:
            for key, value in self:
                cursor = db.cursor().execute('UPDATE settings SET ' + key + '=' + value)
        else:
            if isinstance(newValue, str):
                newValue = "'" + newValue + "'"
            if isinstance(newValue, bool):
                newValue = int(newValue)

            print('UPDATE settings SET ' + column + '=' + str(newValue))
            cursor = db.cursor().execute('UPDATE settings SET ' + column + '=' + str(newValue))
            db.commit()

    def __init__(self):
        self.updateFromDB()

    @property
    def toggleSingle(self):
        self._toggleSingle = self.updateFromDB('toggleSingle')
        return self._toggleSingle

    @toggleSingle.setter
    def toggleSingle(self, value):
        self.updateDB('toggleSingle', value)
        self._toggleSingle = value

    @property
    def toggleOn(self):
        self._toggleOn = self.updateFromDB('toggleOn')
        return self._toggleOn

    @toggleOn.setter
    def toggleOn(self, value):
        self.updateDB('toggleOn', value)
        self._toggleOn = value

    @property
    def toggleAdsorption(self):
        self._toggleAdsorption = self.updateFromDB('toggleAdsorption')
        return self._toggleAdsorption

    @toggleAdsorption.setter
    def toggleAdsorption(self, value):
        self.updateDB('toggleAdsorption', value)
        self._toggleAdsorption = value

    @property
    def textDocument(self):
        self._textDocument = self.updateFromDB('textDocument')
        return self._textDocument

    @textDocument.setter
    def textDocument(self, value):
        self.updateDB('textDocument', value)
        self._textDocument = value

    @property
    def timeAdsorption(self):
        self._timeAdsorption = self.updateFromDB('timeAdsorption')
        return self._timeAdsorption

    @timeAdsorption.setter
    def timeAdsorption(self, value):
        self.updateDB('timeAdsorption', value)
        self._timeAdsorption = value

    @property
    def timeDesorption(self):
        self._timeDesorption = self.updateFromDB('timeDesorption')
        return self._timeDesorption

    @timeDesorption.setter
    def timeDesorption(self, value):
        self.updateDB('timeDesorption', value)
        self._timeDesorption = value

    @property
    def minConductivityAdsorption(self):
        self._minConductivityAdsorption = self.updateFromDB('minConductivityAdsorption')
        return self._minConductivityAdsorption

    @minConductivityAdsorption.setter
    def minConductivityAdsorption(self, value):
        self.updateDB('minConductivityAdsorption', value)
        self._minConductivityAdsorption = value

    @property
    def maxConductivityDesorption(self):
        self._maxConductivityDesorption = self.updateFromDB('maxConductivityDesorption')
        return self._maxConductivityDesorption

    @maxConductivityDesorption.setter
    def maxConductivityDesorption(self, value):
        self.updateDB('maxConductivityDesorption', value)
        self._maxConductivityDesorption = value

    @property
    def cutPotentialAdsorption(self):
        self._cutPotentialAdsorption = self.updateFromDB('cutPotentialAdsorption')
        return self._cutPotentialAdsorption

    @cutPotentialAdsorption.setter
    def cutPotentialAdsorption(self, value):
        self.updateDB('cutPotentialAdsorption', value)
        self._cutPotentialAdsorption = value

    @property
    def cutPotentialDesorption(self):
        self._cutPotentialDesorption = self.updateFromDB('cutPotentialDesorption')
        return self._cutPotentialDesorption

    @cutPotentialDesorption.setter
    def cutPotentialDesorption(self, value):
        self.updateDB('cutPotentialDesorption', value)
        self._cutPotentialDesorption = value

    @property
    def numberCicles(self):
        self._numberCicles = self.updateFromDB('numberCicles')
        return self._numberCicles

    @numberCicles.setter
    def numberCicles(self, value):
        self.updateDB('numberCicles', value)
        self._numberCicles = value

    @property
    def maxConductivity(self):
        self._maxConductivity = self.updateFromDB('maxConductivity')
        return self._maxConductivity

    @maxConductivity.setter
    def maxConductivity(self, value):
        self.updateDB('maxConductivity', value)
        self._maxConductivity = value

    @property
    def modeID(self):
        self._modeID = self.updateFromDB('modeID')
        return self._modeID

    @modeID.setter
    def modeID(self, value):
        self.updateDB('modeID', value)
        self._modeID = value

    @property
    def fonte1(self):
        self._fonte1 = self.updateFromDB('fonte1')
        return self._fonte1

    @fonte1.setter
    def fonte1(self, value):
        self.updateDB('fonte1', value)
        self._fonte1 = value

    @property
    def fonte2(self):
        self._fonte2 = self.updateFromDB('fonte2')
        return self._fonte2

    @fonte2.setter
    def fonte2(self, value):
        self.updateDB('fonte2', value)
        self._fonte2 = value

    @property
    def solenoide(self):
        self._solenoide = self.updateFromDB('solenoide')
        return self._solenoide

    @solenoide.setter
    def solenoide(self, value):
        self.updateDB('solenoide', value)
        self._solenoide = value

    @property
    def stateID(self):
        self._stateID = self.updateFromDB('stateID')
        return self._stateID

    @stateID.setter
    def stateID(self, value):
        self.updateDB('stateID', value)
        self._stateID = value

    @property
    def stateStartTime(self):
        self._stateStartTime = self.updateFromDB('stateStartTime')
        return self._stateStartTime

    @stateStartTime.setter
    def stateStartTime(self, value):
        self.updateDB('stateStartTime', value)
        self._stateStartTime = value

    @property
    def currentUUID(self):
        self._currentUUID = self.updateFromDB('currentUUID')
        return self._currentUUID

    @currentUUID.setter
    def currentUUID(self, value):
        self.updateDB('currentUUID', value)
        self._currentUUID = value
    @property
    def currentExecutionStartTime(self):
        self._currentExecutionStartTime = self.updateFromDB('currentExecutionStartTime')
        return self._currentExecutionStartTime

    @currentExecutionStartTime.setter
    def currentExecutionStartTime(self, value):
        self.updateDB('currentExecutionStartTime', value)
        self._currentExecutionStartTime = value

    def timeInCurrentState(self):
        if self.stateStartTime != 0:
            return time.time() - self.stateStartTime
        else:
            return 0
