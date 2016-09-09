@echo off
echo Instalando Git
Setup/Git-2.10.0-32-bit.exe
echo Fazendo download do projeto
git clone --depth 1 https://projetodeq:senhadoprojetdeq@github.com/rangelfinal/deq.git
cd Setup
echo Instalando Python
python-3.5.2.exe
echo Instalando dependencias do projeto.
pip install -r requirements.txt >nul
echo Criando banco de dados
python3 createDB.py >nul
echo Instalação concluida com sucesso!
