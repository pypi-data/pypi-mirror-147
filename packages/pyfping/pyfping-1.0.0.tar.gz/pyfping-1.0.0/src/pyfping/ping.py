#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys
import argparse 
import math
import socket
import struct
import select
import signal
import time


class PingStats():
    """stats for a pinger"""

    def __init__(self, host):
        self._sent = 0
        self._received = 0
        self._rtt = []
        self._sum = 0
        self._sumsq = 0
        self._min = 999999999
        self._max = 0
        self._avg = 0
        self._stddev = 0
        self._current = 0
        self._ts = 0
        self._host = host


    def append_sent(self, timestamp, seq):
        self._sent += 1
        self._current = seq
        self._ts = timestamp


    def append_received(self, timestamp):
        self._received += 1
        rtt = timestamp - self._ts
        if self._min > rtt:
            self._min = rtt
        if self._max < rtt:
            self._max = rtt
        self._sum += rtt
        self._sumsq += rtt*rtt

    def get_stats(self):
        if self._received == 0:
            return 0,0,0,0,0,0
        else:
            mean = self._sum / self._received
            stddev = math.sqrt(self._sumsq/self._received - mean * mean)
            return self._sent, self._received, self._min, self._max, mean, stddev

class FPinger(object):
    """ fping-like: pinger for multihost """

    def __init__(self, single_host, filename, count=4, interval=1, timeout=5, pktlen=98):
        pid = os.getpid() & 0xFFFF
        self._id = pid
        self.hosts = []
        self.ipaddr = []
        self._stats = []
        self._dict = {}
        self._total = 0
        if single_host is not None:
            self.hosts.append(single_host)
            self.ipaddr.append(socket.gethostbyname(single_host))
            self._stats.append(PingStats(single_host))
            self._dict[single_host] = self._total
            self._total += 1
        if filename is not None:
            with open(filename) as f:
                for l in f:
                    host = l.rstrip('\n')
                    if len(host) > 0:
                        self.hosts.append(host)
                        self.ipaddr.append(socket.gethostbyname(host))
                        self._stats.append(PingStats(host))
                        self._dict[host] = self._total
                        self._total += 1
        self.count = count
        self.timeout = timeout
        self.pktlen = pktlen
        self.interval = interval
        try:
            # use SOCK_DGRAM so avoid root privileged
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
            # sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except socket.error as e:
            if e.errno == 1:
                e.msg +=  "ICMP messages need privileged"
            raise socket.error(e.msg)
        except Exception as e:
            print ("Exception: %s" %(e))
        self.sock.settimeout(timeout)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)


    def _checksum(self, data):
        """  Verify the packet integritity """
        sum = 0
        data += b'\x00'

        for i in range(0, len(data) - 1, 2):
            sum += (data[i] << 8) + data[i + 1]
            sum  = (sum & 0xffff) + (sum >> 16)

        sum = ~sum & 0xffff

        return sum


    def _rx_pong(self, host, ip):
        """
        Receive ping from the socket.
        """
        time_remaining = self.timeout
        while True:
            start_time = time.time() * 1000
            readable = select.select([self.sock], [], [], time_remaining)
            time_spent = (time.time() * 1000 - start_time)
            if readable[0] == []: # Timeout
                return

            time_received = time.time() * 1000
            recv_packet, addr = self.sock.recvfrom(self.pktlen+40)
            ip_header = recv_packet[:20]
            icmp_len = len(recv_packet) - 20
            icmp_header = recv_packet[20:28]
            ipv, tos, iplen, ipid, ipoff, ttl, ipproto, ipsum, ipsrc, ipdst = struct.unpack("!BBHHHBBH4s4s", ip_header)
            ipsrc = socket.inet_ntoa(ipsrc)
            # ipdst = socket.inet_ntoa(ipdst)
            type, code, checksum, packet_id, seq = struct.unpack("bbHHh", icmp_header)
            if packet_id == self._id:
                bytes_In_double = struct.calcsize("d")
                time_sent = struct.unpack("d", recv_packet[28:28 + bytes_In_double])[0] * 1000
                # print("type: [" + str(type) + "] code: [" + str(code) + "] checksum: [" + str(checksum) + "] p_id: [" + str(packet_id) + "] sequence: [" + str(seq) + "]")
                print("%d bytes from %s(%s): icmp_seq=%d ttl=%d time=%0.4f ms" %(icmp_len, host, ipsrc, seq, ttl, (time_received - time_sent)))
                idx = self._dict[host]
                self._stats[idx].append_received(time_received)
                return time_received - time_sent

            time_remaining = time_remaining - time_spent
            if time_remaining <= 0:
                return


    def send_ping(self, host, ip, sequence=1):
        """
        Send ping to the target host
        """
        ICMP_ECHO_REQUEST = 8
        content = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        checksum = 0

        # Create a dummy heder with a 0 checksum.
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, checksum, self._id, sequence)
        bytes_In_double = struct.calcsize("d")
        if self.pktlen < len(content):
            data = content[:(self.pktlen - bytes_In_double)]
        else:
            ntimes = (self.pktlen - bytes_In_double) / len(content)
            padding = (self.pktlen - bytes_In_double) % len(content)
            data = content * int(ntimes) + content[:padding]
        
        ts = time.time()
        data = struct.pack("d", ts) + bytes(data.encode('utf-8'))
        # Get the checksum on the data and the dummy header.
        checksum = self._checksum(header + data)
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(checksum), self._id, sequence)
        packet = header + data
        self.sock.sendto(packet, (ip, 1))
        idx = self._dict[host]
        self._stats[idx].append_sent(ts * 1000, sequence)
        # print("type: [" + str(ICMP_ECHO_REQUEST) + "] code: [" + str(0) + "] checksum: [" + str(checksum) + "] p_id: [" + str(ID) + "] sequence: [" + str(1) + "]")


    def ping_pong(self, host, ip, seq):
        """
        Returns the delay (in seconds) or none on timeout.
        """

        self.send_ping(host, ip, sequence=seq)
        delay = self._rx_pong(host, ip)
        return delay


    def ping_all(self):
        """
        ping hosts
        """
        for host, ip in zip(self.hosts, self.ipaddr):
            print ("Ping %s (%s): %d data bytes" % (host, ip, self.pktlen))
        for i in range(self.count):
            for host, ip in zip(self.hosts, self.ipaddr):
                try:
                    delay = self.ping_pong(host, ip, i)
                except socket.gaierror as e:
                    print ("Ping failed. (socket error: '%s')" % e[1])
                    break

                if delay == None:
                    print ("Ping failed. (timeout within %ssec.)" % self.timeout)
                else:
                    delay = delay * 1000
            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                break


    def print_icmp_stats(self):
        print("")
        for host in self.hosts:
            idx = self._dict[host]
            tx, rx, min, max, mean, stddev = self._stats[idx].get_stats()
            print("--- %s ping statistics ---" % host)
            print("%d packets transmitted, %d packets received, %.2f%% packet loss" % (tx, rx, (100* (tx - rx)/ tx)))
            print("round-trip min/avg/max/stddev = %.2f/%.2f/%.2f/%.2f ms" %(min, mean, max, stddev))
            print("")


    def __del__(self):
        if self.sock is not None:
            self.sock.close()


def signal_handler():
    sys.exit()


def main():
    parser = argparse.ArgumentParser(description='python ping script similar to fping')
    parser.add_argument(dest='host', nargs="?", action="store", help='single target host')
    parser.add_argument('-f', '--file', dest='filename', action="store", type=str, help='file contains host list')
    parser.add_argument('-c', '--count', dest='count', action="store", type=int, default=4, help='icmp packet count to a destination')
    parser.add_argument('-i', '--interval', dest='interval', action="store", type=float, default=1, help='icmp packet interval to a destination')
    parser.add_argument('-s', '--size', dest='size', action="store", type=int, default=98, help='icmp packet size')

    args = parser.parse_args()
    args.host
    if args.host is None and args.filename is None:
        print("specify a host or host file")
        sys.exit(0)
    pinger = FPinger(single_host=args.host, filename=args.filename, count=args.count, interval=args.interval, pktlen=args.size)

    signal.signal(signal.SIGINT, lambda signal, frame: signal_handler())
    pinger.ping_all()
    pinger.print_icmp_stats()


if __name__ == '__main__':
    main()
