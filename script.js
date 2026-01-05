const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const typing = document.getElementById("typing");

input.addEventListener("keypress", function(e) {
  if (e.key === "Enter") sendMessage();
});

function addMessage(text, className) {
  const div = document.createElement("div");
  div.className = className;
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user-message");
  input.value = "";

  typing.style.display = "block";

  fetch("/api/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-KEY": "chatbot-uas-2025"
  },
  body: JSON.stringify({ message })
});
}
