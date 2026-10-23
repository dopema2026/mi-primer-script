@echo off
rem Doble clic: Codex hace todas sus tareas pendientes.
rem Solo puede escribir dentro de esta carpeta (sandbox workspace-write).
cd /d "%~dp0"
codex exec -s workspace-write -C "%~dp0." --skip-git-repo-check "Eres Codex. Lee REGLAS.md y haz todas las tareas de cola/pendientes que terminan en _codex."
pause
