# WinWebV2
## Python Webview2 GUI

Windows10

<br>

## WIP

<br>

Create DLL (VC++)  
Main (Python)

<br><br>

## Sample

<pre>


def main():  
    url = os.path.abspath("html/index.html")

    wv2 = WinWebV2(message_handler)
    wv2.create_window(url, -1, -1, 600, 400)
    # (x = -1 or y = -1) == CW_USEDEFAULT

    # execute script
    wv2.set_startup_js('alert(0);')
    wv2.execute_js('alert(0);')


def message_handler(jsondata):
    print(jsondata)
    pass


</pre>

<br><br><br>

## Class

<pre>

    class WinWebV2

        create_window(
            x,
            y,
            width,
            height
        )

        execute_js(
            string
        )

        set_startup_js(
            string
        )

        send_json(
            string
        )

        reload_page()


</pre>

<br>

## Communication

<pre>

    --- js ---
 
    window.chrome.webview.postMessage(message);
    window.chrome.webview.addEventListener('message', messageHandler);



    --- pythoon ---

    WinWebV2.send_json('{ "msg" : "Hello world" }')
    def message_handler(jsondata):


</pre>

<br><br><br>

## Events
<pre>

message_handler

{'msg': 'DOMContentLoaded'}
{'msg': 'WM_DESTROY'}

</pre>


