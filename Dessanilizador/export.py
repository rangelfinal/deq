import sqlite3
import csv
import sys
import os

# http://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def query_yes_no(question, default="no"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Resposta padrão inválida: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Por favor responda com 'yes' ou 'no' "
                             "(ou 'y' ou 'n').\n")

db = sqlite3.connect('DEQ.sqlite')

if os.path.isfile('output.csv'):
    if query_yes_no("output.csv já existe! Deseja sobreescrever?"):
        os.remove('output.csv')
    else:
        sys.exit()
print("Exportando dados para output.csv!")

with open('output.csv', 'w') as f:

    csv.writer(f).writerow(['Variavel', 'Valor', 'TempoNoEstado', 'TempoTotal', 'Modo', 'Adsorcao', 'Dessorcao', 'Solenoide', 'Horario'])

    SQLString = 'SELECT AV.name, A.value, A.timeInCurrentState, A.totalTime, AM.name, A.fonte1, A.fonte2, A.solenoide, A.currentTime ' \
    'FROM arduino A, arduinoVariables AV, arduinoModes AM ' \
    'WHERE A.variableID=AV.variableID AND A.modeID=AM.modeID ' \
    'ORDER BY A.currentTime'

    cursor = db.cursor().execute(SQLString)

    for line in cursor:
        data = cursor.fetchone()
        csv.writer(f).writerow(data)

print("Exportação concluída!")
if query_yes_no("Deseja limpar o banco de dados?"):
    db.cursor().execute('DELETE FROM arduino')
