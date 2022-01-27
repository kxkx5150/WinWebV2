const messageHandler = event => {
    let msg = event.data.msg;

    switch (msg) {
        case "test":
            console.log("test");
            break;

        default:
            console.log(`Received unexpected message: ${JSON.stringify(event.data)}`);
    }
};
function OnFileSelect(inptelem) {
    Array.prototype.forEach.call(inptelem.files, (file) => {
        const fileReader = new FileReader();
        fileReader.onload = function () {
            sendMSG("base64", "image", this.result);
        };
        fileReader.readAsDataURL(file);
    });
}
function sendMSG(msg, type = "", base64 = "") {
    const message = {
        msg: msg,
        type:type,
        base64: base64
    };
    window.chrome.webview.postMessage(message);
}
function init() {
    window.chrome.webview.addEventListener('message', messageHandler);
    sendMSG("Hello world");

    document.getElementById("load_google").addEventListener("click",(e)=>{
        sendMSG("load_google");
    })
    document.getElementById("close_window").addEventListener("click",(e)=>{
        sendMSG("close_window");
    })
    document.getElementById("minimize_window").addEventListener("click",(e)=>{
        sendMSG("minimize_window");
    })
    document.getElementById("maximize_window").addEventListener("click",(e)=>{
        sendMSG("maximize_window");
    })

    document.getElementById("execute_js").addEventListener("click",(e)=>{
        sendMSG("execute_js");
    })
    document.getElementById("send_json").addEventListener("click",(e)=>{
        sendMSG("send_json");
    })
    document.getElementById("reload_page").addEventListener("click",(e)=>{
        sendMSG("reload_page");
    })
}
init();
