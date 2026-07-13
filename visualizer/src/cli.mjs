#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { startViewer } from './server.mjs';

function usage() {
  return `Usage: planning-diagram-viewer [options] <markdown-file> [more-files...]

Options:
  --host <host>   Bind host (default: 127.0.0.1)
  --port <port>   Bind port (default: 3456; use 0 for any free port)
  --no-open       Do not open a browser automatically
  --help          Show this help`;
}

export function parseArgs(argv) {
  const options = { host: '127.0.0.1', port: 3456, open: true, filePaths: [] };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--help' || value === '-h') return { ...options, help: true };
    if (value === '--no-open') { options.open = false; continue; }
    if (value === '--host' || value === '--port') {
      const next = argv[index + 1];
      if (!next) throw new Error(`${value} requires a value.`);
      index += 1;
      if (value === '--host') options.host = next;
      else options.port = Number(next);
      continue;
    }
    if (value.startsWith('--')) throw new Error(`Unknown option: ${value}`);
    options.filePaths.push(value);
  }

  if (!Number.isInteger(options.port) || options.port < 0 || options.port > 65535) {
    throw new Error('Port must be an integer between 0 and 65535.');
  }
  return options;
}

function openBrowser(url) {
  const command = process.platform === 'darwin'
    ? ['open', [url]]
    : process.platform === 'win32'
      ? ['cmd', ['/c', 'start', '', url]]
      : ['xdg-open', [url]];
  const child = spawn(command[0], command[1], { detached: true, stdio: 'ignore' });
  child.on('error', () => {});
  child.unref();
}

async function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      console.log(usage());
      return;
    }
    if (options.filePaths.length === 0) throw new Error('Provide at least one Markdown file.');

    const viewer = await startViewer(options);
    for (const path of options.filePaths) console.log(`Watching: ${resolve(path)}`);
    console.log(`Viewer: ${viewer.url}`);
    if (options.open) openBrowser(viewer.url);

    const stop = async () => {
      await viewer.close();
      process.exit(0);
    };
    process.once('SIGINT', stop);
    process.once('SIGTERM', stop);
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error));
    console.error(usage());
    process.exitCode = 1;
  }
}

if (resolve(process.argv[1] || '') === fileURLToPath(import.meta.url)) {
  await main();
}
