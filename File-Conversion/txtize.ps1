# Specify the path to the directory
$directoryPath = "C:\Users\Srulik's User\OneDrive\Documents\SideQuester - Copy"

# Get all files in the directory and its subdirectories
Get-ChildItem -Path $directoryPath -File -Recurse | ForEach-Object {
    # Check if the file does not already end with .txt
    if ($_ -notmatch "\.txt$") {
        # Append .txt to the file name
        $newName = $_.FullName + ".txt"
        Rename-Item -Path $_.FullName -NewName $newName

        # Log the change to the console
        Write-Output "Renamed '$($_.FullName)' to '$newName'"
    }
}

Write-Output "File renaming completed."
