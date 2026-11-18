# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: n-retry.spec.ts >> N 在 over 真实结果画面重试并重置完整状态与 RNG
- Location: tests\integration\n-retry.spec.ts:52:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: "play"
Received: "over"
```

# Test source

```ts
  1   | import { expect, test, type Page } from '@playwright/test';
  2   | import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
  3   | import { resolve } from 'node:path';
  4   | import { pathToFileURL } from 'node:url';
  5   | import type { State } from '../../src/game/types';
  6   |
  7   | const config = JSON.parse(readFileSync('data/config.json', 'utf8'));
  8   | const evidence = 'production/qa/evidence/story-001-n-retry';
  9   | const build = pathToFileURL(resolve('dist-single/index.html')).href;
  10  |
  11  | async function open(page: Page): Promise<string[]> {
  12  |   const errors: string[] = [];
  13  |   page.on('pageerror', e => errors.push(e.message));
  14  |   page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  15  |   await page.goto(`${build}?manual=1&seed=${config.seed}`);
  16  |   await expect.poll(() => page.evaluate(() => typeof window.game?.step)).toBe('function');
  17  |   return errors;
  18  | }
  19  |
  20  | async function state(page: Page): Promise<State> {
  21  |   return page.evaluate(() => window.game!.state as State);
  22  | }
  23  |
  24  | async function press(page: Page, key: string, frames = 1): Promise<void> {
  25  |   await page.keyboard.press(key);
  26  |   await page.evaluate(n => window.game!.step(n), frames);
  27  | }
  28  |
  29  | async function reachEnding(page: Page, ending: 'over' | 'results'): Promise<State> {
  30  |   // 所有输入经过真实 Chrome 键盘；仅用现有 hook 推进确定帧数。
  31  |   await page.keyboard.down('ArrowRight');
  32  |   await page.evaluate(() => window.game!.step(30, false));
  33  |   await press(page, 'Space', 4);
  34  |   expect((await state(page)).score).toBe(1);
  35  |   if (ending === 'over') {
  36  |     await page.evaluate(n => window.game!.step(n), Math.ceil(config.duration.value / config.step.value) + 1);
  37  |   } else {
  38  |     await page.evaluate(() => window.game!.step(69, false));
  39  |     await press(page, 'Space', 4);
  40  |     await page.evaluate(() => window.game!.step(75, false));
  41  |     await press(page, 'Space', 4);
  42  |   }
  43  |   await page.keyboard.up('ArrowRight');
  44  |   expect(await page.evaluate(() => window.game!.scene)).toBe(ending);
  45  |   const ended = await state(page);
  46  |   expect(ended.x).toBeGreaterThan(config.startX.value);
  47  |   expect(ended.score).toBe(ending === 'over' ? 1 : config.quota.value);
  48  |   return ended;
  49  | }
  50  |
  51  | for (const ending of ['over', 'results'] as const) {
  52  |   test(`N 在 ${ending} 真实结果画面重试并重置完整状态与 RNG`, async ({ page }) => {
  53  |     const errors = await open(page);
  54  |     const initial = await state(page);
  55  |     await press(page, 'Enter');
  56  |     const before = await reachEnding(page, ending);
  57  |     mkdirSync(evidence, { recursive: true });
  58  |     await page.screenshot({ path: `${evidence}/n-${ending}-before.png` });
  59  |
  60  |     await press(page, 'n');
  61  |     const after = await state(page);
  62  |     const scene = await page.evaluate(() => window.game!.scene);
  63  |     const events = await page.evaluate(() => window.game!.events);
  64  |     writeFileSync(`${evidence}/n-${ending}-attempt.json`, JSON.stringify({ initial, before, after, scene, events }, null, 2));
> 65  |     expect(scene).toBe('play');
      |                   ^ Error: expect(received).toBe(expected) // Object.is equality
  66  |     expect(after).toEqual(initial);
  67  |     expect(events).toEqual(['start']);
  68  |     await page.screenshot({ path: `${evidence}/n-${ending}-after.png` });
  69  |
  70  |     // 同样输入再次完成一局，验证 reset 同时重置随机序列。
  71  |     expect(await reachEnding(page, ending)).toEqual(before);
  72  |     expect(errors).toEqual([]);
  73  |   });
  74  | }
  75  |
  76  | test('N 在标题、游玩和暂停均不重开且与无 N 的同 seed 对照一致', async ({ page }) => {
  77  |   async function run(withN: boolean) {
  78  |     const errors = await open(page);
  79  |     const title = await state(page);
  80  |     await press(page, 'n');
  81  |     expect(await page.evaluate(() => window.game!.scene)).toBe('title');
  82  |     expect(await state(page)).toEqual(title);
  83  |     await press(page, 'Enter');
  84  |     await page.keyboard.down('ArrowRight');
  85  |     await page.evaluate(() => window.game!.step(60, false));
  86  |     await page.keyboard.up('ArrowRight');
  87  |     if (withN) await page.keyboard.press('n');
  88  |     await page.evaluate(() => window.game!.step());
  89  |     const active = await state(page);
  90  |     expect(active.t).toBeGreaterThan(1);
  91  |     expect(active.x).toBeGreaterThan(config.startX.value);
  92  |     expect(await page.evaluate(() => window.game!.scene)).toBe('play');
  93  |     await press(page, 'p');
  94  |     const paused = await state(page);
  95  |     await press(page, 'n');
  96  |     expect(await page.evaluate(() => window.game!.scene)).toBe('pause');
  97  |     expect(await state(page)).toEqual(paused);
  98  |     expect(errors).toEqual([]);
  99  |     return { active, paused, events: await page.evaluate(() => window.game!.events) };
  100 |   }
  101 |   expect(await run(true)).toEqual(await run(false));
  102 | });
  103 |
```
