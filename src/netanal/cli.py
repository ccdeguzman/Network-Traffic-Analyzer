"""
Command-line entry point: 'netanal capture -i <interface>'
"""
from __future__ import annotations
import os
import sys
import click
from .capture import Capture
from .display import LiveDashboard, console, packet_line, render
from .stats import TrafficStats


@click.group()
@click.version_option(package_name="netanal")
def main() -> None:
	"""netanal - live network traffic  capture and analysis"""

@main.command()
@click.option("-i", "--interface", required=True, help="Network interface to capture on (e.g. eth0).")
@click.option("-c", "--count", default=0, show_default=True, help="Number of packets to capture. 0 = until Ctrl+C.")
@click.option("-f", "--filter", "bpf_filter", default=None,  help="BPF filter expression (e.g. 'tcp port 443').")
@click.option("-v", "--verbose", is_flag=True,  help="Print each packet's flow instead of the live dashboard")
@click.option("--top", default=10, show_default=True, help="Number of top talkers to display.")
def capture(interface: str, count: int, bpf_filter:str | None, verbose: bool, top: int) -> None:
	"""
	Capture live traffic and report protocol distribution, top talkers, and bandwidth
	"""
	if os.name == "posix" and hasattr(os, "geteuid") and os.geteuid() != 0:
		console.print(
			"[yellow]Warning:[/yellow] packet capture usually requires root "
			"or CAP_NET_RAW. Try running with sudo if capture fails.\n"
		)
	stats = TrafficStats()

	try:
		if verbose:
			console.print(f"[bold]Capturing on {interface}[/bold] "
				      f"(filter: {bpf_filter or 'none'}, count: {count or 'unlimited'})\n")
			cap = Capture(interface, stats, count=count, bpf_filter=bpf_filter, on_packet=packet_line)
			cap.run()
		else:
			with LiveDashboard(stats, top_n=top) as dash:
				def _refresh(_info):
					dash.refresh()

				cap = Capture(interface, stats, count=count, bpf_filter=bpf_filter, on_packet=_refresh)
				cap.run()
	except KeyboardInterrupt:
		pass
	except PermissionError:
		console.print("[red]Permission denied.[/red] Run with sudo or grant CAP_NET_RAW.")
		sys.exit(1)
	except OSError as exc:
		console.print(f"[red]Capture failed:[/red] {exc}")
		sys.exit(1)

	console.print("\n[bold]Final Summary[/bold]")
	console.print(render(stats, top))

if __name__ == "__main__":
	main()
