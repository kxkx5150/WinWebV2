#pragma once
#include <Windows.h>

#ifdef WEBV2DLL_EXPORTS
#define __DLL_PORT extern "C" __declspec(dllexport)
#else
#define __DLL_PORT extern "C" __declspec(dllimport)
#endif

__DLL_PORT int WebV2dllCreate(const TCHAR* url,
    int x = CW_USEDEFAULT, int y = CW_USEDEFAULT, 
    int width = CW_USEDEFAULT, int height = CW_USEDEFAULT);

__DLL_PORT HWND get_main_hwnd();
__DLL_PORT void resize_webview(HWND hWnd);
__DLL_PORT int get_webview_wmmsg_id();
__DLL_PORT void receive_randomid(int randomid);

__DLL_PORT void load_url(const TCHAR* url);

__DLL_PORT void exec_js(const TCHAR* script);
__DLL_PORT void set_startup_script(const TCHAR* script);

__DLL_PORT void send_json(const TCHAR* jsonstr);

__DLL_PORT void reload_page();

