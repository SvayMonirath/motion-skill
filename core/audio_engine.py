"""
FOSS Audio Narration & Subtitle Engine using Edge-TTS.
Generates neural voice narration and parses subtitle cue timestamps
for frame-accurate audio-visual synchronization.
"""

import subprocess
import os
import re
from typing import Dict, Any, List, Optional

class AudioEngine:
    def __init__(self, default_voice: str = "en-US-ChristopherNeural"):
        # Highly natural neural voices: en-US-ChristopherNeural, en-US-EmmaMultilingualNeural, en-US-GuyNeural
        self.default_voice = default_voice

    def generate_narration(
        self,
        script_text: str,
        output_mp3_path: str,
        output_vtt_path: Optional[str] = None,
        voice: Optional[str] = None,
        rate: str = "+0%"
    ) -> Dict[str, Any]:
        """
        Generates MP3 audio and WebVTT timestamps using edge-tts CLI.
        """
        selected_voice = voice or self.default_voice
        os.makedirs(os.path.dirname(os.path.abspath(output_mp3_path)), exist_ok=True)
        
        if not output_vtt_path:
            output_vtt_path = os.path.splitext(output_mp3_path)[0] + ".vtt"

        cmd = [
            "edge-tts",
            "--text", script_text,
            "--write-media", output_mp3_path,
            "--write-subtitles", output_vtt_path,
            "--voice", selected_voice,
            "--rate", rate
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"edge-tts failed: {res.stderr}")

        # Probe duration via ffprobe
        duration = self.probe_duration(output_mp3_path)
        cues = self.parse_vtt(output_vtt_path)

        return {
            "audio_file": output_mp3_path,
            "vtt_file": output_vtt_path,
            "duration": duration,
            "voice": selected_voice,
            "cues": cues
        }

    def probe_duration(self, audio_file: str) -> float:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_file
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            try:
                return float(res.stdout.strip())
            except ValueError:
                pass
        return 0.0

    @staticmethod
    def parse_vtt(vtt_file: str) -> List[Dict[str, Any]]:
        """
        Parses WebVTT timing cues into structured timestamped segments.
        """
        cues = []
        if not os.path.exists(vtt_file):
            return cues

        with open(vtt_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Regex for VTT timestamp: 00:00:01.000 --> 00:00:03.500
        time_pattern = re.compile(
            r"(\d{2}):(\d{2}):(\d{2}\.\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}\.\d{3})"
        )

        blocks = content.strip().split("\n\n")
        for block in blocks:
            lines = [l.strip() for l in block.splitlines() if l.strip()]
            for i, line in enumerate(lines):
                match = time_pattern.search(line)
                if match:
                    h1, m1, s1, h2, m2, s2 = match.groups()
                    start_sec = int(h1) * 3600 + int(m1) * 60 + float(s1)
                    end_sec = int(h2) * 3600 + int(m2) * 60 + float(s2)
                    text = " ".join(lines[i+1:]) if i + 1 < len(lines) else ""
                    cues.append({
                        "start": round(start_sec, 3),
                        "end": round(end_sec, 3),
                        "duration": round(end_sec - start_sec, 3),
                        "text": text
                    })
                    break
        return cues

if __name__ == "__main__":
    eng = AudioEngine()
    test_out = "/Users/sorpheatepy/.gemini/antigravity-cli/brain/cfa1eb73-450d-45e9-8063-224820b118ae/scratch/test_voice.mp3"
    info = eng.generate_narration("Binary search eliminates half the search space with every comparison.", test_out)
    print("Generated duration:", info["duration"])
    print("Parsed cues:", info["cues"])
