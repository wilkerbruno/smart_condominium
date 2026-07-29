// script.js

document.addEventListener('DOMContentLoaded', () => {
    const recadosList = document.getElementById('recados-list');
    const recadoForm = document.getElementById('recado-form');
    const recadoInput = document.getElementById('recado-input');

    let recados = [];

    // Carregar recados do armazenamento local
    function loadRecados() {
        const savedRecados = JSON.parse(localStorage.getItem('recados')) || [];
        recados = savedRecados;
        renderRecados();
    }

    // Salvar recados no armazenamento local
    function saveRecados() {
        localStorage.setItem('recados', JSON.stringify(recados));
    }

    // Renderizar recados
    function renderRecados() {
        recadosList.innerHTML = '';
        recados.forEach((recado, index) => {
            const recadoElement = document.createElement('div');
            recadoElement.className = 'recado';
            recadoElement.innerHTML = `
                <p>${recado}</p>
                <button onclick="removeRecado(${index})">Remover</button>
            `;
            recadosList.appendChild(recadoElement);
        });
    }

    // Adicionar novo recado
    recadoForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const newRecado = recadoInput.value.trim();
        if (newRecado !== '') {
            recados.push(newRecado);
            recadoInput.value = '';
            saveRecados();
            renderRecados();
        }
    });

    // Remover recado
    window.removeRecado = function(index) {
        recados.splice(index, 1);
        saveRecados();
        renderRecados();
    };

    loadRecados();
});
