choco install --no-progress ytt

python -mvenv build\.venv
. build\.venv\Scripts\activate.ps1
pip install --use-feature=in-tree-build --disable-pip-version-check --quiet --quiet wheel --editable .[testing]
pip list
$wix_dir = (Get-ChildItem -Recurse C:\Program*\Wix*Toolset*\bin -Filter "heat.exe" | select-object -first 1).Directory.FullName
$env:PATH = "$wix_dir;$env:PATH"
