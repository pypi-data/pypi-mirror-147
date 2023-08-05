choco install --no-progress beyondcompare
$CurrentValue = [Environment]::GetEnvironmentVariable("PATH", "User")
$prefix = @{$true='';$false=';'}[$CurrentValue -eq '']
$bcompare_dir = (Get-ChildItem -Recurse C:\Program*\Beyond*Compare* -Filter "bcompare.exe" | select-object -first 1).Directory.FullName
[Environment]::SetEnvironmentVariable("PATH", $CurrentValue + "${prefix}$bcompare_dir", "User")
$env:PATH = "$bcompare_dir;$env:PATH"
