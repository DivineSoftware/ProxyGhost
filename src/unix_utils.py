import os

def set_proxy(proxy_server):
    os.environ['https_proxy'] = proxy_server
    os.environ['http_proxy'] = proxy_server
    return proxy_server

def unset_proxy():
    os.environ['http_proxy'] = ""
    os.environ['https_proxy'] = ""
