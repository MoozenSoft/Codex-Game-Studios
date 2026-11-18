param(
  [Parameter(Mandatory=$true)][string]$Phase,
  [Parameter(Mandatory=$true)][ValidateSet('bash','npm','node','git')][string]$Tool,
  [Parameter(Mandatory=$true)][string[]]$ArgumentList
)
$ErrorActionPreference = 'Stop'
$acceptanceRoot = (Get-Location).Path
if ($acceptanceRoot.Replace('\','/') -cne 'D:/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance') { throw 'cwd 不匹配' }
if ((git branch --show-current).Trim() -cne 'app-acceptance') { throw '分支不匹配' }
if ($Phase -notmatch '^[a-z0-9-]+$') { throw '无效阶段名' }
$gitExec = git --exec-path
if ($LASTEXITCODE -ne 0) { throw 'Git 不可用' }
$gitRoot = Split-Path (Split-Path (Split-Path $gitExec.Trim()))
$bashPath = Join-Path $gitRoot 'bin/bash.exe'
if (-not (Test-Path -LiteralPath $bashPath)) { throw '实际 Git Bash 不存在' }
$env:CGS_PYTHON = 'C:/Users/xingxing/AppData/Local/Python/pythoncore-3.12-64/python.exe'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PAGE_SHOT_BROWSER = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
$env:PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD = '1'
$env:npm_config_cache = Join-Path $acceptanceRoot '.npm'
$env:GIT_OPTIONAL_LOCKS = '0'
$executable = switch ($Tool) { 'bash' { $bashPath } 'npm' { (Get-Command npm.cmd).Source } 'node' { (Get-Command node.exe).Source } 'git' { (Get-Command git.exe).Source } }
$evidenceRoot = Join-Path $acceptanceRoot 'production/qa/evidence/app-acceptance'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$started = [DateTimeOffset]::Now.ToString('o')
$ErrorActionPreference = 'Continue'
$lines = @(& $executable @ArgumentList 2>&1 | ForEach-Object { $_.ToString() })
$commandExit = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
[System.IO.File]::WriteAllText((Join-Path $evidenceRoot ($Phase + '.log')), ($lines -join "`n") + "`n", $utf8)
$record = [pscustomobject]@{ phase=$Phase; executable=$executable; args=$ArgumentList; started=$started; exit=$commandExit; log=('production/qa/evidence/app-acceptance/' + $Phase + '.log') }
$json = $record | ConvertTo-Json -Depth 4 -Compress
[System.IO.File]::AppendAllText((Join-Path $evidenceRoot 'commands.jsonl'), $json + "`n", $utf8)
Write-Output $json
$lines | Select-Object -Last 20 | Write-Output
exit $commandExit
