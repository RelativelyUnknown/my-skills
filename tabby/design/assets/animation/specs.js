// specs.js — one entry per scene: window.SPECS.<scene> = { title, … }. Plain data, no logic.
// Compute real values in your own code (any language) and write them here; scenes only draw.
// Optional brand: window.THEME = { ACCENT: '#1B7F5C', SURFACE: '#101614', INK: '#EAF2EE', FONT: { sans: "'IBM Plex Sans', IN, sans-serif" } };
window.SPECS = {
  example: {
    title: 'a request through the service',
    nodes: [
      { id: 'client', name: 'client', role: 'browser', x: 130, y: 230 },
      { id: 'api', name: 'api', role: 'http server', x: 350, y: 230 },
      { id: 'queue', name: 'queue', role: 'redis list', x: 570, y: 230 },
      { id: 'worker', name: 'worker', role: 'python process', x: 790, y: 230 },
      { id: 'db', name: 'database', role: 'postgres', x: 790, y: 390 },
    ],
    edges: [
      { from: 'client', to: 'api', kind: 'main', label: 'POST' },
      { from: 'api', to: 'queue', kind: 'main', label: 'ENQUEUE' },
      { from: 'queue', to: 'worker', kind: 'main', label: 'CONSUME' },
      { from: 'worker', to: 'db', kind: 'secondary', label: 'WRITE' },
      { from: 'worker', to: 'queue', kind: 'retry', label: 'RETRY' },
    ],
    highlight: 'queue',
  },
};
