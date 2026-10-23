# mi-primer-script
## Así hablaban los grandes personajes de la historia (@dopemaweb)

- `01_manifest/scenes.json`: las 6 escenas (rótulos, voz, SFX, prompts de imagen y Seedance, duraciones).
- `scripts/build_master.py`: posproducción local con FFmpeg.
  - `python3 scripts/build_master.py audio cesar` → voz entra en 1.5 s sobre el ambiente, con ducking.
  - `python3 scripts/build_master.py scene cesar` → rótulo (0.2–3.5 s) + marca `@dopemaweb`.
  - `python3 scripts/build_master.py master` → máster 1080×1920, 24 fps, -14 LUFS, ~62.5 s.
