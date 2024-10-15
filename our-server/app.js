const express = require('express');
const WebSocket = require('ws');
const bodyParser = require('body-parser');

const rpiIP = '100.95.25.48'
// const rpiIP = '127.0.0.1'
const rpiPort = 65432
const webServerPort = 3000;
const ws = new WebSocket(`ws://${rpiIP}:${rpiPort}`); // Replace with the address of the server
const app = express();

ws.on('open', () => {
  console.log('Connected to WebSocket server');
});

ws.on('message', (data) => {
  console.log('Received message:', data.toString());
});

ws.on('close', () => {
  console.log('WebSocket connection closed');
});

app.use(express.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

app.post('/request', async (req, res) => {
  const data = req.body; // Access the POST data
  console.log('Received POST data:', data);
  ws.send(JSON.stringify(req.body));

  if (data.request === "sensor_data") {
    const response = await new Promise((resolve) => {
      ws.on('message', (data) => {
        resolve(data.toString());
      });
    })
    return res.json({ message: 'Request received', data: response });
  } else {
    return res.json({ message: 'Request received' });
  }
});

app.listen(webServerPort, () => {
  console.log(`Server listening on port ${webServerPort}`);
});
