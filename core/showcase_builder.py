"""
Product Showcase & Commercial Builder.
Creates a high-end 3D isometric perspective motion-graphics showcase of an application
using its native design tokens, cursor interactions, and feature callouts.
"""

import os
import json
import subprocess
from typing import Dict, Any, Optional
from core.visual_qa import VisualQA
from core.audio_engine import AudioEngine

class ShowcaseBuilder:
    def __init__(self, output_dir: str):
        self.output_dir = os.path.abspath(output_dir)
        self.comp_dir = os.path.join(self.output_dir, "composition")
        os.makedirs(self.comp_dir, exist_ok=True)

    def generate_showcase_html(self, product_info: Dict[str, Any], duration_sec: float = 18.0) -> str:
        name = product_info.get("name", "Product Showcase")
        tagline = product_info.get("tagline", "Designed for modern productivity")
        primary = product_info.get("primary_color", "#38bdf8")
        accent = product_info.get("accent_color", "#818cf8")
        bg = product_info.get("bg_color", "#090d16")
        features = product_info.get("features", ["Instant execution", "High craft UI", "Zero latency"])

        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1920, height=1080" />
  <title>{name} Showcase</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: {bg};
      color: #ffffff;
      font-family: 'Inter', -apple-system, sans-serif;
      overflow: hidden;
      width: 1920px;
      height: 1080px;
    }}
    #root {{
      position: relative;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at 60% 30%, rgba(56, 189, 248, 0.12) 0%, transparent 60%),
                  radial-gradient(circle at 20% 80%, rgba(129, 140, 248, 0.08) 0%, transparent 50%),
                  linear-gradient(180deg, {bg} 0%, #030508 100%);
      perspective: 1200px;
      overflow: hidden;
    }}
    /* Top Brand Nav */
    .nav-bar {{
      position: absolute;
      top: 40px;
      left: 80px;
      right: 80px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }}
    .brand-logo {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }}
    .brand-icon {{
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: linear-gradient(135deg, {primary}, {accent});
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }}
    .tagline-badge {{
      font-size: 15px;
      padding: 6px 16px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #94a3b8;
    }}

    /* Hero Text */
    .hero-container {{
      position: absolute;
      top: 140px;
      left: 80px;
      width: 600px;
      z-index: 10;
    }}
    .hero-title {{
      font-size: 58px;
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -0.03em;
      margin-bottom: 20px;
      background: linear-gradient(180deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .hero-desc {{
      font-size: 20px;
      color: #94a3b8;
      line-height: 1.5;
      margin-bottom: 36px;
    }}
    .feature-list {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .feature-item {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 18px;
      font-weight: 600;
      color: #e2e8f0;
      opacity: 0;
      transform: translateX(-20px);
    }}
    .feature-bullet {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: {primary};
      box-shadow: 0 0 12px {primary};
    }}

    /* 3D App Canvas Container */
    .viewport-3d {{
      position: absolute;
      right: -40px;
      top: 120px;
      width: 1150px;
      height: 750px;
      transform-style: preserve-3d;
      transform: rotateX(12deg) rotateY(-16deg) rotateZ(2deg);
      transition: transform 1s ease;
    }}
    .app-window {{
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 20px;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.8), 0 0 60px rgba(56, 189, 248, 0.15);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }}
    .window-header {{
      height: 52px;
      background: rgba(255, 255, 255, 0.03);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      padding: 0 20px;
      gap: 8px;
    }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .dot-r {{ background: #ef4444; }}
    .dot-y {{ background: #f59e0b; }}
    .dot-g {{ background: #10b981; }}
    .window-url {{
      margin-left: 20px;
      background: rgba(0, 0, 0, 0.3);
      padding: 4px 16px;
      border-radius: 6px;
      font-size: 13px;
      color: #64748b;
      font-family: monospace;
    }}

    /* Live App UI Stage */
    .app-body {{
      flex: 1;
      padding: 30px;
      display: grid;
      grid-template-columns: 240px 1fr;
      gap: 24px;
    }}
    .sidebar {{
      background: rgba(255, 255, 255, 0.02);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .nav-btn {{
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 500;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .nav-btn.active {{
      background: rgba(56, 189, 248, 0.15);
      color: {primary};
      border-left: 3px solid {primary};
    }}
    .main-view {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .stats-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }}
    .stat-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .stat-label {{ font-size: 13px; color: #64748b; text-transform: uppercase; font-weight: 600; }}
    .stat-val {{ font-size: 28px; font-weight: 700; color: #ffffff; }}
    .chart-card {{
      flex: 1;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 24px;
      position: relative;
    }}
    .cta-btn {{
      position: absolute;
      bottom: 24px;
      right: 24px;
      background: linear-gradient(135deg, {primary}, {accent});
      color: #ffffff;
      padding: 12px 28px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 15px;
      box-shadow: 0 8px 24px rgba(56, 189, 248, 0.4);
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}

    /* Animated Cursor */
    .simulated-cursor {{
      position: absolute;
      top: 300px;
      left: 400px;
      width: 24px;
      height: 24px;
      z-index: 100;
      pointer-events: none;
      filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.5));
    }}
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
    <nav class="nav-bar">
      <div class="brand-logo">
        <div class="brand-icon"></div>
        <span>{name}</span>
      </div>
      <div class="tagline-badge">{tagline}</div>
    </nav>

    <div class="hero-container">
      <h1 class="hero-title">{name}</h1>
      <p class="hero-desc">{tagline}</p>
      <div class="feature-list">
        {''.join([f'''
        <div class="feature-item" id="feat-{i}">
          <div class="feature-bullet"></div>
          <span>{f}</span>
        </div>''' for i, f in enumerate(features[:3])])}
      </div>
    </div>

    <!-- 3D Perspective App Window -->
    <div class="viewport-3d" id="viewport-3d">
      <div class="app-window" id="app-window">
        <div class="window-header">
          <div class="dot dot-r"></div>
          <div class="dot dot-y"></div>
          <div class="dot dot-g"></div>
          <div class="window-url">app://{name.lower().replace(' ', '-')}/dashboard</div>
        </div>
        <div class="app-body">
          <div class="sidebar">
            <div class="nav-btn active">Dashboard</div>
            <div class="nav-btn">Analytics</div>
            <div class="nav-btn">Integrations</div>
            <div class="nav-btn">Settings</div>
          </div>
          <div class="main-view">
            <div class="stats-row">
              <div class="stat-card" id="card-1">
                <span class="stat-label">Throughput</span>
                <span class="stat-val" id="stat-val-1">99.98%</span>
              </div>
              <div class="stat-card" id="card-2">
                <span class="stat-label">Latency</span>
                <span class="stat-val">12ms</span>
              </div>
              <div class="stat-card" id="card-3">
                <span class="stat-label">Active Users</span>
                <span class="stat-val">24,500</span>
              </div>
            </div>
            <div class="chart-card">
              <div style="font-size:16px;font-weight:600;margin-bottom:12px;">Realtime Performance</div>
              <svg width="100%" height="160" viewBox="0 0 600 160" fill="none">
                <path id="sparkline" d="M0 120 Q 150 40 300 90 T 600 20" stroke="{primary}" stroke-width="4" fill="none"/>
              </svg>
              <div class="cta-btn" id="cta-btn">Deploy Now →</div>
            </div>
          </div>
        </div>
        <!-- Cursor -->
        <svg class="simulated-cursor" id="cursor" viewBox="0 0 24 24" fill="none">
          <path d="M5.5 3.5l12 12-5.5 1.5-3 5.5-2-1 3-5.5-4.5-1.5z" fill="#ffffff" stroke="#000000" stroke-width="1.5"/>
        </svg>
      </div>
    </div>
  </div>

  <script>
    const tl = gsap.timeline({{ paused: true }});

    // 0.0s - 3.0s: Opening reveal & 3D entrance
    tl.from(".brand-logo", {{ y: -20, opacity: 0, duration: 0.8, ease: "power3.out" }}, 0.2);
    tl.from(".tagline-badge", {{ y: -20, opacity: 0, duration: 0.8, ease: "power3.out" }}, 0.4);
    tl.from(".hero-title", {{ y: 30, opacity: 0, duration: 0.8, ease: "power3.out" }}, 0.6);
    tl.from(".hero-desc", {{ y: 20, opacity: 0, duration: 0.8, ease: "power3.out" }}, 0.8);
    
    // 3D window swoops in with smooth perspective rotation
    tl.from("#viewport-3d", {{
      x: 300,
      rotateX: 25,
      rotateY: -35,
      opacity: 0,
      duration: 1.4,
      ease: "power3.out"
    }}, 0.5);

    // Feature highlights staggering
    tl.to("#feat-0", {{ opacity: 1, x: 0, duration: 0.5 }}, 2.5);
    tl.to("#feat-1", {{ opacity: 1, x: 0, duration: 0.5 }}, 4.0);
    tl.to("#feat-2", {{ opacity: 1, x: 0, duration: 0.5 }}, 5.5);

    // Cursor movement & interactive simulation
    tl.from("#cursor", {{ opacity: 0, duration: 0.4 }}, 3.0);
    tl.to("#cursor", {{
      left: 780,
      top: 420,
      duration: 1.5,
      ease: "power2.inOut"
    }}, 3.5);

    // Click effect on CTA button
    tl.to("#cta-btn", {{ scale: 0.94, duration: 0.15, yoyo: true, repeat: 1 }}, 5.2);
    tl.to("#card-1", {{
      borderColor: "{primary}",
      boxShadow: "0 0 25px rgba(56, 189, 248, 0.4)",
      duration: 0.4
    }}, 5.4);

    // Camera shift: Punch in / focus on the 3D canvas
    tl.to("#viewport-3d", {{
      x: -120,
      rotateX: 6,
      rotateY: -8,
      scale: 1.08,
      duration: 2.2,
      ease: "power2.inOut"
    }}, 7.0);

    // Dynamic graph line draw
    tl.from("#sparkline", {{
      strokeDasharray: 800,
      strokeDashoffset: 800,
      duration: 2.0,
      ease: "power2.out"
    }}, 8.0);

    // Hold and outro glow
    tl.to("#cta-btn", {{
      boxShadow: "0 0 40px rgba(56, 189, 248, 0.7)",
      duration: 0.8,
      yoyo: true,
      repeat: 3
    }}, 11.0);

    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""
        index_path = os.path.join(self.comp_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        return index_path

    def render_showcase(self, output_mp4: str) -> str:
        cmd = [
            "npx", "-y", "hyperframes",
            "render",
            "--quality", "looks",
            "--output", os.path.abspath(output_mp4)
        ]
        res = subprocess.run(cmd, cwd=self.comp_dir, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Showcase render failed: {res.stderr}\n{res.stdout}")
        return os.path.abspath(output_mp4)
