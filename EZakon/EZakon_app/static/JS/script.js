function ShowMenu() {
  const menu = document.getElementById("menu");

  menu.classList.toggle("open");
}

const ChatForm = document.getElementById("chat-form");
const ChatWindow = document.getElementById("chat-window");
const UserInput = document.getElementById("user-input");

const csrftoken = document.querySelector("[name=csrf-token]").content;

function showTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("chat-message", "bot", "typing-indicator");
  typingDiv.id = "typing-indicator";
  typingDiv.innerHTML = `
    <span class="dot"></span>
    <span class="dot"></span>
    <span class="dot"></span>
  `;
  ChatWindow.appendChild(typingDiv);
  ChatWindow.scrollTop = ChatWindow.scrollHeight;
  return typingDiv;
}

function removeTypingIndicator() {
  const typingIndicator = document.getElementById("typing-indicator");
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

function Message(text, sender) {
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("chat-message", sender);

  if (Array.isArray(text)) {
    text.forEach((part, index) => {
      const partDiv = document.createElement("div");
      partDiv.innerHTML = part.replace(/\n/g, "<br>");
      partDiv.style.marginBottom = index < text.length - 1 ? "0.5em" : "0";
      messageContainer.appendChild(partDiv);
    });
  } else if (typeof text === "string") {
    messageContainer.innerHTML = text.replace(/\n/g, "<br>");
  } else {
    messageContainer.textContent = "Некорректный формат ответа";
  }

  ChatWindow.appendChild(messageContainer);
  ChatWindow.scrollTop = ChatWindow.scrollHeight;
}

ChatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const UserMessage = UserInput.value.trim();
  if (!UserMessage) return; 

  Message(UserMessage, "user");
  UserInput.value = "";

  showTypingIndicator();

  try {
    const response = await fetch("/chat_with_ai/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ message: UserMessage }),
    });

    removeTypingIndicator();

    if (response.status === 401) {
      Message(
        "❌ Требуется вход в аккаунт. Пожалуйста, войдите для использования чата.",
        "bot"
      );
      return;
    }

    if (!response.ok) {
      const errorData = await response.json();
      const errorMessage = errorData.error || `Ошибка ${response.status}`;
      Message(`❌ ${errorMessage}`, "bot");
      return;
    }

    const data = await response.json();

    if (data.error) {
      Message(`❌ ${data.error}`, "bot");
      return;
    }

    if (data.reply) {
      Message(data.reply, "bot");
    } else {
      Message("❌ Получен пустой ответ от сервера", "bot");
    }
  } catch (error) {
    removeTypingIndicator();
    console.error("Ошибка:", error);
    Message(
      "❌ Ошибка при подключении к серверу. Пожалуйста, проверьте соединение и попробуйте позже.",
      "bot"
    );
  }
});
const Test = document.getElementById("forma");
if (Test) {
  Test.addEventListener("post", function (e) {
    e.preventDefault();
  });
}
