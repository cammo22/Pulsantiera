#!/usr/bin/env python3
"""Separa i 10 effetti grafici in file HTML individuali e testabili."""
import re, os

SRC = "index.html"
OUTDIR = "test"
os.makedirs(OUTDIR, exist_ok=True)

src = open(SRC, encoding="utf-8").read()

# --- estrai CSS originale ---
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)

# --- engine comune (estratto dall'originale: da 'const fx' a fine spawn) ---
engine_start = src.index("const fx = document.getElementById('fx');")
engine_end = src.index("function drawStar(", src.index("function startLoop()"))
# prendiamo tutto fino alla fine di spawn()
spawn_end = src.index("startLoop();", engine_start) + len("startLoop();")
engine = src[engine_start:spawn_end]
# chiudiamo il for di spawn che manca (l'originale ha la parentesi dopo startLoop();)
engine += "\n}"  # chiude il for(...) dello spawn
engine += "\n\nfunction illuminateButtons(except) { /* noop in test individuale */ }"

# --- trigger comune ---
trigger_tmpl = """
const go = document.getElementById('go');
function trigger() {
  const r = go.getBoundingClientRect();
  @@CALL@@;
}
go.addEventListener('click', trigger);
document.getElementById('auto').addEventListener('change', function () {
  if (this.checked) window._iv = setInterval(trigger, 3000);
  else clearInterval(window._iv);
});
trigger(); // mostra un'subito all'apertura
"""

# --- definizione dei 10 effetti: id, label, classe bottone, codice JS ---
effects = {
  "confetti": (
    "🎉 Confetti", "b1",
    """function confetti(x, y) {
  spawn(x, y, { count: 90, speed: 9, gravity: 0.3, size: 10, colors: ['#ff5f6d','#ffd200','#38f9d7','#00c6ff','#f5576c'], up: 7 });
}""",
    "confetti(cx, cy);",
  ),
  "firework": (
    "🎆 Fuochi d'Artificio", "b2",
    """function firework(x, y) {
  const colors = ['#ff5f6d','#00c6ff','#38f9d7','#ffd200','#f5576c','#7bffb0'];
  spawn(x, y, { count: 60, speed: 7, gravity: 0.18, size: 6, colors, decay: 0.014, shape: 'rect' });
  const fl = document.createElement('div');
  fl.style.cssText = `position:fixed;left:${x}px;top:${y}px;width:12px;height:12px;
    background:#fff;border-radius:50%;transform:translate(-50%,-50%);
    box-shadow:0 0 40px 20px #fff;pointer-events:none;z-index:998;transition:.3s;`;
  document.body.appendChild(fl);
  requestAnimationFrame(() => { fl.style.opacity = '0'; });
  setTimeout(() => fl.remove(), 320);
}""",
    "firework(cx, cy);",
  ),
  "supernova": (
    "🚀 Supernova", "b5",
    """function supernova(x, y) {
  const colors = ['#ff9a00','#ffea00','#ff3c00','#fff','#ff7ee7'];
  spawn(x, y, { count: 40, speed: 5, gravity: 0, size: 6, colors: ['#fff'], decay: 0.02 });
  spawn(x, y, { count: 24, speed: 2.5, gravity: 0, size: 16, colors: ['#ffea00'], decay: 0.02, shape: 'ring' });
  spawn(x, y, { count: 220, speed: 16, gravity: 0.05, size: 11, colors, decay: 0.007, shape: 'star' });
  setTimeout(() => spawn(x, y, { count: 130, speed: 9, gravity: 0.12, size: 8, colors, decay: 0.011, shape: 'star' }), 150);
  const fl = document.createElement('div');
  fl.style.cssText = `position:fixed;left:${x}px;top:${y}px;width:24px;height:24px;border-radius:50%;
    background:radial-gradient(circle,#fff 0%,rgba(255,234,0,.95) 25%,rgba(255,154,0,.4) 55%,rgba(255,154,0,0) 75%);
    transform:translate(-50%,-50%) scale(1);pointer-events:none;z-index:996;
    transition:scale .7s ease-out, opacity .7s;`;
  document.body.appendChild(fl);
  requestAnimationFrame(() => { fl.style.transform = `translate(-50%,-50%) scale(22)`; fl.style.opacity = '0'; });
  setTimeout(() => fl.remove(), 720);
}""",
    "supernova(cx, cy);",
  ),
  "matrix": (
    "💻 Matrix Rain", "b3",
    """let matrixStreams = null;
let matrixTimer = null;
const MATRIX_FS = 20;
const MATRIX_RUN_MS = 8000;

function matrixRain() {
  const glyphs = 'アカサタナ0123456789ABCDEFλ#$%&*@漢字猫';
  const cols = Math.max(1, Math.ceil(innerWidth / MATRIX_FS));
  matrixStreams = [];
  for (let c = 0; c < cols; c++) {
    matrixStreams.push({
      x: c * MATRIX_FS + MATRIX_FS / 2,
      speed: 4 + Math.random() * 6,
      offset: -Math.random() * innerHeight,
      len: 14 + (Math.random() * 18 | 0),
      glyphs: Array.from({ length: 50 }, () => glyphs[(Math.random() * glyphs.length) | 0])
    });
  }
  stopAllAnimations();
  if (!rafId) matrixLoop();
  clearTimeout(matrixTimer);
  matrixTimer = setTimeout(() => { matrixStreams = null; }, MATRIX_RUN_MS);
}

function matrixLoop() {
  ctx.globalCompositeOperation = 'destination-out';
  ctx.fillStyle = 'rgba(0,0,0,0.13)';
  ctx.fillRect(0, 0, W, H);
  if (matrixStreams) {
    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    ctx.font = MATRIX_FS + 'px monospace';
    for (const s of matrixStreams) {
      s.offset += s.speed;
      if (s.offset - s.len * MATRIX_FS > innerHeight) {
        s.offset = -Math.random() * 300;
        s.speed = 4 + Math.random() * 6;
      }
      for (let t = s.len - 1; t >= 0; t--) {
        const yy = s.offset - t * MATRIX_FS;
        if (yy < -MATRIX_FS || yy > innerHeight + MATRIX_FS) continue;
        const ch = s.glyphs[(((s.len - 1 - t) % s.glyphs.length) + s.glyphs.length) % s.glyphs.length];
        if (t === 0) {
          ctx.fillStyle = '#eaffea';
          ctx.shadowColor = '#7dff7a'; ctx.shadowBlur = 14;
        } else {
          ctx.shadowBlur = 0;
          const g = 0.85 - (t / s.len) * 0.7;
          ctx.fillStyle = 'rgba(57,255,20,' + Math.max(0.08, g) + ')';
        }
        ctx.fillText(ch, s.x, yy);
      }
    }
    ctx.shadowBlur = 0;
  }
  if (matrixStreams) {
    rafId = requestAnimationFrame(matrixLoop);
  } else {
    cancelAnimationFrame(rafId);
    rafId = null;
  }
}""",
    "matrixRain();",
  ),
  "ripple": (
    "🌊 Ripple", "b4",
    """function ripple(x, y) {
  const c = '#00c6ff';
  for (let k = 0; k < 7; k++) {
    setTimeout(() => {
      const r = document.createElement('div');
      const size = 24;
      const lw = Math.max(1, 3 - k * 0.3);
      r.style.cssText = `position:fixed;left:${x}px;top:${y}px;width:${size}px;height:${size}px;
        border:${lw}px solid ${c};border-radius:50%;transform:translate(-50%,-50%) scale(1);
        box-shadow:0 0 10px ${c}, inset 0 0 6px ${c};
        pointer-events:none;z-index:999;
        transition:transform 1s cubic-bezier(.2,.7,.2,1), opacity 1s;`;
      document.body.appendChild(r);
      requestAnimationFrame(() => { r.style.transform = `translate(-50%,-50%) scale(${(460/size)})`; r.style.opacity = '0'; });
      setTimeout(() => r.remove(), 1050);
    }, k * 130);
  }
}""",
    "ripple(cx, cy);",
  ),
  "spiral": (
    "🌀 Vortice Galattico", "b6",
    """function spiral(x, y) {
  const colors = ['#667eea','#764ba2','#36d1dc','#5b86e5'];
  let i = 0;
  const iv = setInterval(() => {
    const a = i * 0.6;
    const r = i * 2.2;
    particles.push({
      x: x + Math.cos(a) * r, y: y + Math.sin(a) * r,
      vx: 0, vy: 0, gravity: 0, friction: 1,
      life: 1, decay: 0.02, size: 6,
      color: colors[i % colors.length], rot: 0, spin: 0.3, shape: 'rect'
    });
    startLoop();
    i++;
    if (i > 80) clearInterval(iv);
  }, 16);
}""",
    "spiral(cx, cy);",
  ),
  "neon": (
    "⚡ Scarica Neon", "b7",
    """function neon(x, y) {
  const colors = ['#00f260','#0575e6','#00c6ff','#fff'];
  for (let b = 0; b < 3; b++) {
    setTimeout(() => { spawn(x, y, { count: 50, speed: 9, gravity: 0, size: 5, colors, decay: 0.02 }); }, b * 80);
  }
}""",
    "neon(cx, cy);",
  ),
  "explode": (
    "💥 Esplosione", "b8",
    """function explode(x, y) {
  const colors = ['#ff4166','#ff4b2b','#ff9a00','#fff'];
  spawn(x, y, { count: 90, speed: 11, gravity: 0.25, size: 10, colors, decay: 0.016 });
}""",
    "explode(cx, cy);",
  ),
  "aurora": (
    "🌌 Aurora", "b9",
    """function aurora(x, y) {
  const colors = ['#39ff14','#7bffb0','#00ff88','#c06bff','#b24bf3','#55efc4'];
  for (let i = 0; i < 7; i++) {
    setTimeout(() => {
      spawn(x + (Math.random() * 440 - 220), y + (Math.random() * 80 - 40), { count: 24, speed: 1.5, gravity: -0.02, size: 26, colors, decay: 0.0035, up: 1, swayAmp: 0.07 + Math.random() * 0.09 });
    }, i * 80);
  }
}""",
    "aurora(cx, cy);",
  ),
  "magic": (
    "✨ Magia Pura", "b10",
    """function magic(x, y) {
  const colors = ['#f093fb','#f5576c','#ffd200','#7bffb0','#79c0ff'];
  spawn(x, y, { count: 90, speed: 8, gravity: 0.2, size: 8, colors, decay: 0.014, shape: 'star' });
}""",
    "magic(cx, cy);",
  ),
}

# --- template HTML ---
def build(name, label, cls, code, call):
    call = call.replace("cx, cy", "r.left + r.width/2, r.top + r.height/2")
    trigger = trigger_tmpl.replace("@@CALL@@", call)
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{label} — Test</title>
<style>
{css}
.auto {{ opacity: .6; font-size: .8rem; margin-top: -14px; }}
.auto input {{ vertical-align: middle; }}
</style>
</head>
<body>
  <canvas id="fx"></canvas>
  <div class="wrap">
    <h1>✨ {label} ✨</h1>
    <p class="sub">Test individuale · effetto <code>{name}</code></p>
    <button class="{cls}" id="go">{label}</button>
    <label class="auto"><input type="checkbox" id="auto"> Auto (ogni 3s)</label>
  </div>
  <div class="hint">File singolo · {name} · Canvas + CSS</div>
<script>
{engine}
{code}
{trigger}
</script>
</body>
</html>
"""
    return html

for name, (label, cls, code, call) in effects.items():
    out = os.path.join(OUTDIR, f"{name}.html")
    open(out, "w", encoding="utf-8").write(build(name, label, cls, code, call))
    print(f"scritto: {out}")

print("\nFatti:", len(effects), "file in test/")
