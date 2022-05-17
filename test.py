import os

from PyRoxy import Proxy, ProxyChecker, ProxyType, ProxyUtiles
from concurrent.futures import ThreadPoolExecutor, as_completed
from logging import basicConfig, getLogger, shutdown
from typing import Any, List, Set, Tuple
from PyRoxy import Tools as ProxyTools
from json import load, dumps
from contextlib import suppress
from secrets import choice as randchoice
from requests import Response, Session, exceptions, get, cookies
from pathlib import Path
from yarl import URL

basicConfig(format='[%(asctime)s - %(levelname)s] %(message)s',
            datefmt="%H:%M:%S")
logger = getLogger("MHDDoS")
logger.setLevel("INFO")
threads = 20
__dir__: Path = Path(__file__).parent
proxy_ty = 0
proxy_li = Path(__dir__ / "files/proxies/https.txt")
targets = Path(__dir__ / "files/proxies/targets.json")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ProxyManager:

    @staticmethod
    def DownloadFromConfig(cf, Proxy_type: int) -> Set[Proxy]:
        providrs = [
            provider for provider in cf["proxy-providers"]
            if provider["type"] == Proxy_type or Proxy_type == 0
        ]
        logger.info(
            f"{bcolors.WARNING}Downloading Proxies from {bcolors.OKBLUE}%d{bcolors.WARNING} "
            f"Providers{bcolors.RESET}" % len(
                providrs))
        proxes: Set[Proxy] = set()

        with ThreadPoolExecutor(len(providrs)) as executor:
            future_to_download = {
                executor.submit(
                    ProxyManager.download, provider,
                    ProxyType.stringToProxyType(str(provider["type"])))
                for provider in providrs
            }
            for future in as_completed(future_to_download):
                for pro in future.result():
                    proxes.add(pro)
        return proxes

    @staticmethod
    def download(provider, proxy_type: ProxyType) -> Set[Proxy]:
        logger.debug(
            f"{bcolors.WARNING}Proxies from (URL: {bcolors.OKBLUE}%s{bcolors.WARNING}, Type: {bcolors.OKBLUE}%s{bcolors.WARNING}, Timeout: {bcolors.OKBLUE}%d{bcolors.WARNING}){bcolors.RESET}" %
            (provider["url"], proxy_type.name, provider["timeout"]))
        proxes: Set[Proxy] = set()
        with suppress(TimeoutError, exceptions.ConnectionError,
                      exceptions.ReadTimeout):
            data = get(provider["url"], timeout=provider["timeout"]).text
            try:
                for proxy in ProxyUtiles.parseAllIPPort(
                        data.splitlines(), proxy_type):
                    proxes.add(proxy)
            except Exception as e:
                logger.error(f'Download Proxy Error: {(e.__str__() or e.__repr__())}')
        return proxes


def handleProxyList(con, proxy_ty, url=None):
    if proxy_ty not in {4, 5, 1, 0, 6}:
        exit("Socks Type Not Found [4, 5, 1, 0, 6]")
    if proxy_ty == 6:
        proxy_ty = randchoice([4, 5, 1])
    if proxy_li.exists():
        os.remove(proxy_li)
    proxy_li.parent.mkdir(parents=True, exist_ok=True)
    with proxy_li.open("w") as wr:
        Proxies: Set[Proxy] = ProxyManager.DownloadFromConfig(con, proxy_ty)
        logger.info(
            f"{bcolors.OKBLUE}{len(Proxies):,}{bcolors.WARNING} Proxies are getting checked, this may take awhile{bcolors.RESET}!"
        )
        Proxies = ProxyChecker.checkAll(
            Proxies, timeout=1, threads=threads,
            url=url.human_repr() if url else "http://httpbin.org/get",
        )

        if not Proxies:
            exit(
                "Proxy Check failed, Your network may be the problem"
                " | The target may not be available."
            )
        stringBuilder = ""
        for proxy in Proxies:
            stringBuilder += (proxy.__str__() + "\n")
        wr.write(stringBuilder)

    proxies = ProxyUtiles.readFromFile(proxy_li)
    if proxies:
        logger.info(f"{bcolors.WARNING}Proxy Count: {bcolors.OKBLUE}{len(proxies):,}{bcolors.RESET}")
    else:
        logger.info(
            f"{bcolors.WARNING}Empty Proxy File, running flood witout proxy{bcolors.RESET}")
        proxies = None

    return proxies
#
# with open("./config.json") as f:
#     con = load(f)
# print(handleProxyList(con, proxy_ty=1, url=URL("https://www.rbc.ru/search/")))

def validate_urls(url_list):
    result = []
    with ThreadPoolExecutor(4) as executor:
        future_to_check = {
            executor.submit(check_access, url)
            for url in url_list
        }
        for future in as_completed(future_to_check):
            if future.result()["url"] and future.result()["proxy"]:
                result.append({"url": future.result()["url"], "proxy": future.result()["proxy"], "status": True})
            elif future.result()["url"] and not future.result()["proxy"]:
                result.append({"url": future.result()["url"], "status": False})
    return result

def check_access(url):
    if not url:
        return {'url': None, 'proxy': None}
    result = {'url': url, 'proxy': []}
    with proxy_li.open("r") as f:
        with ThreadPoolExecutor(threads) as executor:
            future_to_check = {
                executor.submit(check_proxy, url, line)
                for line in f.readlines()
            }
            for future in as_completed(future_to_check):
                if future.result()["proxy"]:
                    result["proxy"].append(future.result()["proxy"])
    if result["proxy"]:
        result["proxy"] = ",".join(result["proxy"])
    return result


def check_proxy(url, proxy):
    try:
        resp = get(url, proxies={'http': proxy.strip(), 'https': proxy.strip()}, timeout=20, verify=False)
    except:
        return {'url': url, 'proxy': None}
    if resp.status_code in [200, 302]:
        return {'url': url, 'proxy': proxy.strip()}
    return {'url': url, 'proxy': None}
