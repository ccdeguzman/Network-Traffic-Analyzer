# Network Traffic Analyzer
- Live packet capture on any interface, with an optional packet count limit
- Real-time protocol distribution (TCP/ UDP / ICMP / ARP / other) with percent breakdowns
- Top talkers ranking by bytes sent/received per IP endpoint
- Running bandwidth calculation (bytes/sec)
- Verbose mode prints each packet's protocol, endpoints, ports, and size as it's captured

## Developer
Christian de Guzman

## Purpose
The goal of this project is to strengthen my understanding of networking and cybersecurity by building a packet analyzer from the ground up. There are already existing tools out there but I wanted to learn how network traffic is captured, classified, and analyzes in real time using Python and Scapy.

---
## Project Structure
```
src/	
    └── netanal/
	 	├── capture.py		# scapy sniff wrapper and packet classification
    	├── cli.py			# click CLI entry point
 	 	├── __init__.py
 	 	├── display.py		# Rich dashboard and verbose packet log
    	└── stats.py			# protocol distribution, top talkers, bandwidth
.gitignore
pyproject.toml
README.md
```
---

## Set up
```
git clone https://github.com/ccdeguzman/Network-Traffic-Analyzer
cd Network-Traffic-Analyzer

python -m venv venv
venv\Scripts\activate        # Windows
    OR
source venv/bin/activate     # Mac/Linux

sudo apt update && sudo apt install -y libpcap-dev
pip install scapy click rich
```
---
## How To Use

```
sudo venv/bin/netanal capture -i <interface> [OPTIONS]
```

| Option | Description |
|---|---|
| `-i, --interface` | Network interface to capture on (required), e.g. `eth0`. |
| `-c, --count` | Number of packets to capture. `0` (default) runs until Ctrl+C. |
| `-f, --filter` | BPF filter expression, e.g. `"tcp port 443"` or `"host 10.0.0.5"`. |
| `-v, --verbose` | Print each packet's flow instead of the live dashboard. |
| `--top` | Number of top talkers to display (default 10). |

## Examples:
```
# Live dashboard, unlimited capture
sudo venv/bin/netanal capture -i eth0

# Capture exactly 50 packets, filtered to DNS traffic
sudo venv/bin/netanal capture -i eth0 -c 50 -f "udp port 53"

# Verbose per-packet log
sudo venv/bin/netanal capture -i eth0 -v
```
Press `Ctrl+C` at any time to stop and a final summary will show
---

## How It Works
1. **`capture.py`** — wraps `scapy.sniff()`. Each packet is classified by protocol (ARP / TCP / UDP / ICMP / other-IP) and reduced to source/destination IP, ports, and size.
2. **`stats.py`** — a `TrafficStats` object accumulates protocol counts and per-endpoint byte/packet totals as packets arrive, and derives bandwidth and top-talker rankings on demand.
3. **`display.py`** — renders a live-refreshing Rich dashboard, or streams a one-line-per-packet log in verbose mode.
4. **`cli.py`** — a Click command (`netanal capture`) wires interface/filter/count options to the capture loop.


## What I Learned
- Network packet capture using Scapy
- Object-Oriented programming in Python



