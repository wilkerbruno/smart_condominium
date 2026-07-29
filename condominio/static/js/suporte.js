const supportButton = document.getElementById('support-button');
const supportChat = document.getElementById('support-chat');
const supportInput = document.getElementById('support-input');
const sendButton = document.getElementById('send-button');
const supportMessages = document.getElementById('support-messages');

supportButton.addEventListener('click', () => {
  if (supportChat.style.display === 'none' || supportChat.style.display === '') {
    supportChat.style.display = 'block';
  } else {
    supportChat.style.display = 'none';
  }
});

supportChat.addEventListener('click', (e) => {
  if (e.target === supportChat) {
    supportChat.style.display = 'none';
  }
});

const supportResponses = [
  "Olá! Como posso ajudar?",
  "Aguarde um momento enquanto buscamos a resposta para você.",
  "Desculpe, não entendi a pergunta. Por favor, tente ser mais específico.",
  "Infelizmente, não podemos ajudar com isso no momento. Tente novamente mais tarde.",
];

const addMessage = (message, isUser) => {
  const messageHTML = `
    <div class="messages">
      <p><span class="${isUser ? 'user-message' : 'support-message'}">${isUser ? 'Você' : 'Suporte'}:</span></p>
    </div>
  `;
  supportMessages.innerHTML += messageHTML;

  // Selecione a última mensagem
  const lastMessage = supportMessages.lastElementChild;
  lastMessage.scrollIntoView();

  // Adicione um balão em volta da mensagem
  const bubble = document.createElement('span');
  bubble.classList.add(isUser ? 'user-bubble' : 'support-bubble');
  const text = document.createElement('span');
  text.classList.add(isUser ? 'user-text' : 'support-text');
  text.textContent = message;
  bubble.appendChild(text);
  lastMessage.querySelector(`.${isUser ? 'user-message' : 'support-message'}`).after(bubble);
};

const handleSendMessage = () => {
  const message = supportInput.value;
  if (message !== '') {
    addMessage(message, true);
    supportInput.value = '';

    // Escolha uma resposta automática
    const response = supportResponses[Math.floor(Math.random() * supportResponses.length)];
    addMessage(response, false);
  }
};

sendButton.addEventListener('click', handleSendMessage);

supportInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    handleSendMessage();
  }
});