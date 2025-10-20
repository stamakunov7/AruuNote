#!/bin/bash
# Скрипт для активации виртуального окружения и запуска

echo "🎵 Активируем виртуальное окружение..."
cd "/Users/stam7/Documents/Coding Workspace/AruuNote/audiototext"
source venv/bin/activate

echo "✅ Виртуальное окружение активировано!"
echo ""
echo "Доступные команды:"
echo "1. python quick_start.py          - Интерактивный режим"
echo "2. python audio_to_text.py <файл> - Быстрое преобразование"
echo "3. python app.py                  - Веб-интерфейс"
echo "4. python advanced_audio_to_text.py <файл> - Расширенное преобразование"
echo ""
echo "📁 Папка для аудиофайлов: $(pwd)/audio_files"
echo ""
echo "Для выхода из виртуального окружения введите: deactivate"
echo ""

# Запускаем интерактивный режим по умолчанию
python quick_start.py
