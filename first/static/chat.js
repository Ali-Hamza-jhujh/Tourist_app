document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chatcontainer");
    const sendBtn = document.getElementById("sendBtn");
    const messageInput = document.getElementById("messageInput");
    const receiverId = document.getElementById("receiver-id").value;
    const currentUserId = document.getElementById("user-id").value;
    const csrftoken = getCookie("csrftoken");

    let isEditing = false;   // 🔹 New flag
    let refreshInterval;     // 🔹 Store setInterval reference

    // ========== SEND MESSAGE ==========
    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage();
    });

    function sendMessage() {
        let content = messageInput.value.trim();
        if (!content) return;

        fetch("/chat/send/", {
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            body: new URLSearchParams({ content, receiver_id: receiverId })
        })
            .then(res => res.json())
            .then(() => {
                messageInput.value = "";
                loadMessages();
            });
    }

    // ========== LOAD MESSAGES ==========
    function loadMessages() {
        if (isEditing) return; // 🔹 Don’t reload while editing

        fetch(`/chat/${receiverId}/fetch/`)
            .then(res => res.json())
            .then(data => {
                chatContainer.innerHTML = "";
                data.forEach(msg => {
                    const div = document.createElement("div");
                    div.className = "flex " + (msg.sender_id == currentUserId ? "justify-end" : "justify-start");

                    const localTime = new Date(msg.timestamp)
                        .toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

                    let messageText = msg.deleted
                        ? `<i class="text-gray-400">This message was deleted</i>`
                        : msg.content;

                    div.innerHTML = `
                      <div class="message-wrapper relative p-3 rounded-lg shadow max-w-md w-fit break-words
                          ${msg.sender_id == currentUserId ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"}"
                          data-id="${msg.id}">
                          
                          <span class="content block">${messageText}</span>
                          ${msg.edited && !msg.deleted ? '<span class="text-xs italic">(edited)</span>' : ''}

                          ${msg.sender_id == currentUserId && !msg.deleted ? `
                              <div class="flex gap-3 mt-2 text-xs">
                                  <a href="#" class="edit-btn text-yellow-200 hover:text-yellow-400">Edit</a>
                                  <a href="#" class="delete-btn text-red-200 hover:text-red-400">Delete</a>
                              </div>
                          ` : ""}

                          <div class="timestamp text-[10px] opacity-70 mt-1">${localTime}</div>
                      </div>
                  `;
                    chatContainer.appendChild(div);
                });
                attachEventListeners();
                chatContainer.scrollTop = chatContainer.scrollHeight;
            });
    }

    // ========== AUTO REFRESH ==========
    function startAutoRefresh() {
        refreshInterval = setInterval(loadMessages, 2000);
    }
    function stopAutoRefresh() {
        clearInterval(refreshInterval);
    }
    startAutoRefresh();
    loadMessages();

    // ========== EDIT & DELETE ==========
    function attachEventListeners() {
        document.querySelectorAll(".edit-btn").forEach(btn => {
            btn.onclick = function (e) {
                e.preventDefault();
                stopAutoRefresh();   // 🔹 Pause refresh
                isEditing = true;

                const wrapper = this.closest(".message-wrapper");
                const contentSpan = wrapper.querySelector(".content");
                const oldText = contentSpan.innerText;

                const input = document.createElement("input");
                input.type = "text";
                input.value = oldText;
                input.className = "border rounded px-2 py-1 w-full text-black mt-1";

                contentSpan.replaceWith(input);
                input.focus();

                input.addEventListener("keydown", (e) => {
                    if (e.key === "Enter") {
                        fetch(`/message/${wrapper.dataset.id}/edit/`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": csrftoken
                            },
                            body: JSON.stringify({ content: input.value })
                        })
                            .then(res => res.json())
                            .then(data => {
                                if (data.status === "success") {
                                    isEditing = false;
                                    startAutoRefresh(); // 🔹 Resume refresh
                                    loadMessages();
                                }
                            });
                    }
                    if (e.key === "Escape") { 
                        // cancel editing
                        isEditing = false;
                        startAutoRefresh();
                        loadMessages();
                    }
                });
            };
        });

        document.querySelectorAll(".delete-btn").forEach(btn => {
            btn.onclick = function (e) {
                e.preventDefault();
                const wrapper = this.closest(".message-wrapper");
                fetch(`/message/${wrapper.dataset.id}/delete/`, {
                    method: "POST",
                    headers: { "X-CSRFToken": csrftoken }
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === "success") {
                            loadMessages();
                        }
                    });
            };
        });
    }

    // ========== HELPER ==========
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
