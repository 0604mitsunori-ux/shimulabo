# シミュラボ 毎朝のランキング・回数カウンター更新
#   GA4 → assets/ranking.json / assets/sim-counts.json を作り直し、変わっていれば push（Vercelが自動公開）
#   Windows タスク「Shimulabo_DailyRanking」から毎朝 6:00 に実行（PCが切れていたら次に起動したとき）
#   ログ: scripts/logs/daily_ranking.log（git管理外）
$ErrorActionPreference = 'Continue'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$logDir = Join-Path $PSScriptRoot 'logs'
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir 'daily_ranking.log'
function Log($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" | Out-File -FilePath $log -Append -Encoding utf8 }

Log '--- start'
git pull --rebase --autostash -q origin main 2>&1 | ForEach-Object { Log "pull: $_" }
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$out = python scripts/build_ranking.py 2>&1
$code = $LASTEXITCODE
$out | ForEach-Object { Log "build: $_" }
if ($code -ne 0) { Log "build failed ($code)"; exit 1 }

git add assets/ranking.json assets/sim-counts.json
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Log 'no change'; exit 0 }
git commit -q -m "毎朝の人気ランキング・回数カウンター更新（$(Get-Date -Format 'yyyy-MM-dd')）" 2>&1 | ForEach-Object { Log "commit: $_" }
git push -q origin HEAD:main 2>&1 | ForEach-Object { Log "push: $_" }
if ($LASTEXITCODE -ne 0) { Log 'push failed'; exit 1 }
Log 'pushed'
