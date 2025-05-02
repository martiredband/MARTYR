# 🎛️ MARTYR — AI-Powered Local Audio Mastering

**MARTYR** is a local-first, Python-based audio mastering application that uses advanced machine learning algorithms to emulate the precision and nuance of professional studio mastering. Built for musicians, engineers, and creators who need fast, private, and high-quality results—without relying on the cloud.

---

## ✨ Features

| Core Technology | Description |
|-----------------|-------------|
| **Machine Learning Core** | Trained on thousands of professionally mixed songs from well-known bands. Learns tonal balance, dynamics, and spatial profiles to make intelligent mastering decisions. |
| **Precision Algorithms** | Executes billions of spectral operations per track, enabling detailed nonlinear analysis and enhancements beyond real-time DSP limitations. |
| **Automated Decision System** | Adapts dynamically to your input audio, mimicking expert engineer decisions in EQ, compression, stereo width, and loudness. |
| **Local Processing** | 100% offline. No data sent to the cloud. Leverages your own CPU/GPU for full privacy and control. |

---

## ⚙️ Technology

MARTYR is built entirely in **Python**, using the open-source engine [Matchering](https://github.com/sergree/matchering). It applies a **reference mastering technique** — matching the sonic characteristics of your track to a professionally mastered reference.

- Smart matching of dynamic range, loudness (LUFS), and stereo image.
- Uses deep signal analysis with mathematically optimized models.
- Output formats include `WAV`, `FLAC`, and `MP3`.

---

## 📦 Installation

> The application is **under development**. Full cross-platform support and GUI updates coming soon.

### 🔽 Download Package

You can download the current version here:

**🔗 [Download MARTYR](https://martired.com/martyr-downloads/)**

Included files:
- `MARTYR.exe` — Standalone executable for Windows
- `MARTYR.py` — Python source code

### 🐍 Python Dependencies

If you're running the source version, install dependencies with:

```bash
pip install matchering==2.1.6 pandas numpy soundfile matplotlib imageio-ffmpeg requests
