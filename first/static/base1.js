const chatContainer = document.getElementById("chatcontainer");
const sendBtn = document.getElementById("sendBtn");
const messageInput = document.getElementById("messageInput");

sendBtn.addEventListener("click", async () => {
  const userMessage = messageInput.value.trim();
  if (!userMessage) return;

  // show user message
  addMessage(userMessage, userImageUrl);

  // send to backend
  const response = await fetch("/chatbot-page/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage }),
  });

  const data = await response.json();
  addMessage(data.reply || "Error from API", aiImageUrl);

  messageInput.value = "";
});

function addMessage(text, avatar) {
  const box = document.createElement("div");
  box.className = "aichatbox";
  box.innerHTML = `
    <img src="${avatar}" class="chat-avatar">
    <div class="aichatarea">${text}</div>
  `;
  chatContainer.appendChild(box);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}
async function sendMessage() {
  const messageInput = document.getElementById("messageInput");
  const userMessage = messageInput.value.trim();
  if (!userMessage) return;

  // show user message
  addMessage(userMessage, true);

  // send to backend
  const response = await fetch("/chatbot-api/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage })
  });

  const data = await response.json();
  const botReply = data.reply || "Error: No reply";

  // show bot reply
  addMessage(botReply, false);

  messageInput.value = "";
}
