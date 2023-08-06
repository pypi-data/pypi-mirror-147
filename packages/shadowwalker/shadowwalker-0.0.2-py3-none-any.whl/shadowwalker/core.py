from omnitools import IS_WIN32, def_template, randstr
from subprocess import Popen, run, PIPE
from pathlib import Path
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
        self.proxies = yaml.safe_load(requests.get(SOURCE).content.decode())["proxies"]
        self.test_latency(exclude_country)
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
        Popen([clash_bin])

    def test_latency(self, exclude_country):
        print("testing latency, please wait")
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**4))
        # self.proxies = self.proxies[:10]
        self.proxies = [_ for _ in self.proxies if _["country"][-2:] not in exclude_country]
        for i, proxy in enumerate(self.proxies):
            def job(i, proxy):
                print("\r", i+1, len(self.proxies), "pinging", proxy["server"], end="", flush=True)
                ping = [999]
                for i in range(0, 5):
                    p = self.ping(proxy["server"])
                    ping.append(p)
                    if p < 999:
                        break
                proxy["ping"] = min(ping)
                print("\r", i+1, len(self.proxies), "pinging", proxy["server"], proxy["ping"], end="", flush=True)
            tw.add(job=def_template(job, i, proxy))
        tw.wait()
        self.proxies = [_ for _ in self.proxies if _["ping"] <= 171]
        print("\r", self.proxies)

    def ping(self, host):
        output = run("ping -{} 1{} {}".format(
            "n" if IS_WIN32 else "c",
            " -w 500" if IS_WIN32 else " -W 1",
            host
        ), shell=True, stdout=PIPE, stderr=PIPE)
        if IS_WIN32:
            try:
                # print(output.stdout.decode())
                # print(output.stdout.decode().splitlines()[2].split("ms")[0].split("=")[-1])
                return float(output.stdout.decode().splitlines()[2].split("ms")[0].split("=")[-1])
            except:
                return 999
        else:
            try:
                return float(output.stdout.decode().splitlines()[-1].split(" ")[-2].split("/")[0])
            except:
                return 999



