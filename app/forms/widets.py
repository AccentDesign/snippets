from markdownx.widgets import MarkdownxWidget as BaseMarkdownxWidget


class MarkdownxWidget(BaseMarkdownxWidget):
    class Media:
        js = [
            "dist/js/markdownx.js",
        ]
