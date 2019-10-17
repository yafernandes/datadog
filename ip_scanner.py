#!/usr/local/bin/python3
import ipaddress
import os
import socket
from concurrent.futures import ThreadPoolExecutor

import dns.resolver
import requests


def scan(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((ip, port))
        print(f'{ip}:{port}\tOpen')
        sock.close()
    except Exception as e:
        print(f'{ip}:{port} \tFailed\t{e}')
    finally:
        sock.close()

def scan_endpoint(fqdn, port):
    print(f'\n\n=== Testing endpoint {fqdn} on port {port} ===\n')
    with ThreadPoolExecutor(max_workers=128) as executor:
        answers = dns.resolver.query("intake.logs.datadoghq.com", 'A')
        for server in answers:
            executor.submit(scan, server.address, port)
        executor.shutdown(wait=True)

def scan_iprange(service, port):
    print(f'\n\n=== Testing ip range for {service} on port {port} ===\n')
    with ThreadPoolExecutor(max_workers=128) as executor:
        for cidr in ipranges[service]["prefixes_ipv4"]:
            for ip in ipaddress.IPv4Network(cidr):
                executor.submit(scan, ip.exploded, port)
        executor.shutdown(wait=True)


ipranges = requests.get("https://ip-ranges.datadoghq.com/").json()

scan_endpoint("intake.logs.datadoghq.com", 10516)

scan_iprange("agents", 443)
scan_iprange("api", 443)
scan_iprange("apm", 443)
scan_iprange("logs", 10516)
scan_iprange("process", 443)
