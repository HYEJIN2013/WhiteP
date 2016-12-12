#!/usr/bin/env python2.7


"""
LPR server for remote control to serial port via network supporting auto discover of the server.
"""

import serial
import socket
import select

import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class LPR(object):
	_s_con = None
	_conn = socket.socket()
	_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	_listen = socket.socket()

	def __init__(self):
		self._udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
		self._udp_sock.bind(("0.0.0.0", 1235))
		self._listen.bind(("0.0.0.0", 9100))
		self._listen.listen(1)


	def open(self):
		self._conn.close()
		self._conn, addr = self._listen.accept()
		if self._s_con:
			self._s_con.close()
		self._s_con = serial.Serial(1, 115200, 8, 'N', 1, None, xonxoff=True, rtscts=False)
		logging.info("new connection from %s", addr)


	def write(self):
		out = []
		while select.select([self._conn], [], [], 0)[0]:
			out.append(self._conn.recv(4096))
		data = ''.join(out)

		if not data:
			logging.warning("broken pipe")

		self._s_con.write(data)
		logging.info("writing %d bytes into serial", len(data))
	
	def main(self):

		evts = select.select([self._udp_sock, self._listen, self._conn], [], [])[0]

		if self._udp_sock in evts:
			data, addr = self._udp_sock.recvfrom(2048)
			logging.info("sending address to addr %s", addr[0])
			self._udp_sock.sendto("ok", addr)
			return

		if self._listen in evts:
			self.open()
			return

		if self._conn in evts:
			self.write()

if __name__ == '__main__':
	logging.info("starting daemon")
	lpr = LPR()
	while True: lpr.main()
