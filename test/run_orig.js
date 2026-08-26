const { chromium } = require('playwright-core');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 700 } });
  let jsError = null;
  page.on('pageerror', e => { jsError = e.message; });
  await page.goto('file://' + path.join(__dirname, '..', 'index.html'));
  await page.evaluate(() => {
    window.__particles = particles;              // array ref invariato → vista live
    window.__getStreams = () => matrixStreams;   // getter: matrixStreams viene riassegnato
    window.__fxReady = true;
  });
  const signalOf = {
    matrix: async (page) => page.evaluate(() => window.__getStreams() ? window.__getStreams().length : 0),
    ripple: async (page) => page.evaluate(() => Array.from(document.querySelectorAll('div')).filter(d => (d.getAttribute('style') || '').includes('z-index')).length),
  };
  // clicca su ogni pulsante
  const btns = await page.$$('#grid button');
  for (const b of btns) {
    await b.click();
    await page.waitForTimeout(300);
    const name = await b.evaluate(el => el.dataset.fx);
    const count = signalOf[name] ? await signalOf[name](page) : await page.evaluate(() => window.__particles ? window.__particles.length : -1);
    console.log(`ORIGINAL ${name} ->`, count, 'error=', jsError || 'none');
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
