const chatcontainer = document.querySelector('#chatcontainer');
const messageinput = document.querySelector("#messageInput");
const chatimage = document.querySelector("#imageInput");
const sendbut = document.getElementById("sendBtn");

function createChatBox(html, classes) {
  const div = document.createElement("div");
  div.innerHTML = html;
  div.classList.add(classes);
  return div;
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      resolve({
        base64: reader.result.split(",")[1],
        mimeType: file.type
      });
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

// Send request to backend
async function handleAIResponse(message, imagefile) {
  let imageData = null;
  if (imagefile) imageData = await fileToBase64(imagefile);

  const res = await fetch("http://localhost:3000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      image: imageData ? imageData.base64 : null,
      mimeType: imageData ? imageData.mimeType : null
    })
  });

  const data = await res.json();
  if (data.error) return "Error: " + data.error;
  return data.reply;
}

// Render a chat message (user or AI)
function renderMessage(message, imgSrc, isUser = true) {
  let html = `<div class="${isUser ? "userchatarea" : "aichatarea"}">`;
  if (message) html += `<p>${message}</p>`;
  if (imgSrc) html += `<img src="${imgSrc}" alt="Image" style="max-width:200px; display:block; margin-top:5px;">`;
  html += `</div>`;
  html += `<img src="${isUser ? userImageUrl : aiImageUrl}" class="chat-avatar">`;

  const chatbox = createChatBox(html, isUser ? "userchatbox" : "aichatbox");
  chatcontainer.appendChild(chatbox);
  chatcontainer.scrollTop = chatcontainer.scrollHeight;
}

// Main chat handler
async function handleChatArea(message, imagefile) {
  if (!message.trim() && !imagefile) return;

  const userImgURL = imagefile ? URL.createObjectURL(imagefile) : null;
  renderMessage(message, userImgURL, true);

  // AI loading
  const loadingHTML = `<img src="${aiImageUrl}" class="chat-avatar">
  <div class="aichatarea"><div class="spinner"></div></div>
                       `;
  const botchat = createChatBox(loadingHTML, "aichatbox");
  chatcontainer.appendChild(botchat);
  chatcontainer.scrollTop = chatcontainer.scrollHeight;

  // AI response
  const reply = await handleAIResponse(message, imagefile);

  // Parse reply: check if AI returned image data in Base64
  let replyText = reply;
  let aiImageSrc = null;

  // If the AI includes "data:image" URL, split it
  const dataMatch = reply.match(/data:image\/[a-zA-Z]+;base64,[^"\s]+/);
  if (dataMatch) {
    aiImageSrc = dataMatch[0];
    replyText = reply.replace(aiImageSrc, "");
  }

  botchat.querySelector(".aichatarea").innerHTML = marked.parse(replyText);
  if (aiImageSrc) {
    const img = document.createElement("img");
    img.src = aiImageSrc;
    img.style.maxWidth = "200px";
    img.style.display = "block";
    img.style.marginTop = "5px";
    botchat.querySelector(".aichatarea").appendChild(img);
  }

  document.querySelectorAll("pre code").forEach(el => hljs.highlightElement(el));
  chatcontainer.scrollTop = chatcontainer.scrollHeight;
}

// Send message
function sendMessage() {
  handleChatArea(messageinput.value, chatimage.files[0]);
  messageinput.value = "";
  chatimage.value = "";
}

// Event listeners
messageinput.addEventListener('keydown', e => {
  if (e.key === 'Enter') sendMessage();
});
sendbut.addEventListener('click', sendMessage);
