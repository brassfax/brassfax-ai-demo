(function() {
  document.addEventListener("DOMContentLoaded", function() {

    // Create launcher button
    const button = document.createElement("div");
    button.style = "position:fixed;bottom:20px;right:20px;width:60px;height:60px;background:#2E3A59;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:9999;font-size:30px;";
    button.innerText = "💬";
    document.body.appendChild(button);

    // Create chat window
    const chatContainer = document.createElement("div");
    chatContainer.style = "position:fixed;bottom:90px;right:20px;width:400px;height:600px;box-shadow:0 0 10px rgba(0,0,0,0.2);border-radius:10px;overflow:hidden;z-index:9998;background:white;display:none;flex-direction:column;";

    chatContainer.innerHTML = `
      <div style="background:#2E3A59;color:#fff;padding:12px;text-align:center;font-weight:bold;">Brass Fax AI Assistant</div>
      <div id="messages" style="padding:10px;flex:1;overflow-y:auto;background:#fff;"></div>
      <div style="display:flex;border-top:1px solid #ddd;padding:10px;background:#f2f2f2;">
        <input id="userInput" type="text" placeholder="Ask a question..." style="flex:1;padding:10px;border:1px solid #ccc;border-radius:5px;">
        <button id="sendBtn" style="margin-left:10px;padding:10px 20px;background:#2E3A59;color:#fff;border:none;border-radius:5px;cursor:pointer;">Send</button>
      </div>
    `;

    document.body.appendChild(chatContainer);

    button.onclick = () => {
      chatContainer.style.display = chatContainer.style.display === "none" ? "flex" : "none";
    };

    function appendMessage(role, text) {
      const msgDiv = document.getElementById("messages");
      const message = document.createElement("div");
      message.style.marginBottom = "8px";
      message.style.textAlign = (role === "user") ? "right" : "left";
      message.textContent = text;
      msgDiv.appendChild(message);
      msgDiv.scrollTop = msgDiv.scrollHeight;
    }

    async function send() {
      const input = document.getElementById("userInput");
      const question = input.value.trim();
      if (!question) return;
      appendMessage("user", question);
      input.value = "";

      try {
        const res = await fetch("https://brassfax-ai-demo-production.up.railway.app/query", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ client_id: "brassfax_internal", question: question })
        });
        const data = await res.json();
        appendMessage("ai", data.answer);
      } catch {
        appendMessage("ai", "Sorry, there was an error connecting to Brass Fax.");
      }
    }

    document.getElementById("sendBtn").onclick = send;
    document.getElementById("userInput").addEventListener("keydown", function(e) {
      if (e.key === "Enter") send();
    });

  });
})();
