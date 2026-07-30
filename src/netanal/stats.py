"""
Traffic statistics: protocol distribution, top talkers, bandwidth
"""
from __future__ import annotations

import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field

@dataclass				# auto generates __init__, __repr__, __eq__
class EndpointStats:
	"""
	Bytes and packets sent/received for a single IP endpoint
	"""
	bytes_sent: int = 0
	bytes_recv: int = 0
	packets_sent: int =0
	packets_recv: int = 0

	@property
	def total_bytes(self) -> int:
		return self.bytes_sent + self.bytes_recv

@dataclass
class TrafficStats:
	"""
	Stores everything about the network capture
	"""

	protocol_counts: Counter = field(default_factory=Counter)
	endpoints: dict[str, EndpointStats] = field(default_factory=lambda: defaultdict(EndpointStats))
	total_packets: int = 0
	total_bytes: int = 0
	start_time: float = field(default_factory=time.time)

	def record(self, protocol: str, src_ip: str | None, dst_ip: str | None, size: int) -> None:
		"""
		Record's one packet's protocol, endpoints, and size. Every time a packet is capture, the function updates everything
		"""
		self.protocol_counts[protocol] += 1
		self.total_packets += 1
		self.total_bytes += size

		if src_ip:
			ep = self.endpoints[src_ip]
			ep.bytes_sent += size
			ep.packets_sent += 1
		if dst_ip:
			ep = self.endpoints[dst_ip]
			ep.bytes_recv += size
			ep.packets_recv += 1

	def elapsed(self) -> float:
		"""
		How long has the packet capture been running
		"""
		return max(time.time() - self.start_time, 1e-6)

	def bandwidth_bps(self) -> float:
		"""
		The average bandwidth. How many bytes are transferred every second
		"""
		return self.total_bytes / self.elapsed()

	def protocol_distribution(self) -> list[tuple[str, int, float]]:
		"""
		What percentage of traffic is TCP, UDP, ICMP, etc. sorted by count descending
		"""
		if self.total_packets == 0:
			return []
		return [
			(proto, count, 100 * count / self.total_packets)
			for proto, count in self.protocol_counts.most_common()
		]

	def top_talkers(self, n: int = 10) -> list[tuple[str, EndpointStats]]:
		"""
		Top N endpoints sorted by total bytes transferred
		"""
		return sorted(
			self.endpoints.items(),
			key=lambda kv: kv[1].total_bytes,
			reverse=True,
		)[:n]
