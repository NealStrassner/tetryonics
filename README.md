# Tetryonics

Two computational libraries — one **Python**, one **JavaScript** — that calculate
physics using **Kelvin Abraham's Tetryonic geometry**. Particles, charges, masses
and elements all derive from one geometric quantum.

**Created by Neal Strassner.** The libraries implement Kelvin Abraham's Tetryonic
theory, used with his permission. The theory itself is © Kelvin C. Abraham
(www.tetryonics.com).

## What's in here

- `tetryonics/`      — the Python library (pure Python, no dependencies)
- `tetryonics.js`    — the same library for JavaScript (browser or Node)
- `tests/`           — 185 tests that prove the math
- `examples/demo.py` — runnable examples
- `MANUAL.md`        — full list of every function
- `pyproject.toml`   — Python install file
- `package.json`     — JavaScript (npm) install file

24 modules, 448 functions (plus 9 builder classes), zero dependencies. The JavaScript
library mirrors the Python one — same functions, same numbers.

## Python — quick start

Needs only Python 3.9+. Nothing to install.

```python
import tetryonics as t

t.proton().charge_e                        # 1.0
t.element(6).mass_amu                       # 11.997  (carbon)
t.spectra.line_wavelength("balmer", 3)      # 6.603e-7 m  (hydrogen red line)
t.cosmology.body_escape_velocity("earth")   # 11187 m/s
```

### Add it to your project (pick one)

- **Just drop it in** — copy the `tetryonics/` folder into your project and
  `import tetryonics`. No install, no dependencies.
- **From GitHub:**
  ```bash
  pip install git+https://github.com/NealStrassner/tetryonics
  ```
- **From a local copy** — run `pip install .` inside this folder.

Run the tests:

```bash
python tests/test_core.py     # -> 16/16 passed
```

## JavaScript — quick start

```js
const T = require('./tetryonics.js');    // or window.Tetryonics in a browser

T.particles.proton().chargeE             // 1
T.elements.element(6).massAmu            // 11.997  (carbon)
T.spectra.lineWavelength('balmer', 3)    // 6.603e-7 m
T.cosmology.bodyEscapeVelocity('earth')  // 11187 m/s
```

### Add it to your project (pick one)

- **Browser:** `<script src="tetryonics.js"></script>`, then use `Tetryonics`.
- **Node:** `const T = require('./tetryonics.js');`
- **npm, from GitHub:** `npm install github:NealStrassner/tetryonics`, then `const T = require('tetryonics');`

Python and JavaScript give the same numbers.

## A few of the numbers it computes

| Check | Result |
|---|---|
| mass quantum  m_q = h/c²        | 7.376×10⁻⁵¹ kg |
| charge quantum Ω/c² = 1/12 of e | 1.335×10⁻²⁰ C |
| elementary charge  12×q         | 1.602×10⁻¹⁹ C |
| proton / electron mass ratio    | 1875 |
| hydrogen red line (H-α)         | 660.3 nm |
| fine-structure  α = 2π·Ω        | 0.0075398 |
| c from ε₀, μ₀                   | 299,792,458 m/s |

All 185 tests pass.

## License

Released under the **PolyForm Noncommercial License 1.0.0** — see [LICENSE](LICENSE).

- ✅ Free for any **noncommercial** use — study, research, teaching, hobby projects.
  Use it, change it, share it.
- ⛔ **No commercial use or resale** without written permission from the author,
  Neal Strassner. *No Boeing starships.* 🙂
- The license covers the **software only**. The underlying **Tetryonic theory is
  © Kelvin C. Abraham** and isn't yours to sell or publish without his separate OK.

Kelvin Abraham has approved this release.
