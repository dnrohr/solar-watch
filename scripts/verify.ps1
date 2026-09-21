$ErrorActionPreference = "Stop"
.\.venv\Scripts\python.exe -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "pytest failed with exit code $LASTEXITCODE" }
.\.venv\Scripts\python.exe -m solar_watch.cli generate --root . | Out-Null
if ($LASTEXITCODE -ne 0) { throw "artifact generation failed with exit code $LASTEXITCODE" }
git diff --exit-code -- data artifacts/plots printables/p1
if ($LASTEXITCODE -ne 0) { throw "generated artifacts differ from the committed files" }
