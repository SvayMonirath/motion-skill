"""
Educational Storyboard & Visual Explanation Planner.
Deconstructs an educational concept into structured scenes, visual representations,
narration scripts, and coordinated visual cues.
"""

from typing import Dict, Any, List, Optional
import json
import re

class EducationalPlanner:
    BANNED_JARGON = {
        "delve": "look",
        "tapestry": "structure",
        "seamlessly": "smoothly",
        "leverage": "use",
        "orchestrate": "run",
        "paradigm": "approach",
        "robust": "solid",
        "revolutionize": "transform",
        "synergy": "teamwork",
        "multifaceted": "complete",
        "utilize": "use",
        "furthermore": "also",
        "embark": "start",
        "dive deep": "look closely"
    }

    def __init__(self, style_name: str = "dark_cinematic"):
        self.style_name = style_name

    def sanitize_text(self, text: str) -> str:
        out = text
        for buzz, clean in self.BANNED_JARGON.items():
            out = re.sub(rf"\b{buzz}\b", clean, out, flags=re.IGNORECASE)
        return out

    def plan_algorithm_explanation(
        self,
        title: str,
        concept: str,
        source_code: str,
        trace_data: Dict[str, Any],
        key_steps_summary: List[Dict[str, Any]],
        complexity: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Creates a structured multi-scene educational storyboard for an algorithmic topic
        enforcing plain English without AI jargon.
        """
        storyboard = {
            "title": title,
            "concept": concept,
            "style": self.style_name,
            "dimensions": {"width": 1920, "height": 1080, "fps": 30},
            "scenes": [
                {
                    "id": "scene-intro",
                    "title": "Concept Introduction",
                    "type": "concept_overview",
                    "narration": f"Welcome to this visual walkthrough of {title}. {concept}",
                    "visuals": {
                        "heading": title,
                        "subheading": concept,
                        "badges": ["Divide and Conquer", f"Time: {complexity.get('time', 'O(log N)')}", f"Space: {complexity.get('space', 'O(1)')}"]
                    }
                },
                {
                    "id": "scene-setup",
                    "title": "Initial State & Search Space",
                    "type": "data_structure_state",
                    "narration": "We start with a sorted array. Two pointers, low and high, bracket our initial active search boundary.",
                    "visuals": {
                        "focus": "pointers_init",
                        "highlight_range": [0, len(trace_data.get("events", [{}])[0].get("variables", {}).get("arr", [])) - 1]
                    }
                },
                {
                    "id": "scene-execution",
                    "title": "Step-by-Step Divide & Conquer",
                    "type": "algorithm_walkthrough",
                    "narration": "In each iteration, we probe the middle element. If our target is larger, we eliminate the entire left half instantly.",
                    "steps": key_steps_summary
                },
                {
                    "id": "scene-conclusion",
                    "title": "Efficiency & Complexity",
                    "type": "summary",
                    "narration": f"Because we halve the search space at every step, {title} achieves logarithmic time complexity, resolving in O of log N operations.",
                    "visuals": {
                        "time_complexity": complexity.get("time", "O(log N)"),
                        "space_complexity": complexity.get("space", "O(1)"),
                        "key_takeaway": "Logarithmic scaling enables searching billions of elements in just 30 comparisons."
                    }
                }
            ]
        }
        return storyboard
