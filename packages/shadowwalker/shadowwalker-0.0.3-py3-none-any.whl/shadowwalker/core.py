from omnitools import def_template, randstr, IS_WIN32
from subprocess import Popen
from pathlib import Path
from .utils import ping
import threadwrapper
import threading
import requests
import random
import shutil
import yaml
import time
import os


SOURCE = "https://fq.lonxin.net/clash/proxies?type=ss"


class ShadowWalker:
    def __init__(self, clash_bin="clash", exclude_country=["US", "CA"]):
        self.proxies = []
        for i in range(0, 10):
            try:
                print("\r", "fetching proxies, try {}/10".format(i+1), end="", flush=True)
                self.proxies = yaml.safe_load(requests.get(SOURCE, timeout=3).content.decode())["proxies"]
                break
            except:
                pass
        print("\n")
        self.test_latency(exclude_country)
        self.start_clash(clash_bin)

    def start_clash(self, clash_bin):
        if not self.proxies:
            raise ValueError("empty proxies")
        config_fp = os.path.join(str(Path.home()), ".config", "clash", "config.yaml")
        if os.path.isfile(config_fp):
            shutil.move(config_fp, config_fp+"."+str(int(time.time())))
        secret = randstr(32)
        proxy = random.SystemRandom().choice(self.proxies)
        proxy = random.SystemRandom().choice(self.proxies)
        open(config_fp, "wb").write(('''\
port: 7890
external-controller: 127.0.0.1:9090
secret: {}
allow-lan: true
mode: rule
proxies:
  - name: "PROXY"
    type: ss
    server: "{}"
    port: {}
    cipher: {}
    password: "{}"
rules:
  - MATCH,PROXY
'''.format(
            secret,
            proxy["server"],
            proxy["port"],
            proxy["cipher"],
            proxy["password"],
        )).encode())
        print(proxy)
        print("clash secret", secret)
        print("starting clash")
        Popen([clash_bin], close_fds=not IS_WIN32)

    def test_latency(self, exclude_country):
        print("testing latency, please wait")
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**4))
        # self.proxies = self.proxies[:10]
        self.proxies = [_ for _ in self.proxies if _["country"][-2:] not in exclude_country]
        for i, proxy in enumerate(self.proxies):
            def job(i, proxy):
                print("\r", i+1, len(self.proxies), "pinging", proxy["server"], end="", flush=True)
                pings = [999]
                for i in range(0, 5):
                    p = ping(proxy["server"])
                    pings.append(p)
                    if p < 999:
                        break
                proxy["ping"] = min(pings)
                print("\r", i+1, len(self.proxies), "pinging", proxy["server"], proxy["ping"], end="", flush=True)
            tw.add(job=def_template(job, i, proxy))
        tw.wait()
        self.proxies = [_ for _ in self.proxies if _["ping"] <= 171]
        print("\n")
        # print("\r", self.proxies)




