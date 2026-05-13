$ErrorActionPreference = "Continue"

$base = Join-Path $env:APPDATA "io.github.clash-verge-rev.clash-verge-rev"

Write-Host "== Clash Verge config dir =="
Write-Host $base
if (-not (Test-Path $base)) {
  Write-Host "not found"
  exit 1
}

Write-Host "`n== Current profile =="
$profilesYaml = Join-Path $base "profiles.yaml"
if (Test-Path $profilesYaml) {
  Get-Content $profilesYaml -TotalCount 250 | Select-String -Pattern "current:|rules:|merge:" -Context 0,2
} else {
  Write-Host "profiles.yaml not found"
}

Write-Host "`n== DNS config markers =="
$dnsConfig = Join-Path $base "dns_config.yaml"
if (Test-Path $dnsConfig) {
  Get-Content $dnsConfig -TotalCount 180 | Select-String -Pattern "respect-rules|fake-ip-filter|zphz|direct-nameserver|nameserver-policy"
} else {
  Write-Host "dns_config.yaml not found"
}

Write-Host "`n== Company DNS lookup =="
nslookup jumpserver.zphz.cn

Write-Host "`n== Proxy/VPN processes =="
Get-Process | Where-Object {
  $_.ProcessName -match "clash|verge|mihomo|corplink|feilian|ssh"
} | Select-Object Id, ProcessName, Path

Write-Host "`n== Route hints =="
route print | Select-String -Pattern "10\.12\.|198\.18\.|0\.0\.0\.0"

Write-Host "`n== SSH verbose probe hint =="
Write-Host "Run manually when needed: ssh -vvv zhipu30"
