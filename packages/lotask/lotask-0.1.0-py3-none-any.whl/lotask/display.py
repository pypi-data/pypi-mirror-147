import markdown2

markdown_extras = ["fenced-code-blocks", "cuddled-lists", "code-friendly", "tables"]


def markdown_to_html(content):
    return markdown2.markdown(content, markdown_extras)


class HTML:
    def __init__(self, data: str):
        self.data = data

    def _repr_html_(self):
        return self.data


class Markdown:
    def __init__(self, data: str):
        self.data = data

    def _repr_markdown_(self):
        return self.data


class Display:
    def __init__(self):
        self.items = []

    def display(self, item):
        self.items.append(item)

    def display_html(self, item):
        if type(item) == str:
            item = HTML(item)
        self.display(item)

    def display_markdown(self, item):
        if type(item) == str:
            item = Markdown(item)

        self.display(item)

    def reset(self):
        self.items = []

    def _repr_by_type_(self, obj, t):
        if t == "html":
            if hasattr(obj, "_repr_html_"):
                return getattr(obj, "_repr_html_")()
            elif hasattr(obj, "_repr_markdown_"):
                return markdown_to_html(getattr(obj, "_repr_markdown_")())
            elif hasattr(obj, "__repr__"):
                # FIXME: escape
                return "<p>" + getattr(obj, "__repr__")() + "</p>"
            else:
                # FIXME: escape
                return "<p>" + str(obj) + "</p>"
        elif t == "text":
            if hasattr(obj, "__repr__"):
                return obj.__repr__()
            elif hasattr(obj, "__str__"):
                return obj.__str__()
            else:
                return str(obj)
        else:
            raise Exception("unknown type")

    def __repr__(self) -> str:
        rst = []
        for x in self.items:
            rst.append(self._repr_by_type_(x, "text"))

        return "\n".join(rst)

    def _repr_html_(self) -> str:
        rst = []
        for x in self.items:
            rst.append(self._repr_by_type_(x, "html"))

        return "\n".join(rst)
