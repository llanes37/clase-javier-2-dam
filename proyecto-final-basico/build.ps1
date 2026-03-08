param(
    [string]$SrcDir = "src",
    [string]$BinDir = "bin",
    [string]$LibDir = "lib"
)

if (-not (Test-Path $BinDir)) {
    New-Item -ItemType Directory -Path $BinDir | Out-Null
}

$sources = Get-ChildItem -Recurse $SrcDir -Filter *.java | ForEach-Object { $_.FullName }
if ($sources.Count -eq 0) {
    Write-Host "No se encontraron archivos .java en $SrcDir"
    exit 1
}

Write-Host "Compilando $($sources.Count) fuentes..."
javac -encoding UTF-8 -cp "$BinDir;$LibDir/*" -d $BinDir $sources

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error de compilacion"
    exit 1
}

Write-Host "Compilacion completada."

