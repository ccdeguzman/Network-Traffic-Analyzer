"""
Live packet capture and per-packet classification via Scapy
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional
from scapy.all import ARP, ICMP, IP, TCP, UDP, Packet, sniff
from .stats import TrafficStats

@dataclass
class PacketInfo:
	"""
	Only keeping the needed information for display display/logging
	"""
	protocol: str
	src: Optional[str]
	dst: Optional[str]
	sport: Optional[int]
	dport: Optional[int]
	size: int

def  classify(packet: Packet) -> PacketInfo:
	"""
	Identify protocol and endpoints for one packet
	"""
	size = len(packet)
	
	if packet.haslayer(ARP):
		arp = packet[ARP]
		return PacketInfo("ARP", arp.psrc, arp.pdst, None, None, size)

	if packet.haslayer(IP):
		ip = packet[IP]
		src, dst = ip.src, ip.dst

		if packet.haslayer(TCP):
			tcp = packet[TCP]
			return PacketInfo("TCP", src, dst, tcp.sport, tcp.dport, size)
		if packet.haslayer(UDP):
			udp = packet[UDP]
			return PacketInfo("UDP", src, dst, udp.sport, udp.dport, size)
		if packet.haslayer(ICMP):
			return PacketInfo("ICMP", src, dst, None, None, size)
		return PacketInfo("Other IP", src, dst, None, None, size)

	return PacketInfo("Other", None, None, None, None, size)
	
class Capture:
	"""
	Using Scapy to capture packets, update the traffic statistics, and optionally notify another part of the program whenever a packet is captured
	"""
	def __init__(
		# Creating new Capture object
		self,
		interface: str,
		stats: TrafficStats,
		count: int = 0,
		bpf_filter: Optional[str] = None,
		on_packet: Optional[Callable[[PacketInfo], None]] = None,
	) -> None:
		self.interface = interface
		self.stats = stats
		self.count = count
		self.bpf_filter = bpf_filter
		self.on_packet = on_packet

	def _handle(self, packet: Packet) -> None:
		info = classify(packet)							# Converts the raw Scapy packet into a simpler PacketInfo object
		self.stats.record(info.protocol, info.src, info.dst, info.size)		# Update all the statistics
		if self.on_packet:
			self.on_packet(info)

	def run(self) -> None:
		"""
			Start sniffing. Blocks until 'count' packets are seen or Ctrl+C
		"""
		sniff(
			iface=self.interface,
			prn=self._handle,
			count=self.count,
			filter=self.bpf_filter,
			store=False,
		)
