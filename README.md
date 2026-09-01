# ✨ Pulsantiera — Effetti Grafici Modulari

Una demo di **12 effetti grafici** (confetti, fuochi d'artificio, matrix rain, ripple, supernova, vortice galattico, scarica neon, esplosione, aurora, magia pura, galaxy e arcobaleno) realizzata in **un unico file HTML**: Canvas 2D + CSS, zero dipendenze.

- **Clicca un pulsante** → l'effetto parte dal centro del bottone. 🎉
- **▶ Play Pulsantiera** → avvia la modalità *play* che cicla automaticamente tutti gli effetti (~1,4s ciascuno); clicca di nuovo per **⏸ Pause**.

L'architettura è **modulare**: ogni effetto e pulsante è descritto da una sola riga nell'registry `EFFECTS`, quindi aggiungere nuovi effetti è facilissimo.

## 🚀 Come usarlo

Basta aprire `index.html` con un browser moderno (doppio click o trinalo nel browser). Non serve un server né Node.js.

```
index.html   ← tutto qui: HTML + CSS + JavaScript
```

## 🌐 Anteprima live (GitHub Pages)

Vuoi vederla al volo senza scaricare nulla? Apri l'anteprima ospitata su **GitHub Pages**:

[![Apri l'anteprima live](https://img.shields.io/badge/%E2%9A%A8%E2%AF%88_Apri_l%27ant%C3%ADmina_live-10881B?style=for-the-badge&logo=github)](https://cammo22.github.io/Pulsantiera/)

Il sito serve `index.html` direttamente dal branch **main** (cartella radice `/`): ogni commit su main aggiorna automaticamente l'anteprima.

## 🎨 Gli 12 effetti

| # | Effetto | Descrizione |
|---|---------|-------------|
| 1 | 🎉 Confetti      | Pioggia di confetti colorati che balzano verso l'alto |
| 2 | 🎆 Fuochi d'Artificio | Spara un fuoco e illumina gli altri pulsanti |
| 3 | 💻 Matrix Rain   | Pioggia di katakana/full-screen stile Matrix |
| 4 | 🌊 Ripple        | Onde concentriche come sull'acqua |
| 5 | 🚀 Supernova     | Esplosione radiale di stelle con onda d'urto |
| 6 | 🌀 Vortice Galattico | Spirale che si avvolge su se stessa |
| 7 | ⚡ Scarica Neon  | Tre scarate elettriche multicolori |
| 8 | 💥 Esplosione    | Bombarda tutto con particelle veloci |
| 9 | 🌌 Aurora        | Cortine verdi/viola che salgono e ondeggiano |
| 10 | ✨ Magia Pura   | Esplosione radiale di stelle che cadono (sparkler) |
| 11 | 🪐 Galaxy       | Spirale di stelle con 3 bracci che ruotano |
| 12 | 🌈 Arcobaleno    | Fontana arcobaleno che ondeggia sinuosamente |

## ➕ Aggiungere un nuovo effetto

Tutto gira attorno a una semplice **registry** (`EFFECTS`) e a una palette di gradiente (`GRADIENTS`). I pulsanti non sono scritti a mano: vengono generati automaticamente da `renderButtons()`, e la modalità *Play* sa già usare qualsiasi effetto registrato.

Per aggiungere un nuovo pulsante/effetto servono **solo 2 passi**:

```js
// 1) la funzione dell'effetto (usa spawn() per le particelle, o disegna liberamente)
function mioEffetto(x, y){
  spawn(x, y, { count: 60, speed: 8, size: 10, colors:['#ff0','#08f'] });
}

// 2) registrala — il bottone e la modalità Play si occupano del resto
EFFECTS.push({ id:'mioEffetto', label:'🚀 Mio Effetto', run: mioEffetto });
```

Regole pratici:
- Gli effetti **basati sulle particelle** usano `spawn(x, y, {count, speed, size, colors, gravity, ...})`.
- Gli effetti **liberi** (es. `matrix`, `ripple`) possono disegnare direttamente sul canvas o creare elementi DOM.
- Il `id` deve essere univoco; `label` è il testo del bottone; `run` riceve coordinate `(x, y)` al centro del bottone cliccato.

## 🧪 Test (Playwright)

Ogni effetto può essere testato singolarmente. Lo script Python `gen_tests.py` separa l'`index.html` in **file HTML individuali** dentro `test/`, ognuno con un bottone e una checkbox "Auto" (trigger ogni 3s).

```bash
# genera i file di test in test/ (uno per effetto)
python gen_tests.py

# installa le dipendenze di test
npm install

# esegue i test su tutti gli effetti (uno per volta, pagina pulita ciascuna)
node test/run.js
```

I test caricano la pagina via `file://`, simulano il click sul bottone e verificano che l'effetto produca output (particelle / stream di Matrix / nodi DOM del ripple) **senza errori JavaScript**. Gli effetti senza particelle (`matrix`, `ripple`) vengono verificati con il loro meccanismo specifico.

## 🛠️ Stack

- **HTML5 Canvas** — motore particellari condiviso (`requestAnimationFrame`)
- **CSS3** — gradienti, animazioni (glitch / shake / pulse / rainbow / bounce)
- **Vanilla JavaScript** — nessuna dipendenza in produzione
- **Playwright** — test end-to-end del rendering sui 12 effetti
- **Python** — generazione dei file di test

## 📁 Struttura

```
.
├── index.html          # demo completa (i 12 pulsanti + modalità Play)
├── gen_tests.py        # separa ogni effetto in un file HTML di test
├── package.json        # dipendenza: playwright
└── test/
    ├── *.html          # effetti singoli (generati da gen_tests.py)
    ├── run.js          # test per effetto (uno per pagina)
    └── run_orig.js     # test combinato su index.html (click su ogni bottone)
```

## Licenza

MIT
