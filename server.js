const net = require('net');
const http = require('http');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

// Jalankan web di port 3001
http.createServer((req, res) => {
    fs.readFile(path.join(__dirname, 'index.html'), (err, data) => {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(data);
    });
}).listen(3001);

const wss = new WebSocket.Server({ port: 8080 });
let browser = null;

wss.on('connection', (ws) => {
    console.log('Browser terhubung');
    browser = ws;
});

const tcpServer = net.createServer((socket) => {
    console.log('ESP32 sedang streaming suara...');
    socket.on('data', (data) => {
        if (browser && browser.readyState === WebSocket.OPEN) {
            browser.send(data);
        }
    });
});

tcpServer.listen(5000, '0.0.0.0', () => {
    console.log('SERVER AKTIF');
    console.log('Web: http://localhost:3001 | TCP: 5000');
});