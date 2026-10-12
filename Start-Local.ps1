param(
    [string]$Root,
    [int]$Port = 8000
)

$ErrorActionPreference = 'Stop'
$pythonExe = Join-Path $PSScriptRoot 'runtime\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
    & $pythonExe -c "import sys; raise SystemExit(sys.version_info < (3, 11))"
    if ($LASTEXITCODE -ne 0) {
        throw 'Python 3.11 or newer is required when the bundled runtime is unavailable.'
    }
}
$arguments = @((Join-Path $PSScriptRoot 'serve_local.py'), '--open', '--port', "$Port")
if ($Root) {
    $arguments += @('--root', $Root)
}
& $pythonExe @arguments
exit $LASTEXITCODE
