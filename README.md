# car

**停好停滿 Park Formosa** — a hard, original parking game in the browser. Twelve levels mixing the Taiwanese driving-test items (reverse bay, parallel parking, S-curve forward and in reverse) with a gas station, a three-point turn, a night-market street, a cliffside lookout, a B3 garage and a townhouse garage. Four vehicles (kei car, sports car, SUV, light truck) unlocked with stars; a route hint planned by hybrid A* on the game's own kinematics; a 3-second rewind after a crash. Touching a line or anything solid fails the level. Rear camera with guide lines, parking sensors, real wheel angles.

- `index.html` — the parking game, plus a Taiwanese small-car driving-test simulation (小型車場考: start-off checks, crosswalk, signalised right turn, railway crossing, hill start, parallel parking, reverse bay, S-curve) scored with the Highway Bureau deduction sheet incl. the 2026-03-31 rules (single file, Three.js from CDN, procedural car models and audio)
- `drive.html` — the earlier open-world mode (Hualien coast)
- `site/` — the searchable intro page; GitHub Pages serves it at `/`, the game at `/play/`, open world at `/drive/`

Controls: `W`/`S` drive and reverse · `A`/`D` steering wheel · `Space` brake · `C` camera · `H` route hint · `R` retry · `Esc` pause · mouse drag to look around. Phones: landscape, steering wheel on the left, pedals on the right.
