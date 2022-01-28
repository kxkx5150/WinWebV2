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


class WindInfo:
    def __init__(self):
        self.hwnd = None
        self.wndproc = None
        self.closed = False

    def set_hwnd(self, hwnd):
        self.hwnd = hwnd

    def set_wndproc(self, wndproc):
        self.wndproc = wndproc

    def get_hwnd(self):
        return self.hwnd

    def get_wndproc(self):
        return self.wndproc

    def close(self):
        self.closed = True


class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', wintypes.LPARAM),
        ('cbData', wintypes.DWORD),
        ('lpData', ctypes.c_void_p)
    ]


class WinWebV2:
    def __init__(self, cb, use_windows_proc=False):
        if not callable(cb):
            print("Error arguments\nPlease set Callback Function")
            return

        self.WINDOWPROC = WINFUNCTYPE(LPARAM, HWND, UINT, WPARAM, LPARAM)
        ctypes.windll.user32.GetWindowLongPtrW.restype = c_void_p
        ctypes.windll.user32.SetWindowLongPtrW.argtypes = [HWND, c_int, c_void_p]
        ctypes.windll.user32.SetWindowLongPtrW.restype = c_void_p

        target_path = os.path.join(os.path.dirname(__file__), 'dll/WebV2dll')
        self.webview2 = ctypes.WinDLL(target_path)

        self.webview2.get_webview_wmmsg_id.restype = c_int
        self.WM_WEBV_USER = self.webview2.get_webview_wmmsg_id()
        self.PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)
        self.randomid = random.randint(1, 2147483640)
        self.webview2.receive_randomid(self.randomid)
        self.webview2.receive_randomid.argtypes = [c_int]
        self.message_handler = cb

        self.webview2.WebV2dllCreate.argtypes = [c_int, c_wchar_p, c_int, c_int, c_int, c_int]
        self.webview2.create_window.argtypes = [c_int, c_wchar_p, c_int, c_int, c_int, c_int]
        self.webview2.create_window.restype = HWND

        self.webview2.get_main_hwnd.argtypes = [c_int]
        self.webview2.get_main_hwnd.restype = HWND
        self.webview2.resize_webview.argtypes = [HWND]
        self.webview2.close_window.argtypes = [HWND]

        self.webview2.reload_page.argtypes = [HWND]
        self.webview2.load_url.argtypes = [HWND, c_wchar_p]
        self.webview2.set_global_startup_script.argtypes = [c_wchar_p]
        self.webview2.set_startup_script.argtypes = [HWND, c_wchar_p]
        self.webview2.exec_js.argtypes = [HWND, c_wchar_p]
        self.webview2.send_json.argtypes = [HWND, c_wchar_p]

        self.use_windows_windproc = use_windows_proc
        self.window_infos = {}

    #
    # private
    def create_main_window(self, createid, url, x, y, width, height):
        self.webview2.WebV2dllCreate(createid, url, x, y, width, height)

    def wndproc(self, hwnd, message, wparm, lparam):
        if message == win32con.WM_DESTROY:
            self.apply_message_handler(hwnd, "receive_json", json.loads('{"msg":"WM_DESTROY"}'))
            self.window_infos[hwnd].close()
            if 0 == self.count_open_windows():
                self.apply_message_handler(hwnd, "receive_json", json.loads('{"msg":"post_quit_message"}'))
                windll.user32.PostQuitMessage(0)
                return 0

        elif message == win32con.WM_SIZE:
            self.webview2.resize_webview(self.window_infos[hwnd].get_hwnd())
            self.apply_message_handler(hwnd, "receive_json", json.loads('{"msg":"resize_window"}'))
            return 0

        elif message == win32con.WM_COPYDATA:
            pcds = ctypes.cast(lparam, self.PCOPYDATASTRUCT)
            dwdata = pcds.contents.dwData
            if self.randomid != dwdata:
                return 0

            msgstr = ctypes.wstring_at(pcds.contents.lpData)
            self.apply_message_handler(hwnd, "receive_json", json.loads(msgstr))
            return 0

        wndproc = self.window_infos[hwnd].get_wndproc()
        return wndproc(ctypes.c_void_p(hwnd), ctypes.c_uint(message),
                       ctypes.c_ulonglong(wparm), ctypes.c_longlong(lparam))

    def windows_windproc(self, hwnd, message, wparm, lparam):
        if 0 == self.message_handler(hwnd, message, wparm, lparam):
            return 0

        wndproc = self.window_infos[hwnd].get_wndproc()
        return wndproc(ctypes.c_void_p(hwnd), ctypes.c_uint(message),
                       ctypes.c_ulonglong(wparm), ctypes.c_longlong(lparam))

    def apply_message_handler(self, hwnd, msg, jsondata=None):
        _json = {
            "sender": self,
            "hwnd": hwnd,
            "msg": msg,
            "json": jsondata
        }
        self.message_handler(_json)

    def set_wndproc(self, hwnd):
        wndinf = WindInfo()
        wndinf.set_hwnd(hwnd)
        orgproc = windll.user32.GetWindowLongPtrW(hwnd, win32con.GWL_WNDPROC)
        wndinf.set_wndproc(self.WINDOWPROC(orgproc))
        self.window_infos[hwnd] = wndinf

        if self.use_windows_windproc:
            windll.user32.SetWindowLongPtrW(
                c_void_p(hwnd), win32con.GWL_WNDPROC, cast(self.WINDOWPROC(self.windows_windproc), c_void_p))
        else:
            windll.user32.SetWindowLongPtrW(
                c_void_p(hwnd), win32con.GWL_WNDPROC, cast(self.WINDOWPROC(self.wndproc), c_void_p))

    #
    # public
    def create_window(self, url, x, y, width, height):
        createid = random.randint(1, 2147483640)
        thread = threading.Thread(target=self.create_main_window, args=(createid, url, x, y, width, height),
                                  daemon=True)
        thread.start()
        time.sleep(0.1)
        hwnd = self.webview2.get_main_hwnd(createid)
        self.set_wndproc(hwnd)
        thread.join()

    def create_subwindow(self, url, x, y, width, height):
        createid = random.randint(1, 2147483640)
        hwnd = self.webview2.create_window(createid, url, x, y, width, height)
        self.set_wndproc(hwnd)

    def close_window(self, hwnd):
        self.webview2.close_window(hwnd)

    def minimize_window(self, hwnd):
        windll.user32.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize_window(self, hwnd):
        windll.user32.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def show_window(self, hwnd):
        windll.user32.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

    def get_active_hwnd(self):
        hwnd = windll.user32.GetActiveWindow()
        if not hwnd:
            return None
        if not ctypes.windll.user32.IsWindowVisible(hwnd):
            return None
        if hwnd not in self.window_infos:
            return None
        return hwnd

    def get_all_hwnds(self):
        hwnds = []
        for info in self.window_infos:
            item = self.window_infos[info]
            if item.closed:
                continue
            hwnds.append(item.get_hwnd())
        return hwnds

    def count_open_windows(self):
        wlist = self.get_all_hwnds()
        return len(wlist)

    def load_url(self, hwnd, url):
        self.webview2.load_url(hwnd, url)

    def reload_page(self, hwnd):
        self.webview2.reload_page(hwnd)

    def set_startup_js(self, script):
        self.webview2.set_global_startup_script(script)

    def execute_js(self, hwnd, script):
        self.webview2.exec_js(hwnd, script)

    def send_json(self, hwnd, jsonstr):
        self.webview2.send_json(hwnd, jsonstr)

#
# exsample
def message_handler(jsondata):
    if jsondata['msg'] == 'receive_json':

        if jsondata['json']['msg'] == "DOMContentLoaded":
            print("DOMContentLoaded")

        elif jsondata['json']['msg'] == "WM_DESTROY":
            print("WM_DESTROY")

        elif jsondata['json']['msg'] == "post_quit_message":
            print("post_quit_message")

        elif jsondata['json']['msg'] == "resize_window":
            print("resize_window")

        elif jsondata['json']['msg'] == "load_google":
            jsondata['sender'].load_url(jsondata['hwnd'], "https://www.google.com/")

        elif jsondata['json']['msg'] == "close_window":
            jsondata['sender'].close_window(jsondata['hwnd'])

        elif jsondata['json']['msg'] == "reload_page":
            jsondata['sender'].reload_page(jsondata['hwnd'])

        elif jsondata['json']['msg'] == "minimize_window":
            jsondata['sender'].minimize_window(jsondata['hwnd'])

        elif jsondata['json']['msg'] == "maximize_window":
            jsondata['sender'].maximize_window(jsondata['hwnd'])

        elif jsondata['json']['msg'] == "show_window":
            jsondata['sender'].show_window(jsondata['hwnd'])

        elif jsondata['json']['msg'] == "execute_js":
            jsondata['sender'].execute_js(jsondata['hwnd'], "alert(1);")

        elif jsondata['json']['msg'] == "send_json":
            jsondata['sender'].send_json(jsondata['hwnd'], '{"msg":"test"}')

        elif jsondata['json']['msg'] == "create_subwindow":
            jsondata['sender'].create_subwindow("https://www.google.com/", -1, -1, 600, 500)

        elif jsondata['json']['msg'] == "get_active_hwnd":
            hwnd = jsondata['sender'].get_active_hwnd()
            print(hwnd)

        elif jsondata['json']['msg'] == "get_all_hwnds":
            hwnds = jsondata['sender'].get_all_hwnds()
            print(hwnds)


def windows_windproc(hwnd, message, wparm, lparam) -> int:
    if message == win32con.WM_MOVE:
        print("WM_MOVE")
        return 0
    elif message == win32con.WM_SIZE:
        print("WM_SIZE")
        return 0
    elif message == win32con.WM_COPYDATA:
        print("Receive message")
        copystrct = ctypes.POINTER(COPYDATASTRUCT)
        pcds = ctypes.cast(lparam, copystrct)
        msgstr = ctypes.wstring_at(pcds.contents.lpData)
        print(json.loads(msgstr))
        return 0

    return -1


def main():
    use_windows_proc = False

    if use_windows_proc:
        # Advanced
        wv2 = WinWebV2(windows_windproc, use_windows_proc)
    else:
        # Default
        wv2 = WinWebV2(message_handler)

    target_path = os.path.join(os.path.dirname(__file__), '../example/html/index.html')
    url = os.path.abspath(target_path)
    wv2.create_window(url, -1, -1, 700, 600)


if __name__ == "__main__":
    main()
