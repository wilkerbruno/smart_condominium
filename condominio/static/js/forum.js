
document.getElementById('postForum').addEventListener('submit', function(event) {
    event.preventDefault();

    const questionInput = document.getElementById('question');
    const imageInput = document.getElementById('imageInput');
    const postsContainer = document.getElementById('posts');

    const questionText = questionInput.value;

    if (!questionText) {
        alert('Por favor, digite uma pergunta.');
        return;
    }

    const postDiv = document.createElement('div');
    postDiv.classList.add('post');

    const questionPara = document.createElement('p');
    questionPara.textContent = questionText;
    postDiv.appendChild(questionPara);

    if (imageInput.files && imageInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            postDiv.appendChild(img);
        }
        reader.readAsDataURL(imageInput.files[0]);
    }

    const responseButton = document.createElement('button');
    responseButton.textContent = 'Responder';
    responseButton.addEventListener('click', function() {
        toggleResponseForm(responseForm);
    });
    postDiv.appendChild(responseButton);

    const responseForm = document.createElement('form');
    responseForm.classList.add('response-form');
    responseForm.style.display = 'none';

    const responseInput = document.createElement('input');
    responseInput.type = 'text';
    responseInput.placeholder = 'Digite sua resposta';
    responseForm.appendChild(responseInput);

    const responseSubmit = document.createElement('button');
    responseSubmit.type = 'submit';
    responseSubmit.textContent = 'Enviar';
    responseForm.appendChild(responseSubmit);

    responseForm.addEventListener('submit', function(event) {
        event.preventDefault();
        addResponse(responsesDiv, responseInput.value);
        responseInput.value = '';
        responseForm.style.display = 'none';
    });

    postDiv.appendChild(responseForm);

    const responsesDiv = document.createElement('div');
    responsesDiv.classList.add('responses');
    postDiv.appendChild(responsesDiv);

    postsContainer.appendChild(postDiv);

    // Limpar o formulário
    questionInput.value = '';
    imageInput.value = '';
});

function toggleResponseForm(responseForm) {
    responseForm.style.display = responseForm.style.display === 'none' ? 'block' : 'none';
}

function addResponse(responsesDiv, responseText) {
    if (!responseText.trim()) {
        alert('Por favor, digite uma resposta.');
        return;
    }

    const responseDiv = document.createElement('div');
    responseDiv.classList.add('response');
    responseDiv.textContent = responseText;

    responsesDiv.appendChild(responseDiv);
}
