"""Scan permitted hosts: Python sockets for localhost, Nmap for scanme.nmap.org."""

import argparse
from datetime import datetime, timezone
import ipaddress
import shutil
import socket
import subprocess
import sys
import time


LOCAL_HOSTS = {"localhost", "127.0.0.1"}
EXTERNAL_HOST = "scanme.nmap.org"
COMMON_PORTS = (21, 22, 80, 443)
LOCAL_DELAY = 0.15
EXTERNAL_DELAY_MS = 300


def valid_port(value: str) -> int:
    """Reject nonnumeric ports and ports outside the TCP port range."""
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("port must be a number from 1 to 65535") from error
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be from 1 to 65535")
    return port


def parse_ports(text: str) -> list[int]:
    """Turn a comma-separated list into unique, validated ports."""
    if not text or any(not item.strip() for item in text.split(",")):
        raise argparse.ArgumentTypeError("use comma-separated ports such as 21,22,80,443")
    return list(dict.fromkeys(valid_port(item.strip()) for item in text.split(",")))


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="localhost, 127.0.0.1, or scanme.nmap.org")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--ports", type=parse_ports, help="selected ports, e.g. 21,22,80,443")
    selection.add_argument("--start", type=valid_port, help="first port in an inclusive range")
    parser.add_argument("--end", type=valid_port, help="last port in an inclusive range; requires --start")
    parser.add_argument("--simulate-unreachable", action="store_true",
                        help="show an unreachable-host error without contacting any host")
    args = parser.parse_args()

    # Check the exact host text before DNS resolution; never accept another IP or domain.
    if args.host not in LOCAL_HOSTS | {EXTERNAL_HOST}:
        parser.error("host is not permitted; use 127.0.0.1, localhost, or scanme.nmap.org")
    if (args.start is None) != (args.end is None):
        parser.error("--start and --end must be supplied together")
    if args.start is not None:
        if args.start > args.end:
            parser.error("--start must be less than or equal to --end")
        ports = list(range(args.start, args.end + 1))
    else:
        ports = args.ports if args.ports is not None else list(COMMON_PORTS)
    limit = 10 if args.host == EXTERNAL_HOST else 100
    if len(ports) > limit:
        parser.error(f"choose at most {limit} ports for this host")
    args.selected_ports = ports
    return args


def scan_local(ports: list[int]) -> None:
    """Attempt one TCP connection per port and close every socket afterward."""
    counts = {"open": 0, "closed": 0, "timed out": 0, "error": 0}
    for index, port in enumerate(ports):
        try:
            # create_connection waits for the connection result on Windows too.
            # A context manager closes the socket immediately after checking.
            with socket.create_connection(("127.0.0.1", port), timeout=0.75):
                status = "open"
        except ConnectionRefusedError:
            status = "closed"  # The local machine refused the TCP connection.
        except socket.timeout:
            status = "timed out"  # A timeout does not prove a port is closed.
        except OSError as error:
            status = "error"
            print(f"Port {port}: {status} ({error})")
            counts[status] += 1
            continue
        print(f"Port {port}: {status}")
        counts[status] += 1
        if index < len(ports) - 1:
            time.sleep(LOCAL_DELAY)
    print("Summary: " + ", ".join(f"{name}={count}" for name, count in counts.items()))


def scan_external(ports: list[int]) -> None:
    """Use Nmap for its explicitly permitted testing target."""
    executable = shutil.which("nmap")
    if executable is None:
        raise RuntimeError("Nmap is required for scanme.nmap.org; run 'nmap --version' after installing it")

    # Resolve first and pin Nmap to the resulting public IPv4 address. This avoids
    # unexpectedly following DNS to a private or loopback address.
    try:
        addresses = socket.getaddrinfo(EXTERNAL_HOST, None, socket.AF_INET, socket.SOCK_STREAM)
    except socket.gaierror as error:
        raise RuntimeError(f"Host unreachable: could not resolve {EXTERNAL_HOST} ({error})") from error
    if not addresses:
        raise RuntimeError(f"Host unreachable: {EXTERNAL_HOST} has no IPv4 address")
    address = addresses[0][4][0]
    if not ipaddress.ip_address(address).is_global:
        raise RuntimeError("Host resolution did not return a public address; scan cancelled")
    print(f"Nmap testing target: {EXTERNAL_HOST} ({address})", flush=True)
    command = [executable, "-sT", "-Pn", "-n", "-p", ",".join(map(str, ports)),
               "--scan-delay", f"{EXTERNAL_DELAY_MS}ms", "--max-retries", "1",
               "--host-timeout", "45s", address]
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=55, check=False)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("Host unreachable or scan took too long") from error
    if result.returncode:
        raise RuntimeError(f"Nmap failed: {(result.stderr or result.stdout).strip()}")
    print(result.stdout.strip())


def main() -> int:
    args = arguments()
    print(f"Started (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}", flush=True)
    print(f"Target: {args.host} | Ports: {','.join(map(str, args.selected_ports))}", flush=True)
    start = time.perf_counter()
    try:
        if args.simulate_unreachable:
            # This documents the error path without probing an unauthorized host.
            raise RuntimeError("Host unreachable (simulated; no network connection attempted)")
        if args.host in LOCAL_HOSTS:
            scan_local(args.selected_ports)
        else:
            scan_external(args.selected_ports)
    except RuntimeError as error:
        print(f"Scan error: {error}", file=sys.stderr, flush=True)
        return 1
    finally:
        print(f"Elapsed: {time.perf_counter() - start:.2f} seconds", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
