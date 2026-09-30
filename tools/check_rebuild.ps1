param([string]$SdkPath = $env:RENPY_SDK)
$ErrorActionPreference = 'Stop'
if (-not $SdkPath) {
    $SdkPath = Join-Path $env:TEMP 'fpt-commit-rebuild-sdk\renpy-8.5.3-sdk'
}
$projectRoot = Split-Path -Parent $PSScriptRoot
$sdkPython = Join-Path $SdkPath 'lib\py3-windows-x86_64\python.exe'
$renpyScript = Join-Path $SdkPath 'renpy.py'
if (-not (Test-Path -LiteralPath $sdkPython)) {
    throw 'Set RENPY_SDK or pass -SdkPath with a Windows RenPy 8.5.3+ SDK directory.'
}
$reports = Join-Path $projectRoot 'tests\rebuild'
$runner = Join-Path $reports ('runner-' + [guid]::NewGuid().ToString('N'))
$testSaves = Join-Path $runner 'player-saves'
Push-Location -LiteralPath $projectRoot
try {
    & $sdkPython -X utf8 (Join-Path $PSScriptRoot 'verify_chapter1.py')
    if ($LASTEXITCODE -ne 0) { throw 'Source preservation/static audit failed.' }
    & $sdkPython -X utf8 (Join-Path $PSScriptRoot 'verify_fonts.py') $SdkPath
    if ($LASTEXITCODE -ne 0) { throw 'Font coverage audit failed.' }
    & $sdkPython -X utf8 (Join-Path $PSScriptRoot 'prepare_test_project.py') $runner
    if ($LASTEXITCODE -ne 0) { throw 'Could not prepare isolated test project.' }
    & $sdkPython $renpyScript --savedir $testSaves $runner lint --error-code *> (Join-Path $reports 'lint.txt')
    if ($LASTEXITCODE -ne 0) { throw 'RenPy lint failed. See tests/rebuild/lint.txt.' }
    & $sdkPython $renpyScript --savedir $testSaves $runner test --overwrite-screenshots *> (Join-Path $reports 'engine-tests.txt')
    $engineStatus = $LASTEXITCODE
    Get-Content -LiteralPath (Join-Path $reports 'engine-tests.txt') -Tail 10
    if ($engineStatus -ne 0) { throw 'Engine tests failed. See tests/rebuild/engine-tests.txt.' }
    Get-ChildItem -LiteralPath (Join-Path $runner 'tests\rebuild\screenshots') -File | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $reports 'screenshots') -Force
    }
} finally {
    Pop-Location
}
