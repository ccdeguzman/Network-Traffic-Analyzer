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

def protocol_table(stats: TrafficStats) -> Table:
	table = Table(title="Protocol Distribution", expand=True)
	table.add_column("Protocol")
	table.add_column("Packets", justify="right")
	table.add_column("Percent", justify="right")

	for proto, count, pct in stats.protocol_distribution():
		color = PROTO_COLORS.get(proto, "white")
		table.add_row(f"[{color}]{proto}[/{color}]", str(count), f"{pct:.1f}%")

	return table

def talkers_table(stats: TrafficStats, top_n: int) -> Table:
	table = Table(title=f"Top {top_n} Talkers", expand=True)
	table.add_column("IP")
	table.add_column("Sent", justify="right")
	table.add_column("Recv", justify="right")
	table.add_column("Total", justify="right")

	for ip, ep in stats.top_talkers(top_n):
		table.add_row(
			ip,
			_human_bytes(ep.bytes_sent),
			_human_bytes(ep.bytes_recv),
			_human_bytes(ep.total_bytes),
		)
	return table

def summary_panel(stats: TrafficStats) -> Panel:
	elapsed = stats.elapsed()
	text = Text()
	text.append(f"Packets: {stats.total_packets}  ", style="bold")
	text.append(f"Bytes: {_human_bytes(stats.total_bytes)}  ")
	text.append(f"Elapsed: {elapsed:.1f}s  ")
	text.append(f"Bandwidth: {_human_bytes(stats.bandwidth_bps())}/s")
	return Panel(text, title="Capture Summary")

def render(stats: TrafficStats, top_n: int) -> Group:
	return Group(summary_panel(stats), protocol_table(stats), talkers_table(stats, top_n))

def packet_line(info: PacketInfo) -> None:
	"""
	Print one line for a single packet
	"""
	color = PROTO_COLORS.get(info.protocol, "white")
	src = info.src or "-"
	dst = info.dst or "-"
	ports = f":{info.sport} -> :{info.dport}" if info.sport and info.dport else ""
	console.print(
		f"[{color}]{info.protocol:<9}[/{color}] {src} {ports} -> {dst} "
		f"({info.size} bytes)"
	)

class LiveDashboard:
	"""
		COntext manager wrapping a Rich Live view that refreshes on demand
	"""
	def __init__(self, stats: TrafficStats, top_n: int = 10, refresh_per_second: int = 4):
		self.stats = stats
		self.top_n = top_n
		self._live = Live(render(stats, top_n), console=console, refresh_per_second=refresh_per_second)

	def __enter__(self) -> "LiveDashboard":
		self._live.__enter__()
		return self

	def __exit__(self, *exc) -> None:
		self._live.__exit__(*exc)

	def refresh(self) -> None:
		self._live.update(render(self.stats, self.top_n))
