const { chromium } = require('playwright-core');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 700 } });
  let jsError = null;
  page.on('pageerror', e => { jsError = e.message; });
  await page.goto('file://' + path.join(__dirname, '..', 'index.html'));
  await page.evaluate(() => { window.__particles = particles; window.__fxReady = true; });
  // clicca su ogni pulsante
  const btns = await page.$$('#grid button');
  for (const b of btns) {
    await b.click();
    await page.waitForTimeout(300);
    const count = await page.evaluate(() => window.__particles ? window.__particles.length : -1);
    console.log('ORIGINAL particles after click:', count, 'error=', jsError || 'none');
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
