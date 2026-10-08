# Motion: Autonomous Product Showcase & Educational Video Engine

> Turn any codebase into a high-end **3D product showcase commercial** using your native design tokens (`/motion-showcase`), or transform algorithms and code into **1080p educational motion graphics** with deterministic runtime tracing (`/motion-explain`).

**100% Local & FOSS** · **Zero Cloud API Subscriptions** · **Zero AI Hallucination or Buzzwords**

---

## Overview

Most AI video systems generate generic PowerPoint-like slides or hallucinate what code does step-by-step. 

This system operates as an **autonomous orchestration and quality-control pipeline** combining proven Free and Open Source Software (FOSS) tools:
1. **Deterministic Execution Tracing**: Uses Python's native `sys.settrace` and Abstract Syntax Tree (AST) parser to observe actual runtime memory, variables, and line transitions rather than guessing.
2. **Web-Grade Motion Graphics**: Uses **HyperFrames** to render seekable HTML5, CSS3, SVG, and GSAP timelines via a local Headless Chrome shell with Hardware GPU acceleration (Apple Metal / Vulkan).
3. **Neural Speech Narration**: Synthesizes human-grade neural voiceover and parses WebVTT timestamp cues via **Edge-TTS** to synchronize visual events to the spoken word.
4. **Empirical Visual QA**: Samples representative frames with **FFmpeg** and audits image variance with **Pillow** to detect black screens, overlapping text, or audio/video drift before delivering the video.
5. **Anti-Jargon Scripting**: Enforces strict plain-English pedagogical rules—no corporate AI buzzwords (*"delve"*, *"tapestry"*, *"seamlessly"*).

---

## Architecture

```text
               Educational Input (Code / Algorithm / Concept)
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │  [Execution & Semantic Layer]                          │
        │  • Deterministic Tracer (sys.settrace + AST)           │
        │  • Syntax Highlighter & Line Tokenizer (Pygments)       │
        └────────────────────────────┬───────────────────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │  [Pedagogical Planning Layer]                          │
        │  • Plain-English Storyboard Planner                    │
        │  • Visual Design System Presets                        │
        └────────────────────────────┬───────────────────────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
       [Audio Narration Engine]           [Motion Composition Engine]
       • Edge-TTS Neural Voice            • Column-Slot Physical Layout
       • WebVTT Cue Timestamps            • GSAP Seekable Timeline
       • Audio Duration Probe             • DOM & SVG State Animations
                     │                               │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │  [Headless GPU Renderer (Hyperframes)]                 │
        │  • Headless Chrome Shell with Metal/ANGLE GPU          │
        │  • Frame-by-Frame Streaming & Capture                  │
        └────────────────────────────┬───────────────────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │  [Media Multiplexing & Assembly (FFmpeg)]              │
        │  • High-Profile H.264 Video + 24kHz AAC Audio Mux      │
        │  • Strict Duration Synchronization (0.0s drift)        │
        └────────────────────────────┬───────────────────────────┘
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │  [Empirical Visual QA Layer]                           │
        │  • Temporal Keyframe Extraction (FFmpeg)               │
        │  • Brightness, Variance & Blank Detection (PIL)        │
        │  • Resolution & Audio/Video Stream Inspection          │
        └────────────────────────────────────────────────────────┘
```

---

## Design System Presets

Switch styles at runtime via `--style <name>`:

| Style Preset | Aesthetic & Tokens | Best For |
| :--- | :--- | :--- |
| `dark_cinematic` *(Default)* | Obsidian `#090d16`, ambient sky-cyan glow, Inter + JetBrains Mono, glassmorphism cards | Modern developer tooling, CS algorithms |
| `technical` | Slate `#0f172a`, blueprint borders, sharp 1px grid, compact data pills | Architecture diagrams, network flows |
| `mathematical` | Chalkboard `#121417`, gold accents `#eab308`, formula callouts, serif math type | Calculus, linear algebra, 3Blue1Brown style |
| `anime_cartoon` | Deep indigo `#13111c`, sakura pink `#ff79c6`, neon lime `#50fa7b`, bouncy elastic springs | Engaging tutorials, social media, playful guides |

---

## Prerequisites

Ensure these free tools are installed on your machine:
- **Node.js** (v22.0 or higher): `node -v`
- **Python** (v3.10 or higher): `python3 --version`
- **FFmpeg & ffprobe**: `ffmpeg -version` (e.g. `brew install ffmpeg` on macOS)

---

## Quickstart

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/your-username/educational-motion-graphics.git
cd educational-motion-graphics

# Install Python requirements
pip install -r requirements.txt
```

*(Node dependencies and HyperFrames run on-demand via `npx`—no global npm bloat).*

### 2. Generate a Video

#### A. Showcase Your Product (`/motion-showcase`)
Scans your current repository (Flutter, React, Next.js, Vue), pulls your brand colors and features, and generates a 3D isometric commercial:

```bash
# In your app directory
python3 /path/to/motion/bin/motion showcase .

# With different tone presets
python3 /path/to/motion/bin/motion showcase . --tone hype
python3 /path/to/motion/bin/motion showcase . --tone apple-minimal
```

#### B. Explain an Algorithm or Code (`/motion-explain`)
Traces execution, highlights code step-by-step, and creates a 1080p educational video:

```bash
# Default Dark Cinematic style with neural narration
python3 bin/motion explain "Explain binary search"

# Cartoon & Anime style
python3 bin/motion explain "Explain binary search" --style "cartoon + anime"

# Technical blueprint without audio
python3 bin/motion explain "Explain binary search" --style technical --no-audio
```

### 3. View the Result

Your final video, audio track, storyboard, and QA inspection report are saved in `output/`:

```bash
# Play on macOS
open output/binary_search/educational_binary_search.mp4
```

---

## Agent Skill Integration

This repository ships with a ready-to-use agent skill definition for **Google Antigravity / Gemini**, **Claude Code**, and **Cursor**.

### Installing for Gemini / Antigravity CLI

Link the skill folder into your agent config:

```bash
mkdir -p ~/.gemini/config/skills
ln -s "$(pwd)/skills/educational-motion-graphics" ~/.gemini/config/skills/educational-motion-graphics
```

Then simply ask your agent in chat:
```text
/animate Explain binary search
/animate Explain this Python code
/animate Explain how TCP handshake works
```

---

## Project Structure

```text
educational-motion-graphics/
├── bin/
│   └── edumotion.py            # Unified CLI entry point for planning, tracing, rendering, QA
├── core/
│   ├── execution_tracer.py     # Deterministic Python runtime execution tracer (AST & sys.settrace)
│   ├── code_highlighter.py     # Pygments syntax highlighter with line tagging
│   ├── audio_engine.py         # Edge-TTS voiceover & subtitle generator
│   ├── planner.py              # Visual explanation & storyboard planner (anti-jargon)
│   ├── renderer.py             # HyperFrames composition builder & render caller
│   └── visual_qa.py            # FFmpeg frame extractor & automated visual quality auditor
├── styles/
│   └── presets.py              # Visual design presets (Cinematic, Technical, Math, Anime)
├── skills/
│   └── educational-motion-graphics/
│       └── SKILL.md            # Agent skill prompt definition
├── output/                     # Rendered MP4s, MP3s, and QA frames
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## License

MIT License. Free to use, modify, and distribute for personal, educational, and commercial projects.
