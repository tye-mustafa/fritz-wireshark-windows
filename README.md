#This is personal experiment

Wireguard can now capture directly from Firtz capture tool 

FRITZ!Box remote capture extcap for Windows
===========================================

Files
-----
- fritzcap.py: Windows-compatible Wireshark extcap implementation (Python 3).
- fritzcap.bat: launcher for testing/manual invocation.

Requirements
------------
- Windows 10/11
- Wireshark installed
- Python 3 installed and available through the Windows `py -3` launcher
- FRITZ!Box reachable from this PC, with a FRITZ!Box user account allowed to access it

Install
-------
1. Extract this folder somewhere permanent, for example:
   C:\Wireshark\extcap\fritzcap\
2. In Wireshark, open Help > About Wireshark > Folders and find the
   Personal Extcap path. Copy fritzcap.py and fritzcap.bat into that folder.
   If your Wireshark version does not discover .bat launchers as extcap
   programs, use the executable packaging option below.
3. Restart Wireshark. Look for “FRITZ!Box remote capture”.

List of all Available interfaces here
https://github.com/jpluimers/fritzcap/blob/master/fritzcap-interfaces-table.md

credits goes to the user @Rob--W
