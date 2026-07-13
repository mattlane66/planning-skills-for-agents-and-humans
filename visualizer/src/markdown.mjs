import { readFile } from 'node:fs/promises';
import { basename, resolve } from 'node:path';

function safeId(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

export function extractMermaidBlocks(markdown, filePath = 'planning.md') {
  const lines = markdown.split(/\r?\n/);
  const diagrams = [];
  let heading = '';
  let active = null;

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];

    if (!active) {
      const headingMatch = line.match(/^#{1,6}\s+(.+?)\s*$/);
      if (headingMatch) heading = headingMatch[1];

      const opening = line.match(/^\s*(`{3,}|~{3,})mermaid(?:\s+.*)?\s*$/i);
      if (opening) {
        active = {
          fenceCharacter: opening[1][0],
          fenceLength: opening[1].length,
          heading,
          startLine: index + 2,
          source: [],
        };
      }
      continue;
    }

    const closing = line.match(/^\s*(`{3,}|~{3,})\s*$/);
    if (
      closing
      && closing[1][0] === active.fenceCharacter
      && closing[1].length >= active.fenceLength
    ) {
      const number = diagrams.length + 1;
      const fileName = basename(filePath);
      diagrams.push({
        id: `${safeId(fileName) || 'planning'}-${number}`,
        title: active.heading || `Diagram ${number}`,
        source: active.source.join('\n').trim(),
        startLine: active.startLine,
      });
      active = null;
      continue;
    }

    active.source.push(line);
  }

  return diagrams;
}

export async function collectPlanningDiagrams(filePaths, cwd = process.cwd()) {
  return Promise.all(filePaths.map(async (filePath) => {
    const absolutePath = resolve(cwd, filePath);
    const markdown = await readFile(absolutePath, 'utf8');
    return {
      path: filePath,
      absolutePath,
      diagrams: extractMermaidBlocks(markdown, filePath),
    };
  }));
}
