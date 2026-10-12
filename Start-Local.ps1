param(
    [string]$Root,
    [int]$Port = 8000
)

$ErrorActionPreference = 'Stop'
$pythonExe = Join-Path $PSScriptRoot 'runtime\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}
$arguments = @((Join-Path $PSScriptRoot 'serve_local.py'), '--open', '--port', "$Port")
if ($Root) {
    $arguments += @('--root', $Root)
}
& $pythonExe @arguments
exit $LASTEXITCODE
