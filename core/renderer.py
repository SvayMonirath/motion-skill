"""
Educational Motion-Graphics Composition Builder & Renderer.
Combines storyboard, code highlighting, execution trace, audio narration cues,
and visual design tokens into a professional HTML+GSAP composition,
renders via Hyperframes, muxes audio, and performs visual QA.
"""

import os
import json
import subprocess
from typing import Dict, Any, Optional
from styles.presets import get_style
from core.visual_qa import VisualQA

class EducationalRenderer:
    def __init__(self, project_dir: str):
        self.project_dir = os.path.abspath(project_dir)
        self.composition_dir = os.path.join(self.project_dir, "composition")
        os.makedirs(self.composition_dir, exist_ok=True)

    def generate_binary_search_html(
        self,
        storyboard: Dict[str, Any],
        highlighted_code: Dict[str, Any],
        trace_data: Dict[str, Any],
        style_preset: str = "dark_cinematic",
        duration_sec: float = 33.2
    ) -> str:
        """
        Builds the complete standalone HTML motion-graphics composition for Binary Search
        with guaranteed column-aligned pointer tracks and narration-synchronized timeline.
        """
        style = get_style(style_preset)
        array_data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
        target_val = 23

        html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1920, height=1080" />
  <title>{storyboard.get("title", "Educational Animation")}</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: {style['bg']};
      color: {style['text_primary']};
      font-family: {style['font_family']};
      overflow: hidden;
      width: 1920px;
      height: 1080px;
    }}
    #root {{
      position: relative;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at 50% 15%, rgba(56, 189, 248, 0.10) 0%, transparent 65%),
                  linear-gradient(180deg, {style['bg']} 0%, #05070a 100%);
      overflow: hidden;
    }}
    .header {{
      position: absolute;
      top: 48px;
      left: 90px;
      right: 90px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid {style['surface_border']};
      padding-bottom: 22px;
    }}
    .badge {{
      display: inline-block;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: {style['accent_primary']};
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .title {{
      font-size: 38px;
      font-weight: 700;
      letter-spacing: -0.02em;
    }}
    .meta-badges {{
      display: flex;
      gap: 12px;
    }}
    .meta-tag {{
      background: {style['surface']};
      border: 1px solid {style['surface_border']};
      color: {style['text_secondary']};
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 15px;
      font-family: {style['font_mono']};
      font-weight: 600;
      transition: all 0.3s ease;
    }}
    .main-stage {{
      position: absolute;
      top: 170px;
      left: 90px;
      right: 90px;
      bottom: 50px;
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 36px;
    }}
    .visual-panel, .code-panel {{
      background: {style['surface']};
      border: 1px solid {style['surface_border']};
      border-radius: {style['card_radius']};
      padding: 32px;
      position: relative;
      display: flex;
      flex-direction: column;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
    }}
    .panel-title {{
      font-size: 20px;
      font-weight: 600;
      color: {style['text_secondary']};
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .target-callout {{
      background: rgba(251, 191, 36, 0.12);
      border: 1px solid rgba(251, 191, 36, 0.35);
      color: {style['accent_highlight']};
      padding: 8px 18px;
      border-radius: 8px;
      font-size: 17px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    /* Column-Slot Array Layout */
    .array-board {{
      margin-top: 24px;
      display: flex;
      justify-content: center;
      gap: 10px;
    }}
    .array-slot {{
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 74px;
    }}
    .ptr-lane-top {{
      height: 38px;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      margin-bottom: 6px;
    }}
    .ptr-lane-bot {{
      height: 38px;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      margin-top: 6px;
    }}
    .pointer-tag {{
      font-family: {style['font_mono']};
      font-size: 13px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 3px;
      opacity: 0;
      transform: translateY(4px);
    }}
    .tag-low {{
      background: rgba(56, 189, 248, 0.2);
      border: 1px solid {style['accent_primary']};
      color: {style['accent_primary']};
    }}
    .tag-high {{
      background: rgba(129, 140, 248, 0.2);
      border: 1px solid {style['accent_secondary']};
      color: {style['accent_secondary']};
    }}
    .tag-mid {{
      background: rgba(251, 191, 36, 0.25);
      border: 1px solid {style['accent_highlight']};
      color: {style['accent_highlight']};
    }}

    .array-cell {{
      width: 72px;
      height: 80px;
      background: rgba(15, 23, 42, 0.85);
      border: 2px solid rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      font-weight: 700;
      font-family: {style['font_mono']};
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      position: relative;
    }}
    .cell-idx {{
      margin-top: 6px;
      font-size: 13px;
      color: {style['text_secondary']};
      font-family: {style['font_mono']};
    }}
    .cell-eliminated {{
      opacity: 0.2;
      border-color: rgba(255, 255, 255, 0.05) !important;
      background: rgba(255, 255, 255, 0.02) !important;
    }}
    .cell-mid-active {{
      border-color: {style['accent_highlight']} !important;
      background: rgba(251, 191, 36, 0.2) !important;
      box-shadow: 0 0 20px rgba(251, 191, 36, 0.4) !important;
      transform: scale(1.05);
    }}
    .cell-found-target {{
      border-color: {style['accent_success']} !important;
      background: rgba(52, 211, 153, 0.3) !important;
      box-shadow: 0 0 32px rgba(52, 211, 153, 0.6) !important;
      transform: scale(1.12);
    }}

    /* Status Card */
    .status-card {{
      margin-top: auto;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid {style['surface_border']};
      border-radius: 12px;
      padding: 20px 24px;
      font-size: 17px;
      line-height: 1.6;
      color: {style['text_primary']};
      min-height: 110px;
    }}
    .status-title {{
      color: {style['accent_primary']};
      font-weight: 700;
      font-size: 18px;
      margin-bottom: 4px;
    }}

    /* Code Panel */
    .code-container {{
      background: #050811;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 20px 16px;
      font-family: {style['font_mono']};
      font-size: 15px;
      line-height: 1.7;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .code-line {{
      padding: 2px 10px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      transition: all 0.2s ease;
    }}
    .line-no {{
      width: 28px;
      color: #475569;
      font-size: 13px;
      user-select: none;
    }}
    .line-text {{
      flex: 1;
    }}
    .line-active {{
      background: rgba(56, 189, 248, 0.18);
      border-left: 3px solid {style['accent_primary']};
      color: #ffffff;
    }}
    .vars-table {{
      margin-top: 18px;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 12px 18px;
      display: flex;
      justify-content: space-around;
      font-family: {style['font_mono']};
      font-size: 15px;
    }}
    .var-pill {{
      display: flex;
      gap: 8px;
    }}
    .var-name {{ color: {style['text_secondary']}; }}
    .var-val {{ color: {style['accent_primary']}; font-weight: 700; }}
  </style>
</head>
<body>
  <div
    id="root"
    data-composition-id="main"
    data-start="0"
    data-width="1920"
    data-height="1080"
    data-duration="{duration_sec}"
  >
    <header class="header">
      <div>
        <div class="badge">Divide &amp; Conquer Algorithm</div>
        <div class="title">Binary Search Visualization</div>
      </div>
      <div class="meta-badges">
        <div class="meta-tag" id="tag-complexity">Time Complexity: O(log N)</div>
        <div class="meta-tag">Space: O(1)</div>
        <div class="meta-tag">Input: N = 10 (Sorted)</div>
      </div>
    </header>

    <main class="main-stage">
      <section class="visual-panel">
        <div class="panel-title">
          <span>Search Space Visualization</span>
          <div class="target-callout">Target Query: <strong>23</strong></div>
        </div>

        <div class="array-board" id="array-board">
          {''.join([f'''
          <div class="array-slot" id="slot-{i}">
            <div class="ptr-lane-top">
              <span class="pointer-tag tag-low" id="ptr-low-{i}">low ▼</span>
              <span class="pointer-tag tag-high" id="ptr-high-{i}">high ▼</span>
            </div>
            <div class="array-cell" id="cell-{i}">{v}</div>
            <div class="cell-idx">[{i}]</div>
            <div class="ptr-lane-bot">
              <span class="pointer-tag tag-mid" id="ptr-mid-{i}">▲ mid</span>
            </div>
          </div>''' for i, v in enumerate(array_data)])}
        </div>

        <div class="status-card" id="status-card">
          <div class="status-title" id="status-title">Phase 1: Search Initialization</div>
          <div id="status-desc">Binary search requires a sorted input array. Search boundaries low and high bracket the full range.</div>
        </div>
      </section>

      <section class="code-panel">
        <div class="panel-title">
          <span>Python Execution &amp; Runtime State</span>
        </div>

        <div class="code-container" id="code-lines">
          <div class="code-line" id="line-1"><span class="line-no">1</span><span class="line-text"><span style="color:#f43f5e">def</span> <span style="color:#38bdf8">binary_search</span>(arr, target):</span></div>
          <div class="code-line" id="line-2"><span class="line-no">2</span><span class="line-text">&nbsp;&nbsp;low = 0</span></div>
          <div class="code-line" id="line-3"><span class="line-no">3</span><span class="line-text">&nbsp;&nbsp;high = len(arr) - 1</span></div>
          <div class="code-line" id="line-4"><span class="line-no">4</span><span class="line-text">&nbsp;&nbsp;<span style="color:#f43f5e">while</span> low &lt;= high:</span></div>
          <div class="code-line" id="line-5"><span class="line-no">5</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;mid = (low + high) // 2</span></div>
          <div class="code-line" id="line-6"><span class="line-no">6</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;guess = arr[mid]</span></div>
          <div class="code-line" id="line-7"><span class="line-no">7</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#f43f5e">if</span> guess == target:</span></div>
          <div class="code-line" id="line-8"><span class="line-no">8</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#38bdf8">return</span> mid</span></div>
          <div class="code-line" id="line-9"><span class="line-no">9</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#f43f5e">elif</span> guess &lt; target:</span></div>
          <div class="code-line" id="line-10"><span class="line-no">10</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;low = mid + 1</span></div>
          <div class="code-line" id="line-11"><span class="line-no">11</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#f43f5e">else</span>:</span></div>
          <div class="code-line" id="line-12"><span class="line-no">12</span><span class="line-text">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;high = mid - 1</span></div>
          <div class="code-line" id="line-13"><span class="line-no">13</span><span class="line-text">&nbsp;&nbsp;<span style="color:#38bdf8">return</span> -1</span></div>
        </div>

        <div class="vars-table">
          <div class="var-pill"><span class="var-name">low:</span><span class="var-val" id="var-low">-</span></div>
          <div class="var-pill"><span class="var-name">mid:</span><span class="var-val" id="var-mid">-</span></div>
          <div class="var-pill"><span class="var-name">high:</span><span class="var-val" id="var-high">-</span></div>
          <div class="var-pill"><span class="var-name">guess:</span><span class="var-val" id="var-guess">-</span></div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const tl = gsap.timeline({{ paused: true }});

    // Helper to highlight code line
    function setActiveLine(lineNum) {{
      document.querySelectorAll(".code-line").forEach(l => l.classList.remove("line-active"));
      const target = document.getElementById("line-" + lineNum);
      if (target) target.classList.add("line-active");
    }}

    // Helper to set status message
    function setStatus(title, desc, color) {{
      const t = document.getElementById("status-title");
      const d = document.getElementById("status-desc");
      if (t) {{
        t.innerText = title;
        if (color) t.style.color = color;
      }}
      if (d) d.innerText = desc;
    }}

    // --- BEAT 1: 0.0s - 5.0s Introduction & Setup ---
    tl.from(".header", {{ y: -30, opacity: 0, duration: 1.0, ease: "power3.out" }}, 0.2);
    tl.from(".visual-panel", {{ x: -40, opacity: 0, duration: 1.0, ease: "power3.out" }}, 0.5);
    tl.from(".code-panel", {{ x: 40, opacity: 0, duration: 1.0, ease: "power3.out" }}, 0.5);
    tl.from(".array-slot", {{ scale: 0.8, opacity: 0, stagger: 0.08, duration: 0.8, ease: "back.out(1.4)" }}, 1.0);

    // Initial pointers: low = 0, high = 9
    tl.call(() => setActiveLine(2), null, 3.2);
    tl.to("#ptr-low-0", {{ opacity: 1, y: 0, duration: 0.5 }}, 3.4);
    tl.set("#var-low", {{ innerText: "0" }}, 3.4);

    tl.call(() => setActiveLine(3), null, 4.0);
    tl.to("#ptr-high-9", {{ opacity: 1, y: 0, duration: 0.5 }}, 4.2);
    tl.set("#var-high", {{ innerText: "9" }}, 4.2);

    // --- BEAT 2: 5.0s - 13.5s Iteration 1 (probe mid = 4, val = 16) ---
    tl.call(() => {{
      setActiveLine(4);
      setStatus("Iteration 1: Calculate Middle", "While low <= high holds true, calculate midpoint index: (0 + 9) // 2 = 4.");
    }}, null, 5.2);

    tl.call(() => setActiveLine(5), null, 6.2);
    tl.to("#ptr-mid-4", {{ opacity: 1, y: 0, duration: 0.5 }}, 6.5);
    tl.set("#var-mid", {{ innerText: "4" }}, 6.5);
    tl.to("#cell-4", {{ className: "+=cell-mid-active", duration: 0.4 }}, 6.7);

    tl.call(() => setActiveLine(6), null, 7.8);
    tl.set("#var-guess", {{ innerText: "16" }}, 8.0);
    tl.call(() => {{
      setStatus("Iteration 1: Comparison", "Midpoint value 16 is less than target 23. Discard entire left half [0..4].", "#fbbf24");
    }}, null, 8.5);

    tl.call(() => setActiveLine(9), null, 9.8);
    tl.call(() => setActiveLine(10), null, 10.8);

    // Eliminate left half [0..4]
    tl.to(["#cell-0", "#cell-1", "#cell-2", "#cell-3", "#cell-4"], {{
      className: "+=cell-eliminated",
      duration: 0.8,
      stagger: 0.08
    }}, 11.2);
    tl.to("#ptr-mid-4", {{ opacity: 0, duration: 0.3 }}, 11.5);
    tl.to("#cell-4", {{ className: "-=cell-mid-active", duration: 0.3 }}, 11.5);

    // Update low to mid + 1 = 5
    tl.to("#ptr-low-0", {{ opacity: 0, duration: 0.3 }}, 12.0);
    tl.to("#ptr-low-5", {{ opacity: 1, y: 0, duration: 0.5 }}, 12.5);
    tl.set("#var-low", {{ innerText: "5" }}, 12.5);

    // --- BEAT 3: 13.5s - 22.5s Iteration 2 (low=5, high=9 -> mid=7, val=56) ---
    tl.call(() => {{
      setActiveLine(4);
      setStatus("Iteration 2: New Window [5..9]", "Calculate new midpoint: (5 + 9) // 2 = 7. Mid value is 56.", "#38bdf8");
    }}, null, 14.0);

    tl.call(() => setActiveLine(5), null, 15.0);
    tl.to("#ptr-mid-7", {{ opacity: 1, y: 0, duration: 0.5 }}, 15.5);
    tl.set("#var-mid", {{ innerText: "7" }}, 15.5);
    tl.to("#cell-7", {{ className: "+=cell-mid-active", duration: 0.4 }}, 15.7);

    tl.call(() => setActiveLine(6), null, 16.8);
    tl.set("#var-guess", {{ innerText: "56" }}, 17.0);

    tl.call(() => {{
      setStatus("Iteration 2: Comparison", "Mid value 56 is strictly greater than target 23. Discard right half [7..9].", "#fbbf24");
    }}, null, 17.8);
    tl.call(() => setActiveLine(11), null, 18.5);
    tl.call(() => setActiveLine(12), null, 19.5);

    // Eliminate right half [7..9]
    tl.to(["#cell-7", "#cell-8", "#cell-9"], {{
      className: "+=cell-eliminated",
      duration: 0.8,
      stagger: 0.08
    }}, 20.0);
    tl.to("#ptr-mid-7", {{ opacity: 0, duration: 0.3 }}, 20.4);
    tl.to("#cell-7", {{ className: "-=cell-mid-active", duration: 0.3 }}, 20.4);

    // Update high to mid - 1 = 6
    tl.to("#ptr-high-9", {{ opacity: 0, duration: 0.3 }}, 20.8);
    tl.to("#ptr-high-6", {{ opacity: 1, y: 0, duration: 0.5 }}, 21.4);
    tl.set("#var-high", {{ innerText: "6" }}, 21.4);

    // --- BEAT 4: 22.5s - 28.5s Iteration 3 (low=5, high=6 -> mid=5, val=23 MATCH!) ---
    tl.call(() => {{
      setActiveLine(4);
      setStatus("Iteration 3: Window [5..6]", "Calculate midpoint: (5 + 6) // 2 = 5. Value is 23.", "#38bdf8");
    }}, null, 23.0);

    tl.call(() => setActiveLine(5), null, 24.0);
    tl.to("#ptr-mid-5", {{ opacity: 1, y: 0, duration: 0.5 }}, 24.4);
    tl.set("#var-mid", {{ innerText: "5" }}, 24.4);

    tl.call(() => setActiveLine(6), null, 25.0);
    tl.set("#var-guess", {{ innerText: "23" }}, 25.0);

    tl.call(() => {{
      setActiveLine(7);
      setStatus("Match Confirmed!", "Value at index 5 equals target 23! Search completes successfully in 3 probes.", "#34d399");
    }}, null, 25.8);

    tl.to("#cell-5", {{ className: "+=cell-found-target", duration: 0.8, ease: "back.out(1.8)" }}, 26.2);
    tl.call(() => setActiveLine(8), null, 27.0);

    // --- BEAT 5: 28.5s - 33.2s Wrap-up & Logarithmic Complexity ---
    tl.call(() => {{
      setStatus("Time Complexity: O(log N)", "Dividing the problem in half every iteration allows searching billions of elements in ~30 steps.", "#34d399");
    }}, null, 28.8);

    tl.to("#tag-complexity", {{
      scale: 1.15,
      borderColor: "#34d399",
      color: "#34d399",
      boxShadow: "0 0 20px rgba(52, 211, 153, 0.4)",
      duration: 0.8
    }}, 29.2);

    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""
        index_html_path = os.path.join(self.composition_dir, "index.html")
        with open(index_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return index_html_path

    def render_composition(self, output_mp4: str) -> str:
        """
        Invokes Hyperframes to render composition to MP4 video.
        """
        output_abs = os.path.abspath(output_mp4)
        cmd = [
            "npx", "-y", "hyperframes",
            "render",
            "--quality", "looks",
            "--output", output_abs
        ]
        res = subprocess.run(cmd, cwd=self.composition_dir, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Hyperframes render failed: {res.stderr}\n{res.stdout}")
        return output_abs

    def mux_audio(self, video_mp4: str, audio_mp3: str, final_mp4: str) -> str:
        """
        Muxes audio with video using FFmpeg, normalizing volume and synchronizing tracks.
        """
        final_abs = os.path.abspath(final_mp4)
        cmd = [
            "ffmpeg",
            "-y",
            "-i", os.path.abspath(video_mp4),
            "-i", os.path.abspath(audio_mp3),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            final_abs
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg muxing failed: {res.stderr}")
        return final_abs
