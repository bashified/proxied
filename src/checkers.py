import socket
import time
import threading
from queue import Queue
from websocket import create_connection
import httpx
import requests

TEST_URL = "http://httpbin.org/ip" # test url for HTTP/S, change this in future if needed
WS_TEST_URL = "ws://echo.websocket.events"  # this is a This is a public echo WebSocket server provided for testing.

def checkreq(proxy):
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        r = requests.get(TEST_URL, proxies=proxies, timeout=5)
        return r.status_code == 200
    except:
        return False

def checksock(proxy):
    try:
        ip, port = proxy.split(":")
        socket.create_connection((ip, int(port)), timeout=5).close()
        return True
    except:
        return False

def checkwebsock(proxy):
    try:
        ws = create_connection(WS_TEST_URL,
                               http_proxy_host=proxy.split(":")[0],
                               http_proxy_port=int(proxy.split(":")[1]),
                               timeout=5)
        ws.send("ping")
        _ = ws.recv()
        ws.close()
        return True
    except:
        return False

def checkhttpx(proxy):
    try:
        with httpx.Client(proxies={"http://": f"http://{proxy}", "https://": f"http://{proxy}"}, timeout=5) as client:
            r = client.get(TEST_URL)
            return r.status_code == 200
    except:
        return False