var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database(':memory:');

router.post('/interface', (req, res, next) => {
  res.send(select('interface'));
});

router.post('/interface/:id', (req, res, next) => {
  res.send(selectOne('interface', null, 'ID = ' + req.params[0]));
});

router.post('/interface/insert', (req, res, next) => {
  res.send(insert('interface', req.body.values, req.body.columns));
});

router.post('/interface/update', (req, res, next) => {
  res.send(update('interface', req.body.values, req.body.conditions));
});

router.post('/python', (req, res, next) => {
  res.send(select('python'));
});

router.post('/python/:id', (req, res, next) => {
  res.send(selectOne('python', null, 'ID = ' + req.params[0]));
});

router.post('/python/insert', (req, res, next) => {
  res.send(insert('python', req.body.values, req.body.columns));
});

router.post('/python/update', (req, res, next) => {
  res.send(update('python', req.body.values, req.body.conditions));
});

router.post('/arduino', (req, res, next) => {
  res.send(select('arduino'));
});

router.post('/arduino/:id', (req, res, next) => {
  res.send(selectOne('arduino', null, 'ID = ' + req.params[0]));
});

router.post('/arduino/insert', (req, res, next) => {
  res.send(insert('arduino', req.body.values, req.body.columns));
});

router.post('/arduino/update', (req, res, next) => {
  res.send(update('arduino', req.body.values, req.body.conditions));
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
