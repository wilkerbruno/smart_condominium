from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Diretório para salvar os arquivos enviados
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Armazena mensagens e arquivos por morador
messages = {
    1: [],  # Morador 1
    2: [],  # Morador 2
    3: [],  # Morador 3
    4: []   # Morador 4
}

@app.route('/api/messages/<int:resident_id>', methods=['GET'])
def get_messages(resident_id):
    """Obtém todas as mensagens para um residente específico."""
    return jsonify(messages.get(resident_id, []))

@app.route('/api/messages/<int:resident_id>', methods=['POST'])
def post_message(resident_id):
    """Posta uma mensagem ou arquivo para um residente específico."""
    if 'file' in request.files:
        file = request.files['file']
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Adiciona a mensagem com o caminho do arquivo
        messages[resident_id].append({'file_url': file_path, 'sender': 'porteiro/sindico'})
        return jsonify({'success': True, 'file_url': file_path})

    else:
        data = request.form
        text = data.get('text')
        sender = data.get('sender', 'porteiro/sindico')

        if resident_id not in messages:
            messages[resident_id] = []

        messages[resident_id].append({'text': text, 'sender': sender})
        return jsonify({'success': True})

if __name__ == '__main__':
    app.run(port=3000)
