# 🪶 AruuNote — From Love to Learning

AruuNote is a simple yet powerful tool for converting audio into text using **OpenAI Whisper**.  
Originally created for my girlfriend **Aruuke**, it’s now available for every student who wants to study smarter, not harder.

## 🎥 Project Demo

[![Watch the demo](https://img.youtube.com/vi/6RxnuA61fRI/hqdefault.jpg)](https://youtu.be/6RxnuA61fRI)

> Click the image to watch the demo on YouTube.

---

## ✨ Features

- **Command-line scripts** – quick and easy transcription from the terminal  
- **Web interface** – user-friendly browser experience  
- **Multiple audio formats** – MP3, WAV, M4A, FLAC, AAC, OGG, WMA  
- **Flexible models** – from the fastest (tiny) to the most accurate (large)  
- **Export options** – TXT, SRT subtitles, WebVTT  
- **Multilingual** – automatic language detection  

---

## 💖 Project Story

This project began as something personal — a gift for my girlfriend, **Aruuke**.  
I wanted to make her studies easier by building a tool that could quickly and accurately turn lectures and recordings into text.

As time went on, I realized that many other students face the same challenges.  
So I decided to share **AruuNote** with the world.  
What started as a project for one person now helps many — transforming audio into clarity and convenience for learners everywhere.  

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aruunote.git
cd aruunote

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

#### 1. Simple script
```bash
python audio_to_text.py audio.mp3
python audio_to_text.py audio.mp3 large
```

#### 2. Advanced script
```bash
# Basic usage
python advanced_audio_to_text.py audio.mp3

# Specify language
python advanced_audio_to_text.py audio.mp3 -l ru

# Export subtitles (SRT)
python advanced_audio_to_text.py audio.mp3 -f srt -o subtitles.srt
```

#### 3. Web Application
```bash
python app.py
# Open http://localhost:5000 in your browser
```

> **🌐 Multilingual Interface**: The web app is originally designed in Russian, but includes an English translation for international users. Use the language switcher (RUS/ENG) in the top-right corner to switch between languages.

## 📊 Whisper Models

| Model  | Size     | Speed        | Accuracy  | Recommended Use  |
| ------ | -------- | ------------ | --------- | ---------------- |
| tiny   | ~39 MB   | ⚡ Very fast  | Low       | Quick tests      |
| base   | ~74 MB   | ⚡ Fast       | Good      | **Recommended**  |
| small  | ~244 MB  | ⚖️ Moderate  | High      | Quality work     |
| medium | ~769 MB  | 🕓 Slow      | Very high | Professional     |
| large  | ~1550 MB | 🐢 Very slow | Maximum   | Highest accuracy |


## 📁 Project Structure

```
aruunote/
├── audio_to_text.py          # Simple transcription script
├── advanced_audio_to_text.py # Advanced version with CLI options
├── app.py                    # Flask web app
├── requirements.txt          # Dependencies
├── templates/
│   └── index.html            # Web UI template
└── README.md                 # Documentation
```

## 🎯 Example Use Cases

### Transcribe a podcast
```bash
python advanced_audio_to_text.py podcast.mp3 -m medium -f srt -o podcast.srt
```

### Quick meeting notes
```bash
python audio_to_text.py meeting.wav tiny
```

### Use the web app
```bash
python app.py
# Upload your file via browser at http://localhost:5000
```

## ⚡ System Requirements 

- **Minimum**: 4GB RAM, Python 3.8+
- **Recommended**: 8GB RAM, GPU with CUDA
- **FFmpeg** for audio processing

## 🐛 Troubleshooting

### Error "No module named 'whisper'"
```bash
pip install openai-whisper
```

### Error FFmpeg
```bash
# Check installation of FFmpeg
ffmpeg -version
```

### Out of memory?
- Use a smaller model (tiny, base)
- Split large audio files into segments

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) - core speech-to-text engine
- [Flask](https://flask.palletsprojects.com/) - lightweight web framework
- [Pydub](https://github.com/jiaaro/pydub) - audio processing library

---

## 🌸 Originally made for Aruuke. Now made for everyone.
