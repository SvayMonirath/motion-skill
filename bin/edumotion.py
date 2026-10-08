#!/usr/bin/env python3
"""
Autonomous AI Educational Motion-Graphics System CLI.
Command-line orchestrator for visual planning, execution tracing,
motion rendering, audio synchronization, and visual QA.
"""

import sys
import os
import argparse
import json

# Ensure core and styles are on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.execution_tracer import ExecutionTracer
from core.code_highlighter import CodeHighlighter
from core.audio_engine import AudioEngine
from core.planner import EducationalPlanner
from core.renderer import EducationalRenderer
from core.visual_qa import VisualQA

SAMPLE_BINARY_SEARCH_CODE = """def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = arr[mid]
        if guess == target:
            return mid
        elif guess < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

result = binary_search([2, 5, 8, 12, 16, 23, 38, 56, 72, 91], 23)
"""

NARRATION_SCRIPT = (
    "Binary search efficiently finds an element in a sorted array by repeatedly dividing the search space in half. "
    "We initialize low and high pointers at the array boundaries and probe the middle element. "
    "Since our middle value 16 is less than target 23, we discard the entire left half. "
    "Next, probing index 7 yields 56, which is too high, eliminating the right half. "
    "Finally, at index 5, we find an exact match for 23, completing the search in logarithmic time."
)

def run_pipeline(topic: str, output_dir: str, with_audio: bool = True, style: str = "dark_cinematic"):
    print(f"=== Starting Autonomous Educational Motion Pipeline ===")
    print(f"Topic: {topic}")
    print(f"Style: {style}")
    print(f"Output Directory: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    # 1. Execution Tracing
    print("\n[Stage 1] Tracing Execution via Python AST & sys.settrace...")
    tracer = ExecutionTracer()
    trace_data = tracer.trace_code(SAMPLE_BINARY_SEARCH_CODE)
    trace_file = os.path.join(output_dir, "trace.json")
    with open(trace_file, "w") as f:
        json.dump(trace_data, f, indent=2)
    print(f" Captured {trace_data['total_steps']} deterministic execution events -> {trace_file}")

    # 2. Syntax Highlighting
    print("\n[Stage 2] Highlighting Code via Pygments...")
    highlighter = CodeHighlighter()
    highlighted = highlighter.highlight_code(SAMPLE_BINARY_SEARCH_CODE, language="python")

    # 3. Educational Planning & Storyboarding
    print("\n[Stage 3] Generating Educational Storyboard...")
    planner = EducationalPlanner(style_name=style)
    storyboard = planner.plan_algorithm_explanation(
        title="Binary Search Algorithm",
        concept="Divide and conquer logarithmic array search",
        source_code=SAMPLE_BINARY_SEARCH_CODE,
        trace_data=trace_data,
        key_steps_summary=[
            {"iteration": 1, "low": 0, "high": 9, "mid": 4, "val": 16, "action": "eliminate_left"},
            {"iteration": 2, "low": 5, "high": 9, "mid": 7, "val": 56, "action": "eliminate_right"},
            {"iteration": 3, "low": 5, "high": 6, "mid": 5, "val": 23, "action": "found_target"}
        ],
        complexity={"time": "O(log N)", "space": "O(1)"}
    )
    storyboard_file = os.path.join(output_dir, "storyboard.json")
    with open(storyboard_file, "w") as f:
        json.dump(storyboard, f, indent=2)
    print(f" Generated 4-scene storyboard -> {storyboard_file}")

    # 4. Audio Narration Generation
    audio_file = os.path.join(output_dir, "narration.mp3")
    vtt_file = os.path.join(output_dir, "narration.vtt")
    audio_duration = 12.0
    if with_audio:
        print("\n[Stage 4] Synthesizing Neural Audio Narration via Edge-TTS...")
        audio_engine = AudioEngine()
        audio_info = audio_engine.generate_narration(
            script_text=NARRATION_SCRIPT,
            output_mp3_path=audio_file,
            output_vtt_path=vtt_file
        )
        audio_duration = max(11.5, audio_info["duration"])
        print(f" Generated {audio_info['duration']:.2f}s narration track ({len(audio_info['cues'])} cues)")

    # 5. Composition Assembly & Rendering
    print(f"\n[Stage 5] Building Composition and Rendering via Hyperframes ({audio_duration:.1f}s)...")
    renderer = EducationalRenderer(project_dir=output_dir)
    html_file = renderer.generate_binary_search_html(
        storyboard=storyboard,
        highlighted_code=highlighted,
        trace_data=trace_data,
        style_preset=style,
        duration_sec=round(audio_duration, 1)
    )
    print(f" Composition HTML authored at {html_file}")

    raw_video = os.path.join(output_dir, "raw_video.mp4")
    print(f" Rendering video to {raw_video}...")
    renderer.render_composition(output_mp4=raw_video)
    print(" Hyperframes render finished successfully.")

    final_video = os.path.join(output_dir, "educational_binary_search.mp4")
    if with_audio and os.path.exists(audio_file):
        print(f"\n[Stage 6] Muxing Audio and Video via FFmpeg...")
        renderer.mux_audio(video_mp4=raw_video, audio_mp3=audio_file, final_mp4=final_video)
        print(f" Muxed final media -> {final_video}")
    else:
        os.rename(raw_video, final_video)

    # 6. Empirical Visual QA
    print("\n[Stage 7] Performing Empirical Visual & Stream QA...")
    qa = VisualQA(output_dir=output_dir)
    qa_report = qa.inspect_video(final_video)
    qa_file = os.path.join(output_dir, "qa_report.json")
    with open(qa_file, "w") as f:
        json.dump(qa_report, f, indent=2)

    print(f" QA Status: {'PASSED' if qa_report['passed'] else 'FAILED'}")
    print(f" - Resolution: {qa_report.get('resolution')}")
    print(f" - Duration: {qa_report.get('duration')}s")
    print(f" - File Size: {qa_report.get('file_size_kb')} KB")
    print(f" - Blank Frames: {qa_report.get('blank_frames_detected')} / {qa_report.get('frames_analyzed')}")
    print(f" - Has Audio: {qa_report.get('has_audio')}")
    print(f" - Audio Drift: {qa_report.get('audio_drift_sec')}s")
    print(f"\nFinal Video Artifact: {final_video}")
    print("=== Pipeline Complete ===")
    return final_video, qa_report

def main():
    parser = argparse.ArgumentParser(description="Autonomous Educational Motion-Graphics CLI")
    parser.add_argument("topic", nargs="?", default="Explain binary search", help="Educational topic")
    parser.add_argument("--output", "-o", default=os.path.join(BASE_DIR, "output", "binary_search"), help="Output directory")
    parser.add_argument("--no-audio", action="store_true", help="Disable audio narration")
    parser.add_argument("--style", default="dark_cinematic", help="Style preset")

    args = parser.parse_args()
    run_pipeline(
        topic=args.topic,
        output_dir=args.output,
        with_audio=not args.no_audio,
        style=args.style
    )

if __name__ == "__main__":
    main()
