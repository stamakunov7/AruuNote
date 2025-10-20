#!/usr/bin/env python3
"""
Простой скрипт для преобразования аудио в текст с использованием OpenAI Whisper
"""

import whisper
import os
import sys
from pathlib import Path

def transcribe_audio(audio_file_path, model_size="base"):
    """
    Преобразует аудиофайл в текст
    
    Args:
        audio_file_path (str): Путь к аудиофайлу
        model_size (str): Размер модели Whisper ("tiny", "base", "small", "medium", "large")
    
    Returns:
        str: Транскрибированный текст
    """
    try:
        # Загружаем модель
        print(f"Загружаем модель Whisper {model_size}...")
        model = whisper.load_model(model_size)
        
        # Проверяем существование файла
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Файл {audio_file_path} не найден")
        
        print(f"Обрабатываем файл: {audio_file_path}")
        
        # Транскрибируем аудио
        result = model.transcribe(audio_file_path)
        
        return result["text"]
    
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return None

def save_transcription(text, output_file):
    """Сохраняет транскрипцию в файл"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Транскрипция сохранена в: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

def main():
    if len(sys.argv) < 2:
        print("Использование: python audio_to_text.py <путь_к_аудиофайлу> [размер_модели]")
        print("Размеры модели: tiny, base, small, medium, large")
        print("Пример: python audio_to_text.py audio.mp3 base")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    print("=== Преобразователь аудио в текст ===")
    print(f"Входной файл: {audio_file}")
    print(f"Модель: {model_size}")
    print()
    
    # Транскрибируем аудио
    text = transcribe_audio(audio_file, model_size)
    
    if text:
        print("=== Результат транскрипции ===")
        print(text)
        print()
        
        # Сохраняем в файл
        audio_path = Path(audio_file)
        output_file = audio_path.stem + "_transcription.txt"
        save_transcription(text, output_file)
    else:
        print("Не удалось выполнить транскрипцию")

if __name__ == "__main__":
    main()
