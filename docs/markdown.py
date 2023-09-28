from pygments.formatters.html import HtmlFormatter


class CustomHtmlFormatter(HtmlFormatter):
    css_class = "highlight"
    use_pygments = True

    def _wrap_code(self, source):
        yield from source
