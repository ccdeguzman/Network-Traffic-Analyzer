# Network Traffic Analyzer

## Developer
Christian de Guzman

## Purpose
The goal of this project is to strengthen my understanding of networking and cybersecurity by building a packet analyzer from the ground up. There are already existing tools out there but I wanted to learn how network traffic is captured, classified, and analyzes in real time using Python and Scapy.

---
## Project Structure
```
src/	
    └── netanal/
	 	├── capture.py
    	 ├── cli.py
 	 	├── __init__.py
 	 	├── display.py
    	 └── stats.py
.gitignore
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

## What I Learned
- Network packet capture using Scapy
- Object-Oriented programming in Python



