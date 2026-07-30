"""
Rich-based terminal rendering: live stats dashboard and verbose packet log
"""
from __future__ import annotations
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from .capture import PacketInfo
from .stats import TrafficStats

console = Console()

PROTO_COLORS = {
	"TCP": "cyan",
	"UDP": "magenta",
	"ICMP": "yellow",
	"ARP": "green",
	"Other IP": "white",
	"Other": "grey50"
}

def _human_bytes(n: float) -> str:
	for unit in ("B", "KB", "MB", "GB"):
		if n < 1024:
			return f"{n:.1f} {unit}"
		n /= 1024
	return f"{n:.1f} TB"
