"""
Autonomous Codebase Scanner for Motion Showcase.
Inspects repository root to detect product name, purpose, framework,
design tokens (colors, fonts), and key UI surfaces.
"""

import os
import json
import re
from typing import Dict, Any, List

class CodebaseScanner:
    def __init__(self, target_dir: str = "."):
        self.target_dir = os.path.abspath(target_dir)

    def scan(self) -> Dict[str, Any]:
        info = {
            "name": os.path.basename(self.target_dir),
            "tagline": "Modern software product",
            "framework": "unknown",
            "primary_color": "#38bdf8",
            "bg_color": "#090d16",
            "accent_color": "#818cf8",
            "features": [],
            "key_files": []
        }

        # 1. Inspect package.json
        pkg_path = os.path.join(self.target_dir, "package.json")
        if os.path.exists(pkg_path):
            try:
                with open(pkg_path, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                    info["name"] = pkg.get("name", info["name"])
                    info["tagline"] = pkg.get("description", info["tagline"])
                    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                    if "next" in deps:
                        info["framework"] = "Next.js"
                    elif "react" in deps:
                        info["framework"] = "React"
                    elif "vue" in deps:
                        info["framework"] = "Vue"
                    elif "tailwindcss" in deps:
                        info["framework"] = "Tailwind"
            except Exception:
                pass

        # 2. Inspect pubspec.yaml (Flutter / Dart)
        pubspec_path = os.path.join(self.target_dir, "pubspec.yaml")
        if os.path.exists(pubspec_path):
            info["framework"] = "Flutter / Dart"
            try:
                with open(pubspec_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    name_match = re.search(r"^name:\s*([^\s#]+)", content, re.MULTILINE)
                    if name_match:
                        info["name"] = name_match.group(1)
                    desc_match = re.search(r"^description:\s*([^\r\n#]+)", content, re.MULTILINE)
                    if desc_match:
                        info["tagline"] = desc_match.group(1).strip()
            except Exception:
                pass

        # 3. Inspect README.md for product purpose & features
        readme_path = os.path.join(self.target_dir, "README.md")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    lines = [l.strip() for l in f.readlines() if l.strip()]
                    for l in lines:
                        if l.startswith("# "):
                            info["name"] = l.replace("#", "").strip()
                            break
                    # Find bullet points for features
                    bullets = [l.lstrip("-* ").strip() for l in lines if l.startswith(("- ", "* ")) and len(l) > 10]
                    if bullets:
                        info["features"] = bullets[:4]
            except Exception:
                pass

        # 4. Search for colors in CSS or Dart themes
        color_regex = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b|Color\(0x[0-9a-fA-F]{8}\)")
        found_colors = []
        for root, _, files in os.walk(self.target_dir):
            if any(skip in root for skip in ["node_modules", ".git", "build", "output", ".cache"]):
                continue
            for file in files:
                if file.endswith((".css", ".scss", ".ts", ".tsx", ".dart")):
                    fpath = os.path.join(root, file)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            text = f.read()
                            matches = color_regex.findall(text)
                            if matches:
                                found_colors.extend(matches[:5])
                    except Exception:
                        pass
                if len(found_colors) > 15:
                    break
            if len(found_colors) > 15:
                break

        if found_colors:
            clean_hex = [c for c in found_colors if c.startswith("#") and len(c) in (4, 7)]
            if clean_hex:
                info["primary_color"] = clean_hex[0]
                if len(clean_hex) > 1:
                    info["accent_color"] = clean_hex[1]

        # Fill default features if none found
        if not info["features"]:
            info["features"] = [
                "Fast & intuitive user workflow",
                "Pixel-perfect responsive design",
                "Real-time reactive state updates"
            ]

        return info

if __name__ == "__main__":
    scanner = CodebaseScanner()
    res = scanner.scan()
    print("Scanned Codebase Info:", json.dumps(res, indent=2))
