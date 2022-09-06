from winproxy import ProxySetting

def set_proxy(proxy_server):
    p = ProxySetting()
    p.server = proxy_server
    p.enable = True
    p.registry_write()
    return proxy_server

def unset_proxy():
    p = ProxySetting()
    p.enable = False
    p.server = ''
    p.registry_write()
