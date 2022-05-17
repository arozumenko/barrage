import docker
import os
from test import check_proxy

file_path = os.path.dirname(__file__)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

client = docker.from_env()

def run_bomber(url, influx_ip, local_results, vus, dur, proxy):
    environment={'URL': url.strip()}
    if proxy:
        proxy_list = proxy.split(",")
        for proxy in proxy_list:
            if check_proxy(url, proxy)["proxy"]:
                environment["HTTP_PROXY"] = proxy
                environment["HTTPS_PROXY"] = proxy
                break
        else:
            return 0
    client.containers.run("grafana/k6", f'run --vus {vus} --duration {dur}s '
                                        f'--out influxdb=http://{influx_ip}:8086/k6 '
                                        f'--insecure-skip-tls-verify barrage.js',
                          environment=environment, volumes={local_results: {"bind": "/home/k6", 'mode': 'rw'}},
                          auto_remove=True)
