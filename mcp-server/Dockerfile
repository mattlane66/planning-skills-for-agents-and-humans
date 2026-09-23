FROM node:22-alpine AS build
WORKDIR /app

COPY mcp-server/package.json mcp-server/package-lock.json ./mcp-server/
RUN cd mcp-server && npm ci

COPY . .
RUN cd mcp-server && npm run build && npm prune --omit=dev

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

COPY --from=build /app /app

EXPOSE 3000
CMD ["node", "mcp-server/dist/http.js"]
