import sqlite3


def createDB():
    db = sqlite3.connect('DEQ.sqlite')
    cursor = db.cursor()

    fd = open('createDB.sql', 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        try:
            cursor.execute(command)
        except Exception as e:
            raise

    db.commit()

if __name__ == '__main__':
    createDB()
