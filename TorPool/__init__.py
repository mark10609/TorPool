# coding: utf-8
name = "ToorPool"

import os 

_TOR_EXE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'TorPool/tor-win32-0.3.5.8/Tor/tor.exe', )
)

from .tor_method import TorMethod