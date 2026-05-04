(function(){
  function qs(sel){ return document.querySelector(sel); }
  function qsa(sel){ return Array.from(document.querySelectorAll(sel)); }
  const usersUl = qs('#usersList');
  const chatTitle = qs('#chatTitle');
  const chatContainer = qs('#chatContainer');
  const input = qs('#messageInput');
  const sendBtn = qs('#sendBtn');
  const status = qs('#status');

  let meId = window.CHAT.meId;
  let selectedUserId = null;
  let socket = null;

  function setStatus(s){ status.textContent = s; }

  // attach click handlers to user list
  qsa('.user-item').forEach(li=>{
    li.addEventListener('click', async ()=>{
      const uid = parseInt(li.dataset.userId);
      if (selectedUserId === uid) return;
      selectedUserId = uid;
      chatTitle.textContent = li.querySelector('.font-semibold').textContent;
      sendBtn.disabled = false;
      input.disabled = false;
      // clear container
      chatContainer.innerHTML = '';
      // clear unread badge
      const b = li.querySelector('.unread'); if (b){ b.classList.add('hidden'); b.textContent=''; }

      // load history
      try{
        const res = await fetch(`/messages/${uid}/history/`);
        const msgs = await res.json();
        msgs.forEach(appendMessage);
      }catch(e){
        console.error('history fetch failed', e);
      }

      // (re)open socket for this pair
      if (socket) { socket.close(); socket = null; }
      openSocket(uid);
    });
  });

  function appendMessage(msg){
    if (msg.deleted) return;
    if (document.getElementById('m-'+msg.id)) return; // dedupe
    const div = document.createElement('div');
    div.id = 'm-'+msg.id;
    div.className = 'bubble ' + (msg.sender_id === meId ? 'sent' : 'recv');
    const text = document.createElement('div');
    text.textContent = msg.content;
    div.appendChild(text);
    const meta = document.createElement('div');
    meta.className = 'msg-meta';
    meta.textContent = msg.timestamp;
    div.appendChild(meta);

    // if own message, show edit/delete
    if (msg.sender_id === meId){
      const controls = document.createElement('div');
      controls.style.marginTop = '6px';
      const edit = document.createElement('button');
      edit.textContent = 'Edit';
      edit.className = 'text-xs underline mr-2';
      edit.onclick = ()=> {
        const nc = prompt('Edit message', msg.content);
        if (nc !== null) {
          socket.send(JSON.stringify({action:'update_message', id: msg.id, content: nc}));
        }
      };
      const del = document.createElement('button');
      del.textContent = 'Delete';
      del.className = 'text-xs underline text-red-600';
      del.onclick = ()=> {
        if (confirm('Delete message?')) {
          socket.send(JSON.stringify({action:'delete_message', id: msg.id}));
        }
      };
      controls.appendChild(edit); controls.appendChild(del);
      div.appendChild(controls);
    }

    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function updateMessageUI(msg){
    const el = document.getElementById('m-'+msg.id);
    if (el){
      el.querySelector('div').textContent = msg.content;
    } else {
      appendMessage(msg);
    }
  }
  function deleteMessageUI(id){
    const el = document.getElementById('m-'+id);
    if (el) el.remove();
  }

  function openSocket(otherId){
    setStatus('Connecting...');
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const wsUrl = protocol + window.location.host + '/ws/chat/' + otherId + '/';
    socket = new WebSocket(wsUrl);

    socket.onopen = ()=> setStatus('Connected');
    socket.onclose = ()=> setStatus('Disconnected');

    socket.onmessage = (e) => {
      try{
        const payload = JSON.parse(e.data);
        if (payload.action === 'message'){
          const msg = payload.message;
          // if chat already open with this user, append; else bump unread
          if (selectedUserId && (msg.sender_id === selectedUserId || msg.receiver_id === selectedUserId)){
            appendMessage(msg);
          } else {
            // bump unread for sender
            const li = usersUl.querySelector(`[data-user-id="${msg.sender_id}"]`);
            if (li){
              const b = li.querySelector('.unread');
              b.classList.remove('hidden');
              const n = (parseInt(b.textContent || '0') || 0) + 1;
              b.textContent = n;
            }
          }
        } else if (payload.action === 'update'){
          updateMessageUI(payload.message);
        } else if (payload.action === 'delete'){
          deleteMessageUI(payload.id);
        }
      }catch(err){ console.error(err); }
    };
  }

  sendBtn.addEventListener('click', ()=>{
    if (!selectedUserId) { alert('Select a user'); return; }
    const text = input.value.trim();
    if (!text) return;
    socket.send(JSON.stringify({action:'send_message', content: text}));
    input.value = '';
  });

  input.addEventListener('keydown', e => { if (e.key === 'Enter') sendBtn.click(); });

  // disable controls until user chosen (initial)
  sendBtn.disabled = true;
  input.disabled = true;
})();
