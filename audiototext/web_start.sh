#!/bin/bash
# Скрипт для запуска веб-интерфейса

echo "🌐 Запускаем веб-интерфейс..."
cd "/Users/stam7/Documents/Coding Workspace/audiototext"
source venv/bin/activate

echo "✅ Виртуальное окружение активировано!"
echo "🚀 Запускаем веб-сервер..."
echo ""
echo "📱 Откройте браузер и перейдите на: http://localhost:5000"
echo "📁 Папка для аудиофайлов: $(pwd)/audio_files"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

python app.py
