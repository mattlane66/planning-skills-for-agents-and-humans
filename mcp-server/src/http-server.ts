import { randomUUID } from 'node:crypto';
import { createServer, type IncomingMessage, type Server as NodeHttpServer, type ServerResponse } from 'node:http';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { isInitializeRequest } from '@modelcontextprotocol/sdk/types.js';
import { createPlanningSkillsServer } from './server.js';

const MAX_BODY_BYTES = 1024 * 1024;

type Session = {
  server: McpServer;
  transport: StreamableHTTPServerTransport;
};

export type PlanningSkillsHttpServer = {
  server: NodeHttpServer;
  close: () => Promise<void>;
};

function getHeader(req: IncomingMessage, name: string): string | undefined {
  const value = req.headers[name.toLowerCase()];
  if (Array.isArray(value)) return value[0];
  return value;
}

function sendJson(res: ServerResponse, status: number, body: unknown): void {
  if (res.headersSent) return;
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(body));
}

function sendJsonRpcError(res: ServerResponse, status: number, message: string): void {
  sendJson(res, status, {
    jsonrpc: '2.0',
    error: { code: -32000, message },
    id: null,
  });
}

async function readJsonBody(req: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];
  let total = 0;

  for await (const chunk of req) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += buffer.length;
    if (total > MAX_BODY_BYTES) {
      throw new Error('Request body exceeds 1 MiB.');
    }
    chunks.push(buffer);
  }

  if (chunks.length === 0) return undefined;
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  if (!raw) return undefined;
  return JSON.parse(raw) as unknown;
}

export function createPlanningSkillsHttpServer(): PlanningSkillsHttpServer {
  const sessions = new Map<string, Session>();

  const closeSession = async (sessionId: string): Promise<void> => {
    const session = sessions.get(sessionId);
    if (!session) return;
    sessions.delete(sessionId);
    try {
      await session.transport.close();
    } finally {
      await session.server.close();
    }
  };

  const server = createServer(async (req, res) => {
    const url = new URL(req.url ?? '/', 'http://localhost');

    if (req.method === 'GET' && url.pathname === '/healthz') {
      sendJson(res, 200, {
        status: 'ok',
        service: 'planning-skills-for-agents-and-humans',
        transport: 'streamable-http',
      });
      return;
    }

    if (url.pathname !== '/mcp') {
      sendJson(res, 404, { error: 'Not found' });
      return;
    }

    try {
      if (req.method === 'POST') {
        const body = await readJsonBody(req);
        const sessionId = getHeader(req, 'mcp-session-id');

        if (sessionId) {
          const session = sessions.get(sessionId);
          if (!session) {
            sendJsonRpcError(res, 404, 'Unknown MCP session.');
            return;
          }
          await session.transport.handleRequest(req, res, body);
          return;
        }

        if (!isInitializeRequest(body)) {
          sendJsonRpcError(res, 400, 'Missing MCP session ID for a non-initialize request.');
          return;
        }

        const mcpServer = createPlanningSkillsServer();
        let initializedSessionId: string | undefined;
        const transport = new StreamableHTTPServerTransport({
          sessionIdGenerator: () => randomUUID(),
          onsessioninitialized: (newSessionId) => {
            initializedSessionId = newSessionId;
            sessions.set(newSessionId, { server: mcpServer, transport });
          },
        });

        transport.onerror = (error) => {
          console.error('[planning-skills-mcp] transport error', error);
        };
        transport.onclose = () => {
          if (initializedSessionId) {
            sessions.delete(initializedSessionId);
          }
          void mcpServer.close();
        };

        await mcpServer.connect(transport);
        await transport.handleRequest(req, res, body);
        return;
      }

      if (req.method === 'GET' || req.method === 'DELETE') {
        const sessionId = getHeader(req, 'mcp-session-id');
        if (!sessionId) {
          sendJsonRpcError(res, 400, 'Missing MCP session ID.');
          return;
        }
        const session = sessions.get(sessionId);
        if (!session) {
          sendJsonRpcError(res, 404, 'Unknown MCP session.');
          return;
        }
        await session.transport.handleRequest(req, res);
        if (req.method === 'DELETE') {
          await closeSession(sessionId);
        }
        return;
      }

      res.setHeader('allow', 'GET, POST, DELETE');
      sendJsonRpcError(res, 405, 'Method not allowed.');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown server error';
      console.error('[planning-skills-mcp] request failed', message);
      sendJsonRpcError(res, message.includes('JSON') || message.includes('1 MiB') ? 400 : 500, message);
    }
  });

  return {
    server,
    close: async () => {
      const ids = [...sessions.keys()];
      await Promise.all(ids.map((sessionId) => closeSession(sessionId)));
      if (!server.listening) return;
      await new Promise<void>((resolveClose, rejectClose) => {
        server.close((error) => {
          if (error) rejectClose(error);
          else resolveClose();
        });
      });
    },
  };
}
