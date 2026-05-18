# Sync zh/ to repo root and push to GitHub
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

git remote set-url origin https://github.com/nozomi0525/zju-helperr.git

Write-Host "Fetching origin main..."
git fetch origin main
git checkout -B main origin/main

Write-Host "Syncing zh/ to repo root..."
$dirs = @("backend", "frontend")
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
    robocopy "zh\$d" $d /E /XD staticfiles __pycache__ node_modules dist .git /NFL /NDL /NJH /NJS | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed for $d" }
}
Copy-Item "zh\docker-compose.yml" "." -Force
Copy-Item "zh\README.md" "." -Force
Copy-Item "zh\start.sh" "." -Force
Copy-Item "zh\stop.sh" "." -Force

git add -A
git status

$msg = "update: profile UI, login state fix, publish count from DB"
$changes = git diff --cached --name-only
if (-not $changes) {
    Write-Host "Nothing to commit."
    exit 0
}

git commit -m $msg
Write-Host "Pushing to origin main..."
git push -u origin main
Write-Host "Done: https://github.com/nozomi0525/zju-helperr"
