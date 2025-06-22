$folderPath = "D:\"
Get-ChildItem -Path $folderPath -Recurse -Include *.opus, *.webm | ForEach-Object {
    $inputFile = $_.FullName
    $outputFile = [System.IO.Path]::ChangeExtension($inputFile, ".mp3")

    # Run ffmpeg to convert the file to mp3
    & ffmpeg -i $inputFile -q:a 2 $outputFile
}
