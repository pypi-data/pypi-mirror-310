import httpx
import os

import os
import sys

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS # type: ignore
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

ssl_gw_crt_path = "C:\\GW\\certificates\\ssl\\v0.0.1.crt"
print(f'SSL Certificate Path 3: {ssl_gw_crt_path} [{os.path.exists(ssl_gw_crt_path)}]')
ssl_gw_crt_path = resource_path(os.path.join('gw_certs', 'v0.0.1.crt'))
print(f'SSL Certificate Path 1: {ssl_gw_crt_path} [{os.path.exists(ssl_gw_crt_path)}]')
ssl_gw_crt_path = resource_path('KeyisBClient/gw_certs/v0.0.1.crt')
print(f'SSL Certificate Path 3: {ssl_gw_crt_path} [{os.path.exists(ssl_gw_crt_path)}]')

class __DNSCore:
    def __init__(self) -> None:
        from KeyisBLogging import logging
        logging.error('\n' + '='*50 +  '\n              CLIENT STARTED\n' + '='*50)
        
        self._connectionAsync = httpx.AsyncClient(verify=ssl_gw_crt_path)
        self._connectionSync = httpx.Client(verify=ssl_gw_crt_path)
        self.hosts = [
                {'host': 'http://51.250.85.38:50000', 'status': 'unknown', 'add_type': 'main'},
                {'host': 'http://api-root-dns.gw.mmbproject.com:50000', 'status': 'unknown', 'add_type': 'main'},
        ]
        self.checkForAnyDNSHosts()
    def checkForAnyDNSHosts(self):
        path = "C:\\GW\\DNS\\hosts.txt"
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            self.hosts.append({
                                'host': line,
                                'status': 'unknown',
                                'add_type': 'outFile'
                                })
            except: pass
DNSCore = __DNSCore()