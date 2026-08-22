from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton

class ThemeButton(MDIconButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "theme-light-dark"
        self.pos_hint = {"center_x": 0.9, "center_y": 0.95}
        self.bind(on_release=self.change_theme)

    def change_theme(self, *args):
        app = MDApp.get_running_app()
        app.theme_cls.theme_style = "Dark" if app.theme_cls.theme_style == "Light" else "Light"
        # Save settings automatically
        app.settings_store.save(
            theme_style=app.theme_cls.theme_style,
            qr_color=app.current_qr_color
        )
