const converter = new showdown.Converter();
let ws;
let response = "";
let conversationStarted = false;

function setButton(value, disabled) {
    var button = document.getElementById('send');
    button.innerHTML = value;
    button.disabled = disabled
    if(disabled) {
        button.classList.add("blink_me");
    } else {
        button.classList.remove("blink_me");
    }
}

function sendMessage(event) {
    event.preventDefault();

    if (!ws) return;
    conversationStarted = true;
    var message = document.getElementById('messageText').value;
    var temp = document.getElementById('tempValue').innerHTML;
    if (message === "") {
        return;
    }
    payload = {
        query: message,
        temperature: parseFloat(temp)
    }
    console.log(payload)
    ws.send(JSON.stringify(payload));
    setButton("{{ res.BUTTON_PROCESSING }}", true)
}

function appendCopy() {
    var messages = document.getElementById('messages');
    var div = messages;

    var span = document.createElement('span');
    span.innerHTML="<span class='btn btn-primary clip-button' onclick='copy()'><img src='/static/img/copy.svg'>&nbsp;Copy to clipboard</span>"
    div.appendChild(span);
}

function copy() {
    var messages = document.getElementById('messages');
    var div = messages.firstChild.firstChild;
    content = div.innerText; 
    navigator.clipboard.writeText(content);
    alert("Copied response to clipboard.")
}

function updateResponseTokens() {
    responseTokenCountValue = document.getElementById("responseTokenCountValue");
    encoded = llamaTokenizer.encode(response)
    responseTokenCountValue.innerText=encoded.length;
    responseTokenCount.classList.remove("d-none");
}

function hideResponseTokens() {
    responseTokenCount = document.getElementById("responseTokenCount");
    responseTokenCount.classList.add("d-none");
}

function connect() {
    ws = new WebSocket("{{ wsurl }}/inference");
    ws.onmessage = function (event) {
        var messages = document.getElementById('messages');
        var data = JSON.parse(event.data);
        handleResBotResponse(data ,messages)

        // Scroll to the bottom of the chat
        messages.scrollTop = messages.scrollHeight;
    };
    ws.onopen = function() {
        setButton("{{ res.BUTTON_SEND }}", false);
    };

    ws.onclose = function(e) {
        setButton("{{ res.BUTTON_WAIT }}", true);
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function() {
            connect();
        }, 1000);
    };
}

function handleResBotResponse(data, messages) {
    switch(data.type) {
        case "start":
            messages.innerHTML = '';
            response = "";
            var div = document.createElement('div');
            div.className = 'server-message';
            var p = document.createElement('p');
            response += data.message;
            p.innerHTML = converter.makeHtml(response);
            div.appendChild(p);
            messages.appendChild(div);
            updateResponseTokens();
            break;

        case "stream":
            setButton("{{ res.BUTTON_TYPING }}", true);
            var p = messages.lastChild.lastChild;
            response += data.message;
            p.innerHTML = converter.makeHtml(response);
            updateResponseTokens();
            break;

        case "end":
            var p = messages.lastChild.lastChild;
            p.innerHTML = converter.makeHtml(response);
            setButton("{{ res.BUTTON_SEND }}", false);
            updateResponseTokens();
            appendCopy();
            break;

        case "info":
            messages.innerHTML = '';
            var div = document.createElement('div');
            div.className = 'server-message';
            var p = document.createElement('p');
            // p.innerHTML = converter.makeHtml(data.message);
            p.innerHTML = data.message;
            div.appendChild(p);
            messages.appendChild(div);
            hideResponseTokens();
            break;

        case "system":
            messages.innerHTML = '';
            var div = document.createElement('div');
            div.className = 'server-message';
            var p = document.createElement('p');
            p.innerHTML = data.message;
            div.appendChild(p);
            messages.appendChild(div);
            hideResponseTokens();
            setButton("{{ res.BUTTON_SEND }}", false);
            break;

        case "error":
            messages.innerHTML = '';
            var div = document.createElement('div');
            div.className = 'server-message';
            var p = document.createElement('p');
            // p.innerHTML = converter.makeHtml(data.message);
            p.innerHTML = data.message;
            div.appendChild(p);
            messages.appendChild(div);
            hideResponseTokens();
            setButton("{{ res.BUTTON_SEND }}", false);
            break;
    }
}

document.addEventListener("DOMContentLoaded", function(event) {
    const slider = document.getElementById("tempSlider");
    const label = document.getElementById("tempValue");
    slider.addEventListener("input", () => {
        label.innerText=slider.value;
    });

    const button = document.getElementById('send');
    const tokenCount = document.getElementById("tokenCount");
    const tokenCountValue = document.getElementById("tokenCountValue");
    const messageText = document.getElementById("messageText");
    messageText.addEventListener("input", () => {
        encoded = llamaTokenizer.encode(messageText.value)
        if (encoded.length > 0) {
            tokenCount.classList.remove("d-none");
            tokenCountValue.innerText=encoded.length
        } else {
            tokenCount.classList.add("d-none");
        }
        if (encoded.length > {{ conf.CONTEXT_TOKENS }}) {
            button.disabled = true;
            tokenCount.classList.add("tokenLimitExceeded");
        } else {
            button.disabled = false;
            tokenCount.classList.remove("tokenLimitExceeded");
        }
    });

    connect();
});
