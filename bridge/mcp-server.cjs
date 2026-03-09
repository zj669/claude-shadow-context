#!/usr/bin/env node

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

function sendResponse(response) {
  console.log(JSON.stringify(response));
}

rl.on('line', (line) => {
  try {
    const request = JSON.parse(line);
    const hasId = Object.prototype.hasOwnProperty.call(request, 'id');

    if (request.method === 'initialize') {
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: {
            tools: {},
            resources: {}
          },
          serverInfo: {
            name: 'claude-shadow-context',
            version: '0.1.0'
          }
        }
      });
    } else if (request.method === 'tools/list') {
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        result: {
          tools: []
        }
      });
    } else if (request.method === 'resources/list') {
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        result: {
          resources: []
        }
      });
    } else if (hasId) {
      sendResponse({
        jsonrpc: '2.0',
        id: request.id,
        error: {
          code: -32601,
          message: 'Method not found'
        }
      });
    }
  } catch (error) {
    // Ignore parse errors
  }
});

process.on('SIGINT', () => {
  process.exit(0);
});

process.on('SIGTERM', () => {
  process.exit(0);
});
