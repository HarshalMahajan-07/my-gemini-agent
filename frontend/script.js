// Replace this after backend deployment (example: "https://my-agent.onrender.com")
const BACKEND_URL = "https://YOUR_BACKEND_URL/chat";

const inputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const messagesEl = document.getElementById("messages");

function appendMessage(sender, text) {
    const wrapper = document.createElement("div");
    wrapper.className = sender === "You" ? "msg user" : "msg ai";
    wrapper.innerHTML = `<strong>${sender}:</strong> <span>${text}</span>`;
    messagesEl.appendChild(wrapper);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;

    appendMessage("You", text);
    inputEl.value = "";
    inputEl.focus();

    try {
        const res = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: text }),
        });

        if (!res.ok) {
            appendMessage("AI", "Error: backend returned " + res.status);
            return;
        }

        const data = await res.json();
        appendMessage("AI", data.reply);
    } catch (err) {
        appendMessage("AI", "Network error: " + err.message);
    }
}

sendBtn.addEventListener("click", sendMessage);

inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});
