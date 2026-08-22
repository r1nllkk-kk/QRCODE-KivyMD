from kivy.storage.jsonstore import JsonStore

class SettingsStore:
    def __init__(self, path: str = "settings.json"):
        self.store = JsonStore(path)

    def load(self) -> dict:
        if self.store.exists("app"):
            return self.store.get("app")
        return {
            "theme_style": "Light",
            "qr_color": "black",
        }

    def save(self, theme_style: str, qr_color: str) -> None:
        self.store.put("app", theme_style=theme_style, qr_color=qr_color)
