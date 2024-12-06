from sys import platform
from platform import machine
import ctypes
import os

version = '1.7.9'
if platform == 'darwin':
    file_ext = f'-darwin-arm64-{version}.dylib' if machine() == "arm64" else f'-darwin-amd64-{version}.dylib'
elif platform in ('win32', 'cygwin'):
    file_ext = f'windows-64-{version}.dll' if 8 == ctypes.sizeof(ctypes.c_voidp) else f'-windows-32-{version}.dll'
else:
    if machine() == "aarch64":
        file_ext = f'-linux-arm64-{version}.so'
    elif "x86" in machine():
        file_ext = f'-linux-x86-{version}.so'
    else:
        file_ext = f'-linux-amd64-{version}.so'

root_dir = os.path.abspath(os.path.dirname(__file__))
library = ctypes.cdll.LoadLibrary(f'{root_dir}/dependencies/tls-client{file_ext}')

# extract the exposed request function from the shared package
request = library.request
request.argtypes = [ctypes.c_char_p]
request.restype = ctypes.c_char_p

freeMemory = library.freeMemory
freeMemory.argtypes = [ctypes.c_char_p]
freeMemory.restype = ctypes.c_char_p

destroySession = library.destroySession
destroySession.argtypes = [ctypes.c_char_p]
destroySession.restype = ctypes.c_char_p
