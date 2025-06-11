(function() {
  // Create launcher button
  const button = document.createElement("div");
  button.style = "position:fixed;bottom:20px;right:20px;width:60px;height:60px;background:#2E3A59;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:9999;font-size:30px;";
  button.innerText = "💬";
  document.body.appendChild(button);

  // Create iframe container (hidden by default)
  const iframeContainer = document.createElement("div");
  iframeContainer.style = "position:fixed;bottom:90px;right:20px;width:400px;height:600px;box-shadow:0 0 10px rgba(0,0,0,0.2);border-radius:10px;overflow:hidden;z-index:9998;display:none;";
  document.body.appendChild(iframeContainer);

  const iframe = document.createElement("iframe");
  iframe.src = "https://your-domain.com/chat.html"; // we'll build this next
  iframe.width = "100%";
  iframe.height = "100%";
  iframe.frameBorder = "0";
  iframeContainer.appendChild(iframe);

  // Toggle chat open/close
  button.onclick = () => {
    iframeContainer.style.display = iframeContainer.style.display === "none" ? "block" : "none";
  };
})();