import os
import json
import win32con
import ctypes
from ctypes import wintypes
import WinWebV2


# exsample

class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', wintypes.LPARAM),
        ('cbData', wintypes.DWORD),
        ('lpData', ctypes.c_void_p)
    ]


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

        elif jsondata['json']['msg'] == "choose_file":
            fname = jsondata['sender'].choose_file()
            print(fname)

        elif jsondata['json']['msg'] == "choose_files":
            fname = jsondata['sender'].choose_file(True)
            print(fname)

        elif jsondata['json']['msg'] == "choose_directory":
            dname = jsondata['sender'].choose_directory()
            print(dname)

        elif jsondata['json']['msg'] == "save_dialog":
            fname = jsondata['sender'].save_dialog()
            print(fname)


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

