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
}
init();
