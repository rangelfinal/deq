import pip
import createDB
import os

def install(package):
    pip.main(['install', package])

if __name__ == '__main__':
    install('matplotlib')
    install('tkinter')
    install('pyserial')
    if not os.path.isfile("../Dessanilizador/DEQ.sqlite"):
        createDB.createDB
    win32api.MessageBox(0, 'Instalação concluida com sucesso', 'Dessanilizador', 0x00001000) 
