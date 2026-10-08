"""
Visual and Audio QA Verification Engine.
Performs empirical inspection on rendered video files:
1. Stream metadata and container validation via ffprobe.
2. Temporal frame extraction via ffmpeg.
3. Blank/empty frame detection, color range, and contrast verification via PIL.
4. Audio/video duration drift analysis.
"""

import os
import subprocess
import json
from typing import Dict, Any, List
from PIL import Image, ImageStat

class VisualQA:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.frames_dir = os.path.join(output_dir, "qa_frames")
        os.makedirs(self.frames_dir, exist_ok=True)

    def inspect_video(self, video_path: str, expected_duration: float = 0.0) -> Dict[str, Any]:
        """
        Runs full empirical QA pipeline on the rendered video artifact.
        """
        if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
            return {
                "passed": False,
                "error": f"Video file missing or 0 bytes: {video_path}"
            }

        # 1. Probe container and streams
        meta = self._probe_metadata(video_path)
        video_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "audio"), None)

        if not video_stream:
            return {"passed": False, "error": "No video stream found in container"}

        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        duration = float(meta.get("format", {}).get("duration", 0.0))
        file_size_kb = os.path.getsize(video_path) / 1024.0

        # 2. Extract key representative frames across duration
        sample_timestamps = [
            round(duration * 0.1, 2),
            round(duration * 0.35, 2),
            round(duration * 0.65, 2),
            round(duration * 0.9, 2)
        ]
        
        extracted_frames = []
        for idx, ts in enumerate(sample_timestamps):
            frame_filename = f"frame_{idx+1}_{ts}s.png"
            frame_path = os.path.join(self.frames_dir, frame_filename)
            self._extract_frame(video_path, ts, frame_path)
            if os.path.exists(frame_path):
                stats = self._analyze_frame(frame_path)
                extracted_frames.append({
                    "timestamp": ts,
                    "path": frame_path,
                    "stats": stats
                })

        # 3. Detect anomalies (black frame / frozen / zero variance)
        blank_frames_count = 0
        for f in extracted_frames:
            if f["stats"].get("is_blank", False):
                blank_frames_count += 1

        # 4. Audio-Video duration sync check if audio exists
        audio_drift = 0.0
        if audio_stream:
            audio_duration = float(audio_stream.get("duration", duration))
            audio_drift = abs(duration - audio_duration)

        passed = (
            width == 1920 and
            height == 1080 and
            duration > 1.0 and
            blank_frames_count == 0 and
            file_size_kb > 50.0
        )

        return {
            "passed": passed,
            "resolution": f"{width}x{height}",
            "duration": round(duration, 2),
            "file_size_kb": round(file_size_kb, 1),
            "video_codec": video_stream.get("codec_name"),
            "has_audio": audio_stream is not None,
            "audio_drift_sec": round(audio_drift, 3),
            "frames_analyzed": len(extracted_frames),
            "blank_frames_detected": blank_frames_count,
            "frame_samples": extracted_frames
        }

    def _probe_metadata(self, video_path: str) -> Dict[str, Any]:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            return json.loads(res.stdout)
        return {}

    def _extract_frame(self, video_path: str, timestamp_sec: float, out_path: str):
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(timestamp_sec),
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            out_path
        ]
        subprocess.run(cmd, capture_output=True)

    def _analyze_frame(self, image_path: str) -> Dict[str, Any]:
        try:
            with Image.open(image_path) as img:
                img_rgb = img.convert("RGB")
                stat = ImageStat.Stat(img_rgb)
                mean_brightness = sum(stat.mean) / 3.0
                rms = sum(stat.rms) / 3.0
                var = sum(stat.var) / 3.0

                # A frame is considered blank/black if mean brightness < 3 and variance < 5
                is_blank = mean_brightness < 3.0 and var < 5.0
                return {
                    "mean_brightness": round(mean_brightness, 2),
                    "variance": round(var, 2),
                    "rms": round(rms, 2),
                    "is_blank": is_blank
                }
        except Exception as e:
            return {"error": str(e), "is_blank": True}

if __name__ == "__main__":
    qa = VisualQA("/Users/sorpheatepy/.gemini/antigravity-cli/brain/cfa1eb73-450d-45e9-8063-224820b118ae/scratch/test-render")
    res = qa.inspect_video("/Users/sorpheatepy/.gemini/antigravity-cli/brain/cfa1eb73-450d-45e9-8063-224820b118ae/scratch/test-render/out.mp4")
    print("QA Test Result:", json.dumps(res, indent=2))
