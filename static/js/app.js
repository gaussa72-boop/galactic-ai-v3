async function sendMsg() {
    const input = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');
    const msg = input.value;
    if (!msg) return;

                         `<div style="color: gold; margin-bottom: 10px;"><b>Du:</b> ${msg}</div>`;
    input.value = '';

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({msg: msg})
    });
    const data = await response.json();

    const aiDiv = document.createElement('div');
    aiDiv.style.color = '#fff';
    aiDiv.innerHTML = `<b>IONOS-7:</b> ${data.reply}`;
    chatLog.appendChild(aiDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}
