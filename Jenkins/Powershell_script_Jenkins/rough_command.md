https://rootsecdev.medium.com/configuring-secure-cipher-suites-in-windows-server-2019-iis-7d1ff1ffe5ea
https://stackoverflow.com/questions/72353470/windows-server-2016-cipher-suites-not-working


REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v2.0.50727" /v "SchUseStrongCrypto" /t REG_DWORD /d 1 /f
REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v2.0.50727" /v "SystemDefaultTlsVersions" /t REG_DWORD /d 1 /f

REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319" /v "SchUseStrongCrypto" /t REG_DWORD /d 1 /f
REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319" /v "SystemDefaultTlsVersions" /t REG_DWORD /d 1 /f

REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework\v2.0.50727" /v "SchUseStrongCrypto" /t REG_DWORD /d 1 /f
REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework\v2.0.50727" /v "SystemDefaultTlsVersions" /t REG_DWORD /d 1 /f

REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework\v4.0.30319" /v "SchUseStrongCrypto" /t REG_DWORD /d 1 /f
REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework\v4.0.30319" /v "SystemDefaultTlsVersions" /t REG_DWORD /d 1 /f

[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12 -bor [System.Net.SecurityProtocolType]::Tls13

[System.Net.ServicePointManager]::SecurityProtocol
Get-ItemPropertyValue -Path HKLM:\SYSTEM\CurrentControlSet\Control\Cryptography\Configuration\Local\SSL\00010002 -Name Functions

Get-TlsCipherSuite -Name TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
Get-TlsCipherSuite

Disable-TlsCipherSuite -Name TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384

Get-TlsCipherSuite -Name TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
 
Enable-TlsCipherSuite -Name TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 -Position 0
Enable-TlsCipherSuite -Name TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 -Position 1

Get-ChildItem 'HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP' -Recurse | Get-ItemProperty -Name Version, Release -ErrorAction 0 | where { $_.PSChildName -match '^(?!S)\p{L}'} | select Version, Release, PSChildName

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Add-DnsServerPrimaryZone -Name "cayan1.com" -ZoneFile "cayan1.com.dns"


$letterArray = 'a','b','c','d'
foreach ($letter in $letterArray)
{
  Write-Host $letter
}

param (
  [parameter(Mandatory=$false,ParameterSetName='DnsList')][string[]]$DnsList = ('cayan.com,merchantware.net,paygateway.com' -split ',')
)



$UpdateDns = {
    $CheckDns = Get-DnsServerZone -Name $Dns
    
    if ($CheckDns){
        Write-Host "No Need to Update $(Dns)"
    }else{
        Add-DnsServerPrimaryZone -Name $args[0] -ZoneFile "$args[0].dns" 
    }

}


foreach ($Dns in $DnsList)
{
    "[$($elapsedTime.Elapsed.ToString())]: Move DTE App DNS setupA" | Out-Host
    try {
      Invoke-CommandErrorChecking `
      -ScriptBlock $UpdateDns `
      - Parameters @($Dns) `
      -InfoLog:$InfoLog
    } catch {
      "[$($elapsedTime.Elapsed.ToString())]: ERROR: Move DTE App DNS setup failed:" | Out-Host
      $_ | Out-Host
      Exit 1
}
    

}

\\ln-jwinbuild07.dev.paygateway.com\C$\