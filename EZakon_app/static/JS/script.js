function ShowMenu() {
  const menu = document.getElementById("menu");

  menu.classList.toggle("open");
}

const ChatForm = document.getElementById("chat-form");
const ChatWindow = document.getElementById("chat-window");
const UserInput = document.getElementById("user-input");

// CSRF
const csrftoken = document.querySelector("[name=csrf-token]").content;

function Message(text, sender) {
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("chat-message", sender);

  if (Array.isArray(text)) {
    text.forEach((part) => {
      const partDiv = document.createElement("div");
      // Заменяем символы новой строки на теги <br> для корректного отображения в HTML
      partDiv.innerHTML = part.replace(/\n/g, "<br>");
      messageContainer.appendChild(partDiv);
      // Добавляем небольшой отступ между частями, если это не последняя часть
      if (text.indexOf(part) < text.length - 1) {
        const spacer = document.createElement("div");
        spacer.style.height = "0.5em"; // Небольшой отступ
        messageContainer.appendChild(spacer);
      }
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
  Message(UserMessage, "user");

  try {
    const response = await fetch("http://127.0.0.1:8000/chat_with_ai/", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrftoken, // Добавление CSRF-токена
      },
      body: JSON.stringify({ message: UserMessage }),
    });

    const data = await response.json();

    Message(data.reply, "bot");
  } catch (error) {
    Message("Ошибка при подключений к серверу", "bot");
  }

  UserInput.value = "";
});
const Test = document.getElementById("forma");
Test.addEventListener("post", function (e) {
  e.preventDefault();
});
