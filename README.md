# WinWebV2
## Python Webview2 GUI
### Create HTML User Interface using WinWebV2 in Python

<br><br><br>

## Windows10    
<pre>
python -m venv .\venv  
.\venv\Scripts\activate  
pip install WinWebV2
</pre>

<br>

### Sample File
<pre>
import WinWebV2

def message_handler(jsondata):
    print(jsondata)

wv2 = WinWebV2(message_handler)
url = 'Document Path'
wv2.create_window(url, -1, -1, 600, 400)
</pre>


<br><br><br>

Create DLL (VC++)  
Main (Python)

<br>

https://user-images.githubusercontent.com/10168979/151161912-bb0a36b8-05dd-4b5b-b6b5-1e90f69a7b90.mp4




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

<br><br><br><br><br><br>


