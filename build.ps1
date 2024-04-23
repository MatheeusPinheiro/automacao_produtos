$exclude = @("venv", "automacao_produtos.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "automacao_produtos.zip" -Force