"""
Deterministic Python Runtime Execution Tracer.
Captures line-by-line runtime state, variable snapshots, and execution paths
without hallucination, using Python's built-in AST and sys.settrace.
"""

import sys
import ast
import json
import io
from contextlib import redirect_stdout
from typing import Dict, Any, List, Optional

class ExecutionTracer:
    def __init__(self, max_steps: int = 200):
        self.max_steps = max_steps

    def trace_code(self, code_str: str, entry_call: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes code_str and captures deterministic runtime trace events.
        """
        # 1. Parse AST to extract line map and verify syntax
        tree = ast.parse(code_str)
        lines = code_str.splitlines()

        events: List[Dict[str, Any]] = []
        captured_output = io.StringIO()
        exec_globals = {"__name__": "__main__"}

        step_counter = 0

        def tracer(frame, event, arg):
            nonlocal step_counter
            if step_counter >= self.max_steps:
                return None
            
            # Filter out frames not originating from the target code string
            if frame.f_code.co_filename != "<string>":
                return tracer

            if event in ("line", "return"):
                lineno = frame.f_lineno
                line_text = lines[lineno - 1] if 1 <= lineno <= len(lines) else ""
                
                # Sanitize and serialize local variables safely
                clean_locals = {}
                for k, v in frame.f_locals.items():
                    if k.startswith("__"):
                        continue
                    try:
                        # Attempt JSON-safe conversion or string representation
                        json.dumps(v)
                        clean_locals[k] = v
                    except (TypeError, OverflowError):
                        clean_locals[k] = repr(v)

                step_counter += 1
                events.append({
                    "step": step_counter,
                    "event": event,
                    "line": lineno,
                    "line_text": line_text.strip(),
                    "variables": clean_locals,
                    "function": frame.f_code.co_name
                })
            return tracer

        with redirect_stdout(captured_output):
            sys.settrace(tracer)
            try:
                compiled = compile(tree, "<string>", "exec")
                exec(compiled, exec_globals)
                if entry_call:
                    exec(entry_call, exec_globals)
            except Exception as e:
                events.append({
                    "step": step_counter + 1,
                    "event": "exception",
                    "line": -1,
                    "line_text": "",
                    "variables": {"error": str(e), "type": type(e).__name__},
                    "function": ""
                })
            finally:
                sys.settrace(None)

        return {
            "source_code": code_str,
            "total_steps": len(events),
            "events": events,
            "stdout": captured_output.getvalue()
        }

if __name__ == "__main__":
    test_code = """
def binary_search(arr, target):
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
    tracer = ExecutionTracer()
    trace_result = tracer.trace_code(test_code)
    print(f"Captured {trace_result['total_steps']} steps.")
    print("First 3 steps:", json.dumps(trace_result['events'][:3], indent=2))
