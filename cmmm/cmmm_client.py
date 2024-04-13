#!/usr/bin/env python

import asyncio
import websockets
import json
from scapy.all import send, IP, UDP
import ipaddress

# settings
DELAY = 2
SOLICITATION = bytes.fromhex("2a9c14000200000057424d4382ecf98f00000000")
PORTS = [6111,6112]
SERVER = "ws://127.0.0.1:8001"


PEERS = [];

def validate_ip(ip):
    try:
        a = ipaddress.ip_address(ip)
        if a.version == 4:
            return True
        return False
    except:
        return False

async def subscribe():
    async with websockets.connect(SERVER) as websocket:
        while True:
            global PEERS
            res = await websocket.recv()
            print(f"received: {res}")
            try:
                PEERS = set(json.loads(res))
            except Exception as e:
                print(f"error: {e}")

async def send_solicitations():
    while True:
        try:
            for ip in PEERS:
                if validate_ip(ip):
                    for port in PORTS:
                        print(f"sending sol to {ip}:{port}")
                        send(IP(dst=ip)/UDP(sport=port,dport=port)/SOLICITATION)
                else:
                    print(f"skipping IP:{ip}")
        except Exception as e:
            print(f"error: {e}")
        await asyncio.sleep(DELAY)

async def main():
    tasks = await asyncio.gather(
        subscribe(),
        send_solicitations(),
        )
    print("done, closing")
            
if __name__ == "__main__":
    asyncio.run(main())