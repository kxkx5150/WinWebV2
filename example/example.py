import WinWebV2
import os

def message_handler(jsondata):
    if jsondata['msg'] == 'receive_json':

        if jsondata['json']['msg'] == "DOMContentLoaded":
            print("DOMContentLoaded")

        elif jsondata['json']['msg'] == "WM_DESTROY":
            print("WM_DESTROY")

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


def main():
    wv2 = WinWebV2(message_handler)
    target_path = os.path.join(os.path.dirname(__file__), 'html/index.html')
    url = os.path.abspath(target_path)
    wv2.create_window(url, -1, -1, 700, 600)


if __name__ == "__main__":
    main()

    