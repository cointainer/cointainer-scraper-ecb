$LANGUAGE = "en"
$URL = "https://www.ecb.europa.eu/euro/coins/comm/html/comm_{0}.{1}.html"

# Only needed once to calculate the hash values for each downloaded file:
# > Get-ChildItem -Filter "*.html" | foreach { Set-Content -Value ( Get-FileHash -Algorithm SHA256 $_ ).Hash "$($_.BaseName).sha256" }
# These values are distributed inside the *.sha256 files inside the repository.

for ($i = 2004 ; $i -le 2022 ; $i++) {
    $formattedUrl = ( $URL -f "$i", "$LANGUAGE" )
    $fileName = $formattedUrl.Split("/")[-1]
    Invoke-WebRequest $formattedUrl -OutFile $fileName

    # $hashFileName = $fileName.Replace(".html", ".sha256")
    # $downloadedFileHash = (Get-FileHash -Algorithm SHA256 $fileName).Hash

    # if (Test-Path $hashFileName) {
    #     $fileHash = Get-Content $hashFileName
    # } else {
    #     Set-Content -Value (Get-FileHash -Algorithm SHA256 $fileName).Hash $hashFileName
    #     Write-Information "Created new hash file '$hashFilename' for '$fileName'."
    #     continue
    # }


    # if ($downloadedFileHash -ne $fileHash) {
    #     Write-Warning "$fileName does not match with needed sha256 hash!"
    # }
}