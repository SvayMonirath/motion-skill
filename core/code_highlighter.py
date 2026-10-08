"""
Syntax Highlighter & Line Tokenizer using Pygments.
Outputs clean HTML markup with line identifiers suitable for motion-graphics
step highlighting and code diff transitions.
"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from typing import Dict, Any, Optional

class CodeHighlighter:
    def __init__(self, theme: str = "monokai"):
        self.theme = theme
        self.formatter = HtmlFormatter(
            style=self.theme,
            noclasses=False,
            linespans="line",
            linenos=True
        )

    def highlight_code(self, code_str: str, language: str = "python") -> Dict[str, Any]:
        """
        Renders code to syntax-highlighted HTML with individual line spans.
        """
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except Exception:
            lexer = guess_lexer(code_str)

        raw_html = highlight(code_str, lexer, self.formatter)
        css_rules = self.formatter.get_style_defs(".highlight")

        # Also produce a clean line-by-line array for precise animation coordination
        lines = code_str.strip().splitlines()
        annotated_lines = []
        for idx, line in enumerate(lines, start=1):
            line_html = highlight(line, lexer, HtmlFormatter(nowrap=True, style=self.theme)).strip()
            annotated_lines.append({
                "line_number": idx,
                "text": line,
                "html": line_html
            })

        return {
            "language": language,
            "theme": self.theme,
            "full_html": raw_html,
            "css": css_rules,
            "lines": annotated_lines,
            "line_count": len(lines)
        }

if __name__ == "__main__":
    code = "def add(a, b):\n    return a + b"
    hl = CodeHighlighter()
    res = hl.highlight_code(code)
    print("Highlighted lines:", len(res["lines"]))
    print("Sample line 1 HTML:", res["lines"][0]["html"])
