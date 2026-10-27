param(
    [string]$Html = "pilot/chapter-05.html",
    [string]$Pdf = "pilot/chapter-05.pdf",
    [string]$RenderDir = "pilot/render",
    [int]$Dpi = 120
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$htmlPath = (Resolve-Path $Html).Path
$pdfPath = Join-Path $root $Pdf
$renderPath = Join-Path $root $RenderDir

$chromeCandidates = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
)

$browser = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $browser) {
    throw "Chrome or Edge was not found. Install one or update the path in this script."
}

Write-Host "Browser: $browser"
Write-Host "Input:   $htmlPath"
Write-Host "Output:  $pdfPath"

$browserArgs = @(
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--virtual-time-budget=10000",
    "--print-to-pdf=$pdfPath",
    "file:///$($htmlPath -replace '\\','/')"
)

$proc = Start-Process -FilePath $browser -ArgumentList $browserArgs -Wait -PassThru -NoNewWindow -ErrorAction SilentlyContinue

if (-not (Test-Path $pdfPath)) {
    throw "PDF generation failed. Browser exit code: $($proc.ExitCode)"
}

Write-Host "PDF created."

if ($Dpi -gt 0) {
    New-Item -ItemType Directory -Force -Path $renderPath | Out-Null
    $py = @"
import pymupdf, os
doc = pymupdf.open(r'$pdfPath')
out = r'$renderPath'
for i, page in enumerate(doc):
    page.get_pixmap(dpi=$Dpi).save(os.path.join(out, f'page-{i+1:02d}.png'))
print('pages', len(doc))
print('size_cm', round(float(doc[0].mediabox.width)/72*2.54, 2), 'x', round(float(doc[0].mediabox.height)/72*2.54, 2))
"@
    & python -c $py
    if ($LASTEXITCODE -ne 0) {
        throw "Page rendering failed with Python exit code $LASTEXITCODE."
    }
}

Write-Host "Export complete."
