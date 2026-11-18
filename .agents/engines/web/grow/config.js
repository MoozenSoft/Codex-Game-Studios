// Every tuning value, from data/config.json: each with value, min, max and step.
// The game's code reads them through window.CONFIG, as the one-shot did, until
// the grow step's TypeScript move gives it imports (src/config.ts). The tweak
// panel is on the dev server only: no build has it.
// 过渡加载器先按经典script保留全局词法绑定与window属性，再用JSON作为可调参数来源。
import './config-source.js';
import data from '../data/config.json';

window.CONFIG = data;
if (import.meta.env.DEV) await import('./dev/tune');
