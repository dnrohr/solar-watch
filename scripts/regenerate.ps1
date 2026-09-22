$ErrorActionPreference = "Stop"
.\.venv\Scripts\python.exe -m solar_watch.cli generate --root .
.\.venv\Scripts\python.exe -m solar_watch.cli generate-p2 --root .
.\.venv\Scripts\python.exe -m solar_watch.cli analyze-p2 --root .
