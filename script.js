const form = document.getElementById("chat-form");
const input = document.getElementById("input");
const messages = document.getElementById("messages");

function addMessage(text, who) {
    const div = document.createElement("div");
    div.className = "msg " + who;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = input.value.trim();
    addMessage(text, "me");
    input.value = "";

    addMessage("...", "bot"); // temporary loading

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    });

    const data = await res.json();

    // replace last bot placeholder
    const lastBot = messages.querySelectorAll(".bot");
    lastBot[lastBot.length - 1].textContent = data.reply || data.error;
});
