from kivymd.uix.textfield import MDTextField

class LinkInput(MDTextField):
    def __init__(self, **kwargs):
        kwargs.setdefault("hint_text", "Paste URL")
        kwargs.setdefault("mode", "rectangle")
        kwargs.setdefault("size_hint_x", 1)
        super().__init__(**kwargs)

    def get_value(self) -> str:
        return (self.text or "").strip()
