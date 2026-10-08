---
name: educational-motion-graphics
description: Autonomous AI educational motion-graphics system. Transforms algorithms, source code, data structures, mathematics, system architecture, and CS concepts into polished 1080p educational motion-graphics with runtime execution tracing, audio narration, and visual QA.
---

# Educational Motion-Graphics System

Autonomous AI system that transforms technical and educational subjects into polished, 60fps/30fps 1080p educational motion graphics using FOSS tools:
- **HyperFrames** (HTML + CSS + GSAP + Three.js + Chrome Headless GPU renderer)
- **Python Execution Tracer** (Deterministic AST analysis & `sys.settrace` for true runtime state without hallucination)
- **Pygments** (Syntax highlighting with individual line tokenization)
- **Edge-TTS / Piper-TTS** (Neural speech narration and subtitle synchronization)
- **FFmpeg & ffprobe** (Audio/video multiplexing, duration sync, and empirical Visual QA)

---

## When to Use

Activate whenever the user asks to explain a concept visually:
```text
/animate Explain binary search
/animate Explain this Python code
/animate Explain Dijkstra's algorithm
/animate Explain matrix multiplication
/animate Explain how TCP handshake works
/animate Explain this system architecture
/animate Explain backpropagation
```

---

## Core Pipeline Architecture

```text
Educational Request (Code, Algorithm, Math, Concept)
                    │
                    ▼
          Content & Execution Analysis
   (sys.settrace for code, AST, or concept extraction)
                    │
                    ▼
          Educational Storyboard Planner
       (Scenes, Beat-by-Beat Timing, Visual Layout)
                    │
                    ▼
         Neural Narration & Subtitle Sync
          (Edge-TTS / Piper audio + VTT cues)
                    │
                    ▼
        Motion Composition Synthesis
   (Column-slot layout, GSAP choreo, Code Highlighting)
                    │
                    ▼
         Headless Chrome & FFmpeg Render
         (1080p H.264 MP4 with Hardware GPU)
                    │
                    ▼
          Empirical Visual & Stream QA
 (Frame extraction, blank detection, audio drift check)
```

---

## CLI Command

Execute the complete end-to-end pipeline via the orchestrator:

```bash
python3 ~/.gemini/educational-motion-graphics/bin/edumotion.py "<topic>" [options]
```

### Options:
- `--output, -o`: Target output directory (default: `output/<topic_slug>`)
- `--no-audio`: Render silent video without narration track
- `--style`: Design preset (`dark_cinematic`, `technical`, `mathematical`)

---

## Visual Design Presets

1. **Dark Cinematic** (`dark_cinematic`):
   - Background: Obsidian `#090d16` with sky-cyan ambient radial glow.
   - Text: Crisp `#f8fafc` Inter typography with JetBrains Mono code.
   - Accents: Sky-blue `#38bdf8`, Amber `#fbbf24`, Emerald `#34d399`.

2. **Technical Blueprint** (`technical`):
   - Background: Slate `#0f172a` with subtle borders and data badges.
   - Accents: Cyan `#06b6d4`, Emerald `#10b981`.

3. **Mathematical / 3Blue1Brown** (`mathematical`):
   - Dark chalk board `#121417`, gold accents `#eab308`, formula cards.

---

## Code Execution Tracing Protocol

For code and algorithmic explanations:
1. Parse the AST to identify statements, loop bounds, and entry functions.
2. Run `ExecutionTracer` using `sys.settrace` to record real runtime step events.
3. Synchronize visual array pointers and variable pill badges strictly against recorded runtime state.
4. Highlight the corresponding line in the code window during each active step.

---

## Visual QA Protocol

Never declare completion without running `VisualQA`:
1. **Container Check**: Ensure valid MP4 container with H.264 video and AAC audio.
2. **Resolution Check**: Enforce exact 1920x1080 dimensions.
3. **Temporal Sampling**: Extract 4 representative frames at 10%, 35%, 65%, and 90% timestamps.
4. **Blank Detection**: Reject any video where mean brightness < 3.0 or pixel variance < 5.0.
5. **Drift Analysis**: Confirm audio and video durations match within 0.1s.

---

## Anti-Jargon & Plain-English Scripting Rules (STRICT)

Both on-screen copy and spoken voiceover MUST be plain, conversational, and jargon-free:
1. **Zero AI Buzzwords**: Banned terms include: *delve, tapestry, seamlessly, leverage, orchestrate, paradigm, robust, revolutionize, synergy, multifaceted, furthermore, utilize, embark*.
2. **No Fake Academic Jargon**: Do not use complex 5-syllable academic phrasing when a short, direct word explains it better.
   - Instead of *"instantiating contiguous index demarcations"*, say *"setting the start and end pointers"*.
   - Instead of *"executing an iterative halving heuristic"*, say *"cutting the search in half every time"*.
   - Instead of *"subsequently terminating execution"*, say *"and we're done"*.
3. **Concrete Analogies Over Theory**: Explain what the code or data actually looks like and does in real life.
4. **Keep Words Under Control**: Sentences should be short, punchy, and sound like a smart engineer speaking out loud over coffee, never a textbook or corporate slide deck.
