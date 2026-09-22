$ErrorActionPreference = "Stop"
.\.venv\Scripts\python.exe -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "pytest failed with exit code $LASTEXITCODE" }
.\.venv\Scripts\python.exe -m solar_watch.cli generate --root . | Out-Null
if ($LASTEXITCODE -ne 0) { throw "artifact generation failed with exit code $LASTEXITCODE" }
git diff --exit-code -- data artifacts/plots/p0_reference_42p1N_2025.png artifacts/plots/p0_validation_errors_42p1N_2025.png artifacts/plots/p1_cam_profiles_42p1N.png printables/p1
if ($LASTEXITCODE -ne 0) { throw "generated artifacts differ from the committed files" }
.\.venv\Scripts\python.exe scripts\verify_p2_regeneration.py
if ($LASTEXITCODE -ne 0) { throw "P2 clean regeneration verification failed" }
