#Query validation script

#Allow script to run without verifying signature. Highly unrecommended. Might trip some alerts. Run as Admin.
Set-ExecutionPolicy Unrestricted

#Query1: Start
Write-Host "[+] Checking query #1..."
#Query1: Hardcode directory to search.
$targetFile1 = "C:\Users\" + $env:UserName + "\AppData\out\"
#Query1: Check if offending directory for scr.exe exists and output accordingly
If (Test-Path -Path $targetFile1){
    Write-Host "[+] File Exists. Machine is confirmed vulnerable. Investigate." -ForegroundColor red
} Else {
    Write-Host "[+] File Does Not Exist. Machine is safe from technique. Continuing..." -ForegroundColor green
}
#Query1: End
#Query2: Start
Write-Host "[+] Checking query #2..."
#Query2: Control flow with error handling. Registry key did not exist in the environment and this piece of code ensures the script fails gracefully no matter the result.


Try{
    if(Get-ItemPropertyValue -Path "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal" -Name "REG_DWORD 100" -ErrorAction Stop -eq True){
        Write-Host "[+] Registry key and value exists. Query and indicator confirmed. Investigate." -ForegroundColor red
    } 
}
Catch{
    Write-Host "[+] Registry key and value do not exist. Proceeding.." -ForegroundColor green
}
#Query2: End
#Query3: Start
Write-Host "[+] Checking query #3..."

#Query3: Check RDP port and populate variable as appropriate.
$port = netstat -na | Select-String ":3389"

#Query3: Check Firewall status and assign values as appropriate
$FWService = (Get-Service | ?{$_.Name -eq "mpssvc"});
$FWService | %{
    If($_.Status -eq "Running"){
        $FWstatus = "True"
        }Else{
        $FWstatus = "False"
        }
    };

#Query3: Find out if the RDP port is really closed and the status of the firewall service.
if ($port -eq $null -and $FWstatus -eq "True"){
    Write-Host "[+] Port 3389 TCP/UDP is closed."  -ForegroundColor green
    Write-Host "[+] Firewall service is enabled" -ForegroundColor green
} elseif ($FWstatus -eq "False"){
    Write-Host "[+] Firewall service is disabled" -ForegroundColor red
} elseif ($port -ne $null){
    Write-Host "[+] Port 3389 TCP/UDP is open" -ForegroundColor red
}
#Query3: End

#Terminate Script
Write-Host "[+] Testing Concluded."
