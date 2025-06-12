(function () {
  console.log("Starting Brass Fax Widget Loader");

  document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded, attempting to build chat widget...");

    try {
      const apiUrl = "https://brassfax-ai-demo-production.up.railway.app/query";
      const clientId = "brassfax_internal";

      // Create launcher button
      const button = document.createElement("div");
      button.style.cssText =
        "position:fixed;bottom:20px;right:20px;width:60px;height:60px;background:#2E3A59;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:9999;font-size:30px;";
      button.innerText = "💬";
      document.body.appendChild(button);
      console.log("Launcher button created and added to DOM");

      // Create chat container (initially hidden)
      const chatContainer = document.createElement("div");
      chatContainer.style.cssText =
        "position:fixed;bottom:90px;right:20px;width:400px;height:600px;box-shadow:0 0 10px rgba(0,0,0,0.2);border-radius:10px;overflow:hidden;z-index:9998;background:white;display:none;flex-direction:column;";
      document.body.appendChild(chatContainer);
      console.log("Chat container created and added to DOM");

      // Header
      const header = document.createElement("div");
      header.style.cssText =
        "background:#2E3A59;color:#fff;padding:12px;text-align:center;font-weight:bold;";
      header.innerText = "Brass Fax AI Assistant";
      chatContainer.appendChild(header);
      console.log("Header injected");

      // Messages area
      const messages = document.createElement("div");
      messages.id = "brassfax-messages";
      messages.style.cssText = "padding:10px;flex:1;overflow-y:auto;background:#fff;";
      chatContainer.appendChild(messages);
      console.log("Messages area injected");

      // Input area
      const inputArea = document.createElement("div");
      inputArea.style.cssText =
        "display:flex;border-top:1px solid #ddd;padding:10px;background:#f2f2f2;";
      chatContainer.appendChild(inputArea);
      console.log("Input area injected");

      const userInput = document.createElement("input");
      userInput.type = "text";
      userInput.placeholder = "Ask a question...";
      userInput.style.cssText =
        "flex:1;padding:10px;border:1px solid #ccc;border-radius:5px;";
      inputArea.appendChild(userInput);

      const sendBtn = document.createElement("button");
      sendBtn.innerText = "Send";
      sendBtn.style.cssText =
        "margin-left:10px;padding:10px 20px;background:#2E3A59;color:#fff;border:none;border-radius:5px;cursor:pointer;";
      inputArea.appendChild(sendBtn);
      console.log("Input + Send button injected");

      // Append message helper
      function appendMessage(role, text) {
        const message = document.createElement("div");
        message.style.marginBottom = "8px";
        message.style.textAlign = role === "user" ? "right" : "left";
        message.textContent = text;
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
      }

      // Send logic
      async function send() {
        const question = userInput.value.trim();
        if (!question) return;
        appendMessage("user", question);
        userInput.value = "";

        try {
          const res = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ client_id: clientId, question: question }),
          });
          const data = await res.json();
          appendMessage("ai", data.answer);
        } catch (err) {
          console.error("Error fetching from backend", err);
          appendMessage("ai", "Sorry, there was an error connecting to Brass Fax.");
        }
      }

      sendBtn.onclick = send;
      userInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") send();
      });

      // Toggle chat open/close
      button.onclick = () => {
        chatContainer.style.display =
          chatContainer.style.display === "none" ? "flex" : "none";
      };

      console.log("Widget fully initialized ✅");
    } catch (err) {
      console.error("Fatal widget initialization error:", err);
    }
  });
})();
