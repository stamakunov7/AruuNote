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
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Глобальная переменная для кэширования модели
model_cache = {}

# Хранилище результатов транскрипции (в продакшене лучше использовать Redis или БД)
transcription_results = {}

def get_model(model_size="base"):
    """Получает модель Whisper, кэширует для повторного использования"""
    if model_size not in model_cache:
        print(f"Загружаем модель {model_size}...")
        model_cache[model_size] = whisper.load_model(model_size)
    return model_cache[model_size]

def format_time_srt(seconds):
    """Форматирует время для SRT"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def format_time_vtt(seconds):
    """Форматирует время для WebVTT"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"

def generate_srt(segments):
    """Генерирует SRT файл из сегментов"""
    srt_content = []
    for i, segment in enumerate(segments, 1):
        start_time = format_time_srt(segment['start'])
        end_time = format_time_srt(segment['end'])
        srt_content.append(f"{i}\n")
        srt_content.append(f"{start_time} --> {end_time}\n")
        srt_content.append(f"{segment['text'].strip()}\n\n")
    return ''.join(srt_content)

def generate_vtt(segments):
    """Генерирует WebVTT файл из сегментов"""
    vtt_content = ["WEBVTT\n\n"]
    for segment in segments:
        start_time = format_time_vtt(segment['start'])
        end_time = format_time_vtt(segment['end'])
        vtt_content.append(f"{start_time} --> {end_time}\n")
        vtt_content.append(f"{segment['text'].strip()}\n\n")
    return ''.join(vtt_content)

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
                segments = result.get('segments', [])
                
                # Сохраняем результат транскрипции с уникальным ID
                transcription_id = str(uuid.uuid4())
                transcription_results[transcription_id] = {
                    'text': text,
                    'segments': segments,
                    'language': result.get('language', 'unknown')
                }
                
                # Очищаем временный файл
                os.remove(temp_path)
                os.rmdir(temp_dir)
                
                return jsonify({
                    'success': True,
                    'text': text,
                    'language': result.get('language', 'unknown'),
                    'segments': segments,
                    'transcription_id': transcription_id
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

@app.route('/download/<transcription_id>/<format>')
def download_file(transcription_id, format):
    """Генерирует и скачивает файл транскрипции в указанном формате"""
    try:
        if transcription_id not in transcription_results:
            return jsonify({'error': 'Транскрипция не найдена'}), 404
        
        result = transcription_results[transcription_id]
        filename_base = 'transcription'
        
        if format == 'txt':
            file_content = result['text']
            mimetype = 'text/plain'
            filename = f'{filename_base}.txt'
        
        elif format == 'srt':
            if not result['segments']:
                return jsonify({'error': 'Нет данных о сегментах для генерации SRT'}), 400
            file_content = generate_srt(result['segments'])
            mimetype = 'text/plain'
            filename = f'{filename_base}.srt'
        
        elif format == 'vtt':
            if not result['segments']:
                return jsonify({'error': 'Нет данных о сегментах для генерации WebVTT'}), 400
            file_content = generate_vtt(result['segments'])
            mimetype = 'text/vtt'
            filename = f'{filename_base}.vtt'
        
        else:
            return jsonify({'error': 'Неподдерживаемый формат'}), 400
        
        # Создаем файл в памяти
        file_obj = BytesIO(file_content.encode('utf-8'))
        
        return send_file(
            file_obj,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': f'Ошибка при генерации файла: {str(e)}'}), 500

if __name__ == '__main__':
    # Создаем папку для шаблонов если её нет
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
