#!/usr/bin/env python
import os
if os.name == 'nt':
    from windows_utils import *
else:
    from unix_utils import *
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.application.current import get_app
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.widgets import *
from prompt_toolkit.styles import Style
from proxy_checking import ProxyChecker
import requests
import threading,multiprocessing
import datetime
import time
import sys
import random

#config
timeout = 5
max_thread_count = 30

thread_iterator = 0
proxies = []
lookups = []
connected = False

def exit_clicked():
    sys.exit()
    get_app().exit()

def print_hr():
    text_area.text += "\n"
    text_area.buffer.cursor_position = len(text_area.text)

def bottom_toolbar():
    return HTML('<style bg="ansiblue">[i]</style> Press <b>Tab</b> to switch between controls')

def check_proxy(server, mode):
    global thread_iterator
    global proxies
    global lookups
    try:
        if requests.get('https://httpbin.org/get', timeout = timeout, proxies={mode:server}).text.find('"url": "https://httpbin.org/get"')!=-1:
            proxies.append(server)
            checker = ProxyChecker()
            lookups.append(checker.check_proxy(server))
        thread_iterator -= 1
    except: thread_iterator -= 1

def proxy_scrape():
    global thread_iterator
    servers = []
    try:
        servers = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=yes&anonymity=all",timeout=timeout).text.split("\r\n")[0:-1]
    except:
        return
    thread_iterator = 0
    for server in servers:
        if thread_iterator<max_thread_count:
            threading.Thread(target=check_proxy,args=(server,"https")).start()
            thread_iterator += 1

def connect_proxy():
    global timeout
    global connected
    global rotator
    global forward
    global proxies
    if connected:
        if checkbox6.checked:
            unset_proxy()
        text_area.text += "\nDisconnected\n"
        connected = False
        button1.text = "Connect"
        print_hr()
    else:
        print_hr()
        timeout = 5
        try:
          with open("proxies.txt","r") as proxylist:
            proxies = proxylist.read().split("\n")
        except:
            proxy_scrape()
        while proxies == []:
            pass
        myip = random.choice(proxies)
        if checkbox6.checked:
            set_proxy(myip)
        text_area.text += f"Connected to {myip}"
        button1.text = "Disconnect"
        connected = True
        print_hr()
        
label1 = Label("""
 ██▓███   ██▀███   ▒█████  ▒██   ██▒▓██   ██▓  ▄████  ██░ ██  ▒█████    ██████ ▄▄▄█████▓
▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▒▒ █ █ ▒░ ▒██  ██▒ ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒░░  █   ░  ▒██ ██░▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░ ░ █ █ ▒   ░ ▐██▓░░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ 
▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░▒██▒ ▒██▒  ░ ██▒▓░░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ 
▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒▒ ░ ░▓ ░   ██▒▒▒  ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   
░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░░   ░▒ ░ ▓██ ░▒░   ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    
░░         ░░   ░ ░ ░ ░ ▒   ░    ░   ▒ ▒ ░░  ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░      
            ░         ░ ░   ░    ░   ░ ░           ░  ░  ░  ░    ░ ░        ░           
                                     ░ ░""")

checkbox6 = Checkbox("System Wide Proxy")

hl = HorizontalLine()
button1 = Button("Connect", handler=connect_proxy)
button2 = Button("Exit", handler=exit_clicked)

bottom_style = Style.from_dict(
    {
        "status": "reverse",
        "shadow": "bg:#ffffff #000000",
    }
)


label4 = Label("Use tab and arrows to switch between controls and enter or spacebar to trigger switches", style="bg:#ffffff #000000")

buttons = HSplit([checkbox6, hl, button1, button2],height = 5,width=25)

text_area = TextArea(focusable=False,scrollbar=True,
height=10,dont_extend_height=True,width=53)

root = VSplit(
    [
        Box(Frame(buttons, style="bg:#ansiblue #ansiwhite"), padding=2),
        Box(Frame(text_area, title="ProxyGhost Event Log"), padding=2),
    ]
)

container = HSplit(
    [
        label1,
        root,
        label4,
    ]
)


layout = Layout(container)

key_bindings = KeyBindings()
key_bindings.add("up")(focus_previous)
key_bindings.add("down")(focus_next)
key_bindings.add("tab")(focus_next)

@key_bindings.add("escape")
def on_escape_press(event):
    event.app.exit()


def main():
    application = Application(
        layout=layout, key_bindings=key_bindings, full_screen=True, mouse_support=True,
        )
    application.run()


if __name__ == "__main__":
    main()