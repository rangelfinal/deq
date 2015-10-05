$text = ( Get-Content data.txt | Out-String ).Trim()
$text | where {$_ -match "\t.*\t.*\t(.*)\t.*\t.*$"} | %{ $Matches[1]}