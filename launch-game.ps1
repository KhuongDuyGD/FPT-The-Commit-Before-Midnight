param([string]$SdkPath = $env:RENPY_SDK)
$ErrorActionPreference = 'Stop'
if (-not $SdkPath) {
    $SdkPath = Join-Path $env:TEMP 'fpt-commit-rebuild-sdk\renpy-8.5.3-sdk'
}
$launcher = Join-Path $SdkPath 'renpy.exe'
if (-not (Test-Path -LiteralPath $launcher)) {
    throw 'Set RENPY_SDK or pass -SdkPath with the directory containing renpy.exe.'
}
# Hide the helper console; Ren'Py creates its normal game window.
Start-Process -FilePath $launcher -ArgumentList ('"{0}"' -f $PSScriptRoot) -WindowStyle Hidden
