@echo off
rem Doble clic: Codex hace todas sus tareas pendientes.
cd /d "%~dp0"
codex exec --full-auto "Eres Codex. Lee REGLAS.md y haz todas las tareas de cola/pendientes que terminan en _codex."
pause
