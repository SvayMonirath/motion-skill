"""
Visual Design System Presets for Educational Motion Graphics.
Defines color palettes, typography, card styling, and animation easing.
"""

from typing import Dict, Any

STYLE_PRESETS: Dict[str, Dict[str, Any]] = {
    "dark_cinematic": {
        "name": "Dark Cinematic",
        "bg": "#090d16",
        "surface": "rgba(255, 255, 255, 0.04)",
        "surface_border": "rgba(255, 255, 255, 0.12)",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "accent_primary": "#38bdf8",     # Cyan / Sky
        "accent_secondary": "#818cf8",   # Indigo
        "accent_highlight": "#fbbf24",   # Amber
        "accent_success": "#34d399",     # Emerald
        "accent_danger": "#f87171",      # Rose
        "font_family": "'Inter', -apple-system, sans-serif",
        "font_mono": "'JetBrains Mono', 'Fira Code', monospace",
        "card_radius": "16px",
        "glow": "0 8px 32px rgba(56, 189, 248, 0.15)",
        "ease_default": "power3.out",
        "ease_spring": "back.out(1.4)"
    },
    "technical": {
        "name": "Technical Blueprint",
        "bg": "#0f172a",
        "surface": "rgba(30, 41, 59, 0.7)",
        "surface_border": "#334155",
        "text_primary": "#f1f5f9",
        "text_secondary": "#64748b",
        "accent_primary": "#06b6d4",
        "accent_secondary": "#3b82f6",
        "accent_highlight": "#eab308",
        "accent_success": "#10b981",
        "accent_danger": "#ef4444",
        "font_family": "'Inter', system-ui, sans-serif",
        "font_mono": "'JetBrains Mono', monospace",
        "card_radius": "12px",
        "glow": "0 4px 20px rgba(6, 182, 212, 0.2)",
        "ease_default": "power2.out",
        "ease_spring": "power3.out"
    },
    "mathematical": {
        "name": "3Blue1Brown / Mathematical",
        "bg": "#121417",
        "surface": "rgba(255, 255, 255, 0.03)",
        "surface_border": "rgba(255, 255, 255, 0.15)",
        "text_primary": "#ffffff",
        "text_secondary": "#a1a1aa",
        "accent_primary": "#eab308",     # Gold
        "accent_secondary": "#3b82f6",   # Deep blue
        "accent_highlight": "#ec4899",   # Pink
        "accent_success": "#22c55e",
        "accent_danger": "#ef4444",
        "font_family": "'Computer Modern', 'KaTeX_Main', serif",
        "font_mono": "'Fira Code', monospace",
        "card_radius": "8px",
        "glow": "none",
        "ease_default": "power2.inOut",
        "ease_spring": "power2.out"
    },
    "anime_cartoon": {
        "name": "Vibrant Anime & Cartoon",
        "bg": "#13111c",
        "surface": "rgba(255, 255, 255, 0.07)",
        "surface_border": "#ff79c6",
        "text_primary": "#ffffff",
        "text_secondary": "#f1fa8c",
        "accent_primary": "#ff79c6",     # Sakura Pink
        "accent_secondary": "#8be9fd",   # Electric Cyan
        "accent_highlight": "#50fa7b",   # Neon Lime
        "accent_success": "#50fa7b",
        "accent_danger": "#ff5555",
        "font_family": "'Fredoka', 'Comic Neue', 'Inter', cursive, sans-serif",
        "font_mono": "'JetBrains Mono', monospace",
        "card_radius": "24px",
        "glow": "0 0 30px rgba(255, 121, 198, 0.35)",
        "ease_default": "back.out(1.8)",
        "ease_spring": "elastic.out(1, 0.35)"
    }
}

def get_style(name: str = "dark_cinematic") -> Dict[str, Any]:
    norm = name.lower().replace("+", "_").replace(" ", "_").replace("-", "_")
    if "anime" in norm or "cartoon" in norm:
        return STYLE_PRESETS["anime_cartoon"]
    return STYLE_PRESETS.get(norm, STYLE_PRESETS["dark_cinematic"])
