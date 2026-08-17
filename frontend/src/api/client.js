const API_BASE = '/api/v1';

/**
 * Send a chat message and get a full (non-streaming) response.
 */
export async function sendMessage(message) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }

  return res.json();
}

/**
 * Send a chat message and receive a streaming response.
 * Calls `onChunk(text)` for every token received.
 * Returns the full assembled text when done.
 */
export async function streamMessage(message, onChunk) {
  const res = await fetch(`${API_BASE}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    throw new Error(`Stream request failed: ${res.status}`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let full = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const text = decoder.decode(value, { stream: true });
    full += text;
    onChunk(text);
  }

  return full;
}

/**
 * Get conversation memory / history.
 */
export async function getMemory() {
  const res = await fetch(`${API_BASE}/memory`);

  if (!res.ok) {
    throw new Error(`Memory request failed: ${res.status}`);
  }

  return res.json();
}

/**
 * Clear all conversation memory.
 */
export async function clearMemory() {
  const res = await fetch(`${API_BASE}/memory/clear`, { method: 'POST' });

  if (!res.ok) {
    throw new Error(`Clear memory failed: ${res.status}`);
  }

  return res.json();
}

/**
 * Check backend health.
 */
export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) return { status: 'unhealthy', version: 'unknown' };
    return res.json();
  } catch {
    return { status: 'offline', version: 'unknown' };
  }
}
