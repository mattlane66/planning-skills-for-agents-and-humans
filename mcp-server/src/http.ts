#!/usr/bin/env node

import { createPlanningSkillsHttpServer } from './http-server.js';

const portRaw = process.env.PORT ?? '3000';
const port = Number.parseInt(portRaw, 10);
if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error(`PORT must be an integer from 1 to 65535; received ${portRaw}`);
}

const host = process.env.HOST ?? '0.0.0.0';
const service = createPlanningSkillsHttpServer();

service.server.listen(port, host, () => {
  console.error(`[planning-skills-mcp] listening on http://${host}:${port}/mcp`);
});

let shuttingDown = false;
const shutdown = async (signal: string) => {
  if (shuttingDown) return;
  shuttingDown = true;
  console.error(`[planning-skills-mcp] received ${signal}; shutting down`);
  try {
    await service.close();
    process.exitCode = 0;
  } catch (error) {
    console.error('[planning-skills-mcp] shutdown failed', error);
    process.exitCode = 1;
  }
};

process.once('SIGTERM', () => void shutdown('SIGTERM'));
process.once('SIGINT', () => void shutdown('SIGINT'));
