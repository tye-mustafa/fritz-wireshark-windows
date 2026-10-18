# FRITZ!Box Remote Capture for Wireshark on Windows

A Windows-oriented Python implementation of a Wireshark **Extcap** helper for streaming packet captures from a compatible AVM FRITZ!Box router into Wireshark.

> **Status: Experimental / not yet verified against a real FRITZ!Box.** The script's command-line and Extcap configuration output can be tested locally, but real router authentication and packet streaming still need to be tested on your FRITZ!OS model/version.

## What it does

- Exposes a `FRITZ!Box remote capture` interface to Wireshark.
- Requests a FRITZ!Box login challenge and calculates the login response.
- Requests a capture from the selected FRITZ!Box interface.
- Streams the returned capture data to the FIFO path provided by Wireshark.
- Uses Python's standard library; no third-party Python packages are required to run the `.py` file.

## Capture interfaces

The script offers these interface identifiers, inherited from the supplied Linux script:

| Display name | Interface identifier |
|---|---|
| Internet | `2-1` |
| Routing Interface | `3-` |
| LAN | `1-lan` |

The interface identifiers available to you can vary by FRITZ!Box model and FRITZ!OS version.

## Requirements

- Windows 10 or Windows 11
- Wireshark
- Python 3, if running the Python script directly
- A reachable FRITZ!Box and a FRITZ!Box account permitted to access the router
- A FRITZ!OS version/model that supports the capture endpoint used by this script

## Installation

### 1. Download this project

On GitHub, select **Code → Download ZIP**, then extract the ZIP file.

### 2. Find Wireshark's Personal Extcap folder

1. Open Wireshark.
2. Select **Help → About Wireshark → Folders**.
3. Find **Personal Extcap path**.
4. Open that folder in File Explorer.

If that entry is not present in your version, consult Wireshark's documentation for extcap installation locations.

### 3. Install the script

Copy `fritzcap.py` into the Personal Extcap folder.

Windows builds of Wireshark may not discover a `.py` or `.bat` script directly as an Extcap program. If the interface does not appear, use the executable method below.

### 4. Optional: package as a Windows executable

Install Python 3 first, then open Command Prompt or PowerShell in the project folder and run:

```powershell
py -3 -m pip install pyinstaller
py -3 -m PyInstaller --onefile --name fritzcap fritzcap.py
```

After the build completes, the executable should be at:

```text
dist\fritzcap.exe
```

Copy `fritzcap.exe` into Wireshark's **Personal Extcap path**, then restart Wireshark. Keep the `.py` source in your project/repository as well; the executable is a generated build artifact.

## Configure and start a capture

1. Restart Wireshark.
2. Open **Capture → Options**.
3. Look for **FRITZ!Box remote capture** in the interface list.
4. Open its configuration and enter:
   - **FRITZ!Box IP address**: commonly `fritz.box` or the router's LAN IP, depending on your network.
   - **Username**: your FRITZ!Box user name.
   - **Password**: your FRITZ!Box password.
   - **Interface Name**: select the interface you want to capture.
5. Start the capture and generate the traffic you want to inspect.

The FRITZ!Box capture is remote. This script does **not** itself decrypt WireGuard traffic on Windows. If you want to inspect traffic after the FRITZ!Box has processed/decrypted it, select a suitable FRITZ!Box capture interface and generate traffic through the VPN. The traffic visible depends on the router, interface, FRITZ!OS version, and capture point.

## Local checks

From the project folder, test that Python can run the script:

```powershell
py -3 .\fritzcap.py --extcap-interfaces
py -3 .\fritzcap.py --extcap-config
```

The first command should print the Extcap interface declaration. The second should print the configurable options.

These checks do **not** prove that login or a real capture will work; those require testing against a compatible FRITZ!Box.

## Troubleshooting

### The interface does not appear in Wireshark

- Confirm the file is in the exact **Personal Extcap path** shown by Wireshark.
- Restart Wireshark.
- If the `.py` file is not discovered, package it as `fritzcap.exe` using the steps above.
- Run the local checks to make sure the program starts.

### Authentication fails

- Verify the FRITZ!Box username and password.
- Check that the user account has the necessary router permissions.
- Confirm that the router's login page is reachable from the PC.

### The router cannot be reached

- Check the router hostname/IP address.
- Confirm the PC can reach the FRITZ!Box over the local network.
- Try the router's normal web interface in a browser.
- Your router settings, FRITZ!OS version, or network configuration may affect access.

### Capture starts but no useful packets appear

- Try another available capture interface.
- Generate traffic through the path you want to inspect.
- Remember that a router capture only sees packets visible at its chosen capture point.

## Security and privacy

- Use a FRITZ!Box account with only the permissions needed for the task.
- Do not commit passwords, session IDs, packet captures, or router configuration files to GitHub.
- Packet captures may contain private browsing, DNS, device, and other network information. Review them carefully before sharing.
- The login URL scheme and capture endpoint are inherited from the source approach. Use this only on a trusted network and understand the security implications of your router's configuration.

## Known limitations

- Real-world authentication and packet streaming have not yet been confirmed across FRITZ!Box models/FRITZ!OS versions.
- Windows Extcap discovery can differ by Wireshark version; packaging as an executable may be necessary.
- The script relies on the FRITZ!Box endpoint `/cgi-bin/capture_notimeout`, which may not be available on every model/version.
- Interface identifiers may vary.
- This project is not affiliated with or endorsed by AVM or the Wireshark project.

## Project files

- `fritzcap.py` — Python implementation.
- `fritzcap.bat` — optional command-line launcher.
- `README.md` — project documentation.

## Source and licensing note

This Windows implementation was prepared from a Linux Bash script supplied for conversion. The original script's author, source URL, and license were not included with the supplied file. Before publishing this repository publicly, identify the original source and check its license/permission requirements. Add appropriate attribution and a license only when you have confirmed you have the right to do so.

## Contributing

Bug reports and test results are welcome. When reporting a problem, include your Windows version, Wireshark version, FRITZ!OS version/model, and the exact error message. **Never include passwords, session IDs, public IPs, or unredacted packet captures in an issue.**
