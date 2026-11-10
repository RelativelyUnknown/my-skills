// specs.js — one entry per scene: window.SPECS.<scene> = { title, … }. Plain data, no logic.
// Compute real values in your own code (any language) and write them here; scenes only draw.
// Optional brand: window.THEME = { ACCENT: '#1B7F5C', SURFACE: '#101614', INK: '#EAF2EE', FONT: { sans: "'IBM Plex Sans', IN, sans-serif" } };
window.SPECS = {
  example: {
    title: 'method comparison – Before vs After',
    labels: ['Before', 'After'],
    step: 60, domain: [-12, 304], yDomain: [8, 22], yTicks: [10, 15, 20],
    tickFmt: s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`,
    ticks: [0, 60, 120, 180, 240],
    points: [{ x: 0, y: 10 }, { x: 20, y: 20 }, { x: 80, y: 14 }, { x: 140, y: 20 }, { x: 170, y: 12 }, { x: 250, y: 20 }],
    left:  [{ x: 0, value: 15, text: '15.0' }, { x: 60, value: 14, text: '14.0' }, { x: 120, value: 16, text: '16.0' }, { x: 180, value: 18, text: '18.0' }, { x: 240, value: 20, text: '20.0' }],
    right: [{ x: 0, value: 10, text: '10.0' }, { x: 60, value: 16, text: '16.0' }, { x: 120, value: 18, text: '18.0' }, { x: 180, value: 13, text: '13.0' }, { x: 240, value: 19, text: '19.0' }],
    highlight: 0,
  },
};
