# DOS_blocker

A lightweight, rate-based DoS firewall built with Python and Scapy that monitors incoming network traffic and automatically blocks IPs exceeding a configurable packet-per-second threshold using iptables.

## How it works

- Sniffs incoming packets on a specified network interface
- Tracks packet rate per source IP over a 3-minute observation window
- Blocks IPs that exceed the threshold using iptables DROP rules
- Automatically unblocks IPs after 15 minutes
- Resets packet count every 8 minutes for IPs that stay within the threshold
- Supports a whitelist for trusted IPs that should never be blocked

## Requirements

- Python 3
- Scapy (`pip install scapy`)
- Root privileges
- Linux (iptables)

## Usage

```bash
sudo python3 DOS_blocker.py
```

You will be prompted to enter the network interface to monitor (e.g. `eth0`, `wlan0`, `vboxnet0`).

## Configuration

Edit the following variables directly in the script:

| ------Variable------ | ------------Default------------ | --------Description------- |
|----------------------|---------------------------------|----------------------------|
| `Max_packet_per_sec` |               100               |    Packet rate threshold   |
|      `whitelist`     | `{'172.16.78.1','172.16.78.3'}` | IPs that are never blocked |

## Disclaimer

This tool is intended for educational purposes and use in controlled lab environments only. Do not deploy against systems you do not own or have explicit permission to monitor.
