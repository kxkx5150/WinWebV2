// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include <combaseapi.h>
#include <commctrl.h>
#include <stdlib.h>
#include <string>
#include <tchar.h>
#include <wil/com.h>
#include <wrl.h>
#include "WebV2dll.h"
#include "WebView2.h"
#pragma comment(lib, "comctl32.lib")

HINSTANCE hInst;
HWND g_hwnd = nullptr;
int g_randomid = 0;
const TCHAR* strClassName = TEXT("CREATE_WEBVIEW2");
#define WM_WEBV_USER (WM_USER + 0)
std::wstring g_startup_script = L"";

using namespace Microsoft::WRL;
static wil::com_ptr<ICoreWebView2> webviewWindow;
static wil::com_ptr<ICoreWebView2_2> m_webView2;
static wil::com_ptr<ICoreWebView2Controller> webviewController;

BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD ul_reason_for_call,
    LPVOID lpReserved)
{
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

void receive_randomid(int randomid)
{
    g_randomid = randomid;
}
void webview_settings()
{
    ICoreWebView2Settings* Settings;
    webviewWindow->get_Settings(&Settings);
    Settings->put_IsScriptEnabled(TRUE);
    Settings->put_AreDefaultScriptDialogsEnabled(TRUE);
    Settings->put_IsWebMessageEnabled(TRUE);
}
void resize_webview(HWND hWnd)
{
    if (webviewController != nullptr) {
        RECT bounds;
        GetClientRect(hWnd, &bounds);
        webviewController->put_Bounds(bounds);
    };
}
int get_webview_wmmsg_id()
{
    return WM_WEBV_USER;
}
void set_str_to_copydata(std::wstring s)
{
    TCHAR* buffer = new TCHAR[s.length() + 1];
    wcscpy_s(buffer, s.length() + 1, s.c_str());
    COPYDATASTRUCT data_to_send = { 0 };
    data_to_send.dwData = g_randomid;
    data_to_send.cbData = (DWORD)8191;
    data_to_send.lpData = buffer;
    SendMessage(g_hwnd, WM_COPYDATA, 0, (LPARAM)&data_to_send);
    delete[] buffer;
}
HWND get_main_hwnd()
{
    return g_hwnd;
}
void load_url(const TCHAR* url)
{
    webviewWindow->Navigate(url);
}
void exec_js(const TCHAR* script)
{
    webviewWindow->ExecuteScript(script,
        Callback<ICoreWebView2ExecuteScriptCompletedHandler>([](HRESULT error, PCWSTR result) -> HRESULT {
            return S_OK;
        }).Get());
}
void send_json(const TCHAR* jsonstr)
{
    webviewWindow->PostWebMessageAsJson(jsonstr);
}
void set_startup_script(const TCHAR* script)
{
    g_startup_script = script;
}
void reload_page()
{
    webviewWindow->Reload();
}
void CHECK_FAILURE(HRESULT hr)
{
    if (FAILED(hr)) {
        std::wstring message;
        message = std::wstring(L"Something went wrong.");
        MessageBoxW(nullptr, message.c_str(), nullptr, MB_OK);
    }
}
void webview_events()
{
    EventRegistrationToken token;
    webviewWindow->add_WebMessageReceived(
        Callback<ICoreWebView2WebMessageReceivedEventHandler>(
            [](ICoreWebView2* webview, ICoreWebView2WebMessageReceivedEventArgs* args) -> HRESULT {
                wil::unique_cotaskmem_string source;
                CHECK_FAILURE(args->get_Source(&source));
                wil::unique_cotaskmem_string webMessageAsJson;
                CHECK_FAILURE(args->get_WebMessageAsJson(&webMessageAsJson));
                Sleep(200);
                set_str_to_copydata(webMessageAsJson.get());
                return S_OK;
            })
            .Get(),
        &token);
    webviewWindow->AddScriptToExecuteOnDocumentCreated(g_startup_script.c_str(),
        Callback<ICoreWebView2AddScriptToExecuteOnDocumentCreatedCompletedHandler>(
            [](HRESULT error, PCWSTR id) -> HRESULT {
                return S_OK;
            })
            .Get());
    EventRegistrationToken m_DOMContentLoadedToken;
    webviewWindow->QueryInterface(IID_PPV_ARGS(&m_webView2));
    m_webView2->add_DOMContentLoaded(
        Callback<ICoreWebView2DOMContentLoadedEventHandler>(
            [](ICoreWebView2* sender, ICoreWebView2DOMContentLoadedEventArgs* args) -> HRESULT {
                std::wstring msgstr = L"{\"msg\"\:\"DOMContentLoaded\"}";
                set_str_to_copydata(msgstr);
                return S_OK;
            })
            .Get(),
        &m_DOMContentLoadedToken);
}
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message) {
    case WM_DESTROY:
        PostQuitMessage(0);
        break;

    default:
        break;
    }

    return DefWindowProc(hWnd, message, wParam, lParam);
}
void init_webview2(HWND hWnd, const TCHAR* url)
{
    CreateCoreWebView2EnvironmentWithOptions(nullptr, nullptr, nullptr,
        Callback<ICoreWebView2CreateCoreWebView2EnvironmentCompletedHandler>(
            [hWnd, url](HRESULT result, ICoreWebView2Environment* env) -> HRESULT {
                env->CreateCoreWebView2Controller(hWnd,
                    Callback<ICoreWebView2CreateCoreWebView2ControllerCompletedHandler>(
                        [hWnd, url](HRESULT result, ICoreWebView2Controller* controller) -> HRESULT {
                            if (controller != nullptr) {
                                webviewController = controller;
                                webviewController->get_CoreWebView2(&webviewWindow);
                            }
                            webview_settings();
                            resize_webview(hWnd);
                            load_url(url);
                            webview_events();
                            return S_OK;
                        })
                        .Get());
                return S_OK;
            })
            .Get());
}
int WebV2dllCreate(const TCHAR* url, int x, int y, int width, int height)
{

    HINSTANCE hInstance = GetModuleHandle(0);
    WNDCLASS winc;
    winc.style = CS_HREDRAW | CS_VREDRAW | CS_DBLCLKS;
    winc.lpfnWndProc = WndProc;
    winc.cbClsExtra = winc.cbWndExtra = 0;
    winc.hInstance = hInstance;
    winc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    winc.hCursor = LoadCursor(NULL, IDC_ARROW);
    winc.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
    winc.lpszMenuName = NULL;
    winc.lpszClassName = strClassName;
    if (!RegisterClass(&winc))
        return 0;

    if (x == -1 || y == -1) {
        x = CW_USEDEFAULT;
        y = CW_USEDEFAULT;
    }
    g_hwnd = CreateWindow(
        strClassName, TEXT(""),
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        x, y, width, height,
        NULL, NULL, hInstance, NULL);

    if (g_hwnd == NULL)
        return 0;

    init_webview2(g_hwnd, url);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        DispatchMessage(&msg);
    }
    return (int)msg.wParam;
}
