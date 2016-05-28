CREATE TABLE arduino(
  ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  variableID TEXT,
  value TEXT,
  currentTime DATETIME DEFAULT CURRENT_TIMESTAMP,
  modeID INTEGER,
  fonte1 BOOLEAN,
  fonte2 BOOLEAN,
  solenoide BOOLEAN
);

# Variáveis possiveis - condutividade, pH, potencialcelula, nciclo, temperatura
CREATE TABLE arduinoVariables(
  variableID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT
);

INSERT INTO arduinoVariables('variableID', 'name') VALUES
  (1, 'Condutividade'),
  (2, 'pH'),
  (3, 'Potencial de Célula'),
  (4, 'Numero de Ciclos'),
  (5, 'Temperatura');

# Modos possíveis - potenciostatico, GalvanoTempo, GalvanoCond, GalvanoPot, GalvanoGeral
CREATE TABLE arduinoModes(
  modeID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT
);

INSERT INTO arduinoModes('modeID', 'name') VALUES
  (1, 'Potenciostático'),
  (2, 'Galvanostático por Tempo'),
  (3, 'Galvanostático por Condutividade'),
  (4, 'Galvanostático por Potencial'),
  (5, 'Galvanostático Geral');

CREATE TABLE arduinoStates(
  stateID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT
);

INSERT INTO arduinoStates('stateID', 'name') VALUES
  (1, 'Adsorção'),
  (2, 'Dessorção');

CREATE TABLE settings(
  toggleSingle BOOLEAN,
  toggleOn BOOLEAN,
  toggleAdsorption BOOLEAN,
  textDocument TEXT,
  timeAdsorption REAL,
  timeDesorption REAL,
  minConductivityAdsorption REAL,
  maxConductivityDesorption REAL,
  cutPotentialAdsorption REAL,
  cutPotentialDesorption REAL,
  numberCicles INTEGER,
  maxConductivity REAL,
  modeID INTEGER,
  fonte1 BOOLEAN,
  fonte2 BOOLEAN,
  solenoide BOOLEAN,
  stateID INTEGER
);

CREATE TABLE
