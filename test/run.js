const { chromium } = require('playwright-core');
const path = require('path');

const effects = ['confetti','firework','supernova','matrix','ripple','spiral','neon','explode','aurora','magic'];

(async () => {
  const browser = await chromium.launch();
  for (const name of effects) {
    const page = await browser.newPage({ viewport: { width: 1000, height: 700 } });
    let jsError = null;
    page.on('pageerror', e => { jsError = e.message; });
    await page.goto('file://' + path.join(__dirname, name + '.html'));
    // esponi le variabili interne su window per il test (solo lettura)
    await page.evaluate(() => {
      window.__particles = particles;
      window.__fxReady = true;
    });
    // simula il click sul bottone
    await page.click('#go');
    await page.waitForTimeout(500);
    const count = await page.evaluate(() => (window.__particles ? window.__particles.length : -1));
    console.log(`${name.padEnd(12)} particles=${count}  error=${jsError||'none'}`);
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
