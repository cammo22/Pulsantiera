const { chromium } = require('playwright-core');
const path = require('path');

const effects = ['confetti','firework','supernova','matrix','ripple','spiral','neon','explode','aurora','magic','galaxy','rainbowWave'];

// Effetti che NON usano l'array di particelle: si verifica il loro meccanismo proprio.
const signalOf = {
  matrix: async (page) => page.evaluate(() => window.__getStreams() ? window.__getStreams().length : 0),
  ripple: async (page) => page.evaluate(() => Array.from(document.querySelectorAll('div')).filter(d => (d.getAttribute('style') || '').includes('z-index')).length),
};

(async () => {
  const browser = await chromium.launch();
  for (const name of effects) {
    const page = await browser.newPage({ viewport: { width: 1000, height: 700 } });
    let jsError = null;
    page.on('pageerror', e => { jsError = e.message; });
    await page.goto('file://' + path.join(__dirname, name + '.html'));
    // esponi le variabili interne su window per il test (solo lettura)
    await page.evaluate(() => {
      window.__particles = particles;          // array ref invariato → vista live
      window.__getStreams = () => matrixStreams; // getter: matrixStreams viene riassegnato
      window.__fxReady = true;
    });
    // simula il click sul bottone
    await page.click('#go');
    await page.waitForTimeout(500);
    const count = signalOf[name]
      ? await signalOf[name](page)
      : await page.evaluate(() => (window.__particles ? window.__particles.length : -1));
    console.log(`${name.padEnd(12)} particles=${count}  error=${jsError||'none'}`);
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
