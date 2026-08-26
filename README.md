# ✨ Pulsanti — 10 Effetti Grafici

Una demo di **10 effetti grafici** (confetti, fuochi d'artificio, matrix rain, ripple, supernova, vortice galattico, scarica neon, esplosione, aurora e magia pura) realizzata in **un unico file HTML**: Canvas 2D + CSS, zero dipendenze.

Clicca un pulsante → l'effetto parte dal centro del bottone. 🎉

![preview](docs/preview.png)

## 🚀 Come usarlo

Basta aprire `index.html` con un browser moderno (doppio click o trinalo nel browser). Non serve un server né Node.js.

```
index.html   ← tutto qui: HTML + CSS + JavaScript
```

## 🎨 Gli 10 effetti

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

## 🧪 Test (Playwright)

Ogni effetto può essere testato singolarmente. Lo script Python `gen_tests.py` separa l'`index.html` in **10 file HTML individuali** dentro `test/`, ognuno con un bottone e una checkbox "Auto" (trigger ogni 3s).

```bash
# genera i 10 file di test in test/
python gen_tests.py

# installa le dipendenze di test
npm install

# esegue i test su tutti gli effetti
node test/run.js          # test combinati (index.html)
node test/run_orig.js     # test singolo per effetto
```

I test caricano la pagina via `file://`, simulano il click sul bottone e verificano che le particelle vengano generate senza errori JavaScript.

## 🛠️ Stack

- **HTML5 Canvas** — motore particellari condiviso (`requestAnimationFrame`)
- **CSS3** — gradienti, animazioni (glitch / shake / pulse / rainbow / bounce)
- **Vanilla JavaScript** — nessuna dipendenza in produzione
- **Playwright** — test end-to-end del rendering sui 10 effetti
- **Python** — generazione dei file di test

## 📁 Struttura

```
.
├── index.html          # demo completa (i 10 pulsanti)
├── gen_tests.py        # separa ogni effetto in un file HTML di test
├── package.json        # dipendenza: playwright
└── test/
    ├── *.html          # 10 effetti singoli (generati da gen_tests.py)
    ├── run.js          # test combinati
    └── run_orig.js     # test singolo per effetto
```

## Licenza

MIT
