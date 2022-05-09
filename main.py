from requests import get
import docker
import os
from traceback import format_exc

file_path = os.path.dirname(__file__)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
}

client = docker.from_env()

def run_bomber(url, influx_ip, local_results, vus, dur):
    client.containers.run("grafana/k6", f'run --vus {vus} --duration {dur}s '
                                        f'--out influxdb=http://{influx_ip}:8086/k6 barrage.js',
                          environment={'URL': url.strip()}, volumes={local_results: {"bind": "/home/k6", 'mode': 'rw'}},
                          auto_remove=True)


def check_access(url):
    print(f'Testing URL: {url}')
    response = get(url, headers=headers, verify=False, timeout=60)
    if response.status_code in [200, 302]:
        print(f'Valid URL: {url}: {response.status_code}')
        return True
    else:
        return False


def validate_urls(url_list):
    result = []
    for each in url_list:
        if not each:
            continue
        try:
            result.append({"url": each, "status": check_access(each)})
        except Exception:
            print(format_exc())
            result.append({"url": each, "status": False})
    return result