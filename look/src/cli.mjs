#!/usr/bin/env node
import { createLookServer } from './server.mjs';
import { spawn } from 'node:child_process';
const session = await createLookServer();
process.stdout.write(`Look preview: ${session.url}\nChoose Camera, Screen/Window, or Video. Ctrl+C stops the session.\n`);
if (process.platform === 'darwin') {
  const child = spawn('open', [session.url], { stdio: 'ignore', detached: true });
  child.on('error', () => {});
  child.unref();
}
process.once('SIGINT', async () => { await session.close(); process.exit(0); });
process.once('SIGTERM', async () => { await session.close(); process.exit(0); });
