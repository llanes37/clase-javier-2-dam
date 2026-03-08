$ErrorActionPreference = 'Stop'
$src = "src"
$bin = "bin"
$lib = "lib"
if (!(Test-Path $bin)) { New-Item -ItemType Directory -Path $bin | Out-Null }

Get-ChildItem -Path $src -Recurse -Filter *.java | ForEach-Object {
  Write-Host "Compilando $($_.FullName)"
  & javac -encoding UTF-8 -cp "$bin;$lib/*" -d $bin $_.FullName
  if ($LASTEXITCODE -ne 0) { throw "Compilación fallida" }
}

Write-Host "Compilación completada."
