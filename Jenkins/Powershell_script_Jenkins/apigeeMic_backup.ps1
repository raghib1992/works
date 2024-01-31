param (
    [string]$VmName
    # ,[parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string]$BundlePattern = $(throw "-BundlePattern is required.")
    # ,[parameter(Mandatory=$false)][ValidateNotNullOrEmpty()][string]$CayanMainPath = '.deploy/cayan-main'
    # ,[parameter(Mandatory=$false)][string]$EnvJsonPath = $null
    ,[parameter(Mandatory=$false,ParameterSetName='VmHost')][string[]]$VmHost = ($env:AllowedVmHosts -split ',')
    ,[parameter(Mandatory=$false)][ValidateNotNullOrEmpty()][string]$QaDnsName
    ,[parameter(Mandatory=$false,ParameterSetName='QaMasterServer')][string[]]$QaMasterServer
    # ,[parameter(Mandatory=$false)][ValidateNotNullOrEmpty()][switch]$InfoLog = $false
    ,[parameter(Mandatory=$false)][ValidateNotNullOrEmpty()][string]$TempWorkspacePath = '.cb'
    ,[parameter(Mandatory=$false)][ValidateNotNullOrEmpty()][string]$RemoteTempWorkspacePath = 'C:\.cb'
    ,[parameter(Mandatory=$false)][ValidateNotNullOrEmpty()][switch]$InfoLog = $false
)

# Provision credential to connect to remote server
$provisionerCredential = New-Object pscredential($env:LocalUserName, $(ConvertTo-SecureString -String $env:LocalPassword -AsPlainText -Force))

# Get VM Ip
if (!$elapsedTime) {
  $elapsedTime = [System.Diagnostics.Stopwatch]::StartNew()
  "[00:00:00.0000000]: $($MyInvocation.MyCommand.Name) start" | Out-Host
}

if (!$PSScriptRoot) {
  $PSScriptRoot = (Get-Location)
  "[$($elapsedTime.Elapsed.ToString())]: No PSScriptRoot set. Attempting to set to path [$($PSScriptRoot)]" | Out-Host
}

$modulePath = "$($PSScriptRoot)\..\common"

if (!(Get-Module 'Artifactory')) { Import-Module "$($modulePath)\Artifactory.psm1"; "[$($elapsedTime.Elapsed.ToString())]: Artifactory.psm1 loaded!" | Out-Host }
if (!(Get-Module 'Vm')) { Import-Module "$($modulePath)\Vm.psm1"; "[$($elapsedTime.Elapsed.ToString())]: Vm.psm1 loaded!" | Out-Host }
if (!(Get-Module 'Utility')) { Import-Module "$($modulePath)\Utility.psm1"; "[$($elapsedTime.Elapsed.ToString())]: Utility.psm1 loaded!" | Out-Host }
if (!(Get-Module 'IO')) { Import-Module "$($modulePath)\IO.psm1"; "[$($elapsedTime.Elapsed.ToString())]: IO.psm1 loaded!" | Out-Host }


"Retrieving VM Info for VM [$($VmName)] on [$(if ($VmCluster) { 'cluster' } else { 'host' })] [$(if ($VmCluster) { $VmCluster } else { $VmHost })]" | Out-Host

$vmInfoArgs = @{
  Name = $VmName
  Computer = $VmHost
  InfoLog = $true
}

$vmInfo = Get-VmInfo @vmInfoArgs
$fqdn = $vmInfo.Computer.VmNetworkAdapters[0].Fqdn

Write-Host "IP is: $($fqdn)"

$session = New-PSSession -ComputerName $fqdn -Credential $provisionerCredential

# "[$($elapsedTime.Elapsed.ToString())]: Downloading cayan main [$($BundlePattern)] to destination [$($CayanMainPath)]" | Out-Host
# try {
#   Invoke-DownloadArtifact `
#   -BuildPattern $BundlePattern `
#   -Destination $CayanMainPath `
#   -EnvJsonPath $EnvJsonPath `
#   -InfoLog:$InfoLog
# } catch {
#   "[$($elapsedTime.Elapsed.ToString())]: ERROR: Downloading cayan main bundle failed" | Out-Host
#   $_ | Out-Host
#   Exit 1 
# }

# Pointing at the MiC QA environment
$MicQaEnv = {
    Push-Location C:\inetpub\mw.genius\1.0
    C:\Windows\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe -pdf "appSettings" .

    $xmlFilePath = "C:\inetpub\mw.genius\1.0\web.config"

    [xml]$xmlData = Get-Content -Path $xmlFilePath

    $AppData = $xmlData.configuration.appSettings.add

    foreach($url in $AppData)
    {
        if($url.key -like "mic_service_url"){
            if($url.value -like "https://wss.qa.paygateway.com/mic"){
                Write-Host "No need to update url"
            }
            else{
                Write-Host "mic_service_url need to update"
                $url.value = "https://wss.qa.paygateway.com/mic"
                $xmlData.save($xmlFilePath)
            }
        }
    }

    iisreset
}

"[$($elapsedTime.Elapsed.ToString())]: The config on the DTE needs updated to correct pointing at the MiC QA" | Out-Host
try {
  Invoke-CommandErrorChecking `
  -ScriptBlock $MicQaEnv `
  -Session $session `
  -InfoLog:$InfoLog
} catch {
  Remove-PSSession $session
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: The config on the DTE needs updated to correct pointing at the MiC QA failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}


# Adding a Stub Zone for qa.paygateway.com

$AddStubZone = {
  Add-DnsServerStubZone -Name $args[0] -MasterServers $args[1] -PassThru -ZoneFile $args[2]
}  

"[$($elapsedTime.Elapsed.ToString())]: Adding a Stub Zone for qa.paygateway.com" | Out-Host
try {
  Invoke-CommandErrorChecking `
  -ScriptBlock $AddStubZone `
  -Session $session `
  -Paramaters @($QaDnsName,$QaMasterServer,"($QaDnsName).dns") `
  -InfoLog:$InfoLog
} catch {
  Remove-PSSession $session
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Adding a Stub Zone for qa.paygateway.com failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}




$shareRemoteTempWorkspacePath = $RemoteTempWorkspacePath -replace '\:', '$'
#Create temp folder, locally and remotely
"[$($elapsedTime.Elapsed.ToString())]: Creating local temporary workspace folder [$($TempWorkspacePath)]" | Out-Host
try {
  New-Item `
  -Path $TempWorkspacePath `
  -ItemType Directory `
  -ErrorAction:Stop | `
  Out-Null
} catch {
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Creating local temporary workspace folder failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

"[$($elapsedTime.Elapsed.ToString())]: Creating temporary workspace [$($RemoteTempWorkspacePath)] on remote computer [$($fqdn)]" | Out-Host
try {
  New-ItemRemote `
  -Path "\\$($fqdn)\$($shareRemoteTempWorkspacePath)" `
  -ItemType Directory `
  -Credential $provisionerCredential `
  -Force `
  -InfoLog:$InfoLog
} catch {
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Creating remote temporary workspace failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

#Download required files to be copied
# $version = '3.9.2.2698'
[System.IO.FileInfo]$IISCrypto = "$($TempWorkspacePath)\Update_apiigee_cipher.ictpl"

"[$($elapsedTime.Elapsed.ToString())]: Downloading Web Deploy installer to local path [$($IISCrypto.FullName)]" | Out-Host
try {
  Invoke-DownloadArtifact `
  -BuildPattern "URL:common/IISCryptoTemplates/$($IISCrypto.Name)" `
  -Destination $IISCrypto `
  -InfoLog:$InfoLog
} catch {
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Downloading Web Deploy installer locally failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

[System.IO.FileInfo]$IISCryptoCli = "$($TempWorkspacePath)\IISCryptoCli.exe"

"[$($elapsedTime.Elapsed.ToString())]: Downloading Web Deploy installer to local path [$($IISCryptoCli.FullName)]" | Out-Host
try {
  Invoke-DownloadArtifact `
  -BuildPattern "URL:common/IISCryptoCLi/$($IISCryptoCli.Name)" `
  -Destination $IISCryptoCli `
  -InfoLog:$InfoLog
} catch {
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Downloading Web Deploy installer locally failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

#Copy files to remote computer
"[$($elapsedTime.Elapsed.ToString())]: Copying items in workspace [$($TempWorkspacePath)] to temp directory [$($RemoteTempWorkspacePath)] on remote computer [$($fqdn)]" | Out-Host
$pathsToCopy = $null
try {
  $pathsToCopy = Get-ChildItem `
  -Path $TempWorkspacePath `
  -ErrorAction Stop | `
  ForEach-Object { $_.FullName }
} catch {
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Iterating through paths to copy in workspace failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

try {
  Copy-ItemRemote `
  -Path $pathsToCopy `
  -Destination "\\$($fqdn)\$($shareRemoteTempWorkspacePath)" `
  -ToCredential $provisionerCredential `
  -Force `
  -Recurse `
  -InfoLog:$InfoLog
} catch {
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Copying workspace to temp directory failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

# Ciphers

$Ciphers = {
  # Enable-TlsCipherSuite -Name TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 -Position 0
  # Enable-TlsCipherSuite -Name TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 -Position 1
  cd C:\.cb
  ./iiscryptocli /template ".\Update_apiigee_cipher.ictpl"
}

"[$($elapsedTime.Elapsed.ToString())]: Fixing Ciphers issues" | Out-Host
try {
  Invoke-CommandErrorChecking `
  -ScriptBlock $Ciphers `
  -Session $session `
  -InfoLog:$InfoLog
} catch {
  Remove-PSSession $session
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Fixing Ciphers Issue failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

#  Create C:\IISCryptofolder on remote computer
# $createCayanDirBlock = {
#   New-Item -Path 'C:\IISCrypto' -ItemType Directory -ErrorAction:Stop | Out-Null
# }

# "[$($elapsedTime.Elapsed.ToString())]: Creating C:\Cayan directory on remote computer [$($fqdn)]" | Out-Host
# try {
#   Invoke-CommandErrorChecking `
#   -ScriptBlock $createCayanDirBlock `
#   -Session $session `
#   -InfoLog:$InfoLog
# } catch {
#   Remove-PSSession $session
#   "[$($elapsedTime.Elapsed.ToString())]: ERROR: Creating C:\Cayan directory failed:" | Out-Host
#   $_ | Out-Host
# }

# Copy cipher template to remote server
# Copy-Item ".\rel-eng\deploy_scripts\cayan-main\IISCryptoCli.exe" -Destination "C:\IISCrypto\" -ToSession $Session
# Copy-Item ".\rel-eng\deploy_scripts\cayan-main\Update_apiigee_cipher.ictpl" -Destination "C:\IISCrypto\" -ToSession $Session




# $DownloadIISCryptoTemplate = {
#   Invoke-WebRequest -Uri https://artifactory.dev.paygateway.com/artifactory/common/IISCryptoCLi/IISCryptoCli.exe -OutFile C:\IIScrypto\IISCryptoCli.exe -Headers @{ Authorization = "Basic "+ [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("sstanley:Sstanley@123#")) }
# }









#Copy files to remote computer
# "[$($elapsedTime.Elapsed.ToString())]: Copying items in workspace [$($TempWorkspacePath)] to temp directory [$($RemoteTempWorkspacePath)] on remote computer [$($fqdn)]" | Out-Host
# $pathsToCopy = $null
# try {
#   $pathsToCopy = Get-ChildItem `
#   -Path $TempWorkspacePath `
#   -ErrorAction Stop | `
#   ForEach-Object { $_.FullName }
# } catch {
#   "[$($elapsedTime.Elapsed.ToString())]: ERROR: Iterating through paths to copy in workspace failed:" | Out-Host
#   $_ | Out-Host
#   Exit 1
# }

# try {
#   Copy-ItemRemote `
#   -Path $pathsToCopy `
#   -Destination "\\$($fqdn)\$($shareRemoteTempWorkspacePath)" `
#   -ToCredential $provisionerCredential `
#   -Force `
#   -Recurse `
#   -InfoLog:$InfoLog
# } catch {
#   "[$($elapsedTime.Elapsed.ToString())]: ERROR: Copying workspace to temp directory failed:" | Out-Host
#   $_ | Out-Host
#   Exit 1
# }





#Delete local temp folder
"[$($elapsedTime.Elapsed.ToString())]: Removing local temporary workspace folder [$($TempWorkspacePath)]" | Out-Host
try {
  Remove-Item `
  -Path $TempWorkspacePath `
  -Force `
  -Recurse `
  -ErrorAction:Stop | `
  Out-Null
} catch {
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Removing local temporary workspace failed:" | Out-Host
  $_ | Out-Host
  Exit 1
}

$scriptBlock =
{
  $carbonBlackInstallArgs = @('/i',"$($args[0])\$($args[1])", 'ALLUSERS=1', '/qn', '/norestart', '/log output.log', 'COMPANY_CODE=F4I2GC5LWU1WXKV9U0P', 'AUTO_CONFIG_MEM_DUMP=0', 'GROUP_NAME="GPI - GW Prod Servers - Standard"')
  Start-Process -FilePath "C:\Windows\System32\msiexec.exe" -ArgumentList $carbonBlackInstallArgs -Wait -ErrorAction:Stop | Out-Null
  Remove-Item -Path "$($args[0])\$($args[1])" -Force -Recurse -ErrorAction:Stop | Out-Null
}

$session = New-PSSession -ComputerName $fqdn -Credential $provisionerCredential 

"[$($elapsedTime.Elapsed.ToString())]: Installing and restarting Carbon Black Protection Agent on remote computer [$($fqdn)]" | Out-Host
try {
  Invoke-CommandErrorChecking `
  -ScriptBlock $scriptBlock `
  -Session $session `
  -Paramaters @($RemoteTempWorkspacePath, $CarbonBlackFile.Name) `
  -InfoLog:$InfoLog
} catch {
  Remove-PSSession $session
  "[$($elapsedTime.Elapsed.ToString())]: ERROR: Failed to install Carbon Black Protection Agent: " | Out-Host
  $_ | Out-Host
  Exit 1
}

"Carbon Black Protection Agent installed successfully" | Out-Host