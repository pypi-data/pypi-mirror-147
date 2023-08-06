from subprocess import run, PIPE
from omnitools import IS_WIN32


def ping(host):
    output = run("ping -{} 1{} {}".format(
        "n" if IS_WIN32 else "c",
        " -w 500" if IS_WIN32 else " -W 1",
        host
    ), shell=True, stdout=PIPE, stderr=PIPE, close_fds=not IS_WIN32)
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


