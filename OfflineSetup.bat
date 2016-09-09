@echo off
cd Setup
echo Instalando Python
python-3.5.2.exe
echo Instalando dependencias do projeto.
pip install -r requirements.txt >nul
echo Criando banco de dados
python3 createDB.py >nul
echo Instalação concluida com sucesso!
