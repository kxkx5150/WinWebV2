import os
import time
import json
import random
import threading
import win32con
import ctypes
from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import *
from pconst import const


class WinWebV2:
    def __init__(self, cb):
        print(callable(cb))
        if not callable(cb):
            print("Error arguments\nPlease set Callback Function")
            return

        self.WINDOWPROC = WINFUNCTYPE(LPARAM, HWND, UINT, WPARAM, LPARAM)
        ctypes.windll.user32.GetWindowLongPtrW.restype = c_void_p
        ctypes.windll.user32.SetWindowLongPtrW.argtypes = [HWND, c_int, c_void_p]
        ctypes.windll.user32.SetWindowLongPtrW.restype = c_void_p

        target_path = os.path.join(os.path.dirname(__file__), 'dll/WebV2dll')
        self.webview2 = ctypes.WinDLL(target_path)
        self.webview2.WebV2dllCreate.argtypes = [c_wchar_p, c_int, c_int, c_int, c_int]
        self.webview2.resize_webview.argtypes = [HWND]
        self.webview2.get_webview_wmmsg_id.restype = c_int
        self.PCOPYDATASTRUCT = ctypes.POINTER(self.COPYDATASTRUCT)
        self.randomid = random.randint(1, 2147483640)
        self.webview2.receive_randomid(self.randomid)
        self.webview2.receive_randomid.argtypes = [c_int]
        self.message_handler = cb

        self.webview2.load_url.argtypes = [c_wchar_p]
        self.webview2.exec_js.argtypes = [c_wchar_p]
        self.webview2.set_startup_script.argtypes = [c_wchar_p]
        self.webview2.send_json.argtypes = [c_wchar_p]

    def myname(self):
        print('WinWebV2')

    def create_window(self, url, x, y, width, height):
        thread1 = threading.Thread(target=self.create_main_window, args=(url, x, y, width, height), daemon=True)
        thread1.start()
        time.sleep(0.1)
        const.g_hwnd = self.webview2.get_main_hwnd()
        orgproc = windll.user32.GetWindowLongPtrW(const.g_hwnd, win32con.GWL_WNDPROC)
        const.wrappedWndProc = self.WINDOWPROC(orgproc)
        const.WM_WEBV_USER = self.webview2.get_webview_wmmsg_id()
        windll.user32.SetWindowLongPtrW(
            c_void_p(const.g_hwnd), win32con.GWL_WNDPROC, cast(self.WINDOWPROC(self.wndproc), c_void_p))
        thread1.join()

    def create_main_window(self, url, x, y, width, height):
        self.webview2.WebV2dllCreate(url, x, y, width, height)

    def wndproc(self, hwnd, message, wparm, lparam):
        if message == win32con.WM_DESTROY:
            jsondata = {
                "msg": "WM_DESTROY"
            }
            self.message_handler(jsondata)
            windll.user32.PostQuitMessage(0)
            return 0
        elif message == win32con.WM_SIZE:
            self.webview2.resize_webview(const.g_hwnd)
            jsondata = {
                "msg": "resize_window"
            }
            self.message_handler(jsondata)
            return 0

        elif message == win32con.WM_COPYDATA:
            pcds = ctypes.cast(lparam, self.PCOPYDATASTRUCT)
            dwdata = pcds.contents.dwData
            if self.randomid != dwdata:
                return 0

            # self.close_window()

            msgstr = ctypes.wstring_at(pcds.contents.lpData)
            jsondata = json.loads(msgstr)
            self.message_handler(jsondata)
            return 0

        return const.wrappedWndProc(ctypes.c_void_p(hwnd), ctypes.c_uint(message),
                                    ctypes.c_ulonglong(wparm), ctypes.c_longlong(lparam))

    def load_url(self, url):
        self.webview2.load_url(url)

    def close_window(self):
        windll.user32.PostQuitMessage(0)
            
    def execute_js(self, script):
        self.webview2.exec_js(script)

    def set_startup_js(self, script):
        self.webview2.set_startup_script(script)

    def send_json(self, jsonstr):
        self.webview2.send_json(jsonstr)

    def reload_page(self):
        self.webview2.reload_page()

    class COPYDATASTRUCT(ctypes.Structure):
        _fields_ = [
            ('dwData', wintypes.LPARAM),
            ('cbData', wintypes.DWORD),
            ('lpData', ctypes.c_void_p)
        ]


def message_handler(jsondata):
    print(jsondata)


def main():
    wv2 = WinWebV2(message_handler)
    target_path = os.path.join(os.path.dirname(__file__), 'html/index.html')
    url = os.path.abspath(target_path)
    # url = "https://twitter.com/home"
    wv2.create_window(url, -1, -1, 700, 600)


if __name__ == "__main__":
    main()
