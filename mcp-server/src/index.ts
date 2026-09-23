#!/usr/bin/env node

import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { createPlanningSkillsServer } from './server.js';

const server = createPlanningSkillsServer();
const transport = new StdioServerTransport();
await server.connect(transport);
