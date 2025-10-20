#!/usr/bin/env python3
"""
Быстрый старт для преобразования аудио в текст
Простой интерфейс командной строки
"""

import os
import sys
from pathlib import Path

def main():
    print("🎵 Преобразователь аудио в текст - Быстрый старт")
    print("=" * 50)
    
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    else:
        # Интерактивный режим
        print("\nВыберите режим:")
        print("1. Обработать файл")
        print("2. Запустить веб-интерфейс")
        print("3. Установить зависимости")
        
        choice = input("\nВведите номер (1-3): ").strip()
        
        if choice == "1":
            audio_file = input("Введите путь к аудиофайлу: ").strip()
            if not audio_file:
                print("❌ Файл не указан")
                return
            
            print("\nВыберите модель:")
            print("1. Tiny (быстро, менее точно)")
            print("2. Base (баланс) - РЕКОМЕНДУЕТСЯ")
            print("3. Small (более точно)")
            print("4. Medium (очень точно)")
            print("5. Large (максимальная точность)")
            
            model_choice = input("Введите номер (1-5): ").strip()
            model_map = {"1": "tiny", "2": "base", "3": "small", "4": "medium", "5": "large"}
            model_size = model_map.get(model_choice, "base")
            
        elif choice == "2":
            print("\n🚀 Запускаем веб-интерфейс...")
            print("Откройте браузер и перейдите на http://localhost:5000")
            os.system("python app.py")
            return
            
        elif choice == "3":
            print("\n📦 Устанавливаем зависимости...")
            os.system("pip install -r requirements.txt")
            print("✅ Зависимости установлены!")
            return
            
        else:
            print("❌ Неверный выбор")
            return
    
    # Проверяем существование файла
    if not os.path.exists(audio_file):
        print(f"❌ Файл {audio_file} не найден")
        return
    
    print(f"\n📁 Файл: {audio_file}")
    print(f"🤖 Модель: {model_size}")
    print("\n⏳ Обрабатываем...")
    
    # Импортируем и запускаем конвертер
    try:
        from audio_to_text import transcribe_audio, save_transcription
        
        # Транскрибируем
        result = transcribe_audio(audio_file, model_size)
        
        if result:
            print("\n✅ Транскрипция завершена!")
            print("\n📝 Результат:")
            print("-" * 40)
            print(result)
            print("-" * 40)
            
            # Сохраняем результат
            audio_path = Path(audio_file)
            output_file = f"{audio_path.stem}_transcription.txt"
            save_transcription(result, output_file)
            
            print(f"\n💾 Результат сохранен в: {output_file}")
        else:
            print("❌ Ошибка при обработке файла")
            
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Убедитесь что установлены все зависимости:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
