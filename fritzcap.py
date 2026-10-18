#!/usr/bin/env python3
"""Wireshark extcap for capturing packets from a FRITZ!Box on Windows."""
import hashlib
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

VERSION = "0.0.3"
DEFAULT_IFACE = "2-1"
USER_AGENT = "fritzcap-windows/0.0.3"


def emit_config():
    print(f"extcap {{version={VERSION}}}")
    print("interface {value=fritzcap}{display=FRITZ!Box remote capture}")


def emit_options():
    print("arg {number=0}{call=--ifname}{display=Interface Name}{type=selector}{tooltip=FRITZ!Box capture interface}")
    print("value {arg=0}{value=2-1}{display=Internet}{default=true}")
    print("value {arg=0}{value=3-}{display=Routing Interface}{default=false}")
    print("value {arg=0}{value=1-lan}{display=LAN}{default=false}")
    print("arg {number=1}{call=--host}{display=FRITZ!Box IP address}{type=string}{tooltip=FRITZ!Box IP address or hostname}{required=true}")
    print("arg {number=2}{call=--username}{display=FRITZ!Box user}{type=string}{tooltip=FRITZ!Box username}")
    print("arg {number=3}{call=--password}{display=FRITZ!Box password}{type=password}{tooltip=FRITZ!Box password}{required=true}")


def parse_args(argv):
    opts = {}
    flags = set()
    value_options = {"--extcap-interface", "--fifo", "--ifname", "--host", "--username", "--password"}
    flag_options = {"--extcap-interfaces", "--extcap-config", "--capture"}
    i = 0
    while i < len(argv):
        raw = argv[i]
        if raw == "--":
            break
        # Wireshark may pass extcap arguments as --name=value or as two tokens.
        if raw.startswith("--") and "=" in raw:
            arg, value = raw.split("=", 1)
            if arg in flag_options:
                if value:
                    print(f"Unexpected value for {arg}", file=sys.stderr)
                flags.add(arg)
            elif arg in value_options:
                opts[arg] = value
            else:
                print(f"Unknown option: {raw}", file=sys.stderr)
            i += 1
        elif raw in flag_options:
            flags.add(raw)
            i += 1
        elif raw in value_options:
            if i + 1 >= len(argv):
                raise ValueError(f"Missing value for {raw}")
            opts[raw] = argv[i + 1]
            i += 2
        else:
            print(f"Unknown option: {raw}", file=sys.stderr)
            i += 1
    return opts, flags


def request_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def get_sid(host, username, password):
    base = host.rstrip("/")
    if "://" not in base:
        base = "http://" + base
    # FRITZ!Box commonly uses HTTP for this local login endpoint. Respect an
    # explicitly supplied http:// or https:// scheme.
    challenge_xml = request_text(base + "/login_sid.lua")
    root = ET.fromstring(challenge_xml)
    challenge = root.findtext("Challenge")
    if not challenge:
        raise RuntimeError("FRITZ!Box did not return a login challenge.")

    response_hash = hashlib.md5(
        (challenge + "-" + password).encode("utf-16le")
    ).hexdigest()
    response_value = challenge + "-" + response_hash
    query = urllib.parse.urlencode({"username": username, "response": response_value})
    login_xml = request_text(base + "/login_sid.lua?" + query)
    login_root = ET.fromstring(login_xml)
    sid = login_root.findtext("SID")
    if not sid or sid == "0000000000000000":
        raise RuntimeError("Authentication failed. Check the FRITZ!Box username and password.")
    return base, sid


def capture(host, username, password, iface, fifo):
    base, sid = get_sid(host, username, password)
    query = urllib.parse.urlencode({
        "ifaceorminor": iface,
        "snaplen": "1600",
        "capture": "Start",
        "sid": sid,
    })
    url = base + "/cgi-bin/capture_notimeout?" + query
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    # Wireshark passes --fifo as a path. On Windows this is usually a named
    # pipe (\\.\pipe\...). Opening it for binary writing connects to Wireshark.
    with urllib.request.urlopen(req, timeout=30) as response:
        with open(fifo, "wb", buffering=0) as output:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                output.write(chunk)


def main():
    try:
        opts, flags = parse_args(sys.argv[1:])
        if "--extcap-interfaces" in flags:
            emit_config()
            return 0
        if "--extcap-config" in flags:
            emit_options()
            return 0
        if "--capture" not in flags:
            return 0

        host = opts.get("--host")
        password = opts.get("--password")
        if not host or password is None:
            raise ValueError("Capture requires --host and --password.")
        fifo = opts.get("--fifo")
        if not fifo:
            raise ValueError("Capture requires --fifo.")
        capture(
            host=host,
            username=opts.get("--username", ""),
            password=password,
            iface=opts.get("--ifname", DEFAULT_IFACE),
            fifo=fifo,
        )
        return 0
    except KeyboardInterrupt:
        return 0
    except (OSError, urllib.error.URLError, ET.ParseError, ValueError, RuntimeError) as exc:
        print(f"fritzcap: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
