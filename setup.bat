@echo off
echo Instalando dependencias do projeto.
pip install -r requirements.txt >nul
echo Criando banco de dados
python3 createDB.py >nul
echo Instalação concluida com sucesso!
