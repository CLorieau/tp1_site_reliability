const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'view')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'view', 'index.html'));
});

app.listen(3000, () => {
  console.log('Product Interface listening on port 3000!');
});