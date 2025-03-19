// Listen for "Enter" key press
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevents form submission (if inside a form)
        sendMessage();  // Calls the sendMessage function
    }
});

async function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");
    let loadingIndicator = document.getElementById("loading");

    // Append user's message as a chat bubble
    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    document.getElementById("user-input").value = "";
    // Create typing indicator
    let typingIndicator = document.createElement("div");
    typingIndicator.classList.add("message", "bot-message", "typing-indicator");
    typingIndicator.innerHTML = '<span></span><span></span><span></span>';
    chatBox.appendChild(typingIndicator);

    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll

    try {
        let response = await fetch("http://127.0.0.1:8080/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        });

        let data = await response.json();
        let chatbotResponse = data.response || "Error: No response from server.";

        //remove typing indicator
        chatBox.removeChild(typingIndicator);

        // Append bot's response as a chat bubble
        let botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot-message");
        botMessage.textContent = chatbotResponse;
        chatBox.appendChild(botMessage);

    } catch (error) {
        let errorMessage = document.createElement("div");
        errorMessage.classList.add("message", "bot-message");
        errorMessage.textContent = "Error connecting to server.";
        chatBox.appendChild(errorMessage);
    } finally {
        loadingIndicator.style.display = "none";  // Hide loading animation
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to latest message
    }

}
