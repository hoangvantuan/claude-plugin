#!/usr/bin/env node
// CDP Paste: dispatch native paste event via Chrome DevTools Protocol
// Chrome performs real paste from system clipboard → isTrusted=true
// Usage: node cdp-paste.js [--port <debug-port>] [--target <url-substring>]

const http = require('http');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
let debugPort = null;
let targetFilter = 'facebook.com';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--port' && args[i + 1]) debugPort = parseInt(args[i + 1], 10);
  if (args[i] === '--target' && args[i + 1]) targetFilter = args[i + 1];
}

function discoverPort() {
  if (debugPort) return debugPort;
  try {
    const ps = execSync("ps aux | grep -o '\\-\\-remote-debugging-port=[0-9]*' | head -1", {
      encoding: 'utf8', timeout: 5000
    }).trim();
    const match = ps.match(/--remote-debugging-port=(\d+)/);
    if (match) return parseInt(match[1], 10);
  } catch {}
  return 9222;
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('timeout')), 8000);
    http.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => { clearTimeout(timeout); resolve(data); });
    }).on('error', (e) => { clearTimeout(timeout); reject(e); });
  });
}

function sendCDP(ws, method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 100000);
    const timeout = setTimeout(() => reject(new Error('CDP timeout')), 8000);
    const handler = (event) => {
      const msg = JSON.parse(event.data || event.toString());
      if (msg.id === id) {
        ws.removeEventListener ? ws.removeEventListener('message', handler) : ws.off('message', handler);
        clearTimeout(timeout);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      }
    };
    ws.addEventListener ? ws.addEventListener('message', handler) : ws.on('message', handler);
    const payload = JSON.stringify({ id, method, params });
    ws.send(payload);
  });
}

async function main() {
  const port = discoverPort();

  let targets;
  try {
    const raw = await httpGet(`http://127.0.0.1:${port}/json`);
    targets = JSON.parse(raw);
  } catch (e) {
    process.stderr.write(`Cannot connect to Chrome debug port ${port}: ${e.message}\n`);
    process.exit(1);
  }

  const page = targets.find(t => t.type === 'page' && t.url && t.url.includes(targetFilter));
  if (!page || !page.webSocketDebuggerUrl) {
    process.stderr.write(`No page matching "${targetFilter}" found on port ${port}\n`);
    process.exit(2);
  }

  let ws;
  try {
    const WebSocket = globalThis.WebSocket || require('ws');
    ws = new WebSocket(page.webSocketDebuggerUrl);
    await new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error('WS connect timeout')), 8000);
      ws.addEventListener ? ws.addEventListener('open', () => { clearTimeout(t); resolve(); })
        : ws.on('open', () => { clearTimeout(t); resolve(); });
      ws.addEventListener ? ws.addEventListener('error', (e) => { clearTimeout(t); reject(e); })
        : ws.on('error', (e) => { clearTimeout(t); reject(e); });
    });
  } catch (e) {
    process.stderr.write(`WebSocket connection failed: ${e.message}\n`);
    process.exit(3);
  }

  try {
    await sendCDP(ws, 'Input.dispatchKeyEvent', {
      type: 'rawKeyDown',
      key: 'v',
      code: 'KeyV',
      modifiers: 4,
      commands: ['Paste'],
      windowsVirtualKeyCode: 86,
      nativeVirtualKeyCode: 86
    });
    await sendCDP(ws, 'Input.dispatchKeyEvent', {
      type: 'keyUp',
      key: 'v',
      code: 'KeyV',
      modifiers: 4,
      windowsVirtualKeyCode: 86,
      nativeVirtualKeyCode: 86
    });
  } catch (e) {
    process.stderr.write(`CDP command failed: ${e.message}\n`);
    ws.close();
    process.exit(4);
  }

  ws.close();
  process.exit(0);
}

main();
