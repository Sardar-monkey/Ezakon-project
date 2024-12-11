function ShowMenu() {
    const menu = document.getElementById("menu");
    
    menu.classList.toggle("open");
};


const ChatForm = document.getElementById("chat-form");
const ChatWindow = document.getElementById("chat-window");
const UserInput = document.getElementById("user-input");

// CSRF
const csrftoken = document.querySelector('[name=csrf-token]').content;

function Message(text, sender) {
    const DivBox = document.createElement('div');
    DivBox.textContent = text;
    DivBox.classList.add('chat-message', sender);
    ChatWindow.appendChild(DivBox);
    ChatWindow.scrollTop = ChatWindow.scrollHeight;
}

ChatForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const UserMessage = UserInput.value.trim();
    Message(UserMessage, 'user')

    try {
        const response = await fetch('http://127.0.0.1:8000/chat_with_ai/', {
            method : 'POST',
            headers : {
                'Content-type' : 'application/json',
                'X-CSRFToken': csrftoken // Добавление CSRF-токена
            },
            body : JSON.stringify({message : UserMessage})
        })

        const data = await response.json();

        Message(data.reply, 'bot');

    } catch(error) {
        Message("Ошибка при подключений к серверу", 'bot');
    }

    UserInput.value = "";

})
const Test = document.getElementById('forma');
Test.addEventListener('post', function(e) {
    e.preventDefault();
})

