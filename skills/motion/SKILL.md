---
name: motion
description: Autonomous product showcase and educational motion-graphics system. Use /motion-showcase to turn any codebase into a 3D product commercial using its native design tokens, or /motion-explain to turn algorithms, code, and concepts into polished 1080p educational motion graphics with runtime tracing and zero AI jargon.
---

# Motion

Autonomous product video and educational motion-graphics engine.

---

## Commands

### 1. `/motion-showcase` (Product Commercial & Demo)
Scans your current codebase, extracts the design system (colors, typography, radii), identifies the core hero features, and produces a 15–30s 3D product commercial featuring your application's real design.

```text
/motion-showcase
/motion-showcase --tone hype
/motion-showcase --tone apple-minimal
/motion-showcase --format vertical
/motion-showcase --no-voice
```

**How It Works:**
1. **Scans Repository**: Auto-detects product name, tagline, and framework (Flutter, React, Next.js, Vue).
2. **Extracts Design Identity**: Pulls primary hex colors, dark/light themes, and font families.
3. **Stages 3D Canvas**: Mounts your interface on a 3D isometric perspective stage with dynamic lighting.
4. **Animates Cursor & State**: Simulates natural cursor clicks, feature reveals, and metric counters.
5. **Renders & Verifies**: Exports 1080p MP4 via Chrome GPU and verifies visual quality.

---

### 2. `/motion-explain` (Educational Motion Graphics)
Turns algorithms, source code, data structures, mathematics, and technical architecture into polished visual walkthroughs with real Python runtime tracing and human neural voiceover.

```text
/motion-explain Explain binary search
/motion-explain Explain this Python code
/motion-explain Explain Dijkstra's algorithm --style technical
/motion-explain Explain recursion --style "cartoon + anime"
```

**How It Works:**
1. **Deterministic Tracing**: Uses Python `sys.settrace` and AST analysis—zero hallucination.
2. **Pygments Highlighting**: Tokenizes lines for synchronous step-by-step code highlighting.
3. **Pedagogical Storyboarding**: Formulates scenes using plain English (zero AI buzzwords).
4. **Column-Slot Alignment**: Pointers and cards are physically bound to prevent layout drift.
5. **Automated Visual QA**: Audits frames with Pillow and FFmpeg before delivery.

---

## Design Presets

| Style / Tone | Visual Tokens | Best For |
| :--- | :--- | :--- |
| `dark_cinematic` *(Default)* | Obsidian `#090d16`, ambient cyan glow, glassmorphism cards | Modern developer tools |
| `apple_minimal` | Clean white/dark glass, crisp typography, subtle depth | Consumer apps, SaaS |
| `technical` | Slate `#0f172a`, blueprint borders, dense telemetry | Infrastructure, backend |
| `anime_cartoon` | Deep indigo `#13111c`, sakura pink `#ff79c6`, neon lime, elastic springs | Playful tutorials, reels |

---

## Direct Terminal Invocation

You can also run the CLI directly from any terminal:

```bash
# Showcase current project
python3 ~/.gemini/educational-motion-graphics/bin/motion showcase .

# Explain an algorithm
python3 ~/.gemini/educational-motion-graphics/bin/motion explain "Explain binary search" --style "cartoon + anime"
```
