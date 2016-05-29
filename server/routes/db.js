var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database(':memory:');

router.post('/db/:table', (req, res) => {
  res.send(select(req.params.table));
});

router.post('/db/:table/select', (req,res) => {
  res.send(select(req.params.table, req.body.columns, req.body.conditions));
});

router.post('/db/:table/selectOne', (req,res) => {
  res.send(selectOne(req.params.table, req.body.columns, req.body.conditions));
});

router.post('/db/:table/:id', (req, res) => {
  res.send(selectOne(req.params.table, req.body.columns, 'ID = ' + req.params.id));
});

router.post('/db/:table/insert', (req, res) => {
  res.send(insert(req.params.table, req.body.values, req.body.columns));
});

router.post('db/:table/update', (req, res) => {
  res.send(update(req.params.table, req.body.values, req.body.conditions));
});

/**
 * Função para consultar uma linha do DB
 * @param  String     table       [description]
 * @param  [String]   columns     [description]
 * @param  String     conditions  [description]
 * @return object                 [description]
 */
function selectOne(table, columns, conditions) {
  let sqlStatement = 'SELECT ';

  if(columns != null) {sqlStatement += columns.join() + ' ';}
  else {sqlStatement += '* ';}

  sqlStatement += 'FROM ' + table;

  if(conditions != null) {sqlStatement += 'WHERE ' + conditions;}

  db.get(sqlStatement, [], (err, row) => {
    if(err !== null) {return err;}
    return row;
  });
}

function select(table, columns, conditions) {
  let sqlStatement = 'SELECT ';

  if(columns != null) {sqlStatement += columns.join() + ' ';}
  else {sqlStatement += '* ';}

  sqlStatement += 'FROM ' + table;

  if(conditions != null) {sqlStatement += 'WHERE ' + conditions;}

  db.get(sqlStatement, [], (err, rows) => {
    if(err !== null) {return err;}
    return rows;
  });
}

function insert(table, values, columns) {
  let sqlStatement = 'INSERT INTO ';

  sqlStatement += table + ' ';

  if(columns != null) {sqlStatement += '(' + columns.join() + ')';}

  sqlStatement += 'VALUES (' + values.join() + ')';

  db.run(sqlStatement, [], (err) => {
    if(err !== null) return err;
    return this.lastId;
  });
}

function update(table, values, conditions) {
  let sqlStatement = 'UPDATE ';

  sqlStatement += table + ' ';

  sqlStatement += 'SET ' + values.join() + ' ';

  sqlStatement += 'WHERE ' + conditions.join();

  db.run(sqlStatement, [], (err) => {
    if(err !== null) return err;
    return this.changes;
  });
}

module.exports = router;
