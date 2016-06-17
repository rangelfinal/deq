import sqlite3

db = sqlite3.connect('DEQ.sqlite')


class ArduinoValues:

    def __init__(self, **args):
        if('limit' in args):
        if('')

    def populate(self, **args):


class ArduinoValue:

    def __init__(self, **args):

    def populate(self, **args):

    def updateFromDB(self, column=None):
        if column == None:
            cursor = db.cursor().execute('SELECT * FROM arduino')
            columns = []
            for c in cursor.description:
                columns.append(c[0])
            row = cursor.fetchone()
            self = dict(zip(columns, row))
        else:
            cursor = db.cursor().execute('SELECT ' + column + ' FROM arduino')
            row = cursor.fetchone()
            setattr(self, column, row[0])

    def updateDB(self, column=None, newValue=None):
        if !hasattr(self, 'id') or self.id = None:
            cursor = db.cursor.execute('INSERT INTO arduino(variableID,value,modeID,fonte1,fonte2,solenoide) VALUES (?, ?, ?, ?, ?, ?)',
                                       self.variableID, self.value, self.modeID, self.fonte1, self.fonte2, self.solenoide)
            self.id = cursor.lastrowid
        if column == None or newValue == None:
            for key, value in self:
                cursor = db.cursor().execute('UPDATE arduino SET ' + key + '=' + value)
        else:
            if newValue == "":
                newValue = "''"
            cursor = db.cursor().execute('UPDATE arduino SET ' + column + '=' + str(newValue))

    @property
    def ID(self):
        self.updateFromDB('ID')
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @property
    def variableID(self):
        self.updateFromDB('variableID')
        return self._variableID

    @variableID.setter
    def variableID(self, value):
        self.updateDB('variableID', value)
        self._variableID = value

    @property
    def value(self):
        self.updateFromDB('value')
        return self._value

    @value.setter
    def value(self, value):
        self.updateDB('value', value)
        self._value = value

    @property
    def currentTime(self):
        self.updateFromDB('currentTime')
        return self._currentTime

    @currentTime.setter
    def currentTime(self, value):
        self.updateDB('currentTime', value)
        self._currentTime = value

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
