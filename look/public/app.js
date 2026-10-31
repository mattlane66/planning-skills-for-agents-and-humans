const token = new URL(location.href).searchParams.get('token');
const $ = (id) => document.getElementById(id);
const sourceButtons = ['camera', 'screen', 'file'];
const state = { stream: null, fileURL: null, source: null, crop: null, seen: new Set(), busy: false, generation: 0 };
const video = $('preview');

async function api(path, method = 'GET', body) {
  const response = await fetch(path, { method, headers: { 'X-Look-Token': token || '', ...(body ? { 'Content-Type': 'application/json' } : {}) }, body: body ? JSON.stringify(body) : undefined, cache: 'no-store' });
  const json = await response.json();
  if (!response.ok) throw new Error(json.error || `HTTP ${response.status}`);
  return json;
}
function status(message) { $('status').textContent = message; }
function connected(active) {
  $('connectionDot').classList.toggle('connected', active);
  $('connection').textContent = active ? `Sharing ${state.source}` : 'No source';
  $('capture').disabled = !active;
  $('resetCrop').disabled = !active;
}
function resetCrop() { state.crop = null; $('selectionBox').hidden = true; $('stageLabel').textContent = 'Full frame'; }
function stopTracks() {
  if (state.stream) state.stream.getTracks().forEach(track => track.stop());
  state.stream = null;
  video.pause();
  video.srcObject = null;
  video.removeAttribute('src');
  video.load();
  if (state.fileURL) URL.revokeObjectURL(state.fileURL);
  state.fileURL = null;
}
function stopLocal() {
  state.generation++; stopTracks(); state.source = null; state.seen.clear(); resetCrop();
  $('stage').classList.remove('has-video');
  video.classList.remove('visible'); $('empty').hidden = false;
  $('stageLabel').hidden = true; $('timeline').hidden = true;
  sourceButtons.forEach(id => $(id).classList.remove('active'));
  connected(false);
}
async function activate(kind, stream, url) {
  stopLocal();
  state.source = kind;
  state.stream = stream;
  state.fileURL = url;
  if (stream) {
    video.srcObject = stream;
    for (const track of stream.getVideoTracks()) track.addEventListener('ended', () => { if (state.stream === stream) { stopLocal(); status('Screen or camera sharing ended.'); } }, { once: true });
  } else video.src = url;
  try { await video.play(); } catch { /* Recorded media may need a separate play gesture. */ }
  video.classList.add('visible'); $('empty').hidden = true;
  $('stage').classList.add('has-video'); $('stageLabel').hidden = false;
  $('timeline').hidden = kind !== 'recording';
  $(kind === 'recording' ? 'file' : kind).classList.add('active');
  connected(true);
  await api('/api/resume', 'POST');
  requestAnimationFrame(syncSelectionLayer);
  status(`Sharing ${kind} locally. Drag to select a region, then capture a frame or ask the agent to look.`);
  await heartbeat();
}
async function heartbeat() {
  try { await api('/api/heartbeat', 'POST', { source: state.source || '' }); }
  catch (error) { status(`Local bridge unavailable: ${error.message}`); }
}
$('camera').addEventListener('click', async () => {
  try { const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false }); await activate('camera', stream, null); }
  catch (error) { status(`Camera could not start: ${error.message}`); }
});
$('screen').addEventListener('click', async () => {
  try {
    if (!navigator.mediaDevices.getDisplayMedia) throw new Error('This browser does not support screen sharing. Try Chrome or another supported browser.');
    const stream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: false });
    await activate('screen', stream, null);
  } catch (error) { status(`Screen sharing could not start: ${error.message}`); }
});
$('file').addEventListener('click', () => $('fileInput').click());
$('fileInput').addEventListener('change', async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  try { await activate('recording', null, url); }
  catch (error) { URL.revokeObjectURL(url); status(`Recording could not open: ${error.message}`); }
  event.target.value = '';
});
$('stop').addEventListener('click', async () => {
  stopLocal(); status('Stopped. Media tracks released and captured frame memory cleared.');
  try { await api('/api/stop', 'POST'); } catch (error) { status(`Preview stopped; bridge stop failed: ${error.message}`); }
});
$('resetCrop').addEventListener('click', resetCrop);
$('cropToggle').addEventListener('change', () => { $('selectionBox').style.opacity = $('cropToggle').checked ? '1' : '.2'; });
$('capture').addEventListener('click', async () => {
  try {
    const frame = await captureFrame();
    await api('/api/manual-frame', 'POST', frame);
    status('Frame saved in local session memory. Tell the agent to call look_latest.');
  } catch (error) { status(`Capture failed: ${error.message}`); }
});
$('play').addEventListener('click', () => video.paused ? video.play() : video.pause());
video.addEventListener('timeupdate', () => {
  if (state.source !== 'recording') return;
  const duration = video.duration || 1;
  $('seek').value = Math.round((video.currentTime / duration) * 1000);
  const totalSeconds = Math.floor(video.currentTime);
  $('time').textContent = `${Math.floor(totalSeconds / 60)}:${String(totalSeconds % 60).padStart(2, '0')}`;
});
$('seek').addEventListener('input', () => { if (Number.isFinite(video.duration)) video.currentTime = Number($('seek').value) / 1000 * video.duration; });

const layer = $('selectionLayer');
let anchor = null;
function clamp(value) { return Math.max(0, Math.min(1, value)); }
function localPoint(event) {
  const rect = layer.getBoundingClientRect();
  return { x: clamp((event.clientX - rect.left) / rect.width), y: clamp((event.clientY - rect.top) / rect.height) };
}
function syncSelectionLayer() {
  if (!video.videoWidth || !video.videoHeight) return;
  const rect = video.getBoundingClientRect();
  const stageRect = $('stage').getBoundingClientRect();
  const scale = Math.min(rect.width / video.videoWidth, rect.height / video.videoHeight);
  const width = video.videoWidth * scale, height = video.videoHeight * scale;
  layer.style.left = `${rect.left - stageRect.left + (rect.width - width) / 2}px`;
  layer.style.top = `${rect.top - stageRect.top + (rect.height - height) / 2}px`;
  layer.style.width = `${width}px`; layer.style.height = `${height}px`;
  layer.style.right = 'auto'; layer.style.bottom = 'auto';
  paintSelection();
}
function paintSelection() {
  const crop = state.crop;
  if (!crop) return;
  const box = $('selectionBox');
  box.hidden = false;
  box.style.left = `${layer.offsetLeft + crop.x * layer.clientWidth}px`; box.style.top = `${layer.offsetTop + crop.y * layer.clientHeight}px`;
  box.style.width = `${crop.width * layer.clientWidth}px`; box.style.height = `${crop.height * layer.clientHeight}px`;
  $('stageLabel').textContent = 'Selected region';
}
layer.addEventListener('pointerdown', event => {
  if (!state.source) return;
  anchor = localPoint(event); layer.setPointerCapture(event.pointerId);
});
layer.addEventListener('pointermove', event => {
  if (!anchor) return;
  const p = localPoint(event);
  state.crop = { x: Math.min(p.x, anchor.x), y: Math.min(p.y, anchor.y), width: Math.abs(p.x - anchor.x), height: Math.abs(p.y - anchor.y) };
  paintSelection();
});
layer.addEventListener('pointerup', event => {
  if (!anchor) return;
  const p = localPoint(event);
  if (Math.abs(p.x - anchor.x) < .02 || Math.abs(p.y - anchor.y) < .02) resetCrop();
  anchor = null;
});
layer.addEventListener('pointercancel', () => { anchor = null; });

function focusRect() {
  if (!$('cropToggle').checked || !state.crop) return { x: 0, y: 0, width: 1, height: 1 };
  return state.crop;
}
function imageCanvas(width, height) {
  const canvas = document.createElement('canvas'); canvas.width = width; canvas.height = height; return canvas;
}
async function readyVideo() {
  if (!state.source || !video.videoWidth || !video.videoHeight || video.readyState < 2) throw new Error('No ready frame in the preview');
}
async function captureFrame(changed = false) {
  await readyVideo();
  const crop = focusRect();
  const width = Math.max(1, Math.round(video.videoWidth * crop.width));
  const height = Math.max(1, Math.round(video.videoHeight * crop.height));
  const scale = Math.min(1, 1600 / Math.max(width, height));
  const canvas = imageCanvas(Math.max(1, Math.round(width * scale)), Math.max(1, Math.round(height * scale)));
  canvas.getContext('2d').drawImage(video, video.videoWidth * crop.x, video.videoHeight * crop.y, width, height, 0, 0, canvas.width, canvas.height);
  const data = canvas.toDataURL('image/jpeg', .83).split(',')[1];
  return { mime: 'image/jpeg', data, focus: crop, source: state.source, videoTime: state.source === 'recording' ? video.currentTime : null, changed };
}
function signature() {
  const crop = focusRect(), canvas = imageCanvas(96, 64);
  canvas.getContext('2d', { willReadFrequently: true }).drawImage(video,
    video.videoWidth * crop.x, video.videoHeight * crop.y,
    video.videoWidth * crop.width, video.videoHeight * crop.height, 0, 0, 96, 64);
  const pixels = canvas.getContext('2d').getImageData(0, 0, 96, 64).data;
  const gray = new Uint8Array(96 * 64);
  for (let i = 0; i < gray.length; i++) gray[i] = (pixels[i * 4] * 3 + pixels[i * 4 + 1] * 6 + pixels[i * 4 + 2]) / 10;
  return gray;
}
function delta(a, b) {
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += Math.abs(a[i] - b[i]);
  return sum / a.length;
}
function changedShare(a, b) {
  let changed = 0;
  for (let i = 0; i < a.length; i++) if (Math.abs(a[i] - b[i]) > 18) changed++;
  return changed / a.length;
}
function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
async function afterChange(maxWaitMs) {
  const generation = state.generation;
  await readyVideo();
  const baseline = signature();
  let previous = baseline, stable = 0, moved = false;
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    await sleep(300);
    if (!state.source || state.generation !== generation) throw new Error('Source changed or stopped during observation');
    const next = signature();
    if (delta(baseline, next) > 1.3 || changedShare(baseline, next) > .003) moved = true;
    stable = moved && delta(previous, next) < 2.5 ? stable + 1 : 0;
    if (stable >= 3) return captureFrame(true);
    previous = next;
  }
  return null;
}
async function poll() {
  try {
    const next = await api('/api/next');
    if (next.stop) { if (state.source) { stopLocal(); status('Agent stopped the observation session.'); } return; }
    if (!next.request || state.busy || state.seen.has(next.request.id)) return;
    state.seen.add(next.request.id); state.busy = true;
    const task = next.request;
    try {
      const frame = task.mode === 'changed' ? await afterChange(task.maxWaitMs) : await captureFrame();
      await api(`/api/frame/${encodeURIComponent(task.id)}`, 'POST', frame || { status: 'unchanged' });
      status(frame ? `Frame sent to the agent from ${state.source}.` : 'No settled visual change detected in the observation window.');
    } catch (error) {
      status(`Agent capture failed: ${error.message}`);
      try { await api(`/api/frame/${encodeURIComponent(task.id)}`, 'POST', { status: 'error', message: error.message }); } catch { /* Request may have expired or been stopped. */ }
    }
    finally { state.busy = false; }
  } catch (error) { status(`Local bridge connection failed: ${error.message}`); }
}
video.addEventListener('loadedmetadata', syncSelectionLayer);
window.addEventListener('resize', syncSelectionLayer);
window.addEventListener('pagehide', () => { stopTracks(); });
setInterval(() => { if (state.source) heartbeat(); }, 1000);
setInterval(poll, 450);
connected(false);
