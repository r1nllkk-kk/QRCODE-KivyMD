from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp


class ColorDropdown(MDRaisedButton):
    def __init__(self, update_color_callback, **kwargs):
        super().__init__(**kwargs)
        self.text = "Color"
        self.pos_hint = {"center_x": 0.5}
        self.update_color_callback = update_color_callback

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Black",
                "on_release": lambda x="black": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Blue",
                "on_release": lambda x="blue": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Red",
                "on_release": lambda x="red": self.set_item(x),
            },
        ]

        self.menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            width_mult=4,
        )

    def on_release(self):
        self.menu.open()

    def set_item(self, text_item):
        self.menu.dismiss()
        self.update_color_callback(text_item)
        # Save settings automatically
        app = MDApp.get_running_app()
        app.settings_store.save(
            theme_style=app.theme_cls.theme_style,
            qr_color=text_item
        )
