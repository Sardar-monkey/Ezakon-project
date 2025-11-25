function ShowMenu() {
  const menu = document.getElementById("menu");

  menu.classList.toggle("open");
}

const ChatForm = document.getElementById("chat-form");
const ChatWindow = document.getElementById("chat-window");
const UserInput = document.getElementById("user-input");

// CSRF
const csrftoken = document.querySelector("[name=csrf-token]").content;

// Функция для создания typing индикатора
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

// Функция для удаления typing индикатора
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
      // Заменяем символы новой строки на теги <br> для корректного отображения в HTML
      partDiv.innerHTML = part.replace(/\n/g, "<br>");
      partDiv.style.marginBottom = index < text.length - 1 ? "0.5em" : "0";
      messageContainer.appendChild(partDiv);
    });
  } else if (typeof text === "string") {
    // Заменяем символы новой строки на теги <br> для корректного отображения в HTML
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
  if (!UserMessage) return; // Не отправляем пустые сообщения

  Message(UserMessage, "user");
  UserInput.value = "";

  // Показываем typing индикатор
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

    // Удаляем typing индикатор
    removeTypingIndicator();

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    Message(data.reply, "bot");
  } catch (error) {
    removeTypingIndicator();
    console.error("Ошибка:", error);
    Message("Ошибка при подключении к серверу. Пожалуйста, попробуйте позже.", "bot");
  }
});
const Test = document.getElementById("forma");
Test.addEventListener("post", function (e) {
  e.preventDefault();
});
