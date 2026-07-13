export const viewerHtml = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Planning Diagram Viewer</title>
  <style>
    :root { color-scheme: light dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
    body { margin: 0; background: #f4f1ea; color: #1f2933; }
    header { position: sticky; top: 0; z-index: 2; display: flex; gap: 1rem; align-items: center; justify-content: space-between; padding: .85rem 1.2rem; background: rgba(255,255,255,.94); border-bottom: 1px solid #d8d4ca; backdrop-filter: blur(10px); }
    h1 { margin: 0; font-size: 1rem; letter-spacing: .01em; }
    #status { font-size: .82rem; color: #52606d; }
    #status.live::before { content: ''; display: inline-block; width: .55rem; height: .55rem; margin-right: .4rem; border-radius: 50%; background: #16a34a; }
    main { display: grid; gap: 1rem; padding: 1rem; }
    section { display: grid; gap: 1rem; }
    section > h2 { margin: .5rem .25rem 0; font-size: .9rem; color: #52606d; font-family: ui-monospace, monospace; }
    article { overflow: auto; padding: 1rem; background: #fff; border: 1px solid #d8d4ca; border-radius: .75rem; box-shadow: 0 8px 28px rgba(31,41,51,.07); }
    article h3 { margin: 0 0 .8rem; font-size: .95rem; }
    .mermaid { min-width: min-content; text-align: center; }
    .empty, .error { padding: 2rem; border-radius: .75rem; background: #fff; border: 1px solid #d8d4ca; }
    .error { color: #b42318; white-space: pre-wrap; }
    @media (prefers-color-scheme: dark) {
      body { background: #101418; color: #edf2f7; }
      header, article, .empty, .error { background: #171c22; border-color: #313943; }
      #status, section > h2 { color: #a7b2be; }
    }
  </style>
</head>
<body>
  <header><h1>Planning Diagram Viewer</h1><span id="status">Connecting...</span></header>
  <main id="app"><div class="empty">Loading Mermaid diagrams...</div></main>
  <script type="module">
    import mermaid from '/vendor/mermaid.esm.min.mjs';

    const colorScheme = window.matchMedia('(prefers-color-scheme: dark)');
    function initializeMermaid() {
      mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: colorScheme.matches ? 'dark' : 'default' });
    }
    initializeMermaid();
    const app = document.querySelector('#app');
    const status = document.querySelector('#status');
    let renderInFlight = false;
    let renderAgain = false;

    function describeError(error) {
      if (error instanceof Error) return error.message;
      if (typeof error === 'string') return error;
      if (error && typeof error === 'object') {
        for (const key of ['message', 'str', 'error']) {
          if (typeof error[key] === 'string') return error[key];
        }
        try {
          return JSON.stringify(error, null, 2);
        } catch {}
      }
      return String(error);
    }

    async function renderOnce() {
      initializeMermaid();
      try {
        const response = await fetch('/api/diagrams', { cache: 'no-store' });
        if (!response.ok) throw new Error(await response.text());
        const payload = await response.json();
        app.replaceChildren();

        let count = 0;
        for (const file of payload.files) {
          const section = document.createElement('section');
          const fileTitle = document.createElement('h2');
          fileTitle.textContent = file.path;
          section.append(fileTitle);

          for (const diagram of file.diagrams) {
            count += 1;
            const article = document.createElement('article');
            const title = document.createElement('h3');
            const graph = document.createElement('pre');
            title.textContent = diagram.title + ' - line ' + diagram.startLine;
            graph.className = 'mermaid';
            graph.textContent = diagram.source;
            article.append(title, graph);
            section.append(article);
          }
          app.append(section);
        }

        if (count === 0) {
          app.innerHTML = '<div class="empty">No fenced <code>mermaid</code> blocks found.</div>';
        } else {
          await mermaid.run({ nodes: [...document.querySelectorAll('.mermaid')] });
        }
        status.textContent = count + ' diagram' + (count === 1 ? '' : 's') + ' - revision ' + payload.revision;
        status.className = 'live';
      } catch (error) {
        const message = describeError(error);
        app.innerHTML = '';
        const box = document.createElement('div');
        box.className = 'error';
        box.textContent = message;
        app.append(box);
        status.textContent = 'Render failed';
        status.className = '';
      }
    }

    async function requestRender() {
      if (renderInFlight) {
        renderAgain = true;
        return;
      }
      renderInFlight = true;
      try {
        do {
          renderAgain = false;
          await renderOnce();
        } while (renderAgain);
      } finally {
        renderInFlight = false;
      }
    }

    const events = new EventSource('/events');
    events.addEventListener('reload', requestRender);
    events.addEventListener('ready', requestRender);
    events.onerror = () => { status.textContent = 'Reconnecting...'; status.className = ''; };
    colorScheme.addEventListener('change', () => {
      requestRender();
    });
    requestRender();
  </script>
</body>
</html>`;
