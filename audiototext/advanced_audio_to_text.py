#!/usr/bin/env python3
"""
Расширенный скрипт для преобразования аудио в текст с поддержкой различных форматов
"""

import whisper
import os
import sys
import argparse
from pathlib import Path
from pydub import AudioSegment
import tempfile

class AudioToTextConverter:
    def __init__(self, model_size="base"):
        """Инициализация конвертера"""
        self.model_size = model_size
        self.model = None
        self.supported_formats = ['.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma']
    
    def load_model(self):
        """Загружает модель Whisper"""
        if self.model is None:
            print(f"Загружаем модель Whisper {self.model_size}...")
            self.model = whisper.load_model(self.model_size)
            print("Модель загружена успешно!")
    
    def convert_audio_format(self, input_path, output_path=None):
        """
        Конвертирует аудио в формат WAV для лучшей совместимости
        
        Args:
            input_path (str): Путь к входному файлу
            output_path (str): Путь для сохранения (если None, создается временный файл)
        
        Returns:
            str: Путь к конвертированному файлу
        """
        try:
            # Определяем формат файла
            file_ext = Path(input_path).suffix.lower()
            
            if file_ext not in self.supported_formats:
                raise ValueError(f"Неподдерживаемый формат: {file_ext}")
            
            # Загружаем аудио
            print(f"Конвертируем {file_ext} в WAV...")
            audio = AudioSegment.from_file(input_path)
            
            # Создаем выходной файл если не указан
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                output_path = temp_file.name
                temp_file.close()
            
            # Экспортируем в WAV
            audio.export(output_path, format="wav")
            print(f"Аудио конвертировано: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"Ошибка при конвертации аудио: {e}")
            return None
    
    def transcribe_audio(self, audio_file_path, language=None):
        """
        Преобразует аудиофайл в текст
        
        Args:
            audio_file_path (str): Путь к аудиофайлу
            language (str): Язык аудио (None для автоопределения)
        
        Returns:
            dict: Результат транскрипции с текстом и метаданными
        """
        try:
            # Загружаем модель если еще не загружена
            self.load_model()
            
            # Проверяем существование файла
            if not os.path.exists(audio_file_path):
                raise FileNotFoundError(f"Файл {audio_file_path} не найден")
            
            print(f"Обрабатываем файл: {audio_file_path}")
            
            # Определяем нужно ли конвертировать
            file_ext = Path(audio_file_path).suffix.lower()
            temp_file = None
            
            if file_ext != '.wav':
                # Конвертируем в WAV для лучшей совместимости
                temp_file = self.convert_audio_format(audio_file_path)
                if temp_file is None:
                    raise Exception("Не удалось конвертировать аудио")
                audio_path = temp_file
            else:
                audio_path = audio_file_path
            
            # Транскрибируем аудио
            print("Выполняем транскрипцию...")
            result = self.model.transcribe(
                audio_path,
                language=language,
                verbose=True
            )
            
            # Очищаем временный файл если создавали
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)
            
            return {
                'text': result['text'],
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'duration': result.get('duration', 0)
            }
            
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")
            return None
    
    def save_transcription(self, result, output_file, format='txt'):
        """
        Сохраняет результат транскрипции в файл
        
        Args:
            result (dict): Результат транскрипции
            output_file (str): Путь к выходному файлу
            format (str): Формат файла ('txt', 'srt', 'vtt')
        """
        try:
            if format == 'txt':
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result['text'])
            
            elif format == 'srt':
                # Создаем SRT субтитры
                with open(output_file, 'w', encoding='utf-8') as f:
                    for i, segment in enumerate(result['segments'], 1):
                        start_time = self._format_time(segment['start'])
                        end_time = self._format_time(segment['end'])
                        f.write(f"{i}\n")
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{segment['text'].strip()}\n\n")
            
            elif format == 'vtt':
                # Создаем WebVTT субтитры
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("WEBVTT\n\n")
                    for segment in result['segments']:
                        start_time = self._format_time_vtt(segment['start'])
                        end_time = self._format_time_vtt(segment['end'])
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{segment['text'].strip()}\n\n")
            
            print(f"Транскрипция сохранена в: {output_file}")
            
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
    
    def _format_time(self, seconds):
        """Форматирует время для SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _format_time_vtt(self, seconds):
        """Форматирует время для WebVTT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"

def main():
    parser = argparse.ArgumentParser(description='Преобразователь аудио в текст')
    parser.add_argument('input_file', help='Путь к аудиофайлу')
    parser.add_argument('-m', '--model', default='base', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Размер модели Whisper')
    parser.add_argument('-l', '--language', help='Язык аудио (например: ru, en, es)')
    parser.add_argument('-o', '--output', help='Путь к выходному файлу')
    parser.add_argument('-f', '--format', default='txt', 
                       choices=['txt', 'srt', 'vtt'],
                       help='Формат выходного файла')
    parser.add_argument('--show-segments', action='store_true',
                       help='Показать сегменты с временными метками')
    
    args = parser.parse_args()
    
    print("=== Расширенный преобразователь аудио в текст ===")
    print(f"Входной файл: {args.input_file}")
    print(f"Модель: {args.model}")
    print(f"Язык: {args.language or 'автоопределение'}")
    print(f"Формат вывода: {args.format}")
    print()
    
    # Создаем конвертер
    converter = AudioToTextConverter(args.model)
    
    # Выполняем транскрипцию
    result = converter.transcribe_audio(args.input_file, args.language)
    
    if result:
        print("=== Результат транскрипции ===")
        print(f"Язык: {result['language']}")
        print(f"Длительность: {result['duration']:.2f} секунд")
        print(f"Количество сегментов: {len(result['segments'])}")
        print()
        print("Текст:")
        print(result['text'])
        print()
        
        if args.show_segments:
            print("=== Сегменты с временными метками ===")
            for i, segment in enumerate(result['segments'], 1):
                start_time = converter._format_time(segment['start'])
                end_time = converter._format_time(segment['end'])
                print(f"{i}. [{start_time} - {end_time}] {segment['text'].strip()}")
            print()
        
        # Сохраняем результат
        if args.output:
            output_file = args.output
        else:
            input_path = Path(args.input_file)
            output_file = f"{input_path.stem}_transcription.{args.format}"
        
        converter.save_transcription(result, output_file, args.format)
        
    else:
        print("Не удалось выполнить транскрипцию")
        sys.exit(1)

if __name__ == "__main__":
    main()
