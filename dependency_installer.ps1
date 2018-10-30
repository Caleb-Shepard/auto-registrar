<# ‍*********************************************************************** #>
<# ‍                                                                        #>
<# ‍                                                        |\              #>
<# ‍    dependency_installer.ps1                      ------| \----         #>
<# ‍                                                  |    \`  \  |  p      #>
<# ‍    By: mihirlad55                                |  \`-\   \ |  o      #>
<# ‍                                                  |---\  \   `|  l      #>
<# ‍    Created: 2018/10/29 18:27:17 by mihirlad55    | ` .\  \   |  y      #>
<# ‍    Updated: 2018/10/29 19:59:11 by mihirlad55    -------------         #>
<# ‍                                                                        #>
<# ‍*********************************************************************** #>

"If you haven't already, you should install Google Chrome"
Read-Host -Prompt "Press Enter to continue"



"Selenium will be installed"
Read-Host -Prompt "Press Enter to continue"

# Install Selenium
"Installing Selenium..."
pip3 install selenium


"Chromedriver will be downloaded"
Read-Host -Prompt "Press Enter to continue"

# Download chromedriver v2.43
"Downloading chromedriver v2.43..."
$wc = New-Object System.Net.WebClient
$wc.DownloadFile("https://chromedriver.storage.googleapis.com/2.43/chromedriver_win32.zip", "chromedriver.zip")

# If chromedriver.exe doesn't exist extract chromedriver.zip
"Unzipping chromedriver.zip..."
if (![System.IO.File]::Exists("chromedriver.exe")) {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory("chromedriver.zip", $PSScriptRoot)
}

# If chromedriver.zip exists, delete it
"Deleting chromedriver.zip..."
if ([System.IO.File]::Exists("chromedriver.zip")) {
    Remove-Item -path "chromedriver.zip"
}


"Done!"