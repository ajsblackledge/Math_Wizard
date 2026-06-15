"""
Custom Anvil Component: MathsLabel
===================================
Renders a string containing LaTeX (delimited by $…$ or $$…$$) using MathJax 3.
Drop this component onto a Form wherever question text or option text needs
mathematical notation.

Usage (in Python):
    from ..MathsLabel import MathsLabel
    widget = MathsLabel(text=r"What is $\\frac{d}{dx}(x^2)$?")
    self.add_component(widget)

Properties:
    text      (str)   – raw string, may contain $…$ LaTeX
    font_size (int)   – pixel font size, default 16
    bold      (bool)  – bold text, default False
    align     (str)   – "left" | "center" | "right", default "left"
"""

from anvil import HtmlTemplate
import anvil.js


MATHJAX_SCRIPT = """
<script>
window.MathJax = {
  tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] },
  options: { skipHtmlTags: ['script','noscript','style','textarea'] }
};
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>
"""


class MathsLabel(HtmlTemplate):
    """
    A custom Anvil component that wraps a <div> with MathJax typesetting.
    Inherits from HtmlTemplate so it can contain raw HTML.
    """

    _template = """
    <div id="{{ id }}"
         style="font-size: {{ font_size }}px;
                font-weight: {{ 'bold' if bold else 'normal' }};
                text-align: {{ align }};
                line-height: 1.5;
                padding: 4px 0;">
      {{ text }}
    </div>
    """ + MATHJAX_SCRIPT

    def __init__(self, text="", font_size=16, bold=False, align="left", **properties):
        self.text = text
        self.font_size = font_size
        self.bold = bold
        self.align = align
        super().__init__(**properties)
        self._render()

    def _render(self):
        """Inject text into the HTML and re-typeset MathJax."""
        self.html = f"""
        <div style="font-size:{self.font_size}px;
                    font-weight:{'bold' if self.bold else 'normal'};
                    text-align:{self.align};
                    line-height:1.5;padding:4px 0;">
          {self.text}
        </div>
        """
        # Trigger MathJax re-typeset after DOM update
        try:
            anvil.js.call_js("eval", """
              if(window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise();
              }
            """)
        except Exception:
            pass
