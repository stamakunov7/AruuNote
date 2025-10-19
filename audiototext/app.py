#!/usr/bin/env python3
"""
Веб-приложение для преобразования аудио в текст
"""

from flask import Flask, request, render_template, jsonify, send_file
import whisper
import os
import tempfile
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Глобальная переменная для кэширования модели
model_cache = {}

def get_model(model_size="base"):
    """Получает модель Whisper, кэширует для повторного использования"""
    if model_size not in model_cache:
        print(f"Загружаем модель {model_size}...")
        model_cache[model_size] = whisper.load_model(model_size)
    return model_cache[model_size]

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Обрабатывает загруженный аудиофайл"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Файл не выбран'}), 400
        
        file = request.files['audio']
        model_size = request.form.get('model_size', 'base')
        
        if file.filename == '':
            return jsonify({'error': 'Файл не выбран'}), 400
        
        if file:
            # Создаем временный файл
            filename = secure_filename(file.filename)
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, filename)
            file.save(temp_path)
            
            try:
                # Получаем модель
                model = get_model(model_size)
                
                # Транскрибируем
                result = model.transcribe(temp_path)
                text = result["text"]
                
                # Очищаем временный файл
                os.remove(temp_path)
                os.rmdir(temp_dir)
                
                return jsonify({
                    'success': True,
                    'text': text,
                    'language': result.get('language', 'unknown')
                })
                
            except Exception as e:
                # Очищаем в случае ошибки
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
                return jsonify({'error': f'Ошибка обработки: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Ошибка сервера: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Скачивает файл транскрипции"""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Файл не найден: {str(e)}'}), 404

if __name__ == '__main__':
    # Создаем папку для шаблонов если её нет
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
